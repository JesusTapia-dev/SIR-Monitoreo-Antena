
import ast
import json
import numpy as np

from polymorphic import PolymorphicModel

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.main.models import Configuration
from .utils import pulses, pulses_from_code, create_mask
# Create your models here.

LINE_TYPES = (
    ('none', 'Not used'),
    ('tr', 'Transmission/reception selector signal'),
    ('tx', 'A modulating signal (Transmission pulse)'),
    ('codes', 'BPSK modulating signal'),
    ('windows', 'Sample window signal'),
    ('sync', 'Synchronizing signal'),
    ('flip', 'IPP related periodic signal'),
    ('prog_pulses', 'Programmable pulse'),
    )


class RCConfiguration(Configuration):
    
    ipp = models.FloatField(verbose_name='Inter pulse period (Km)', validators=[MinValueValidator(1), MaxValueValidator(1000)], default=10)
    ntx = models.PositiveIntegerField(verbose_name='Number of TX', default=1)    
    clock = models.FloatField(verbose_name='Clock Master (MHz)', validators=[MinValueValidator(1), MaxValueValidator(80)], default=1)
    clock_divider = models.PositiveIntegerField(verbose_name='Clock divider', validators=[MinValueValidator(1), MaxValueValidator(256)], default=1)
    time_before = models.PositiveIntegerField(verbose_name='Time before', default=0)
    time_after = models.PositiveIntegerField(verbose_name='Time after', default=0)
    sync = models.PositiveIntegerField(verbose_name='Synchro delay', default=0)

    class Meta:
        db_table = 'rc_configurations'

    def get_number_position(self):
        
        lines = RCLine.objects.filter(rc_configuration=self.rc_configuration)
        if lines:
            return max([line.position for line in lines])

    def get_refs_lines(self):
        
        lines = RCLine.objects.filter(rc_configuration=self.pk, line_type__name='tx')
        return [(line.pk, line.get_name()) for line in lines]

    def get_lines(self, type=None):
        
        if type is not None:
            return RCLine.objects.filter(rc_configuration=self.pk, line_type__name=type)
        else:
            return RCLine.objects.filter(rc_configuration=self.pk)


class RCLineCode(models.Model):
    
    name = models.CharField(max_length=40)
    bits_per_code = models.PositiveIntegerField(default=0)
    number_of_codes = models.PositiveIntegerField(default=0)
    codes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'rc_line_codes'
        ordering = ('name',)
    
    def __unicode__(self):
        return u'%s' % self.name    

class RCLineType(models.Model):
    
    name = models.CharField(choices=LINE_TYPES, max_length=40)
    description = models.TextField(blank=True, null=True)
    params = models.TextField(default='[]')
    
    class Meta:
        db_table = 'rc_line_types'

    def __unicode__(self):
        return u'%s - %s' % (self.name.upper(), self.get_name_display())
    
    
class RCLine(models.Model):
    
    rc_configuration = models.ForeignKey(RCConfiguration)
    line_type = models.ForeignKey(RCLineType)
    channel = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    params = models.TextField(default='{}')
    pulses = models.TextField(default='')
        
    class Meta:
        db_table = 'rc_lines'
        ordering = ['channel']
    
    def __unicode__(self):
        return u'%s - %s' % (self.rc_configuration, self.get_name())
    
    def get_name(self):
        
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        if self.line_type.name in ('tx',):
            return '%s %s' % (self.line_type.name.upper(), chars[self.position])
        elif self.line_type.name in ('codes', 'windows', 'tr'):
            pk = json.loads(self.params)['TX_ref']
            if pk in (0, '0'):
                refs = ','.join(chars[l.position] for l in self.rc_configuration.get_lines('tx'))
                return '%s (%s)' % (self.line_type.name.upper(), refs)
            else:
                ref = RCLine.objects.get(pk=pk)
                return '%s (%s)' % (self.line_type.name.upper(), chars[ref.position])
        elif self.line_type.name in ('flip', 'prog_pulses', 'sync'):
            return '%s %s' % (self.line_type.name.upper(), self.channel)
        else:
            return self.line_type.name.upper()

    def get_lines(self, type=None):
        
        if type is not None:
            return RCLine.objects.filter(rc_configuration=self.rc_configuration, line_type__name=type)
        else:
            return RCLine.objects.filter(rc_configuration=self.rc_configuration)
    
    def pulses_as_array(self):
        
        return (np.fromstring(self.pulses, dtype=np.uint8)-48).astype(np.int8)
    
    @property
    def km2unit(self):
        
        return 20./3*(self.rc_configuration.clock/self.rc_configuration.clock_divider)
    
    def update_pulses(self, save=True, tr=False):
        print self
        KM2U = 20./3*(self.rc_configuration.clock/self.rc_configuration.clock_divider)
        ipp = self.rc_configuration.ipp
        ntx = self.rc_configuration.ntx
        ipp_u = int(ipp*KM2U)
        
        x = np.arange(0, ipp_u*ntx)
        
        if self.line_type.name=='tr':
            params = json.loads(self.params)
            if params['TX_ref'] in ('0', 0):
                txs = [tx.update_pulses(save=False, tr=True) for tx in self.get_lines('tx')]
            else:
                txs = [tx.update_pulses(save=False, tr=True) for tx in RCLine.objects.filter(pk=params['TX_ref'])]
            if len(txs)==0 or 0 in [len(tx) for tx in txs]:
                return
            
            y = np.any(txs, axis=0, out=np.ones(ipp_u*ntx)) 

            ranges = params['range'].split(',')
            if len(ranges)>0 and ranges[0]<>'0':
                mask = create_mask(ranges, ipp_u, ntx, self.rc_configuration.sync)
                y = y.astype(np.int8) & mask
        
        elif self.line_type.name=='tx':
            params = json.loads(self.params)
            delays = [float(d)*KM2U for d in params['delays'].split(',') if d]
            y = pulses(x, ipp_u, float(params['pulse_width'])*KM2U, 
                       delay=delays, 
                       before=self.rc_configuration.time_before,
                       after=self.rc_configuration.time_after if tr else 0,
                       sync=self.rc_configuration.sync)
            ranges = params['range'].split(',')
                                    
            if len(ranges)>0 and ranges[0]<>'0':
                mask = create_mask(ranges, ipp_u, ntx, self.rc_configuration.sync)
                y = y & mask
        
        elif self.line_type.name=='flip':
            width = float(json.loads(self.params)['number_of_flips'])*ipp*KM2U
            y = pulses(x, 2*width, width)
        
        elif self.line_type.name=='codes':
            params = json.loads(self.params)
            codes = ast.literal_eval(RCLineCode.objects.get(pk=json.loads(self.params)['code']).codes)
            tx = RCLine.objects.get(pk=params['TX_ref'])
            tx_params = json.loads(tx.params)
            
            y = pulses_from_code(ipp_u, ntx, codes,
                                 int(float(tx_params['pulse_width'])*KM2U), 
                                 before=self.rc_configuration.time_before+self.rc_configuration.sync)
            
            ranges = tx_params['range'].split(',')
            if len(ranges)>0 and ranges[0]<>'0':
                mask = create_mask(ranges, ipp_u, ntx, self.rc_configuration.sync)
                y = y.astype(np.int8) & mask
        
        elif self.line_type.name=='sync':
            params = json.loads(self.params)
            y = np.zeros(ipp_u*ntx)
            if params['invert'] in ('1', 1):
                y[-1] = 1
            else:
                y[0] = 1
        
        elif self.line_type.name=='prog_pulses':
            params = json.loads(self.params)
            if int(params['periodic'])==0:
                nntx = ntx
            else:
                nntx = 1
            
            if 'params' in params and len(params['params'])>0:                
                y = sum([pulses(x, ipp_u*nntx, (pp['end']-pp['begin']), shift=pp['begin']) for pp in params['params']])
            else:
                y = np.zeros(ipp_u*ntx)
        
        elif self.line_type.name=='windows':
            params = json.loads(self.params)
            if 'params' in params and len(params['params'])>0:
                y = sum([pulses(x, ipp_u, pp['resolution']*pp['number_of_samples']*KM2U,
                                delay=(pp['first_height']-pp['resolution'])*KM2U, 
                                before=self.rc_configuration.time_before) for pp in params['params']])
                tr = self.get_lines('tr')[0]
                ranges = json.loads(tr.params)['range'].split(',')
                if len(ranges)>0 and ranges[0]<>'0':
                    mask = create_mask(ranges, ipp_u, ntx, self.rc_configuration.sync)
                    y = y & mask
            else:
                y = np.zeros(ipp_u*ntx)
        else:
            y = np.zeros(ipp_u*ntx)
        
        if save:            
            self.pulses = (y+48).astype(np.uint8).tostring()
            self.save()
        else:
            return y
        
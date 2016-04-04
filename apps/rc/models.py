
import ast
import json
import numpy as np

from polymorphic import PolymorphicModel

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.main.models import Configuration
from .utils import RCFile, pulses, pulses_from_code, create_mask, pulses_to_points

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


SAMPLING_REFS = (
    ('none', 'No Reference'),
    ('first_baud', 'Middle of the first baud'),
    ('sub_baud', 'Middle of the sub-baud')
                 )

DAT_CMDS = {
        # Pulse Design commands
        'DISABLE' : 0, # Disables pulse generation
        'ENABLE' : 24, # Enables pulse generation
        'DELAY_START' : 40, # Write delay status to memory 
        'FLIP_START' : 48, # Write flip status to memory
        'SAMPLING_PERIOD' : 64, # Establish Sampling Period
        'TX_ONE' : 72, # Output '0' in line TX 
        'TX_ZERO' : 88, # Output '0' in line TX 
        'SW_ONE' : 104, # Output '0' in line SW 
        'SW_ZERO' : 112, # Output '1' in line SW
        'RESTART': 120, # Restarts CR8 Firmware
        'CONTINUE' : 253, # Function Unknown
        # Commands available to new controllers
        # In Pulse Design Executable, the clock divisor code is written as 12 at the start, but it should be written as code 22(below) just before the final enable.
        'CLOCK_DIVISOR_INIT' : 12, # Specifies Clock Divisor. Legacy command, ignored in the actual .dat conversion
        'CLOCK_DIVISOR_LAST' : 22, # Specifies Clock Divisor (default 60 if not included) syntax: 255,22 254,N-1.
        'CLOCK_DIVIDER' : 8, 
            }


class RCConfiguration(Configuration):
    
    ipp = models.FloatField(verbose_name='Inter pulse period (Km)', validators=[MinValueValidator(1), MaxValueValidator(1000)], default=10)
    ntx = models.PositiveIntegerField(verbose_name='Number of TX', validators=[MinValueValidator(1), MaxValueValidator(256)], default=1)    
    clock_in = models.FloatField(verbose_name='Clock in (MHz)', validators=[MinValueValidator(1), MaxValueValidator(80)], default=1)
    clock_divider = models.PositiveIntegerField(verbose_name='Clock divider', validators=[MinValueValidator(1), MaxValueValidator(256)], default=1)
    clock = models.FloatField(verbose_name='Clock Master (MHz)', blank=True, default=1)
    time_before = models.PositiveIntegerField(verbose_name='Time before (&mu;S)', default=0)
    time_after = models.PositiveIntegerField(verbose_name='Time after (&mu;S)', default=0)
    sync = models.PositiveIntegerField(verbose_name='Synchro delay', default=0)
    sampling_reference = models.CharField(verbose_name='Sampling Reference', choices=SAMPLING_REFS, default='none', max_length=40)
    control_tx = models.BooleanField(verbose_name='Control Switch TX', default=False)
    control_sw = models.BooleanField(verbose_name='Control Switch SW', default=False)


    class Meta:
        db_table = 'rc_configurations'
    
    
    def get_absolute_url_plot(self):
        return reverse('url_plot_rc_pulses', args=[str(self.id)])
    
    def get_absolute_url_import(self):
        return reverse('url_import_rc_conf', args=[str(self.id)])
    
    @property
    def us2unit(self):
        
        return self.clock_in/self.clock_divider


    @property
    def km2unit(self):
        
        return 20./3*(self.clock_in/self.clock_divider)


    def get_lines(self, type=None):
        '''
        Retrieve configuration lines 
        '''
        
        if type is not None:
            return RCLine.objects.filter(rc_configuration=self.pk, line_type__name=type)
        else:
            return RCLine.objects.filter(rc_configuration=self.pk)

    def clean_lines(self):
        '''
        '''
        
        empty_line = RCLineType.objects.get(pk=8)
        
        for line in self.get_lines():
            line.line_type = empty_line
            line.params = '{}'
            line.save()

    def parms_to_dict(self):
        '''        
        '''
        
        data = {}
        for field in self._meta.fields:
            
            data[field.name] = '{}'.format(field.value_from_object(self))
        
        data.pop('parameters')
        data['lines'] = []
        
        for line in self.get_lines():
            line_data = json.loads(line.params)
            if 'TX_ref' in line_data and line_data['TX_ref'] not in (0, '0'):
                line_data['TX_ref'] = RCLine.objects.get(pk=line_data['TX_ref']).get_name()
            if 'code' in line_data:
                line_data['code'] = RCLineCode.objects.get(pk=line_data['code']).name
            line_data['type'] = line.line_type.name
            data['lines'].append(line_data)
        
        
        return data
    
    def get_delays(self):
        
        pulses = [line.get_pulses() for line in self.get_lines()]
        points = [tup for tups in pulses for tup in tups]
        points = set([x for tup in points for x in tup])
        points = list(points)
        points.sort()        
        
        if points[0]<>0:
            points.insert(0, 0)
        
        return [points[i+1]-points[i] for i in range(len(points)-1)]
        
    
    def get_flips(self):
        
        line_points = [pulses_to_points(line.pulses_as_array()) for line in self.get_lines()]
        line_points = [[(x, x+y) for x,y in tups] for tups in line_points]
        line_points = [[t for x in tups for t in x] for tups in line_points]        
        states = [[1 if x in tups else 0 for tups in line_points] for x in points]
        
        return states
    
    def add_cmd(self, cmd):
        
        if cmd in DAT_CMDS:
            return (255, DAT_CMDS[cmd])
    
    def add_data(self, value):            
            
        return (254, value-1)
        
    def parms_to_binary(self):
        '''
        Create "dat" stream to be send to CR
        '''
        
        data = []
        # create header
        data.append(self.add_cmd('DISABLE'))
        data.append(self.add_cmd('CONTINUE'))
        data.append(self.add_cmd('RESTART'))
        
        if self.control_sw:
            data.append(self.add_cmd('SW_ONE'))
        else:
            data.append(self.add_cmd('SW_ZERO'))
        
        if self.control_tx:
            data.append(self.add_cmd('TX_ONE'))
        else:
            data.append(self.add_cmd('TX_ZERO'))
        
        # write divider
        data.append(self.add_cmd('CLOCK_DIVIDER'))
        data.append(self.add_data(self.clock_divider))
        
        # write delays
        data.append(self.add_cmd('DELAY_START'))
        # first delay is always zero
        data.append(self.add_data(1))
        line_points = [pulses_to_points(line.pulses_as_array()) for line in self.get_lines()]
        points = [tup for tups in line_points for tup in tups]
        points = [(x, x+y) for x,y in points]
        points = set([x for tup in points for x in tup])
        points = list(points)
        points.sort()        
        
        if points[0]<>0:
            points.insert(0, 0)
        
        delays = [points[i+1]-points[i] for i in range(len(points)-1)]        
        
        for delay in delays:            
            while delay>252:                
                data.append(self.add_data(253))
                delay -= 253
            data.append(self.add_data(delay))
        
        # write flips
        data.append(self.add_cmd('FLIP_START'))        
        line_points = [[(x, x+y) for x,y in tups] for tups in line_points]
        line_points = [[t for x in tups for t in x] for tups in line_points]        
        states = [[1 if x in tups else 0 for tups in line_points] for x in points]
        for flips, delay in zip(states[:-1], delays):
            flips.reverse()
            flip = int(''.join([str(x) for x in flips]), 2)            
            data.append(self.add_data(flip+1))
            while delay>252:
                data.append(self.add_data(1))
                delay -= 253
        
        # write sampling period
        data.append(self.add_cmd('SAMPLING_PERIOD'))
        wins = self.get_lines(type='windows')
        if wins:
            win_params = json.loads(wins[0].params)['params']
            if win_params:
                dh = int(win_params[0]['resolution']*self.km2unit)
            else:
                dh = 1
        else:
            dh = 1
        data.append(self.add_data(dh))
        
        # write enable
        data.append(self.add_cmd('ENABLE'))
        
        return '\n'.join(['{}'.format(x) for tup in data for x in tup])
    
    def update_from_file(self, filename):
        '''
        Update instance from file
        '''
        
        f = RCFile(filename)
        data = f.data
        self.name = data['name']
        self.ipp = data['ipp']
        self.ntx = data['ntx']
        self.clock_in = data['clock_in']        
        self.clock_divider = data['clock_divider']
        self.clock = data['clock']
        self.time_before = data['time_before']
        self.time_after = data['time_after']
        self.sync = data['sync']
        self.sampling_reference = data['sampling_reference']
        self.clean_lines()
                        
        lines = []
        positions = {'tx':0, 'tr':0}                
        
        for i, line_data in enumerate(data['lines']):
            line_type = RCLineType.objects.get(name=line_data.pop('type'))
            if line_type.name=='codes':
                code = RCLineCode.objects.get(name=line_data['code'])
                line_data['code'] = code.pk                
            line = RCLine.objects.filter(rc_configuration=self, channel=i)
            if line:
                line = line[0]
                line.line_type = line_type
                line.params = json.dumps(line_data)
            else:
                line = RCLine(rc_configuration=self, line_type=line_type, 
                              params=json.dumps(line_data),
                              channel=i)
            
            if line_type.name=='tx':
                line.position = positions['tx']
                positions['tx'] += 1
            
            if line_type.name=='tr':
                line.position = positions['tr']
                positions['tr'] += 1
                
            line.save()
            lines.append(line)
            
        for line, line_data in zip(lines, data['lines']):
            if 'TX_ref' in line_data:
                params = json.loads(line.params)
                if line_data['TX_ref'] in (0, '0'):
                    params['TX_ref'] = '0'
                else:
                    params['TX_ref'] = [l.pk for l in lines if l.line_type.name=='tx' and l.get_name()==line_data['TX_ref']][0]
                line.params = json.dumps(params)
                line.save()                     
        

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
        if self.rc_configuration:
            return u'%s - %s' % (self.rc_configuration, self.get_name())
    
    def get_name(self):
        
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        if self.line_type.name in ('tx',):
            return '%s%s' % (self.line_type.name.upper(), chars[self.position])
        elif self.line_type.name in ('codes', 'windows', 'tr'):
            if 'TX_ref' not in json.loads(self.params):
                return self.line_type.name.upper()
            pk = json.loads(self.params)['TX_ref']
            if pk in (0, '0'):
                refs = ','.join(chars[l.position] for l in self.rc_configuration.get_lines('tx'))
                return '%s (%s)' % (self.line_type.name.upper(), refs)
            else:
                ref = RCLine.objects.get(pk=pk)
                return '%s (%s)' % (self.line_type.name.upper(), chars[ref.position])
        elif self.line_type.name in ('flip', 'prog_pulses', 'sync', 'none'):
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
    
    
    def get_pulses(self):
        
        X = self.pulses_as_array()
        
        d = X[1:]-X[:-1]
    
        up = np.where(d==1)[0]
        if X[0]==1:
            up = np.concatenate((np.array([-1]), up))
        up += 1
        
        dw = np.where(d==-1)[0]
        if X[-1]==1:
            dw = np.concatenate((dw, np.array([len(X)-1])))
        dw += 1
    
        return [(tup[0], tup[1]) for tup in zip(up, dw)]
    
    def get_win_ref(self, params, tx_id, km2unit):
        
        ref = self.rc_configuration.sampling_reference
        
        codes = [line for line in self.get_lines(type='code') if int(json.loads(line.params)['TX_ref'])==int(tx_id)]
        
        if codes:
            code_line = RCLineCode.objects.get(pk=json.loads(codes[0].params)['code'])
            tx_width = float(json.loads(RCLine.objects.get(pk=tx_id).params)['pulse_width'])*km2unit/code_line.bits_per_code
        else:
            tx_width = float(json.loads(RCLine.objects.get(pk=tx_id).params)['pulse_width'])*km2unit
        
        if ref=='first_baud':
            return int(1 + (tx_width + 1)/2 + params['first_height']*km2unit - params['resolution']*km2unit)
        elif ref=='sub_baud':
            return int(1 + params['first_height']*km2unit - params['resolution']*km2unit/2)
        else:
            return 0
    
    def update_pulses(self, save=True, tr=False):
        '''
        Update pulses field 
        '''
        
        km2unit = self.rc_configuration.km2unit
        us2unit = self.rc_configuration.us2unit
        ipp = self.rc_configuration.ipp
        ntx = self.rc_configuration.ntx
        ipp_u = int(ipp*km2unit)
        
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
            delays = [float(d)*km2unit for d in params['delays'].split(',') if d]
            y = pulses(x, ipp_u, float(params['pulse_width'])*km2unit, 
                       delay=delays, 
                       before=int(self.rc_configuration.time_before*us2unit),
                       after=int(self.rc_configuration.time_after*us2unit) if tr else 0,
                       sync=self.rc_configuration.sync)
            
            ranges = params['range'].split(',')
            
            if len(ranges)>0 and ranges[0]<>'0':
                mask = create_mask(ranges, ipp_u, ntx, self.rc_configuration.sync)
                y = y & mask
        
        elif self.line_type.name=='flip':
            width = float(json.loads(self.params)['number_of_flips'])*ipp*km2unit
            y = pulses(x, 2*width, width)
        
        elif self.line_type.name=='codes':
            params = json.loads(self.params)
            #codes = ast.literal_eval(RCLineCode.objects.get(pk=json.loads(self.params)['code']).codes)
            tx = RCLine.objects.get(pk=params['TX_ref'])
            tx_params = json.loads(tx.params)
            
            y = pulses_from_code(ipp_u, ntx, params['codes'],
                                 int(float(tx_params['pulse_width'])*km2unit), 
                                 before=int(self.rc_configuration.time_before*us2unit)+self.rc_configuration.sync)
            
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
                print 'REFS'
                print [self.get_win_ref(pp, params['TX_ref'],km2unit) for pp in params['params']]
                y = sum([pulses(x, ipp_u, pp['resolution']*pp['number_of_samples']*km2unit,
                                shift=0, 
                                before=int(self.rc_configuration.time_before*us2unit)+self.get_win_ref(pp, params['TX_ref'],km2unit),
                                sync=self.rc_configuration.sync) for pp in params['params']])
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
    
    
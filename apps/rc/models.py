
from polymorphic import PolymorphicModel

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.main.models import Configuration
# Create your models here.

LINE_TYPES = (
    ('tr', 'Transmission/reception selector signal'),
    ('tx', 'A modulating signal (Transmission pulse)'),
    ('codes', 'BPSK modulating signal'),
    ('windows', 'Sample window signal'),
    ('sync', 'Synchronizing signal'),
    ('flip', 'IPP related periodic signal'),
    ('prog_pulses', 'Programmable pulse'),
    )

LINE_PARAMS = {
    "tr": [{"name":"time_after", "value": 0}],
    "tx": [{"name": "pulse_width", "value": 0},{"name":"delays", "value":""}],
    "codes": [{"name":"tx_ref", "value": ""},{"name":"code", "value": "", "choices":"RCLineCode"}],
    "windows": [{"name":"tx_ref","value":""}, {"name":"first_height", "value":0}, {"name":"number_of_samples","value":0}, {"name":"resolution","value":0}, {"name":"last_height","value":0}],
    "sync": [{"name": "delay", "value": 0}],
    "flip": [{"name":"number_of_flips", "value": 0}],
    "prog_pulses": [{"name": "begin", "value": 0}, {"name": "end","value": 0}],
    }


class RCConfiguration(Configuration):
        
    clock = models.FloatField(verbose_name='Clock Master (MHz)', validators=[MinValueValidator(0), MaxValueValidator(80)], blank=True, null=True)
    clock_divider = models.PositiveIntegerField(verbose_name='Clock divider', validators=[MinValueValidator(0), MaxValueValidator(256)], blank=True, null=True)
    ipp = models.PositiveIntegerField(verbose_name='Inter pulse period (Km)', default=10)
    ntx = models.PositiveIntegerField(verbose_name='Number of pulse of transmit', default=1)
    time_before = models.PositiveIntegerField(verbose_name='Number of pulse of transmit', default=0)

    class Meta:
        db_table = 'rc_configurations'

    def get_number_position(self):
        
        lines = RCLine.objects.filter(rc_configuration=self.rc_configuration)
        if lines:
            return max([line.position for line in lines])

class RCLineCode(models.Model):
    
    name = models.CharField(choices=LINE_TYPES, max_length=40)
    bits_per_code = models.PositiveIntegerField(default=0)
    number_of_codes = models.PositiveIntegerField(default=0)
    codes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'rc_line_codes'
        

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
        
    class Meta:
        db_table = 'rc_lines'
    
    def __unicode__(self):
        return u'%s - %s' % (self.rc_configuration, self.get_name())
    
    def get_name(self):
        
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        if self.line_type.name in ('tx', 'code', 'tr'):
            return '%s%s' % (self.line_type.name.upper(), chars[self.position])
        
        return self.line_type.name.upper()



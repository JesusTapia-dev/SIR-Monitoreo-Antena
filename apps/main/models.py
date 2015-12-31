from itertools import chain
from django.db import models
from polymorphic import PolymorphicModel

STATES = (
          (0, 'Inactive'),
          (1, 'Active'),
         )

DEV_TYPES = (
    ('', 'Select a device type'),
    ('rc', 'Radar Controller'),
    ('dds', 'Direct Digital Synthesizer'),
    ('jars', 'Jicamarca Radar System'),
    ('usrp', 'Universal Software Radio Peripheral'),
    ('cgs', 'Clock Generator System'),
    ('abs', 'Automatic Beam Switching'),
)

# Create your models here.
    
class DeviceType(models.Model):

    name = models.CharField(max_length = 10, choices = DEV_TYPES, default = 'rc')
    
    description = models.TextField(blank=True, null=True)
    
#     info = models.TextField(blank=True, null=True) 
#     status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'db_device_types'
    
    def __unicode__(self):
        return u'%s' % self.name
    
class Device(models.Model):

    device_type = models.ForeignKey(DeviceType)
    name = models.CharField(max_length=40, default='')
    ip_address = models.GenericIPAddressField(protocol='IPv4', default='0.0.0.0')
    port_address = models.PositiveSmallIntegerField(default=2000)
    description = models.TextField(blank=True, null=True)
    
#     serial_number = models.CharField(max_length=40, default='')
#     mac_address = models.CharField(max_length = 20, null=True, blank=True)
#     status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'db_devices'
        
    def __unicode__(self):
        return u'[%s]: %s | %s' % (self.device_type.name, self.name, self.ip_address)

class Campaign(models.Model):

    name = models.CharField(max_length=40, unique=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    tags = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    template = models.BooleanField(default=False)

    class Meta:
        db_table = 'db_campaigns'
    
    def __unicode__(self):
        return u'%s: %s - %s' % (self.name, self.start_date.date(), self.end_date.date())
    
class Experiment(models.Model):

    campaign = models.ForeignKey(Campaign)
    name = models.CharField(max_length=40, default='')
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='23:59:59')

    class Meta:
        db_table = 'db_experiments'
    
    def __unicode__(self):
        return u'[%s]: %s: %s - %s' % (self.campaign.name, self.name, self.start_time, self.end_time)
    
class Configuration(PolymorphicModel):

    experiment = models.ForeignKey(Experiment)
    device = models.ForeignKey(Device)
#     parameters = models.TextField(default='{}')
#     status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'db_configurations'
    
    def __unicode__(self):
        return u'%s [%s]' % (self.experiment.name, self.device.name) 
    
from itertools import chain
from django.db import models
from polymorphic import PolymorphicModel

CONF_TYPES = (
          (0, 'Active'),
          (1, 'Historical'),
         )

DEV_STATES = (
          (0, 'No connected'),
          (1, 'Connected'),
          (2, 'Configured'),
          (3, 'Running'),
         )

DEV_TYPES = (
    ('', 'Select a device type'),
    ('rc', 'Radar Controller'),
    ('dds', 'Direct Digital Synthesizer'),
    ('jars', 'Jicamarca Radar Acquisition System'),
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
        return u'%s' % self.get_name_display()
    
class Device(models.Model):

    device_type = models.ForeignKey(DeviceType)
    name = models.CharField(max_length=40, default='')
    ip_address = models.GenericIPAddressField(protocol='IPv4', default='0.0.0.0')
    port_address = models.PositiveSmallIntegerField(default=2000)
    description = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=0, choices=DEV_STATES)
    
#     serial_number = models.CharField(max_length=40, default='')
#     mac_address = models.CharField(max_length = 20, null=True, blank=True)
    

    class Meta:
        db_table = 'db_devices'
        
    def __unicode__(self):
        return u'%s | %s' % (self.name, self.ip_address)

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
        return u'%s' % (self.name)
    
class Experiment(models.Model):

    campaign = models.ForeignKey(Campaign)
    name = models.CharField(max_length=40, default='')
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='23:59:59')

    class Meta:
        db_table = 'db_experiments'
    
    def __unicode__(self):
        return u'[%s]: %s' % (self.campaign.name, self.name)
    
class Configuration(PolymorphicModel):

    experiment = models.ForeignKey(Experiment)
    device = models.ForeignKey(Device)
    type = models.PositiveSmallIntegerField(default=0, choices=CONF_TYPES)
    
    created_date = models.DateTimeField(auto_now_add=True)
    programmed_date = models.DateTimeField(auto_now=True)
    
    parameters = models.TextField(default='{}')
    
    class Meta:
        db_table = 'db_configurations'
    
    def __unicode__(self):
        return u'[%s - %s]: %s' % (self.experiment.campaign.name,
                                self.experiment.name,
                                self.device.name) 
    
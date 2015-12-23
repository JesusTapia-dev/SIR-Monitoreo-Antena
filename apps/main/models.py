from itertools import chain
from django.db import models
from polymorphic import PolymorphicModel

STATES = (
          (0, 'Inactive'),
          (1, 'Active'),
         )

# Create your models here.

class DeviceType(models.Model):

    name = models.CharField(max_length=40)
    alias = models.CharField(max_length=40)
    info = models.TextField(blank=True, null=True) 
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'device_types'
    
    def __unicode__(self):
        return u'%s' % self.alias
    
class Device(models.Model):

    device_type = models.ForeignKey(DeviceType)
    name = models.CharField(max_length=40, default='')
    model = models.CharField(max_length=40, default='')
    serial_number = models.CharField(max_length=40, default='')
    ip_address = models.GenericIPAddressField(protocol='IPv4', default='0.0.0.0')
    mac_address = models.CharField(max_length = 20, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'devices'
        
    def __unicode__(self):
        return u'%s - %s' % (self.device_type, self.ip_address)
    
class Experiment(models.Model):

    name = models.CharField(max_length=40)
    alias = models.CharField(max_length=40)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    template = models.BooleanField(default=False)   
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'experiments'
    
    def __unicode__(self):
        return u'%s: %s - %s' % (self.alias, self.start_date, self.end_date)
    
class Configuration(PolymorphicModel):

    experiment = models.ForeignKey(Experiment)
    device = models.ForeignKey(Device)
    parameters = models.TextField(default='{}')
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'configurations'
    
    def __unicode__(self):
        return u'%s - %s' % (self.experiment.alias, self.device) 
    
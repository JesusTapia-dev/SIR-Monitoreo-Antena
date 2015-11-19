from django.db import models

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
    model = models.CharField(max_length=40, default='')
    serial = models.CharField(max_length=40, default='')
    ip_address = models.GenericIPAddressField(protocol='IPv4', default='0.0.0.0')   
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'devices'
        
    def __unicode__(self):
        return u'%s-%s' % (self.device_type, self.ip_address)
    
class Experiment(models.Model):

    name = models.CharField(max_length=40)
    alias = models.CharField(max_length=40)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()   
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'experiments'
    
    def __unicode__(self):
        return u'%s: %s-%s' % (self.name, self.start_date, self.end_date)

class Configuration(models.Model):

    device = models.ForeignKey(Device)
    parameters = models.TextField()
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    def __unicode__(self):
        return u'%s Conf' % self.device
    class Meta:
        db_table = 'configurations'

class ExperimentDetail(models.Model):

    experiment = models.ForeignKey(Experiment)
    configurations = models.ManyToManyField(Configuration)
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'experiments_detail'
    
    def __unicode__(self):
        return u'%s Configuration' % self.experiment.name

class ExperimentTemplate(models.Model):

    experiment_detail = models.ForeignKey(ExperimentDetail)
    status = models.PositiveSmallIntegerField(default=1, choices=STATES)

    class Meta:
        db_table = 'templates'
    
    def __unicode__(self):
        return u'%s Template' % (self.experiment_detail.experiment.name)
    
from django.db import models
from polymorphic import PolymorphicModel

from django.core.urlresolvers import reverse

CONF_STATES = (
                 (0, 'Disconnected'),
                 (1, 'Connected'),
                 (2, 'Running'),
             )

EXP_STATES = (
                 (0,'Error'),        #RED
                 (1,'Configurated'), #BLUE
                 (2,'Running'),      #GREEN
                 (3,'Waiting'),      #YELLOW
                 (4,'Nothing'),      #WHITE
             )

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

DEV_PORTS = {
                'rc'    : 2000,
                'dds'   : 2000,
                'jars'  : 2000,
                'usrp'  : 2000,
                'cgs'   : 8080,
                'abs'   : 8080
            }

RADAR_STATES = (
                 (0, 'No connected'),
                 (1, 'Connnected'),
                 (2, 'Configured'),
                 (3, 'Running'),
                 (4, 'Scheduled'),
             )
# Create your models here.

    
class Location(models.Model):

    name = models.CharField(max_length = 30)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'db_location'
    
    def __unicode__(self):
        return u'%s' % self.name

class DeviceType(models.Model):

    name = models.CharField(max_length = 10, choices = DEV_TYPES, default = 'rc')
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'db_device_types'
    
    def __unicode__(self):
        return u'%s' % self.get_name_display()
    
class Device(models.Model):

    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=40, default='')
    ip_address = models.GenericIPAddressField(protocol='IPv4', default='0.0.0.0')
    port_address = models.PositiveSmallIntegerField(default=2000)
    description = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=0, choices=DEV_STATES)

    class Meta:
        db_table = 'db_devices'
        
    def __unicode__(self):
        return u'%s | %s' % (self.name, self.ip_address)
    
    def get_status(self):
        
        return self.status
    

class Campaign(models.Model):

    template = models.BooleanField(default=False)
    
    name = models.CharField(max_length=40, unique=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    tags = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'db_campaigns'
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
# class Radar(models.Model):
# 
# #     name = models.CharField(max_length = 30)
#     experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE)
#     location = models.OneToOneField('Location', on_delete=models.CASCADE)
#     status = models.PositiveSmallIntegerField(default=0, choices=RADAR_STATES)
# 
#     class Meta:
#         db_table = 'db_radar'
#     
#     def __unicode__(self):
#         return u'%s' % self.location

#class RunningExperiment(models.Model):
#    radar = models.OneToOneField('Location', on_delete=models.CASCADE)
#    running_experiment = models.OneToOneField('Experiment', on_delete=models.CASCADE)
#    status = models.PositiveSmallIntegerField(default=0, choices=RADAR_STATES)
    
    
class Experiment(models.Model):

    template = models.BooleanField(default=False)
    
    campaign = models.ForeignKey('Campaign', null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey('Location', null=True, blank=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=40, default='')
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='23:59:59')

    class Meta:
        db_table = 'db_experiments'
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
class Configuration(PolymorphicModel):

    template = models.BooleanField(default=False)
    
    name = models.CharField(verbose_name="Configuration Name", max_length=40, default='')
    
    experiment = models.ForeignKey('Experiment', null=True, blank=True, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    
    type = models.PositiveSmallIntegerField(default=0, choices=CONF_TYPES)
    
    created_date = models.DateTimeField(auto_now_add=True)
    programmed_date = models.DateTimeField(auto_now=True)
    
    parameters = models.TextField(default='{}')
    
    message = ""
    
    class Meta:
        db_table = 'db_configurations'
    
    def __unicode__(self):
        return u'[%s, %s]: %s' % (self.experiment.name,
                                   self.device.name,
                                   self.name)
    
    def parms_to_dict(self):
        
        parameters = {}
        
        for key in self.__dict__.keys():
            parameters[key] = getattr(self, key)
        
        return parameters
    
    def parms_to_text(self):
        
        raise NotImplementedError, "This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper()
        
        return ''
    
    def parms_to_binary(self):
        
        raise NotImplementedError, "This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper()
        
        return ''
    
    def dict_to_parms(self, parameters):
        
        if type(parameters) != type({}):
            return
            
        for key in parameters.keys():
            setattr(self, key, parameters[key])
        
    def export_to_file(self, format="json"):
        
        import json
        
        content_type = ''
            
        if format == 'text':
            content_type = 'text/plain'
            filename = '%s_%s.%s' %(self.device.device_type.name, self.name, self.device.device_type.name)
            content = self.parms_to_text()
        
        if format == 'binary':
            content_type = 'application/octet-stream'
            filename = '%s_%s.bin' %(self.device.device_type.name, self.name)
            content = self.parms_to_binary()
        
        if not content_type:
            content_type = 'application/json'
            filename = '%s_%s.json' %(self.device.device_type.name, self.name)
            content = json.dumps(self.parms_to_dict())
            
        fields = {'content_type':content_type,
                  'filename':filename,
                  'content':content
                  }
        
        return fields
    
    def import_from_file(self, fp):
        
        import os, json
        
        parms = {}
        
        path, ext = os.path.splitext(fp.name)
        
        if ext == '.json':
            parms = json.load(fp)
        
        return parms
      
    def status_device(self):
        
        raise NotImplementedError, "This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper()
        
        return None
    
    def stop_device(self):
        
        raise NotImplementedError, "This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper()
        
        return None
    
    def start_device(self):
        
        raise NotImplementedError, "This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper()
        
        return None
    
    def write_device(self, parms):
        
        raise NotImplementedError, "This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper()
        
        return None
    
    def read_device(self):
        
        raise NotImplementedError, "This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper()
        
        return None
    
    def get_absolute_url(self):
        return reverse('url_%s_conf' % self.device.device_type.name, args=[str(self.id)])
    
    def get_absolute_url_edit(self):
        return reverse('url_edit_%s_conf' % self.device.device_type.name, args=[str(self.id)])
    
    def get_absolute_url_import(self):
        return reverse('url_import_dev_conf', args=[str(self.id)])
    
    def get_absolute_url_export(self):
        return reverse('url_export_dev_conf', args=[str(self.id)])
    
    def get_absolute_url_write(self):
        return reverse('url_write_dev_conf', args=[str(self.id)])
    
    def get_absolute_url_read(self):
        return reverse('url_read_dev_conf', args=[str(self.id)])
    
    def get_absolute_url_start(self):
        return reverse('url_start_dev_conf', args=[str(self.id)])
    
    def get_absolute_url_stop(self):
        return reverse('url_stop_dev_conf', args=[str(self.id)])
    
    def get_absolute_url_status(self):
        return reverse('url_status_dev_conf', args=[str(self.id)])
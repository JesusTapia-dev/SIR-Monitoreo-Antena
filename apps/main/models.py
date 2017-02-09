
import requests
from datetime import datetime
from django.template.base import kwarg_re

try:
    from polymorphic.models import PolymorphicModel
except:
    from polymorphic import PolymorphicModel

from django.db import models
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from devices.dds import api as dds_api

EXP_STATES = (
                 (0,'Error'),                 #RED
                 (1,'Configured'),            #BLUE
                 (2,'Running'),               #GREEN
                 (3,'Scheduled'),             #YELLOW
                 (4,'Not Configured'),        #WHITE
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
                 (4, 'Unknown'),
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
                 (1, 'Connected'),
                 (2, 'Configured'),
                 (3, 'Running'),
                 (4, 'Scheduled'),
             )


class Location(models.Model):

    name = models.CharField(max_length = 30)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'db_location'

    def __str__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('url_location', args=[str(self.id)])


class DeviceType(models.Model):

    name = models.CharField(max_length = 10, choices = DEV_TYPES, default = 'rc')
    sequence = models.PositiveSmallIntegerField(default=1000)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'db_device_types'

    def __str__(self):
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

    def __str__(self):
        return u'[{}]: {}'.format(self.device_type.name.upper(),
                                    self.name)

    def get_status(self):
        return self.status

    @property
    def status_color(self):
        color = 'muted'
        if self.status == 0:
            color = "danger"
        elif self.status == 1:
            color = "warning"
        elif self.status == 2:
            color = "info"
        elif self.status == 3:
            color = "success"

        return color

    def url(self, path=None):

        if path:
            return 'http://{}:{}/{}/'.format(self.ip_address, self.port_address, path)
        else:
            return 'http://{}:{}/'.format(self.ip_address, self.port_address)

    def get_absolute_url(self):

        return reverse('url_device', args=[str(self.id)])

    def change_ip(self, ip_address, mask, gateway, **kwargs):

        if self.device_type.name=='dds':
            try:            
                answer = dds_api.change_ip(ip = self.ip_address,
                                           port = self.port_address,
                                           new_ip = ip_address,
                                           mask = mask,
                                           gateway = gateway)
                if answer[0]=='1':
                    self.message = '25|DDS - {}'.format(answer)
                    self.ip_address = ip_address
                    self.save()
                else:
                    self.message = '30|DDS - {}'.format(answer)
                    return False
            except Exception as e:
                self.message = '40|{}'.format(str(e))
                return False
        
        elif self.device_type.name=='rc':
            payload = {'ip': ip_address,
                       'dns': kwargs.get('dns', '8.8.8.8'),
                       'gateway': gateway,
                       'subnet': mask}            
            req = requests.post(self.url('changeip'), data=payload)
            try:
                answer = req.json()
                if answer['changeip']=='ok':                    
                    self.message = '25|IP succesfully changed'
                    self.ip_address = ip_address
                    self.save()
                else:
                    self.message = '30|An error ocuur when changing IP'
            except Exception as e:
                self.message = '40|{}'.format(str(e))
        else:
            self.message = 'Not implemented'
            return False

        return True


class Campaign(models.Model):

    template = models.BooleanField(default=False)
    name = models.CharField(max_length=60, unique=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    tags = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    experiments = models.ManyToManyField('Experiment', blank=True)

    class Meta:
        db_table = 'db_campaigns'
        ordering = ('name',)

    def __str__(self):
        if self.template:
            return u'{} (template)'.format(self.name)
        else:
            return u'{}'.format(self.name)

    def parms_to_dict(self):

        import json

        parameters = {}
        exp_parameters = {}
        experiments = Experiment.objects.filter(campaign = self)

        i=1
        for experiment in experiments:
            exp_parameters['experiment-'+str(i)]  = json.loads(experiment.parms_to_dict())
            i += 1


        parameters['experiments'] = exp_parameters
        parameters['end_date']    = self.end_date.strftime("%Y-%m-%d")
        parameters['start_date']  = self.start_date.strftime("%Y-%m-%d")
        parameters['campaign']    = self.__str__()
        parameters['tags']        =self.tags

        parameters = json.dumps(parameters, indent=2, sort_keys=False)

        return parameters

    def import_from_file(self, fp):

        import os, json

        parms = {}

        path, ext = os.path.splitext(fp.name)

        if ext == '.json':
            parms = json.loads(fp.read())

        return parms

    def dict_to_parms(self, parms, CONF_MODELS):

        experiments = Experiment.objects.filter(campaign = self)
        configurations = Configuration.objects.filter(experiment = experiments)

        if configurations:
            for configuration in configurations:
                configuration.delete()

        if experiments:
            for experiment in experiments:
                experiment.delete()

        for parms_exp in parms['experiments']:
            location = Location.objects.get(name = parms['experiments'][parms_exp]['radar'])
            new_exp = Experiment(
                                 name        = parms['experiments'][parms_exp]['experiment'],
                                 location    = location,
                                 start_time  = parms['experiments'][parms_exp]['start_time'],
                                 end_time    = parms['experiments'][parms_exp]['end_time'],
                                 )
            new_exp.save()
            new_exp.dict_to_parms(parms['experiments'][parms_exp],CONF_MODELS)
            new_exp.save()

            self.name       = parms['campaign']
            self.start_date = parms['start_date']
            self.end_date   = parms['end_date']
            self.tags       = parms['tags']
            self.experiments.add(new_exp)
            self.save()

        return self

    def get_experiments_by_radar(self, radar=None):

        ret = []
        if radar:
            locations = Location.objects.filter(pk=radar)
        else:
            locations = set([e.location for e in self.experiments.all()])

        for loc in locations:
            dum = {}
            dum['name'] = loc.name
            dum['id'] = loc.pk
            dum['experiments'] = [e for e in self.experiments.all() if e.location==loc]
            ret.append(dum)

        return ret

    def get_absolute_url(self):
        return reverse('url_campaign', args=[str(self.id)])

    def get_absolute_url_edit(self):
        return reverse('url_edit_campaign', args=[str(self.id)])

    def get_absolute_url_export(self):
        return reverse('url_export_campaign', args=[str(self.id)])

    def get_absolute_url_import(self):
        return reverse('url_import_campaign', args=[str(self.id)])



class RunningExperiment(models.Model):
    radar = models.OneToOneField('Location', on_delete=models.CASCADE)
    running_experiment = models.ManyToManyField('Experiment', blank = True)
    status = models.PositiveSmallIntegerField(default=0, choices=RADAR_STATES)


class Experiment(models.Model):

    template = models.BooleanField(default=False)
    name = models.CharField(max_length=40, default='', unique=True)
    location = models.ForeignKey('Location', null=True, blank=True, on_delete=models.CASCADE)
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='23:59:59')
    status = models.PositiveSmallIntegerField(default=4, choices=EXP_STATES)

    class Meta:
        db_table = 'db_experiments'
        ordering = ('template', 'name')

    def __str__(self):
        if self.template:
            return u'%s (template)' % (self.name)
        else:
            return u'%s' % (self.name)

    @property
    def radar_system(self):
        return self.location

    def clone(self, **kwargs):

        confs = Configuration.objects.filter(experiment=self, type=0)
        self.pk = None
        self.name = '{} [{:%Y/%m/%d}]'.format(self.name, datetime.now())
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.save()

        for conf in confs:
            conf.clone(experiment=self, template=False)

        return self

    def start(self):
        '''
        Configure and start experiments's devices
        '''

        result = 2

        confs = Configuration.objects.filter(experiment=self).order_by('device__device_type__sequence')
        for i in range(0,len(confs)): #ABS-CGS-DDS-RC-JARS
            if i==0:
                for conf in confs:
                    if conf.device.device_type.name == 'abs':
                        conf.start_device()
                        break
            if i==1:
                for conf in confs:
                    if conf.device.device_type.name == 'cgs':
                        conf.start_device()
                        break
            if i==2:
                for conf in confs:
                    if conf.device.device_type.name == 'dds':
                        conf.start_device()
                        break
            if i==3:
                for conf in confs:
                    if conf.device.device_type.name == 'rc':
                        conf.start_device()
                        break
            if i==4:
                for conf in confs:
                    if conf.device.device_type.name == 'jars':
                        conf.start_device()
                        break
                #if conf.start_device():
                #    result &= 2
                #else:
                #    result &= 0
            else:
                result &= 0

        return result

    def stop(self):
        '''
        Stop experiments's devices
        '''

        result = 1

        confs = Configuration.objects.filter(experiment=self).order_by('-device__device_type__sequence')
        for i in range(0,len(confs)): 
            if i==0:
                for conf in confs:
                    if conf.device.device_type.name == 'abs':
                        conf.stop_device()
                        break
            if i==1:
                for conf in confs:
                    if conf.device.device_type.name == 'jars':
                        conf.stop_device()
                        break
            if i==2:
                for conf in confs:
                    if conf.device.device_type.name == 'dds':
                        conf.stop_device()
                        break
            if i==3:
                for conf in confs:
                    if conf.device.device_type.name == 'cgs':
                        conf.stop_device()
                        break
            if i==4:
                for conf in confs:
                    if conf.device.device_type.name == 'rc':
                        conf.stop_device()
                        break
                #result &= 1
            else:
                result &= 0

        return result

    def get_status(self):

        confs =  Configuration.objects.filter(experiment=self)
        
        for conf in confs:
            conf.status_device()
        
        total = confs.aggregate(models.Sum('device__status'))['device__status__sum']

        if total==2*confs.count():
            status = 1
        elif total == 3*confs.count():
            status = 2
        else:
            status = 0

        if self.status<>3:
            self.status = status
            self.save()

    def status_color(self):
        color = 'muted'
        if self.status == 0:
            color = "danger"
        elif self.status == 1:
            color = "info"
        elif self.status == 2:
            color = "success"
        elif self.status == 3:
            color = "warning"

        return color

    def parms_to_dict(self):

        import json

        configurations = Configuration.objects.filter(experiment=self)
        conf_parameters = {}
        parameters={}

        for configuration in configurations:
            if 'cgs' in configuration.device.device_type.name:
                conf_parameters['cgs'] = configuration.parms_to_dict()
            if 'dds' in configuration.device.device_type.name:
                conf_parameters['dds'] = configuration.parms_to_dict()
            if 'rc' in configuration.device.device_type.name:
                conf_parameters['rc'] = configuration.parms_to_dict()
            if 'jars' in configuration.device.device_type.name:
                conf_parameters['jars'] = configuration.parms_to_dict()
            if 'usrp' in configuration.device.device_type.name:
                conf_parameters['usrp'] = configuration.parms_to_dict()
            if 'abs' in configuration.device.device_type.name:
                conf_parameters['abs'] = configuration.parms_to_dict()

        parameters['configurations'] = conf_parameters
        parameters['end_time']       = self.end_time.strftime("%H:%M:%S")
        parameters['start_time']     = self.start_time.strftime("%H:%M:%S")
        parameters['radar']          = self.radar_system.name
        parameters['experiment']     = self.name
        parameters = json.dumps(parameters, indent=2)

        return parameters

    def import_from_file(self, fp):

        import os, json

        parms = {}

        path, ext = os.path.splitext(fp.name)

        if ext == '.json':
            parms = json.loads(fp.read().decode('utf-8'))

        return parms

    def dict_to_parms(self, parms, CONF_MODELS):

        configurations = Configuration.objects.filter(experiment=self)

        if configurations:
                    for configuration in configurations:
                        configuration.delete()

        for conf_type in parms['configurations']:
                    #--For ABS Device:
                    #--For USRP Device:
                    #--For JARS Device:
                    if conf_type == 'jars':
                        device = get_object_or_404(Device, pk=parms['configurations']['jars']['device_id'])
                        DevConfModel = CONF_MODELS[conf_type]
                        confjars_form = DevConfModel(
                                                  experiment = self,
                                                  name = 'JARS',
                                                  device=device,
                                                  )
                        confjars_form.dict_to_parms(parms['configurations']['jars'])
                        confjars_form.save()
                    #--For RC Device:
                    if conf_type == 'rc':
                        device = get_object_or_404(Device, pk=parms['configurations']['rc']['device_id'])
                        DevConfModel = CONF_MODELS[conf_type]
                        confrc_form = DevConfModel(
                                                  experiment = self,
                                                  name = 'RC',
                                                  device=device,
                                                  )
                        confrc_form.dict_to_parms(parms['configurations']['rc'])
                        confrc_form.save()
                    #--For DDS Device:
                    if conf_type == 'dds':
                        device = get_object_or_404(Device, pk=parms['configurations']['dds']['device_id'])
                        DevConfModel = CONF_MODELS[conf_type]
                        confdds_form = DevConfModel(
                                                  experiment = self,
                                                  name = 'DDS',
                                                  device=device,
                                                  )
                        confdds_form.dict_to_parms(parms['configurations']['dds'])
                        confdds_form.save()
                    #--For CGS Device:
                    if conf_type == 'cgs':
                        device = get_object_or_404(Device, pk=parms['configurations']['cgs']['device_id'])
                        DevConfModel = CONF_MODELS[conf_type]
                        confcgs_form = DevConfModel(
                                                  experiment = self,
                                                  name = 'CGS',
                                                  device=device,
                                                  )
                        confcgs_form.dict_to_parms(parms['configurations']['cgs'])
                        confcgs_form.save()

        location = Location.objects.get(name = parms['radar'])
        self.name       = parms['experiment']
        self.location   = location
        self.start_time = parms['start_time']
        self.end_time   = parms['end_time']
        self.save()

        return self

    def get_absolute_url(self):
        return reverse('url_experiment', args=[str(self.id)])

    def get_absolute_url_edit(self):
        return reverse('url_edit_experiment', args=[str(self.id)])

    def get_absolute_url_import(self):
        return reverse('url_import_experiment', args=[str(self.id)])

    def get_absolute_url_export(self):
        return reverse('url_export_experiment', args=[str(self.id)])

    def get_absolute_url_start(self):
        return reverse('url_start_experiment', args=[str(self.id)])

    def get_absolute_url_stop(self):
        return reverse('url_stop_experiment', args=[str(self.id)])


class Configuration(PolymorphicModel):

    template = models.BooleanField(default=False)

    name = models.CharField(verbose_name="Configuration Name", max_length=40, default='')

    experiment = models.ForeignKey('Experiment', verbose_name='Experiment', null=True, blank=True, on_delete=models.CASCADE)
    device = models.ForeignKey('Device', verbose_name='Device', null=True, on_delete=models.CASCADE)

    type = models.PositiveSmallIntegerField(default=0, choices=CONF_TYPES)

    created_date = models.DateTimeField(auto_now_add=True)
    programmed_date = models.DateTimeField(auto_now=True)

    parameters = models.TextField(default='{}')

    message = ""

    class Meta:
        db_table = 'db_configurations'

    def __str__(self):

        device = '{}:'.format(self.device.device_type.name.upper())

        if 'mix' in [f.name for f in self._meta.get_fields()]:
            if self.mix:
                device = '{} MIXED:'.format(self.device.device_type.name.upper())

        if self.template:
            return u'{} {} (template)'.format(device, self.name)
        else:
            return u'{} {}'.format(device, self.name)

    def clone(self, **kwargs):

        self.pk = None
        self.id = None
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.save()

        return self

    def parms_to_dict(self):

        parameters = {}

        for key in self.__dict__.keys():
            parameters[key] = getattr(self, key)

        return parameters

    def parms_to_text(self):

        raise NotImplementedError("This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper())


    def parms_to_binary(self):

        raise NotImplementedError("This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper())


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
            filename = '%s_%s.dat' %(self.device.device_type.name, self.name)
            content = self.parms_to_binary()

        if not content_type:
            content_type = 'application/json'
            filename = '%s_%s.json' %(self.device.device_type.name, self.name)
            content = json.dumps(self.parms_to_dict(), indent=2)

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

        self.message = 'Function not implemented'
        return False


    def stop_device(self):

        self.message = 'Function not implemented'
        return False


    def start_device(self):

        self.message = 'Function not implemented'
        return False


    def write_device(self, parms):

        self.message = 'Function not implemented'
        return False


    def read_device(self):

        self.message = 'Function not implemented'
        return False


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

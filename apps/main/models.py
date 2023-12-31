
import os
import json
import requests
import time
from datetime import datetime

try:
    from polymorphic.models import PolymorphicModel
except:
    from polymorphic import PolymorphicModel

from django.template.base import kwarg_re
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.main.utils import Params
from apps.rc.utils import RCFile
from apps.jars.utils import RacpFile
from devices.dds import api as dds_api
from devices.dds import data as dds_data


DEV_PORTS = {
                'rc'    : 2000,
                'dds'   : 2000,
                'jars'  : 2000,
                'usrp'  : 2000,
                'cgs'   : 8080,
                'abs'   : 8080,
                'dds_rest': 80
            }

RADAR_STATES = (
                 (0, 'No connected'),
                 (1, 'Connected'),
                 (2, 'Configured'),
                 (3, 'Running'),
                 (4, 'Scheduled'),
             )

EXPERIMENT_TYPE = (
                   (0, 'RAW_DATA'),
                   (1, 'PDATA'),
                   )

DECODE_TYPE = (
             (0, 'None'),
             (1, 'TimeDomain'),
             (2, 'FreqDomain'),
             (3, 'InvFreqDomain'),
             )

DEV_STATES = (
                 (0, 'No connected'),
                 (1, 'Connected'),
                 (2, 'Configured'),
                 (3, 'Running'),
                 (4, 'Unknown'),
                 (5, 'Busy')
             )

DEV_TYPES = (
                ('', 'Select a device type'),
                ('rc', 'Radar Controller'),
                ('dds', 'Direct Digital Synthesizer'),
                ('jars', 'Jicamarca Radar Acquisition System'),
                ('usrp', 'Universal Software Radio Peripheral'),
                ('cgs', 'Clock Generator System'),
                ('abs', 'Automatic Beam Switching'),
                ('dds_rest', 'Direct Digital Synthesizer_REST'),
                ('atrad', 'Transmitter ATRAD'),
            )

EXP_STATES = (
                 (0,'Error'),                 #RED
                 (1,'Cancelled'),             #YELLOW
                 (2,'Running'),               #GREEN
                 (3,'Scheduled'),             #BLUE
                 (4,'Unknown'),               #WHITE
                 (5,'Busy'),
             )

CONF_TYPES = (
                 (0, 'Active'),
                 (1, 'Historical'),
             )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=30, default='spacelab')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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

    name = models.CharField(max_length = 10, choices = DEV_TYPES, default = 'dds_rest')
    sequence = models.PositiveSmallIntegerField(default=55)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'db_device_types'

    def __str__(self):
        return u'%s' % self.get_name_display()

class Device(models.Model):

    device_type  = models.ForeignKey('DeviceType', on_delete=models.CASCADE)
    location     = models.ForeignKey('Location', on_delete=models.CASCADE)
    ip_address   = models.GenericIPAddressField(protocol='IPv4', default='0.0.0.0')
    port_address = models.PositiveSmallIntegerField(default=2000)
    description  = models.TextField(blank=True, null=True)
    status       = models.PositiveSmallIntegerField(default=4, choices=DEV_STATES)
    conf_active  = models.PositiveIntegerField(default=0, verbose_name='Current configuration')

    class Meta:
        db_table = 'db_devices'

    def __str__(self):
        ret = u'{} [{}]'.format(self.device_type.name.upper(), self.location.name)

        return ret

    @property
    def name(self):
        return str(self)

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

    def get_absolute_url_edit(self):
        return reverse('url_edit_device', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('url_delete_device', args=[str(self.id)])

    def change_ip(self, ip_address, mask, gateway, dns, **kwargs):

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
            headers = {'content-type': "application/json",
                       'cache-control': "no-cache"}

            ip      = [int(x) for x in ip_address.split('.')]
            dns     = [int(x) for x in dns.split('.')]
            gateway = [int(x) for x in gateway.split('.')]
            subnet  = [int(x) for x in mask.split('.')]

            payload = {
                "ip": ip,
                "dns": dns,
                "gateway": gateway,
                "subnet": subnet
                }

            req = requests.post(self.url('changeip'), data=json.dumps(payload), headers=headers)
            try:
                answer = req.json()
                if answer['changeip']=='ok':
                    self.message    = '25|IP succesfully changed'
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

    template    = models.BooleanField(default=False)
    name        = models.CharField(max_length=60, unique=True)
    start_date  = models.DateTimeField(blank=True, null=True)
    end_date    = models.DateTimeField(blank=True, null=True)
    tags        = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    experiments = models.ManyToManyField('Experiment', blank=True)
    author      = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_campaigns'
        ordering = ('name',)

    def __str__(self):
        if self.template:
            return u'{} (template)'.format(self.name)
        else:
            return u'{}'.format(self.name)

    def jsonify(self):

        data = {}

        ignored = ('template')

        for field in self._meta.fields:
            if field.name in ignored:
                continue
            data[field.name] = field.value_from_object(self)

        data['start_date'] = data['start_date'].strftime('%Y-%m-%d')
        data['end_date']   = data['end_date'].strftime('%Y-%m-%d')

        return data

    def parms_to_dict(self):

        params = Params({})
        params.add(self.jsonify(), 'campaigns')

        for exp in Experiment.objects.filter(campaign = self):
            params.add(exp.jsonify(), 'experiments')
            configurations = Configuration.objects.filter(experiment=exp, type=0)

            for conf in configurations:
                params.add(conf.jsonify(), 'configurations')
                if conf.device.device_type.name=='rc':
                    for line in conf.get_lines():
                        params.add(line.jsonify(), 'lines')

        return params.data

    def dict_to_parms(self, parms, CONF_MODELS):

        experiments = Experiment.objects.filter(campaign = self)

        if experiments:
            for experiment in experiments:
                experiment.delete()

        for id_exp in parms['experiments']['allIds']:
            exp_parms = parms['experiments']['byId'][id_exp]
            dum = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
            exp = Experiment(name='{}'.format(dum))
            exp.save()
            exp.dict_to_parms(parms, CONF_MODELS, id_exp=id_exp)
            self.experiments.add(exp)

        camp_parms = parms['campaigns']['byId'][parms['campaigns']['allIds'][0]]

        self.name       = '{}-{}'.format(camp_parms['name'], datetime.now().strftime('%y%m%d'))
        self.start_date = camp_parms['start_date']
        self.end_date   = camp_parms['end_date']
        self.tags       = camp_parms['tags']
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
            dum['name']        = loc.name
            dum['id']          = loc.pk
            dum['experiments'] = [e for e in self.experiments.all() if e.location==loc]
            ret.append(dum)
        return ret

    def get_absolute_url(self):
        return reverse('url_campaign', args=[str(self.id)])

    def get_absolute_url_edit(self):
        return reverse('url_edit_campaign', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('url_delete_campaign', args=[str(self.id)])

    def get_absolute_url_export(self):
        return reverse('url_export_campaign', args=[str(self.id)])

    def get_absolute_url_import(self):
        return reverse('url_import_campaign', args=[str(self.id)])


class RunningExperiment(models.Model):
    radar              = models.OneToOneField('Location', on_delete=models.CASCADE)
    running_experiment = models.ManyToManyField('Experiment', blank = True)
    status             = models.PositiveSmallIntegerField(default=0, choices=RADAR_STATES)


class Experiment(models.Model):

    template   = models.BooleanField(default=False)
    name       = models.CharField(max_length=40, default='', unique=True)
    location   = models.ForeignKey('Location', null=True, blank=True, on_delete=models.CASCADE)
    freq       = models.FloatField(verbose_name='Operating Freq. (MHz)', validators=[MinValueValidator(1), MaxValueValidator(10000)], default=49.9200)
    start_time = models.TimeField(default='00:00:00')
    end_time   = models.TimeField(default='23:59:59')
    task       = models.CharField(max_length=36, default='', blank=True, null=True)
    status     = models.PositiveSmallIntegerField(default=4, choices=EXP_STATES)
    author     = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    hash       = models.CharField(default='', max_length=64, null=True, blank=True)

    class Meta:
        db_table = 'db_experiments'
        ordering = ('template', 'name')

    def __str__(self):
        if self.template:
            return u'%s (template)' % (self.name)
        else:
            return u'%s' % (self.name)

    def jsonify(self):

        data = {}

        ignored = ('template')

        for field in self._meta.fields:
            if field.name in ignored:
                continue
            data[field.name] = field.value_from_object(self)

        data['start_time'] = data['start_time'].strftime('%H:%M:%S')
        data['end_time']   = data['end_time'].strftime('%H:%M:%S')
        data['location']   = self.location.name
        data['configurations'] = ['{}'.format(conf.pk) for
            conf in Configuration.objects.filter(experiment=self, type=0)]

        return data

    @property
    def radar_system(self):
        return self.location

    def clone(self, **kwargs):

        confs = Configuration.objects.filter(experiment=self, type=0)
        self.pk = None
        self.name = '{}_{:%y%m%d%H%M%S}'.format(self.name, datetime.now())
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.save()

        for conf in confs:
            conf.clone(experiment=self, template=False)

        return self

    def start(self):
        '''
        Configure and start experiments's devices
        ABS-CGS-DDS-RC-JARS
        '''
        self.status=5 #Busy
        self.save()
        print("Realizando operación. \nEXPERIMENT STATUS : {}".format(self.status))

        confs = []
        allconfs = Configuration.objects.filter(experiment=self, type = 0).order_by('-device__device_type__sequence')
        rc_mix   = [conf for conf in allconfs if conf.device.device_type.name=='rc' and conf.mix]
        if rc_mix:
            for conf in allconfs:
                if conf.device.device_type.name == 'rc' and  not conf.mix:
                    continue
                confs.append(conf)
        else:
            confs = allconfs


        for conf in confs:
            print("--------------",flush=True)
            print("STATUS: {}".format(conf.device.status))
            print("Stop ",conf.name,flush=True)
            if conf.stop_device() ==False:
                print("Falló Stop ",conf.name)
                print("Cancelando Campaña...",flush=True)
                return 0
            print("Write ",conf.name,flush=True)
            if conf.write_device() ==False:
                print("Falló Write ",conf.name)
                print("Cancelando Campaña...",flush=True)
                return 0
            print("Save",conf.name,flush=True)
            conf.device.conf_active = conf.pk
            conf.device.save()
            print("Start",conf.name,flush=True)
            if conf.start_device()==False:
                print("Falló Start ",conf.name)
                print("Cancelando Campaña...",flush=True)
                return 0
            print("--- CONFIGURACIÓN EXITOSA ---",flush=True)
            time.sleep(1)

        return 2


    def stop(self):
        '''
        Stop experiments's devices
        DDS-JARS-RC-CGS-ABS
        '''

        confs = Configuration.objects.filter(experiment=self, type = 0).order_by('device__device_type__sequence')
        confs = confs.exclude(device__device_type__name='cgs')
        try:
            for conf in confs:
                conf.stop_device()
        except:
            return 0
        return 1

    def get_status(self):

        if self.status == 3:
            return

        confs =  Configuration.objects.filter(experiment=self, type=0)

        for conf in confs:
            conf.status_device()

        total = confs.aggregate(models.Sum('device__status'))['device__status__sum']

        if total==2*confs.count():
            status = 1
        elif total == 3*confs.count():
            status = 2
        else:
            status = 0

        self.status = status
        self.save()

    def status_color(self):
        color = 'muted'
        if self.status == 0:
            color = "danger"
        elif self.status == 1:
            color = "warning"
        elif self.status == 2:
            color = "success"
        elif self.status == 3:
            color = "info"

        return color

    def parms_to_dict(self):

        params = Params({})
        params.add(self.jsonify(), 'experiments')

        configurations = Configuration.objects.filter(experiment=self, type=0)

        for conf in configurations:
            params.add(conf.jsonify(), 'configurations')
            if conf.device.device_type.name=='rc':
                for line in conf.get_lines():
                    params.add(line.jsonify(), 'lines')

        return params.data

    def dict_to_parms(self, parms, CONF_MODELS, id_exp=None):

        configurations = Configuration.objects.filter(experiment=self)

        if id_exp is not None:
            exp_parms = parms['experiments']['byId'][id_exp]
        else:
            exp_parms = parms['experiments']['byId'][parms['experiments']['allIds'][0]]

        if configurations:
            for configuration in configurations:
                configuration.delete()

        for id_conf in exp_parms['configurations']:
            conf_parms = parms['configurations']['byId'][id_conf]
            device     = Device.objects.filter(device_type__name=conf_parms['device_type'])[0]
            model      = CONF_MODELS[conf_parms['device_type']]
            conf = model(
                experiment = self,
                device = device,
                )
            conf.dict_to_parms(parms, id=id_conf)


        location, created = Location.objects.get_or_create(name=exp_parms['location'])
        self.name = '{}-{}'.format(exp_parms['name'], datetime.now().strftime('%y%m%d'))
        self.location   = location
        self.start_time = exp_parms['start_time']
        self.end_time   = exp_parms['end_time']
        self.save()

        return self

    def get_absolute_url(self):
        return reverse('url_experiment', args=[str(self.id)])

    def get_absolute_url_edit(self):
        return reverse('url_edit_experiment', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('url_delete_experiment', args=[str(self.id)])

    def get_absolute_url_import(self):
        return reverse('url_import_experiment', args=[str(self.id)])

    def get_absolute_url_export(self):
        return reverse('url_export_experiment', args=[str(self.id)])

    def get_absolute_url_start(self):
        return reverse('url_start_experiment', args=[str(self.id)])

    def get_absolute_url_stop(self):
        return reverse('url_stop_experiment', args=[str(self.id)])


class Configuration(PolymorphicModel):

    template        = models.BooleanField(default=False)
    # name          = models.CharField(verbose_name="Configuration Name", max_length=40, default='')
    device          = models.ForeignKey('Device', verbose_name='Device', null=True, on_delete=models.CASCADE)
    label           = models.CharField(verbose_name="Label", max_length=40, default='', blank=True, null=True)
    experiment      = models.ForeignKey('Experiment', verbose_name='Experiment', null=True, blank=True, on_delete=models.CASCADE)
    type            = models.PositiveSmallIntegerField(default=0, choices=CONF_TYPES)
    created_date    = models.DateTimeField(auto_now_add=True)
    programmed_date = models.DateTimeField(auto_now=True)
    parameters      = models.TextField(default='{}')
    author          = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    hash            = models.CharField(default='', max_length=64, null=True, blank=True)
    message = ""

    class Meta:
        db_table = 'db_configurations'
        ordering = ('device__device_type__name',)

    def __str__(self):

        ret = u'{} '.format(self.device.device_type.name.upper())

        if 'mix' in [f.name for f in self._meta.get_fields()]:
            if self.mix:
                ret = '{} MIX '.format(self.device.device_type.name.upper())

        if 'label' in [f.name for f in self._meta.get_fields()]:
            ret += '{}'.format(self.label)

        if self.template:
            ret += ' (template)'

        return ret

    @property
    def name(self):

        return str(self)

    def jsonify(self):

        data = {}

        ignored = ('type', 'polymorphic_ctype', 'configuration_ptr',
                   'created_date', 'programmed_date', 'template', 'device',
                   'experiment')

        for field in self._meta.fields:
            if field.name in ignored:
                continue
            data[field.name] = field.value_from_object(self)

        data['device_type'] = self.device.device_type.name

        if self.device.device_type.name == 'rc':
            data['lines'] = ['{}'.format(line.pk) for line in self.get_lines()]
            data['delays'] = self.get_delays()
            data['pulses'] = self.get_pulses()

        elif self.device.device_type.name == 'jars':
            data['decode_type'] = DECODE_TYPE[self.decode_data][1]

        elif self.device.device_type.name == 'dds':
            data['frequencyA_Mhz'] = float(data['frequencyA_Mhz'])
            data['frequencyB_Mhz'] = float(data['frequencyB_Mhz'])
            data['phaseA'] = dds_data.phase_to_binary(data['phaseA_degrees'])
            data['phaseB'] = dds_data.phase_to_binary(data['phaseB_degrees'])

        elif self.device.device_type.name == 'dds_rest':
            data['frequencyA_Mhz'] = float(data['frequencyA_Mhz'])
            data['frequencyB_Mhz'] = float(data['frequencyB_Mhz'])
            data['phaseA'] = dds_data.phase_to_binary(data['phaseA_degrees'])
            data['phaseB'] = dds_data.phase_to_binary(data['phaseB_degrees'])
            data['delta_frequency_Mhz'] = float(data['delta_frequency_Mhz'] or 0.00) 
            data['update_clock_Mhz']    = float(data['update_clock_Mhz'] or 0.00) 
            data['ramp_rate_clock_Mhz'] = float(data['ramp_rate_clock_Mhz'] or 0.0) 
        return data

    def clone(self, **kwargs):

        self.pk = None
        self.id = None
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.save()

        return self

    def parms_to_dict(self):

        params = Params({})
        params.add(self.jsonify(), 'configurations')

        if self.device.device_type.name=='rc':
            for line in self.get_lines():
                params.add(line.jsonify(), 'lines')

        return params.data

    def parms_to_text(self):

        raise NotImplementedError("This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper())


    def parms_to_binary(self):

        raise NotImplementedError("This method should be implemented in %s Configuration model" %str(self.device.device_type.name).upper())


    def dict_to_parms(self, parameters, id=None):

        params = Params(parameters)

        if id:
            data = params.get_conf(id_conf=id)
        else:
            data = params.get_conf(dtype=self.device.device_type.name)

        if data['device_type']=='rc':
            self.clean_lines()
            lines = data.pop('lines', None)
            for line_id in lines:
                pass

        for key, value in data.items():
            if key not in ('id', 'device_type'):
                setattr(self, key, value)

        self.save()


    def export_to_file(self, format="json"):

        content_type = ''

        if format == 'racp':
            content_type = 'text/plain'
            filename = '%s_%s.%s' %(self.device.device_type.name, self.name, 'racp')
            content = self.parms_to_text(file_format = 'racp')

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
            content = json.dumps(self.parms_to_dict(), indent=2)

        fields = {'content_type':content_type,
                  'filename':filename,
                  'content':content
                  }

        return fields

    def import_from_file(self, fp):

        parms = {}

        path, ext = os.path.splitext(fp.name)

        if ext == '.json':
            parms = json.load(fp)

        if ext == '.dds':
            lines = fp.readlines()
            parms = dds_data.text_to_dict(lines)

        if ext == '.racp':
            if self.device.device_type.name == 'jars':
                parms = RacpFile(fp).to_dict()
                parms['filter_parms'] = json.loads(self.filter_parms)
                return parms
            parms = RCFile(fp).to_dict()

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

    def write_device_mqtt(self, parms):

        self.message = 'Function not implemented'
        return False

    def read_device(self):

        self.message = 'Function not implemented'
        return False


    def get_absolute_url(self):
        return reverse('url_%s_conf' % self.device.device_type.name, args=[str(self.id)])
        
    def get_absolute_mqtt_url(self):
        print("----------------- {} ----------------------".format(self.device.device_type.name),flush=True)
        if self.device.device_type.name=='abs':
            return reverse('url_%s_conf_mqtt' % self.device.device_type.name, args=[str(self.id)])
        else:
            return reverse('url_%s_conf' % self.device.device_type.name, args=[str(self.id)])

    def get_absolute_url_edit(self):
        return reverse('url_edit_%s_conf' % self.device.device_type.name, args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('url_delete_dev_conf', args=[str(self.id)])

    def get_absolute_url_import(self):
        return reverse('url_import_dev_conf', args=[str(self.id)])

    def get_absolute_url_export(self):
        return reverse('url_export_dev_conf', args=[str(self.id)])

    def get_absolute_url_write(self):
        return reverse('url_write_dev_conf', args=[str(self.id)])
    
    def get_absolute_url_write_mqtt(self):
        return reverse('url_write_mqtt_dev_conf', args=[str(self.id)])

    def get_absolute_url_read(self):
        return reverse('url_read_dev_conf', args=[str(self.id)])

    def get_absolute_url_start(self):
        return reverse('url_start_dev_conf', args=[str(self.id)])

    def get_absolute_url_stop(self):
        return reverse('url_stop_dev_conf', args=[str(self.id)])
    
    def get_absolute_url_stop_mqtt(self):
        return reverse('url_stop_mqtt_dev_conf', args=[str(self.id)])

    def get_absolute_url_status(self):
        return reverse('url_status_dev_conf', args=[str(self.id)])

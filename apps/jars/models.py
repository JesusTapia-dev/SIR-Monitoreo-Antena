import json
import requests

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse

from apps.main.models import Configuration
from apps.main.utils import Params
from .utils import create_jarsfiles

# Create your models here.

EXPERIMENT_TYPE = (
    (0, 'RAW_DATA'),
    (1, 'PDATA'),
)

DATA_TYPE = (
    (0, 'SHORT'),
    (1, 'FLOAT'),
)

DECODE_TYPE = (
    (0, 'None'),
    (1, 'TimeDomain'),
    (2, 'FreqDomain'),
    (3, 'InvFreqDomain'),
)

FILTER = '{"id":1, "clock": 60, "multiplier": 5, "frequency": 49.92, "f_decimal":	721554506, "fir": 2, "cic_2": 12, "cic_5": 25}'

class JARSFilter(models.Model):

    JARS_NBITS = 32

    name = models.CharField(verbose_name='Name', max_length=60, unique=True, default='')
    clock = models.FloatField(verbose_name='Clock In (MHz)', validators=[
                              MinValueValidator(5), MaxValueValidator(75)], null=True, default=60)
    multiplier = models.PositiveIntegerField(verbose_name='Multiplier', validators=[
                                             MinValueValidator(1), MaxValueValidator(20)], default=5)
    frequency = models.FloatField(verbose_name='Frequency (MHz)', validators=[
                                  MaxValueValidator(150)], null=True, default=49.9200)
    f_decimal = models.BigIntegerField(verbose_name='Frequency (Decimal)', validators=[
                                       MinValueValidator(-9223372036854775808), MaxValueValidator(2**JARS_NBITS-1)], null=True, default=721554505)
    cic_2 = models.PositiveIntegerField(verbose_name='CIC2', validators=[
                                        MinValueValidator(2), MaxValueValidator(100)], default=10)
    scale_cic_2 = models.PositiveIntegerField(verbose_name='Scale CIC2', validators=[
                                              MinValueValidator(0), MaxValueValidator(6)], default=1)
    cic_5 = models.PositiveIntegerField(verbose_name='CIC5', validators=[
                                        MinValueValidator(1), MaxValueValidator(100)], default=1)
    scale_cic_5 = models.PositiveIntegerField(verbose_name='Scale CIC5', validators=[
                                              MinValueValidator(0), MaxValueValidator(20)], default=5)
    fir = models.PositiveIntegerField(verbose_name='FIR', validators=[
                                      MinValueValidator(1), MaxValueValidator(100)], default=6)
    scale_fir = models.PositiveIntegerField(verbose_name='Scale FIR', validators=[
                                            MinValueValidator(0), MaxValueValidator(7)], default=3)
    number_taps = models.PositiveIntegerField(verbose_name='Number of taps', validators=[
                                              MinValueValidator(1), MaxValueValidator(256)], default=4)
    taps = models.CharField(verbose_name='Taps', max_length=256, default='')

    class Meta:
        db_table = 'jars_filters'

    def __unicode__(self):
        return u'%s' % (self.name)

    def jsonify(self):

        data = {}
        ignored = ()

        for field in self._meta.fields:
            if field.name in ignored:
                continue
            data[field.name] = field.value_from_object(self)

        return data

    def parms_to_dict(self):

        parameters = {}

        parameters['name'] = self.name
        parameters['clock'] = float(self.clock)
        parameters['multiplier'] = int(self.multiplier)
        parameters['frequency'] = float(self.frequency)
        parameters['f_decimal'] = int(self.frequency)
        parameters['fir'] = int(self.fir)
        parameters['cic_2'] = int(self.cic_2)
        parameters['cic_5'] = int(self.cic_5)

        return parameters

    def dict_to_parms(self, parameters):

        self.name = parameters['name']
        self.clock = parameters['clock']
        self.multiplier = parameters['multiplier']
        self.frequency = parameters['frequency']
        self.f_decimal = parameters['f_decimal']
        self.fir = parameters['fir']
        self.cic_2 = parameters['cic_2']
        self.cic_5 = parameters['cic_5']


class JARSConfiguration(Configuration):

    ADC_RESOLUTION = 8
    PCI_DIO_BUSWIDTH = 32
    HEADER_VERSION = 1103
    BEGIN_ON_START = True
    REFRESH_RATE = 1

    exp_type = models.PositiveIntegerField(
        verbose_name='Experiment Type', choices=EXPERIMENT_TYPE, default=0)
    cards_number = models.PositiveIntegerField(verbose_name='Number of Cards', validators=[
                                               MinValueValidator(1), MaxValueValidator(4)], default=1)
    channels_number = models.PositiveIntegerField(verbose_name='Number of Channels', validators=[
                                                  MinValueValidator(1), MaxValueValidator(8)], default=5)
    channels = models.CharField(
        verbose_name='Channels', max_length=15, default='1,2,3,4,5')
    data_type = models.PositiveIntegerField(
        verbose_name='Data Type', choices=DATA_TYPE, default=0)
    raw_data_blocks = models.PositiveIntegerField(
        verbose_name='Raw Data Blocks', validators=[MaxValueValidator(5000)], default=60)
    profiles_block = models.PositiveIntegerField(
        verbose_name='Profiles Per Block', default=400)
    acq_profiles = models.PositiveIntegerField(
        verbose_name='Acquired Profiles', default=400)
    ftp_interval = models.PositiveIntegerField(
        verbose_name='FTP Interval', default=60)
    fftpoints = models.PositiveIntegerField(
        verbose_name='FFT Points', default=16)
    cohe_integr_str = models.PositiveIntegerField(
        verbose_name='Coh. Int. Stride', validators=[MinValueValidator(1)], default=30)
    cohe_integr = models.PositiveIntegerField(
        verbose_name='Coherent Integrations', validators=[MinValueValidator(1)], default=30)
    incohe_integr = models.PositiveIntegerField(
        verbose_name='Incoherent Integrations', validators=[MinValueValidator(1)], default=30)
    decode_data = models.PositiveIntegerField(
        verbose_name='Decode Data', choices=DECODE_TYPE, default=0)
    post_coh_int = models.BooleanField(
        verbose_name='Post Coherent Integration', default=False)
    spectral_number = models.PositiveIntegerField(
        verbose_name='# Spectral Combinations', validators=[MinValueValidator(1)], default=1)
    spectral = models.CharField(
        verbose_name='Combinations', max_length=5000, default='[0, 0],')
    create_directory = models.BooleanField(
        verbose_name='Create Directory Per Day', default=True)
    include_expname = models.BooleanField(
        verbose_name='Experiment Name in Directory', default=False)
    #view_raw_data    = models.BooleanField(verbose_name='View Raw Data', default=True)
    save_ch_dc = models.BooleanField(
        verbose_name='Save Channels DC', default=True)
    save_data = models.BooleanField(verbose_name='Save Data', default=True)
    filter_parms = models.CharField(
        max_length=10000, default=FILTER)
    filter = models.ForeignKey(
        'JARSFilter', verbose_name='Filter', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'jars_configurations'

    def filter_resolution(self):
        filter_parms = json.loads(self.filter_parms)
        clock = float(filter_parms['clock'])
        cic_2 = filter_parms['cic_2']
        cic_5 = filter_parms['cic_5']
        fir = filter_parms['fir']
        resolution = round((clock/(cic_2*cic_5*fir)), 2)
        return resolution

    def dict_to_parms(self, params, id=None):

        if id is not None:
            data = Params(params).get_conf(id_conf=id)
        else:
            data = Params(params).get_conf(dtype='jars')
            data['filter_parms'] = params['filter_parms']

        # self.name = data['name']
        self.exp_type = data['exp_type']
        #----PDATA----
        if self.exp_type == 1:
            self.incohe_integr = data['incohe_integr']
            self.spectral_number = data['spectral_number']
            self.spectral = data['spectral']
            self.fftpoints = data['fftpoints']
            self.save_ch_dc = data['save_ch_dc']
        else:
            self.raw_data_blocks = data['raw_data_blocks']
        #----PDATA----
        self.cards_number = data['cards_number']
        self.channels_number = data['channels_number']
        self.channels = data['channels']
        self.data_type = data['data_type']
        self.profiles_block = data['profiles_block']
        self.acq_profiles = data['acq_profiles']
        self.ftp_interval = data['ftp_interval']
        self.cohe_integr_str = data['cohe_integr_str']
        self.cohe_integr = data['cohe_integr']
        #----DECODE----
        self.decode_data = data['decode_data']
        self.post_coh_int = data['post_coh_int']
        #----DECODE----
        self.create_directory = data['create_directory']
        self.include_expname = data['include_expname']
        self.save_data = data['save_data']
        self.filter_parms = json.dumps(data['filter_parms'])

        self.save()

    def parms_to_text(self, file_format='jars'):

        data = self.experiment.parms_to_dict()

        for key in data['configurations']['allIds']:
            if data['configurations']['byId'][key]['device_type'] in ('dds', 'cgs'):
                data['configurations']['allIds'].remove(key)
                data['configurations']['byId'].pop(key)
            elif data['configurations']['byId'][key]['device_type'] == 'jars':
                data['configurations']['byId'][key] = self.parms_to_dict(
                )['configurations']['byId'][str(self.pk)]
            elif data['configurations']['byId'][key]['device_type'] == 'rc':
                    data['configurations']['byId'][key]['pulses'] = ''
                    data['configurations']['byId'][key]['delays'] = ''
        rc_ids = [pk for pk in data['configurations']['allIds']
                  if data['configurations']['byId'][pk]['device_type'] == 'rc']
        mix_ids = [pk for pk in rc_ids if data['configurations']
                   ['byId'][pk]['mix']]

        if mix_ids:
            params = data['configurations']['byId'][mix_ids[0]]['parameters']
            rc = data['configurations']['byId'][params.split(
                '-')[0].split('|')[0]]
            rc['mix'] = True
            data['configurations']['byId'][rc['id']] = rc
        elif len(rc_ids) == 0:
            self.message = 'File needs RC configuration'
            return ''

        json_data = json.dumps(data)
        racp_file, filter_file = create_jarsfiles(json_data)
        if file_format == 'racp':
            return racp_file

        return filter_file

    def request(self, cmd, method='get', **kwargs):

        req = getattr(requests, method)(self.device.url(cmd), **kwargs)
        payload = req.json()
        return payload

    def status_device(self):

        try:
            payload = self.request('status',
                                   params={'name': self.experiment.name})
            self.device.status = payload['status']
            self.device.save()
            self.message = payload['message']
        except Exception as e:
            self.device.status = 0
            self.message = str(e)
            self.device.save()
            return False

        return True

    def stop_device(self):

        try:
            payload = self.request('stop', 'post')
            self.device.status = payload['status']
            self.device.save()
            self.message = payload['message']
        except Exception as e:
            self.device.status = 0
            self.message = str(e)
            self.device.save()
            return False

        return True

    def read_device(self):

        try:
            payload = self.request(
                'read', params={'name': self.experiment.name})
            self.message = 'Configuration loaded'
        except:
            self.device.status = 0
            self.device.save()
            self.message = 'Could not read JARS configuration.'
            return False

        return payload

    def write_device(self):

        if self.device.status == 3:
            self.message = 'Could not configure device. Software Acquisition is running'
            return False

        data = self.experiment.parms_to_dict()

        for key in data['configurations']['allIds']:
            if data['configurations']['byId'][key]['device_type'] in ('dds', 'cgs'):
                data['configurations']['allIds'].remove(key)
                data['configurations']['byId'].pop(key)
            elif data['configurations']['byId'][key]['device_type'] == 'rc':
                    data['configurations']['byId'][key]['pulses'] = ''
                    data['configurations']['byId'][key]['delays'] = ''
        rc_ids = [pk for pk in data['configurations']['allIds']
                  if data['configurations']['byId'][pk]['device_type'] == 'rc']
        if len(rc_ids) == 0:
            self.message = 'Missing RC configuration'
            return False

        json_data = json.dumps(data)

        try:
            payload = self.request('write', 'post', json=json_data)
            self.device.status = payload['status']
            self.message = payload['message']
            self.device.save()
            if self.device.status == 1:
                return False

        except Exception as e:
            self.device.status = 0
            self.message = str(e)
            self.device.save()
            return False

        return True

    def start_device(self):

        try:
            payload = self.request('start', 'post',
                                   json={'name': self.experiment.name})
            self.device.status = payload['status']
            self.message = payload['message']
            self.device.save()
            if self.device.status == 1:
                return False

        except Exception as e:
            self.device.status = 0
            self.message = str(e)
            self.device.save()
            return False

        return True

    def get_log(self):

        payload = None

        try:
            payload = requests.get(self.device.url('get_log'), params={
                                   'name': self.experiment.name})
        except:
            self.device.status = 0
            self.device.save()
            self.message = 'Jars API is not running.'
            return False

        self.message = 'Jars API is running'

        return payload

    def update_from_file(self, filename):

        f = JARSFile(filename)
        self.dict_to_parms(f.data)
        self.save()

    def get_absolute_url_import(self):
        return reverse('url_import_jars_conf', args=[str(self.id)])

    def get_absolute_url_read(self):
        return reverse('url_read_jars_conf', args=[str(self.id)])

    def get_absolute_url_log(self):
        return reverse('url_get_jars_log', args=[str(self.id)])

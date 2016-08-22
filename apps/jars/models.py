from django.db import models
from apps.main.models import Configuration
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse
from devices.jars import api

from apps.rc.models import RCConfiguration

import json
# Create your models here.

EXPERIMENT_TYPE = (
                   (0, 'RAW_DATA'),
                   (1, 'PDATA'),
                   )

DATA_TYPE = (
             (0, 'SHORT'),
             (1, 'FLOAT'),
             )

class JARSfilter(models.Model):
    
    JARS_NBITS = 32
    
    name        = models.CharField(max_length=60, unique=True, default='')
    clock       = models.FloatField(verbose_name='Clock In (MHz)',validators=[MinValueValidator(5), MaxValueValidator(75)], null=True, default=60)
    mult        = models.PositiveIntegerField(verbose_name='Multiplier',validators=[MinValueValidator(1), MaxValueValidator(20)], default=5)
    fch         = models.DecimalField(verbose_name='Frequency (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, null=True, default=49.9200)
    fch_decimal = models.BigIntegerField(verbose_name='Frequency (Decimal)',validators=[MinValueValidator(0), MaxValueValidator(2**JARS_NBITS-1)], null=True, default=721554505)
    filter_fir  = models.PositiveIntegerField(verbose_name='FIR Filter',validators=[MinValueValidator(1), MaxValueValidator(20)], default = 6)
    filter_2    = models.PositiveIntegerField(verbose_name='Filter 2',validators=[MinValueValidator(1), MaxValueValidator(20)], default = 10)
    filter_5    = models.PositiveIntegerField(verbose_name='Filter 5',validators=[MinValueValidator(1), MaxValueValidator(20)], default = 1)
    speed       = models.PositiveIntegerField(verbose_name='Speed',validators=[MinValueValidator(0), MaxValueValidator(100000)], default = 0)
        
    class Meta:
        db_table = 'jars_filters'
        
    def __unicode__(self):
        return u'%s' % (self.name)
    
    def parms_to_dict(self):
        
        parameters = {}
        
        parameters['name']        = self.name
        parameters['clock']       = float(self.clock)
        parameters['mult']        = int(self.mult)
        parameters['fch']         = float(self.fch)
        parameters['fch_decimal'] = int(self.fch)
        parameters['filter_fir']  = int(self.filter_fir)
        parameters['filter_2']    = int(self.filter_2)
        parameters['filter_5']    = int(self.filter_5)
        parameters['speed']       = int(self.speed)
        
        return parameters
    
    def dict_to_parms(self, parameters):
        
        self.name        = parameters['name']
        self.clock       = parameters['clock']
        self.mult        = parameters['mult']
        self.fch         = parameters['fch']
        self.fch_decimal = parameters['fch_decimal']
        self.filter_fir  = parameters['filter_fir']
        self.filter_2    = parameters['filter_2']
        self.filter_5    = parameters['filter_5']
        self.speed       = parameters['speed']
        

class JARSConfiguration(Configuration):
    
    ADC_RESOLUTION   = 8
    PCI_DIO_BUSWIDTH = 32
    HEADER_VERSION   = 1103
    BEGIN_ON_START   = True
    REFRESH_RATE     = 1
        
    #rc               = models.ForeignKey(RCConfiguration, on_delete=models.CASCADE, null=True)
    exp_type         = models.PositiveIntegerField(verbose_name='Experiment Type', choices=EXPERIMENT_TYPE, default=0)
    cards_number     = models.PositiveIntegerField(verbose_name='Number of Cards', validators=[MinValueValidator(1), MaxValueValidator(4)], default = 1)
    channels_number  = models.PositiveIntegerField(verbose_name='Number of Channels', validators=[MinValueValidator(1), MaxValueValidator(8)], default = 5)
    channels         = models.CharField(verbose_name='Channels', max_length=15, default = '1,2,3,4,5')
    rd_directory     = models.CharField(verbose_name='Raw Data Directory', max_length=200, default='', blank=True, null=True)
    pd_directory     = models.CharField(verbose_name='Process Data Directory', max_length=200, default='', blank=True, null=True)
    #raw_data_blocks  = models.PositiveIntegerField(verbose_name='Raw Data Blocks', validators=[MaxValueValidator(5000)], default=120)
    data_type        = models.PositiveIntegerField(verbose_name='Data Type', choices=DATA_TYPE, default=0)
    acq_profiles     = models.PositiveIntegerField(verbose_name='Acquired Profiles', validators=[MaxValueValidator(5000)], default=400)
    profiles_block   = models.PositiveIntegerField(verbose_name='Profiles Per Block', validators=[MaxValueValidator(5000)], default=400)
    ftp_interval     = models.PositiveIntegerField(verbose_name='FTP Interval', default=60)
    fftpoints        = models.PositiveIntegerField(verbose_name='FFT Points',default=16)
    cohe_integr_str  = models.PositiveIntegerField(verbose_name='Coh. Int. Stride',validators=[MinValueValidator(1)], default=30)
    cohe_integr      = models.PositiveIntegerField(verbose_name='Coherent Integrations',validators=[MinValueValidator(1)], default=30)
    incohe_integr    = models.PositiveIntegerField(verbose_name='Incoherent Integrations',validators=[MinValueValidator(1)], default=30)
    filter           = models.ForeignKey(JARSfilter, on_delete=models.CASCADE, null=True)
    spectral_number  = models.PositiveIntegerField(verbose_name='# Spectral Combinations',validators=[MinValueValidator(1)], default=1)
    spectral         = models.CharField(verbose_name='Combinations', max_length=5000, default = '[0, 0],')
    create_directory = models.BooleanField(verbose_name='Create Directory Per Day', default=True)
    include_expname  = models.BooleanField(verbose_name='Experiment Name in Directory', default=True)
    #acq_link         = models.BooleanField(verbose_name='Acquisition Link', default=True)
    #view_raw_data    = models.BooleanField(verbose_name='View Raw Data', default=True)
    save_ch_dc       = models.BooleanField(verbose_name='Save Channels DC', default=True)
    save_data        = models.BooleanField(verbose_name='Save Data', default=True)
    filter_parms     = models.CharField(max_length=10000, default='{}')

    class Meta:
        db_table = 'jars_configurations'
    
    def parms_to_dict(self):
        
        parameters = {}
        
        parameters['device_id']        = self.device.id
        parameters['name']             = self.name
        #parameters['rc']               = self.rc.name
        parameters['exp_type']         = self.exp_type
        parameters['exptype']          = EXPERIMENT_TYPE[self.exp_type][1]
        parameters['cards_number']     = self.cards_number
        parameters['channels_number']  = self.channels_number
        parameters['channels']         = self.channels
        parameters['rd_directory']     = self.rd_directory
        #parameters['raw_data_blocks']  = self.raw_data_blocks
        parameters['data_type']        = self.data_type
        parameters['cohe_integr_str']  = self.cohe_integr_str
        parameters['acq_profiles']     = self.acq_profiles
        parameters['profiles_block']   = self.profiles_block
        parameters['ftp_interval']     = self.ftp_interval
        parameters['fftpoints']        = self.fftpoints
        parameters['cohe_integr']      = self.cohe_integr
        #parameters['incohe_integr']    = self.incohe_integr
        parameters['filter']           = self.filter.name
        parameters['filter_parms']     = self.filter_parms
        #parameters['spectral_number']  = self.spectral_number
        #parameters['spectral']         = self.spectral
        parameters['create_directory'] = bool(self.create_directory)
        parameters['include_expname']  = bool(self.include_expname)
        #parameters['acq_link']         = bool(self.acq_link)
        #parameters['view_raw_data']    = bool(self.view_raw_data)
        parameters['save_ch_dc']       = bool(self.save_ch_dc)
        parameters['save_data']        = bool(self.save_data)
        
        if parameters['exptype'] == 'PDATA':
            parameters['incohe_integr']    = self.incohe_integr
            parameters['spectral_number']  = self.spectral_number
            parameters['spectral']         = self.spectral
            parameters['pd_directory']     = self.pd_directory
        
        return parameters
    
    def add_parms_to_filter(self):
        self.filter_parms = self.filter.parms_to_dict()
        self.save()
    
    def dict_to_parms(self, parameters):
        
        self.name           = parameters['name']
        self.device.id       = int(parameters['device_id'])
        
        self.exp_type        = int(parameters['exp_type'])
        if parameters['exptype'] == 'PDATA': 
            self.incohe_integr   = parameters['incohe_integr']
            self.spectral_number = parameters['spectral_number']
            self.spectral        = parameters['spectral']
            self.pd_directory    = parameters['pd_directory']
            
        self.cards_number    = int(parameters['cards_number'])
        self.channels_number = int(parameters['channels_number'])
        self.channels        = parameters['channels']
        self.rd_directory    = parameters['rd_directory']
        #self.raw_data_blocks = parameters['raw_data_blocks']
        self.data_type       = parameters['data_type']
        self.cohe_integr_str = parameters['cohe_integr_str']
        self.acq_profiles    = parameters['acq_profiles']
        self.profiles_block  = parameters['profiles_block']
        self.ftp_interval    = parameters['ftp_interval']
        self.fftpoints       = parameters['fftpoints']
        self.cohe_integr     = parameters['cohe_integr']
        
        filter_name       = parameters['filter']
        self.filter    = JARSfilter.objects.get(name=filter_name)
        self.add_parms_to_filter()
        self.filter_parms = parameters['filter_parms']
        
        self.create_directory = bool(parameters['create_directory'])
        self.include_expname  = bool(parameters['include_expname'])
        #self.acq_link         = bool(parameters['acq_link'])
        #self.view_raw_data    = bool(parameters['view_raw_data'])
        self.save_ch_dc       = bool(parameters['save_ch_dc'])
        self.save_data        = bool(parameters['save_data'])
    
    def status_device(self):
        
        answer = api.status(self.device.ip_address,self.device.port_address)
        self.device.status = int(answer[0])
        self.message = answer[2:]
        self.device.save()
        
        return self.device.status
    
    def stop_device(self):
        
        answer = api.stop(self.device.ip_address,self.device.port_address)
        self.device.status = int(answer[0])
        self.message = answer[2:]
        self.device.save()
        
        return self.device.status
    
    def read_device(self):
        
        answer = api.read(self.device.ip_address,self.device.port_address)
        self.device.status = int(answer[0])
        try:
            data = json.loads(answer[2:])
            parms = data['configurations']['jars']
        except:
            self.device.status = 0
            self.device.save()
            self.message = 'Could not read JARS configuration.'
            return ''
        
        #self.dict_to_parms(parms)
        self.message = 'Current JARS configuration was read successfully.'
        self.device.save()
        return parms
    
    
    def write_device(self):
        
        data = self.experiment.parms_to_dict()
        data = json.loads(data)
        data['configurations']['dds']         =''
        data['configurations']['cgs']         =''
        data['configurations']['rc']['pulses']=''
        data['configurations']['rc']['delays']=''
        json_data = json.dumps(data)
        
        answer = api.configure(self.device.ip_address,self.device.port_address,json_data)
        #print answer
        self.device.status = int(answer[0])
        self.message = answer[2:]
        
        self.device.save()
        
        return self.device.status
    
    
    def start_device(self):
        
        self.write_device()
    
    
    def echo(self):
        
        answer = api.echo(self.device.ip_address,self.device.port_address,'(=')
        #print answer
        self.device.status = int(answer[0])
        self.message = answer[2:]
        
        self.device.save()
        
        return #self.device.status
    
    def update_from_file(self, parameters):
        
        self.dict_to_parms(parameters)
        self.save()
    
    def get_absolute_url_import(self):
        return reverse('url_import_jars_conf', args=[str(self.id)])
    
    def get_absolute_url_read(self):
        return reverse('url_read_jars_conf', args=[str(self.id)])
from django.db import models
from apps.main.models import Configuration
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.rc.models import RCConfiguration
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
    
    name       = models.CharField(max_length=60, unique=True, default='')
    filter_fir = models.PositiveIntegerField(verbose_name='FIR Filter',validators=[MinValueValidator(1), MaxValueValidator(20)], default = 1)
    filter_2   = models.PositiveIntegerField(verbose_name='Filter 2',validators=[MinValueValidator(1), MaxValueValidator(20)], default = 1)
    filter_5   = models.PositiveIntegerField(verbose_name='Filter 5',validators=[MinValueValidator(1), MaxValueValidator(20)], default = 1)
        
    class Meta:
        db_table = 'jars_filters'
        #ordering = ['channel']
        

class JARSConfiguration(Configuration):
    
    ADC_RESOLUTION   = 8
    PCI_DIO_BUSWIDTH = 32
    HEADER_VERSION   = 1103
    BEGIN_ON_START   = True
    REFRESH_RATE     = 1
        
    rc               = models.ForeignKey(RCConfiguration, on_delete=models.CASCADE, null=True)
    exp_type         = models.PositiveIntegerField(verbose_name='Experiment Type', choices=EXPERIMENT_TYPE, default=0)
    cards_number     = models.PositiveIntegerField(verbose_name='Number of Cards', validators=[MinValueValidator(1), MaxValueValidator(4)], default = 1)
    channels_number  = models.PositiveIntegerField(verbose_name='Number of Channels', validators=[MinValueValidator(1), MaxValueValidator(8)], default = 5)
    channels         = models.CharField(verbose_name='Channels', max_length=15, default = '1,2,3,4,5')
    rd_directory     = models.CharField(verbose_name='Raw Data Directory', max_length=40, default='', blank=True, null=True)
    raw_data_blocks  = models.PositiveIntegerField(verbose_name='Raw Data Blocks', validators=[MaxValueValidator(5000)], default=120)
    data_type        = models.PositiveIntegerField(verbose_name='Data Type', choices=DATA_TYPE, default=0)
    acq_profiles     = models.PositiveIntegerField(verbose_name='Acquired Profiles', validators=[MaxValueValidator(5000)], default=400)
    profiles_block   = models.PositiveIntegerField(verbose_name='Profiles Per Block', validators=[MaxValueValidator(5000)], default=400)
    fftpoints        = models.PositiveIntegerField(verbose_name='FFT Points',default=16)
    incohe_integr    = models.PositiveIntegerField(verbose_name='Incoherent Integrations',validators=[MinValueValidator(1)], default = 30)
    filter           = models.ForeignKey(JARSfilter, on_delete=models.CASCADE, null=True, blank=True)
    spectral_number  = models.PositiveIntegerField(verbose_name='# Spectral Combinations',validators=[MinValueValidator(1)], null=True, blank=True)
    spectral         = models.CharField(verbose_name='Combinations', max_length=5000, default = '[0,0]')
    create_directory = models.BooleanField(verbose_name='Create Directory Per Day', default=True)
    include_expname  = models.BooleanField(verbose_name='Experiment Name in Directory', default=True)
    acq_link         = models.BooleanField(verbose_name='Acquisition Link', default=True)
    view_raw_data    = models.BooleanField(verbose_name='View Raw Data', default=True)
    save_ch_dc       = models.BooleanField(verbose_name='Save Channels DC', default=True)

    class Meta:
        db_table = 'jars_configurations'
    
    def parms_to_dict(self):
        
        parameters = {}
        
        parameters['name']             = self.name
        parameters['rc']               = self.rc.name
        parameters['exp_type']         = self.exp_type
        parameters['cards_number']     = self.cards_number
        parameters['channels_number']  = self.channels_number
        parameters['channels']         = self.channels
        parameters['rd_directory']     = self.rd_directory
        parameters['raw_data_blocks']  = self.raw_data_blocks
        parameters['data_type']        = self.data_type
        parameters['acq_profiles']     = self.acq_profiles
        parameters['profiles_block']   = self.profiles_block
        parameters['filter']           = self.filter.name
        parameters['create_directory'] = bool(self.create_directory)
        parameters['include_expname']  = bool(self.include_expname)
        parameters['acq_link']         = bool(self.acq_link)
        parameters['view_raw_data']    = bool(self.view_raw_data)          
        
        return parameters
    
    def dict_to_parms(self, parameters):
        return
    
    def status_device(self):
        return 
    
    def read_device(self):
        return 
    
    def write_device(self):
        return
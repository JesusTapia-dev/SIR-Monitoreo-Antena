from django.db import models
from apps.main.models import Configuration
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

ANSWER = (
          (False, 'NO'),
          (True, 'YES'),
          )

class JARSConfiguration(Configuration):
    
    ADC_RESOLUTION   = 8
    PCI_DIO_BUSWIDTH = 32
        
    cards_number     = models.PositiveIntegerField(verbose_name='Number of Cards',validators=[MaxValueValidator(4)], default = 1)
    channels_number  = models.PositiveIntegerField(verbose_name='Number of Channels',validators=[MinValueValidator(1), MaxValueValidator(8)], default = 1)
    rd_directory     = models.CharField(verbose_name='Raw Data Directory', max_length=40, default='', blank=True, null=True)
    raw_data_blocks  = models.PositiveIntegerField(verbose_name='Raw Data Blocks',validators=[MaxValueValidator(5000)], default=120)
    acq_profiles     = models.PositiveIntegerField(verbose_name='Acquired Profiles',validators=[MaxValueValidator(5000)], default=400)
    profiles_block   = models.PositiveIntegerField(verbose_name='Profiles Per Block',validators=[MaxValueValidator(5000)], default=400)
    create_directory = models.BooleanField(verbose_name='Create Directory Per Day', default=True)
    include_expname  = models.BooleanField(verbose_name='Include Experiment Name in Directory', default=True)

    class Meta:
        db_table = 'jars_configurations'
    
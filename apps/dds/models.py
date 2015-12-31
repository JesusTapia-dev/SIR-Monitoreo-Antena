from django.db import models
from apps.main.models import Configuration
# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator

MOD_TYPES = (
    (None, 'Select a modulation type'),
    (0, 'No modulation'),
    (1, 'ASK'),
    (2, 'FSK'),
    (3, 'PSK'),
)

class DDSConfiguration(Configuration):
    
    clock = models.FloatField(verbose_name='Clock Master (MHz)',validators=[MinValueValidator(5), MaxValueValidator(50)], blank=True, null=True)
    multiplier = models.PositiveIntegerField(verbose_name='Multiplier',validators=[MinValueValidator(1), MaxValueValidator(20)], default=4)
    freq_reg = models.PositiveIntegerField(verbose_name='Frequency (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**32-1)], blank=True, null=True)
    phase_reg = models.PositiveIntegerField(verbose_name='Phase (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**14-1)], blank=True, null=True)
    
    amplitude_chA = models.PositiveIntegerField(verbose_name='Amplitude CHA',validators=[MinValueValidator(0), MaxValueValidator(2**10-1)], blank=True, null=True)
    amplitude_chB = models.PositiveIntegerField(verbose_name='Amplitude CHB',validators=[MinValueValidator(0), MaxValueValidator(2**10-1)], blank=True, null=True)
    
    modulation = models.PositiveIntegerField(choices = MOD_TYPES, default = 0)
    freq_reg_mod = models.PositiveIntegerField(verbose_name='Frequency Mod (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**32-1)], blank=True, null=True)
    phase_reg_mod = models.PositiveIntegerField(verbose_name='Phase Mod (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**14-1)], blank=True, null=True)
    
    class Meta:
        db_table = 'dds_configurations'
    
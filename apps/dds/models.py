from django.db import models
from apps.main.models import Configuration
# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator

class DDSConfiguration(Configuration):
    
    clock = models.FloatField(verbose_name='Clock Master',validators=[MinValueValidator(5e6), MaxValueValidator(50e6)], blank=True, null=True)
    multiplier = models.PositiveIntegerField(verbose_name='Multiplier',validators=[MinValueValidator(0), MaxValueValidator(20)], default=4)
    modulation = models.PositiveIntegerField(verbose_name='Modulation',validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    frequency0 = models.PositiveIntegerField(verbose_name='Frequency 0',validators=[MinValueValidator(0), MaxValueValidator(2**32-1)], blank=True, null=True)
    frequency1 = models.PositiveIntegerField(verbose_name='Frequency 1',validators=[MinValueValidator(0), MaxValueValidator(2**32-1)], blank=True, null=True)
    phase0 = models.PositiveIntegerField(verbose_name='Phase 0',validators=[MinValueValidator(0), MaxValueValidator(2**14-1)], blank=True, null=True)
    phase1 = models.PositiveIntegerField(verbose_name='Phase 1',validators=[MinValueValidator(0), MaxValueValidator(2**14-1)], blank=True, null=True)
    amplitude_chA = models.PositiveIntegerField(verbose_name='Amplitude CHA',validators=[MinValueValidator(0), MaxValueValidator(2**10-1)], blank=True, null=True)
    amplitude_chB = models.PositiveIntegerField(verbose_name='Amplitude CHB',validators=[MinValueValidator(0), MaxValueValidator(2**10-1)], blank=True, null=True)
    
    class Meta:
        db_table = 'dds_configurations'
    
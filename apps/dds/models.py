from django.db import models
from apps.main.models import Configuration
# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

MOD_TYPES = (
    (None, 'Select a modulation type'),
    (0, 'Single Tone'),
    (1, 'FSK'),
    (2, 'Ramped FSK'),
    (3, 'Chirp'),
    (4, 'BPSK'),
)

class DDSConfiguration(Configuration):
    
    DDS_NBITS = 48
    
    clock = models.FloatField(verbose_name='Clock Master (MHz)',validators=[MinValueValidator(5), MaxValueValidator(75)])
    multiplier = models.PositiveIntegerField(verbose_name='Multiplier',validators=[MinValueValidator(1), MaxValueValidator(20)], default=4)

    frequency = models.DecimalField(verbose_name='Frequency (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=17, decimal_places=15)
    frequency_bin = models.BigIntegerField(verbose_name='Frequency (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)])
    
    phase = models.FloatField(verbose_name='Phase (Degrees)', validators=[MinValueValidator(0), MaxValueValidator(360)])
#     phase_binary = models.PositiveIntegerField(verbose_name='Phase (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**14-1)])
     
    amplitude_ch_A = models.PositiveIntegerField(verbose_name='Amplitude CHA',validators=[MinValueValidator(0), MaxValueValidator(2**10-1)], blank=True, null=True)
    amplitude_ch_B = models.PositiveIntegerField(verbose_name='Amplitude CHB',validators=[MinValueValidator(0), MaxValueValidator(2**10-1)], blank=True, null=True)
    
    modulation = models.PositiveIntegerField(choices = MOD_TYPES, default = 0)
    
    frequency_mod = models.DecimalField(verbose_name='Frequency Mod. (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=17, decimal_places=15, blank=True, null=True)
    frequency_mod_bin = models.BigIntegerField(verbose_name='Frequency Mod. (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)], blank=True, null=True)
    
    phase_mod = models.FloatField(verbose_name='Phase Mod. (Degrees)', validators=[MinValueValidator(0), MaxValueValidator(360)], blank=True, null=True)
#     phase_binary_mod = models.PositiveIntegerField(verbose_name='Phase Mod (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**14-1)], blank=True, null=True)
    
    def get_nbits(self):
        
        return self.DDS_NBITS
    
    def clean(self):
        
        if self.modulation in [1,2,3]:
            if self.frequency_mod is None or self.frequency_mod_bin is None:
                raise ValidationError({
                    'frequency_mod': 'Frequency modulation has to be defined when FSK or Chirp modulation is selected'
                })
          
        if self.modulation in [4,]:
            if self.phase_mod is None:
                raise ValidationError({
                    'phase_mod': 'Phase modulation has to be defined when BPSK modulation is selected'
                })
        
    def verify_frequencies(self):
        
        return True
    
    def freq2binary(self, freq, mclock):
        
        binary = (float(freq)/mclock)*(2**self.DDS_NBITS)
        
        return binary
    
    def binary2freq(self, binary, mclock):
        
        freq = (float(binary)/(2**self.DDS_NBITS))*mclock
        
        return freq
    
    class Meta:
        db_table = 'dds_configurations'
    
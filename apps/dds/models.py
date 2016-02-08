from django.db import models
from apps.main.models import Configuration
# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from files import read_dds_file, read_json_file

MOD_TYPES = (
    (0, 'Single Tone'),
    (1, 'FSK'),
    (2, 'Ramped FSK'),
    (3, 'Chirp'),
    (4, 'BPSK'),
)

class DDSConfiguration(Configuration):
    
    DDS_NBITS = 48
    
    clock = models.FloatField(verbose_name='Clock Input (MHz)',validators=[MinValueValidator(5), MaxValueValidator(75)], null=True)
    multiplier = models.PositiveIntegerField(verbose_name='Multiplier',validators=[MinValueValidator(1), MaxValueValidator(20)], default=4)

    frequency = models.DecimalField(verbose_name='Frequency (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16)
    frequency_bin = models.BigIntegerField(verbose_name='Frequency (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)])
    
    phase = models.FloatField(verbose_name='Phase (Degrees)', validators=[MinValueValidator(0), MaxValueValidator(360)], default=0)
#     phase_binary = models.PositiveIntegerField(verbose_name='Phase (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**14-1)])
     
    amplitude_ch_A = models.PositiveIntegerField(verbose_name='Amplitude CH A',validators=[MinValueValidator(0), MaxValueValidator(2**12-1)], blank=True, null=True)
    amplitude_ch_B = models.PositiveIntegerField(verbose_name='Amplitude CH B',validators=[MinValueValidator(0), MaxValueValidator(2**12-1)], blank=True, null=True)
    
    modulation = models.PositiveIntegerField(verbose_name='Modulation Type', choices = MOD_TYPES, default = 0)
    
    frequency_mod = models.DecimalField(verbose_name='Mod: Frequency (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], max_digits=19, decimal_places=16, blank=True, null=True)
    frequency_mod_bin = models.BigIntegerField(verbose_name='Mod: Frequency (Binary)',validators=[MinValueValidator(0), MaxValueValidator(2**DDS_NBITS-1)], blank=True, null=True)
    
    phase_mod = models.FloatField(verbose_name='Mod: Phase (Degrees)', validators=[MinValueValidator(0), MaxValueValidator(360)], blank=True, null=True)
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
    
    def phase2binary(self, phase):
        
        binary = phase*8192/180.0
        
        return binary
    
    def binary2phase(self, binary):
        
        phase = binary*180.0/8192
        
        return phase
    
    def export_file(self, ext_file="dds"):
        
        pass
    
    def update_from_file(self, fp, ext_file="dds"):
        
        if ext_file == "dds":
            kwargs = read_dds_file(fp)
        else:
            kwargs = read_json_file(fp)
        
        if not kwargs:
            return False
        
        self.clock = kwargs['clock']
        self.multiplier = kwargs['multiplier']
    
        mclock = self.clock*self.multiplier
        
        self.frequency = self.binary2freq(kwargs['frequency_bin'], mclock)
        self.frequency_bin = kwargs['frequency_bin']
        
        self.frequency_mod = self.binary2freq(kwargs['frequency_mod_bin'], mclock)
        self.frequency_mod_bin = kwargs['frequency_mod_bin']
        
        self.phase = self.binary2phase(kwargs['phase_bin'])
        self.phase_mod = self.binary2phase(kwargs['phase_mod_bin'])
        
        self.modulation = kwargs['modulation']
        
        self.amplitude_ch_A = kwargs['amplitude_ch_A']
        self.amplitude_ch_B = kwargs['amplitude_ch_B']
        
        return True
    
    class Meta:
        db_table = 'dds_configurations'
    
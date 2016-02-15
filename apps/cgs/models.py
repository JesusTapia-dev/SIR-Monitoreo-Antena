from django.db import models
from apps.main.models import Configuration
#from json_field import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator


from apps.main.models import Device, Experiment

from files import read_json_file
# Create your models here.

class CGSConfiguration(Configuration):
    
    freq0 = models.FloatField(verbose_name='Frequency 0',validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)], blank=True, null=True)
    freq1 = models.FloatField(verbose_name='Frequency 1',validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)], blank=True, null=True)
    freq2 = models.FloatField(verbose_name='Frequency 2',validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)], blank=True, null=True)
    freq3 = models.FloatField(verbose_name='Frequency 3',validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)], blank=True, null=True)
    #jfreqs = JSONField(default={"frequencies":[{"f0":freq0,"f1":freq1,"f2":freq2,"f3":freq3}]}, blank=True)
    
    
    def verify_frequencies(self):
        
        return True
    
    
    def update_from_file(self, fp):
        
        kwargs = read_json_file(fp)
        
        if not kwargs:
            return False
        
        self.freq0 = kwargs['freq0']
        self.freq1 = kwargs['freq1']
        self.freq2 = kwargs['freq2']
        self.freq3 = kwargs['freq3']
        
        return True


    class Meta:
        db_table = 'cgs_configurations'

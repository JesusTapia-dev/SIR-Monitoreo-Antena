from django.db import models

from json_field import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator


from apps.main.models import Device, Experiment

# Create your models here.
class CGSConfiguration(models.Model):

    device = models.ForeignKey(Device)
    exp    = models.ForeignKey(Experiment, default = None)
    freq0 = models.FloatField(verbose_name='Frequency 0',validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)])  
    freq1 = models.FloatField(verbose_name='Frequency 1',validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)])  
    freq2 = models.FloatField(verbose_name='Frequency 2',validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)])
    freq3 = models.PositiveIntegerField(verbose_name='Frequency 3',validators=[MinValueValidator(62.5e6), MaxValueValidator(450e6)])  
    freqs = JSONField(default={"frequencies":[{"f0":freq0,"f1":freq1,"f2":freq2,"f3":freq3}]}, blank=True)
    #clk_in = models.PositiveIntegerField(default=10e6)
    #mult = models.PositiveIntegerField(default=40)
    #div = models.PositiveIntegerField(default=1)



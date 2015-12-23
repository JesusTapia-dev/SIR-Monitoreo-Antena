from django import forms
from .models import DDSConfiguration

from django.core.validators import MinValueValidator, MaxValueValidator

class DDSConfigurationForm(forms.ModelForm):
    
    freq0 = forms.FloatField(label='Frequency', validators=[MinValueValidator(0e6), MaxValueValidator(150e6)])
    pha0 = forms.FloatField(label='Phase', validators=[MinValueValidator(0), MaxValueValidator(360)])
    
    freq1 = forms.FloatField(label='Modulated Frequency', validators=[MinValueValidator(5e6), MaxValueValidator(150e6)], required=False)
    pha1 = forms.FloatField(label='Modulated Phase', validators=[MinValueValidator(0), MaxValueValidator(360)], required=False)
    
    def __init__(self, *args, **kwargs):
        #request = kwargs.pop('request')
        super(DDSConfigurationForm, self).__init__(*args, **kwargs)

    def clean(self):
        # Custom validation to force an integer when type of unit = "Unit"
        return 

    class Meta:
        model = DDSConfiguration
        fields = ('clock', 'multiplier', 'modulation')

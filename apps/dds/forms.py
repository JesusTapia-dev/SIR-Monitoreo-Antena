from django import forms
from apps.main.models import Device
from .models import DDSConfiguration

from django.core.validators import MinValueValidator, MaxValueValidator

class DDSConfigurationForm(forms.ModelForm):
    
    frequency = forms.FloatField(label='Frequency (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)])
    phase = forms.FloatField(label='Phase (Degrees)', validators=[MinValueValidator(0), MaxValueValidator(360)])
    
    frequency_mod = forms.FloatField(label='Frequency (MHz)', validators=[MinValueValidator(0), MaxValueValidator(150)], required=False)
    phase_mod = forms.FloatField(label='Phase (Degrees)', validators=[MinValueValidator(0), MaxValueValidator(360)], required=False)
    
    def __init__(self, *args, **kwargs):
        #request = kwargs.pop('request')
        super(DDSConfigurationForm, self).__init__(*args, **kwargs)
        
        instance = getattr(self, 'instance', None)
        
        if instance and instance.pk:
            
            devices = Device.objects.filter(device_type__name='dds')
            items = devices.values('id', 'name', 'device_type__name', 'ip_address')
            
            self.fields['experiment'].widget.attrs['readonly'] = True
            self.fields['device'].widget.choices = [(item['id'], '[%s]: %s | %s' % (item['device_type__name'], item['name'], item['ip_address'])) for item in items]
    
    
    def clean(self):
        # Custom validation to force an integer when type of unit = "Unit"
        return 

    class Meta:
        model = DDSConfiguration
        fields = ('experiment', 'device', 'clock', 'multiplier', 'modulation')

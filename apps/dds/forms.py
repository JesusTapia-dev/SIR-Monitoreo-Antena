from django import forms
from apps.main.models import Device
from .models import DDSConfiguration

# from django.core.validators import MinValueValidator, MaxValueValidator

class DDSConfigurationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        super(DDSConfigurationForm, self).__init__(*args, **kwargs)
        
        instance = getattr(self, 'instance', None)
        
        if instance and instance.pk:
            
            devices = Device.objects.filter(device_type__name='dds')
            
            #if instance.experiment:
            #    self.fields['experiment'].widget.attrs['disabled'] = 'disabled'
            
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
    

    class Meta:
        model = DDSConfiguration
        exclude = ('type', 'parameters', 'status', 'author', 'hash')
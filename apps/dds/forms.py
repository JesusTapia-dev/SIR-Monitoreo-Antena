from django import forms
from apps.main.models import Device
from .models import DDSConfiguration

# from django.core.validators import MinValueValidator, MaxValueValidator

class DDSConfigurationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        #request = kwargs.pop('request')
        super(DDSConfigurationForm, self).__init__(*args, **kwargs)
        
        instance = getattr(self, 'instance', None)
        
        if instance and instance.pk:
            
            devices = Device.objects.filter(device_type__name='dds')
            
            self.fields['experiment'].widget.attrs['readonly'] = True
            
            if instance.experiment is not None:
                self.fields['experiment'].widget.choices = [(instance.experiment.id, instance.experiment)]
            
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
    

    class Meta:
        model = DDSConfiguration
        exclude = ('type', 'parameters', 'status')
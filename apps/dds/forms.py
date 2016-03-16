from django import forms
from apps.main.models import Device
from .models import DDSConfiguration

# from django.core.validators import MinValueValidator, MaxValueValidator

EXT_TYPES = (
    ('dds', '.dds'),
    ('json', '.json'),
)

class DDSConfigurationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        #request = kwargs.pop('request')
        super(DDSConfigurationForm, self).__init__(*args, **kwargs)
        
        instance = getattr(self, 'instance', None)
        
        if instance and instance.pk:
            
            devices = Device.objects.filter(device_type__name='dds')
            
            self.fields['experiment'].widget.attrs['readonly'] = True
            self.fields['experiment'].widget.choices = [(instance.experiment.id, instance.experiment)]
            
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
    
    
    def clean(self):
        # Custom validation to force an integer when type of unit = "Unit"
        return 

    class Meta:
        model = DDSConfiguration
        exclude = ('type', 'parameters', 'status')
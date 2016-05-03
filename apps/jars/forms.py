from django import forms
from apps.main.models import Device
from .models import JARSConfiguration

class JARSConfigurationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JARSConfigurationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
                    
        if instance and instance.pk:
            devices = Device.objects.filter(device_type__name='jars')
            
            if instance.experiment:
                self.fields['experiment'].widget.attrs['disabled'] = 'disabled'
            
            #self.fields['experiment'].widget.attrs['readonly'] = True
            #self.fields['experiment'].widget.choices = [(instance.experiment.id, instance.experiment)]
            
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
            
    class Meta:
        model = JARSConfiguration
        exclude = ('type', 'parameters', 'status')

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
            
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
            
    #-------------JARS Configuration needs an Experiment-----------------
    def clean(self):
        cleaned_data = super(JARSConfigurationForm, self).clean()
        experiment = cleaned_data.get("experiment")
        if experiment == None:
            msg = "Jars Configuration needs an Experiment."
            self.add_error('experiment', msg)

    class Meta:
        model = JARSConfiguration
        exclude = ('type', 'parameters', 'status')

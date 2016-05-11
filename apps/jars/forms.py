from django import forms
from apps.main.models import Device, Experiment
from .models import JARSConfiguration, JARSfilter
from .widgets import SpectralWidget

class JARSConfigurationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JARSConfigurationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
                    
        if instance and instance.pk:
            devices = Device.objects.filter(device_type__name='jars')
                        
            if instance.experiment:
                experiments = Experiment.objects.filter(pk=instance.experiment.id)
                self.fields['experiment'].widget.choices = [(experiment.id, experiment) for experiment in experiments]
                
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
            #self.fields['spectral'].widget = SpectralWidget()
        self.fields['spectral'].widget = SpectralWidget()
    #-------------JARS Configuration needs an Experiment-----------------
    def clean(self):
        cleaned_data = super(JARSConfigurationForm, self).clean()
        experiment = cleaned_data.get('experiment')
        if experiment == None:
            msg = "Error: Jars Configuration needs an Experiment"
            self.add_error('experiment', msg)
    
    class Meta:
        model = JARSConfiguration
        exclude = ('type', 'parameters', 'status')
        
        
class JARSfilterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JARSfilterForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
                    
    class Meta:
        model = JARSfilter
        exclude = ('type', 'parameters', 'status')
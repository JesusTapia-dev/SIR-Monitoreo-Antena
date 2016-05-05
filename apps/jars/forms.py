from django import forms
from apps.main.models import Device, Experiment
from .models import JARSConfiguration

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
            
    #-------------JARS Configuration needs an Experiment-----------------
    def clean(self):
        cleaned_data = super(JARSConfigurationForm, self).clean()
        experiment = cleaned_data.get('experiment')
        if experiment == None:
            msg = "Error: Jars Configuration needs an Experiment"
            self.add_error('experiment', msg)
    
    class Meta:
        model = JARSConfiguration
        exclude = ('type', 'parameters', 'status', 'rc', 'cards_number',
                   'channels_number', 'channels', 'rd_directory', 'raw_data_blocks',
                   'data_type', 'acq_profiles', 'profiles_block', 'filter',
                   'create_directory', 'include_expname', 'acq_link',
                   'view_raw_data')
        

class JARSConfigurationForm_Raw(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JARSConfigurationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
                    
        if instance and instance.pk:
            devices = Device.objects.filter(device_type__name='jars')
                        
            if instance.experiment:
                experiments = Experiment.objects.filter(pk=instance.experiment.id)
                self.fields['experiment'].widget.choices = [(experiment.id, experiment) for experiment in experiments]
                
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
            
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
        
        
class JARSConfigurationForm_Pro(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JARSConfigurationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
                    
        if instance and instance.pk:
            devices = Device.objects.filter(device_type__name='jars')
                        
            if instance.experiment:
                experiments = Experiment.objects.filter(pk=instance.experiment.id)
                self.fields['experiment'].widget.choices = [(experiment.id, experiment) for experiment in experiments]
                
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
            
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

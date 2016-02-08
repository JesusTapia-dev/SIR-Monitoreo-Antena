from django import forms
from apps.main.models import Device
from .models import DDSConfiguration

# from django.core.validators import MinValueValidator, MaxValueValidator

EXT_TYPES = (
    ('dds', '.dds'),
    ('json', '.json'),
)

class DDSConfigurationForm(forms.ModelForm):
    
#     frequency_bin = forms.IntegerField(label='Frequency (Binary)', required=False)
#     phase_bin = forms.IntegerField(label='Phase (Binary)', required=False)
    
#     frequency_mod_bin = forms.IntegerField(label='Frequency Mod (Binary)', required=False)
#     phase_mod_bin = forms.IntegerField(label='Phase Mod (Binary)', required=False)
    
    field_order = ['experiment', 'device',
                   'clock', 'multiplier',
                   'frequency',
                   'frequency_bin',
                   'phase',
                   'phase_bin',
                   'amplitude_chA', 'amplitude_chB',
                   'modulation',
                   'frequency_mod',
                   'frequency_mod_bin',
                   'phase_mod',
                   'phase_mod_bin']
    
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
        exclude = ('type','parameters')

class UploadFileForm(forms.Form):
    
    title = forms.ChoiceField(label='Extension Type', choices=EXT_TYPES)
    file = forms.FileField()
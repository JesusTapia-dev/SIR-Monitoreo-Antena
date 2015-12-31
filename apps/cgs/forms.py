from django import forms
from apps.main.models import Device
from .models import CGSConfiguration

class CGSConfigurationForm(forms.ModelForm):
    #freq0.widget = te 
    def __init__(self, *args, **kwargs):
        #request = kwargs.pop('request')
        super(CGSConfigurationForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        
        if instance and instance.pk:
            
            devices = Device.objects.filter(device_type__name='cgs')
            items = devices.values('id', 'name', 'device_type__name', 'ip_address')
            
            self.fields['experiment'].widget.attrs['readonly'] = True
            self.fields['device'].widget.choices = [(item['id'], '[%s]: %s | %s' % (item['device_type__name'], item['name'], item['ip_address'])) for item in items]
    
    def clean(self):
        return
#         # Custom validation to force an integer when type of unit = "Unit"
#         form_data = self.cleaned_data
#         if (form_data['freq0'] or form_data['freq1'] or form_data['freq2'] or form_data['freq3'] < 0):
#             raise forms.ValidationError("Please introduce positive Number")
#  
#         return form_data

    class Meta:
        model = CGSConfiguration
        #exclude = ('freqs', 'clk_in', 'mult','div',)
#         exclude = ('freqs',)
        fields = ('experiment', 'device', 'freq0', 'freq1', 'freq2', 'freq3')

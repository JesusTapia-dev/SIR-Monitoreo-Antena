from django import forms
from apps.main.models import Device
from .models import JARSConfiguration

class JARSConfigurationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JARSConfigurationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['experiment'].widget.attrs['disabled'] = True
            self.fields['device'].widget.choices = [(item['id'], '%s | %s' % (item['device_type__name'], item['ip_address'])) for item in Device.objects.filter(device_type__name='jars').values('id', 'device_type__name', 'ip_address')]
    
    class Meta:
        model = JARSConfiguration
        exclude = ('parameters', 'status')

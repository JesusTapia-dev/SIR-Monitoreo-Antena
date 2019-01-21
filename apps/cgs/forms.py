from django import forms
from apps.main.models import Device
from .models import CGSConfiguration

class CGSConfigurationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #request = kwargs.pop('request')
        super(CGSConfigurationForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)

        if instance and instance.pk:

            devices = Device.objects.filter(device_type__name='cgs')

            if instance.experiment:
                self.fields['experiment'].widget.attrs['disabled'] = 'disabled'

            self.fields['device'].widget.choices = [(device.id, device) for device in devices]

    def clean(self):
        return       

    class Meta:
        model = CGSConfiguration
        exclude = ('type', 'parameters', 'status', 'author', 'hash')


class UploadFileForm(forms.Form):
    title = forms.CharField(label='Extension Type', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    file = forms.FileField()

from django import forms
from apps.main.models import Device
from .models import DDSRestConfiguration

# from django.core.validators import MinValueValidator, MaxValueValidator

class DDSRestConfigurationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(DDSRestConfigurationForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)

        if instance and instance.pk:

            devices = Device.objects.filter(device_type__name='dds_rest')

            #if instance.experiment:
            #    self.fields['experiment'].widget.attrs['disabled'] = 'disabled'

            self.fields['device'].widget.choices = [(device.id, device) for device in devices]


    class Meta:
        model = DDSRestConfiguration
        exclude = ('type', 'parameters', 'status', 'author', 'hash')

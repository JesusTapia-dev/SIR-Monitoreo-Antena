import os

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
        self.fields['spectral_number'].widget.attrs['readonly'] = True
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
        exclude = ('type', 'parameters', 'status', 'filter_parms')


class JARSfilterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JARSfilterForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.fields['fch_decimal'].widget.attrs['readonly'] = True

        if 'initial' in kwargs:
            self.fields.pop('name')
            #self.fields['name'].widget.attrs['disabled'] = 'disabled'


    class Meta:
        model = JARSfilter
        exclude = ('type', 'parameters', 'status')

class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    >>> from django.core.files.uploadedfile import SimpleUploadedFile
    >>>
    >>> t = ExtFileField(ext_whitelist=(".pdf", ".txt"))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.pdf', 'Some File Content'))
    >>> t.clean(SimpleUploadedFile('filename.txt', 'Some File Content'))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.exe', 'Some File Content'))
    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """
    def __init__(self, *args, **kwargs):
        extensions = kwargs.pop("extensions")
        self.extensions = [i.lower() for i in extensions]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        filename = data.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in self.extensions:
            raise forms.ValidationError('Not allowed file type: %s' % ext)


class JARSImportForm(forms.Form):

    #file_name = ExtFileField(extensions=['.racp', '.json', '.dat'])
    file_name = ExtFileField(extensions=['.json'])

import os

from django import forms
from apps.main.models import Device, Experiment
from .models import JARSConfiguration, JARSfilter
from .widgets import SpectralWidget
from apps.main.forms import add_empty_choice

def create_choices_from_model(model, filter_id=None):

    #instance = globals()[model]
    choices = model.objects.all().values_list('pk', 'name')
    choices = add_empty_choice(choices)
    return choices

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
            if 'filter_id' not in kwargs['initial']:
                self.fields.pop('name')
            else:
                self.fields['name'] = forms.ChoiceField(choices=create_choices_from_model(JARSfilter))
                filter_id = kwargs['initial']['filter_id']

                if filter_id == 0:
                    for value in self.fields:
                        if value != 'name':
                            self.fields.pop(value)
                    self.fields['name'].label = "Filter Template Name"
                else:
                    self.fields['name'] = forms.ChoiceField(choices=create_choices_from_model(JARSfilter, kwargs['initial']['filter_id']))
                    jars_filter = JARSfilter.objects.get(pk=kwargs['initial']['filter_id'])  
                    labels = [f.name for f in jars_filter._meta.get_fields()]
                    
                    for label in ['id']:
                        labels.remove(label)
                    for label in labels:
                        self.fields['name'].initial = kwargs['initial']['filter_id']
                        self.fields[label].initial = getattr(jars_filter,label)
                    self.fields['name'].label = "Filter Template Name"

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

    file_name = ExtFileField(extensions=['.racp','.json'])

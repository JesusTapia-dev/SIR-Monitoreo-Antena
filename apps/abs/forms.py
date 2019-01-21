from django import forms
from .models import ABSConfiguration, ABSBeam
from .widgets import UpDataWidget, DownDataWidget, EditUpDataWidget, EditDownDataWidget
from apps.main.models import Configuration
import os

class ABSConfigurationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ABSConfigurationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ABSConfiguration
        exclude = ('type', 'status', 'parameters', 'active_beam', 
            'module_status', 'module_messages', 'module_mode',
            'author', 'hash')


class ABSBeamAddForm(forms.Form):

    up_data = forms.CharField(widget=UpDataWidget, label='')
    down_data = forms.CharField(widget=DownDataWidget, label='')

    def __init__(self, *args, **kwargs):
        super(ABSBeamAddForm, self).__init__(*args, **kwargs)



class ABSBeamEditForm(forms.Form):

    up_data = forms.CharField(widget=EditUpDataWidget, label='')
    down_data = forms.CharField(widget=EditDownDataWidget, label='')

    def __init__(self, *args, **kwargs):
        super(ABSBeamEditForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            if 'beam' in self.initial:
                self.fields['up_data'].initial  = self.initial['beam']
                self.fields['down_data'].initial  = self.initial['beam']


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


class ABSImportForm(forms.Form):

    file_name = ExtFileField(extensions=['.json'])

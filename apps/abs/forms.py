from django import forms
from .models import ABSConfiguration, ABSBeam
from .widgets import UpDataWidget, DownDataWidget, EditUpDataWidget, EditDownDataWidget
from apps.main.models import Configuration

class ABSConfigurationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ABSConfigurationForm, self).__init__(*args, **kwargs)
        #instance = getattr(self, 'instance', None)

        #if instance and instance.pk:
        #    devices = Device.objects.filter(device_type__name='abs')

        #if instance.experiment:
        #        experiments = Experiment.objects.filter(pk=instance.experiment.id)
        #        self.fields['experiment'].widget.choices = [(experiment.id, experiment) for experiment in experiments]

    class Meta:
        model = ABSConfiguration
        exclude = ('type', 'status', 'parameters', 'active_beam', 'module_status')

class ABSBeamAddForm(forms.Form):

    #abs_conf = forms.CharField(widget=forms.HiddenInput)
    #name = forms.CharField(max_length=60)
    up_data = forms.CharField(widget=UpDataWidget, label='')
    down_data = forms.CharField(widget=DownDataWidget, label='')

    def __init__(self, *args, **kwargs):
        super(ABSBeamAddForm, self).__init__(*args, **kwargs)
        #if 'abs_conf' in self.initial:
        #    self.fields['abs_conf'].initial = self.initial['abs_conf']
            #self.fields['name'].initial = 'Beam'
        #    self.fields['up_data'].initial  = self.initial['abs_conf']
        #    self.fields['down_data'].initial  = self.initial['abs_conf']
        #self.fields['abs_conf'].initial = self.initial['abs_conf']
        #self.fields['name'].initial = 'Beam'
        #self.fields['up_data'].initial  = self.initial['abs_conf']
        #self.fields['down_data'].initial  = self.initial['abs_conf']



class ABSBeamEditForm(forms.Form):

    #abs_conf = forms.CharField(widget=forms.HiddenInput)
    up_data = forms.CharField(widget=EditUpDataWidget, label='')
    down_data = forms.CharField(widget=EditDownDataWidget, label='')

    def __init__(self, *args, **kwargs):
        super(ABSBeamEditForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            if 'beam' in self.initial:
                #self.fields['abs_conf'].initial = self.initial['beam'].abs_conf
                self.fields['up_data'].initial  = self.initial['beam']
                self.fields['down_data'].initial  = self.initial['beam']

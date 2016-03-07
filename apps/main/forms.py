from django import forms
from django.utils.safestring import mark_safe
        
from .models import DeviceType, Device, Experiment, Campaign, Configuration, Location

def add_empty_choice(choices, pos=0, label='-----'):
    if len(choices)>0:
        choices = list(choices)
        choices.insert(0, (0, label))
        return choices
    else:
        return [(0, label)]

class DatepickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        input_html = super(DatepickerWidget, self).render(name, value, attrs)
        html = '<div class="input-group date">'+input_html+'<span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span></div>'
        return mark_safe(html)

class TimepickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        input_html = super(TimepickerWidget, self).render(name, value, attrs)
        html = '<div class="input-group time">'+input_html+'<span class="input-group-addon"><i class="glyphicon glyphicon-time"></i></span></div>'
        return mark_safe(html)

class CampaignForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = DatepickerWidget(self.fields['start_date'].widget.attrs)
        self.fields['end_date'].widget = DatepickerWidget(self.fields['end_date'].widget.attrs)
    
    class Meta:
        model = Campaign
        exclude = ['']
         
class ExperimentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = TimepickerWidget(self.fields['start_time'].widget.attrs)
        self.fields['end_time'].widget = TimepickerWidget(self.fields['end_time'].widget.attrs)
    
        self.fields['campaign'].widget.attrs['readonly'] = True
        
    class Meta:
        model = Experiment
        exclude = ['']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ['']
        
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ['status']

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['type', 'created_date', 'programmed_date', 'parameters']
        
class DeviceTypeForm(forms.Form):
    device_type = forms.ChoiceField(choices=add_empty_choice(DeviceType.objects.all().order_by('name').values_list('id', 'name')))

from django import forms
from django.utils.safestring import mark_safe
        
from .models import DeviceType, Device, Experiment

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

class NewExperimentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewExperimentForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = DatepickerWidget(self.fields['start_date'].widget.attrs)
        self.fields['end_date'].widget = DatepickerWidget(self.fields['end_date'].widget.attrs)
    
    class Meta:
        model = Experiment
        fields = ['name', 'alias', 'start_date', 'end_date']

class NewDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ['status']

class DeviceTypeForm(forms.Form):
    device_type = forms.ChoiceField(choices=add_empty_choice(DeviceType.objects.all().order_by('name').values_list('id', 'name')))
    

import json

from django import forms
from .models import RCConfiguration, RCLine, RCLineType

class RCConfigurationForm(forms.ModelForm):
    
    class Meta:
        model = RCConfiguration
        exclude = ('clock', 'ipp', 'ntx', 'clock_divider')

        
class RCLineForm(forms.ModelForm):
    
    class Meta:
        model = RCLine
        fields = ('rc_configuration', 'line_type', 'channel')
        widgets = {
            'channel': forms.HiddenInput(),
        }
        
    def save(self):        
        line = super(RCLineForm, self).save()
        #auto add channel
        line.channel = RCLine.objects.filter(rc_configuration=line.rc_configuration).count()-1
        #auto add position for TX, TR & CODE
        if line.line_type.name in ('tx', 'tr', 'code'):
            line.position = RCLine.objects.filter(rc_configuration=line.rc_configuration, line_type=line.line_type).count()-1
        #add default params
        params = {}
        for field in json.loads(line.line_type.params):
            params[field['name']] = field['value']
        line.params = json.dumps(params)
        line.save()
        return
    
class RCLineViewForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields')
        super(RCLineViewForm, self).__init__(*args, **kwargs)
        for label, value in extra_fields.items():
            self.fields[label] = forms.CharField(initial=value)
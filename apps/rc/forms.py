import json

from django import forms
from .models import RCConfiguration, RCLine, RCLineType, RCLineCode

def create_choices_from_model(model, conf_id):
    
    if model=='RCLine':
        instance = RCConfiguration.objects.get(pk=conf_id)
        return instance.get_refs_lines()
    else:
        instance = globals()[model]
        return instance.objects.all().values_list('pk', 'name')

class RCConfigurationForm(forms.ModelForm):
    
    class Meta:
        model = RCConfiguration
        exclude = ('clock', 'ipp', 'ntx', 'clock_divider')

        
class RCLineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.extra_fields = kwargs.pop('extra_fields', [])
        super(RCLineForm, self).__init__(*args, **kwargs)
        if 'initial'in kwargs:
            for item in self.extra_fields:
                if 'model' in item:
                    self.fields[item['name']] = forms.ChoiceField(choices=create_choices_from_model(item['model'], 
                                                                                                    kwargs['initial']['rc_configuration']))
                else:
                    self.fields[item['name']] = forms.CharField(initial=item['value'])
    
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
        if line.line_type.name in ('tx', 'tr', 'codes', 'windows'):
            line.position = RCLine.objects.filter(rc_configuration=line.rc_configuration, line_type=line.line_type).count()-1
        
        #save extra fields in params
        params = {}
        for item in self.extra_fields:
            params[item['name']] = self.data[item['name']]
        line.params = json.dumps(params)
        line.save()
        return
    
class RCLineViewForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields')
        super(RCLineViewForm, self).__init__(*args, **kwargs)
        for label, value in extra_fields.items():
            if 'ref' in label:
                value = RCLine.objects.get(pk=value).get_name()
            elif 'code' in label:
                value = RCLineCode.objects.get(pk=value).name
            self.fields[label] = forms.CharField(initial=value)
            
class RCLineEditForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.extra_fields = kwargs.pop('extra_fields', [])
        super(RCLineEditForm, self).__init__(*args, **kwargs)
        if 'initial'in kwargs:
            for item in self.extra_fields:
                if 'model' in item:
                    self.fields[item['name']] = forms.ChoiceField(choices=create_choices_from_model(item['model'], 
                                                                                                    kwargs['initial']['rc_configuration']),
                                                                  initial=item['value'],
                                                                  widget=forms.Select(attrs={'name':'%s|%s' % (kwargs['initial']['line'], item['name'])}))
                else:
                    self.fields[item['name']] = forms.CharField(initial=item['value'],
                                                                widget=forms.TextInput(attrs={'name':'%s|%s' % (kwargs['initial']['line'], item['name'])}))
    
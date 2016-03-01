import os
import json

from django import forms
from django.utils.safestring import mark_safe
from apps.main.models import Device
from apps.main.forms import add_empty_choice
from .models import RCConfiguration, RCLine, RCLineType, RCLineCode

def create_choices_from_model(model, conf_id):
    
    if model=='RCLine':
        instance = RCConfiguration.objects.get(pk=conf_id)
        choices =  instance.get_refs_lines()
    else:
        instance = globals()[model]
        choices = instance.objects.all().values_list('pk', 'name')
        
    return add_empty_choice(choices, label='All')


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
            raise forms.ValidationError('Not allowed filetype: %s' % ext)
        

class KmUnitWidget(forms.widgets.TextInput):
    
    def render(self, name, value, attrs=None):
        
        if isinstance(value, (int, float)):
            unit = int(value*attrs['line'].km2unit)
        elif isinstance(value, basestring):
            units = []
            values = [s for s in value.split(',') if s]
            for val in values:
                units.append('{0:.0f}'.format(float(val)*attrs['line'].km2unit))
        
            unit = ','.join(units)
        
        html = '<div class="col-md-4"><input disabled type="text" class="form-control" id="id_{0}" value="{1}"></div><div class="col-md-1">Km</div><div class="col-md-4"><input disabled type="text" class="form-control" value="{2}"></div><div class="col-md-1">Units</div>'.format(name, value, unit)
        
        return mark_safe(html)

class DefaultWidget(forms.widgets.TextInput):
    
    def render(self, name, value, attrs=None):
        
        html = '<div class="col-md-4"><input disabled type="text" class="form-control" id="id_{0}" value="{1}"></div>'.format(name, value)
        
        return mark_safe(html)

class RCConfigurationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(RCConfigurationForm, self).__init__(*args, **kwargs)
        
        instance = getattr(self, 'instance', None)
        
        if instance and instance.pk:
            
            devices = Device.objects.filter(device_type__name='rc')
            
            self.fields['experiment'].widget.attrs['readonly'] = True
            self.fields['experiment'].widget.choices = [(instance.experiment.id, instance.experiment)]
            
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
    
    class Meta:
        model = RCConfiguration
        exclude = ('type', 'parameters', 'status')

    
        
class RCLineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.extra_fields = kwargs.pop('extra_fields', [])
        super(RCLineForm, self).__init__(*args, **kwargs)
        if 'initial'in kwargs:
            for item in self.extra_fields:
                if item['name']=='params':
                    continue
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
        if line.line_type.name in ('tx', ):
            line.position = RCLine.objects.filter(rc_configuration=line.rc_configuration, line_type=line.line_type).count()-1
        
        #save extra fields in params
        params = {}
        for item in self.extra_fields:
            if item['name']=='params':
                params['params'] = []
            else:
                params[item['name']] = self.data[item['name']]
        line.params = json.dumps(params)
        line.save()
        return
    
    
class RCLineViewForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields')
        line = kwargs.pop('line')
        subform = kwargs.pop('subform', False)
        super(RCLineViewForm, self).__init__(*args, **kwargs)
        print line
        for label, value in extra_fields.items():
            if label=='params':
                continue
            if 'ref' in label:
                if value in (0, '0'):
                    value = 'All'
                else:
                    value = RCLine.objects.get(pk=value).get_name()
            elif 'code' in label:
                value = RCLineCode.objects.get(pk=value).name
            
            self.fields[label] = forms.CharField(initial=value)
            
            if subform:
                params = json.loads(line.line_type.params)['params']
            else:
                params = json.loads(line.line_type.params)
            
            if 'widget' in params[label]:
                if params[label]['widget']=='km':
                    self.fields[label].widget = KmUnitWidget(attrs={'line':line})
            else:
                self.fields[label].widget = DefaultWidget()
            
class RCLineEditForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.extra_fields = kwargs.pop('extra_fields', [])
        super(RCLineEditForm, self).__init__(*args, **kwargs)
        if 'initial'in kwargs:
            for item, values in self.extra_fields.items():
                if item=='params':
                    continue
                if 'help' in values:
                    help_text = values['help']
                else:
                    help_text = ''
                
                if 'model' in values:                    
                    self.fields[item] = forms.ChoiceField(choices=create_choices_from_model(values['model'], kwargs['initial']['rc_configuration']),
                                                initial=values['value'],
                                                widget=forms.Select(attrs={'name':'%s|%s' % (kwargs['initial']['line'], item)}),
                                                help_text=help_text)
                    
                else:                    
                    self.fields[item] = forms.CharField(initial=values['value'],
                                                widget=forms.TextInput(attrs={'name':'%s|%s' % (kwargs['initial']['line'], item)}),
                                                help_text=help_text)
                    

    class Meta:
        model = RCLine
        exclude = ('rc_configuration', 'line_type', 'channel', 'position', 'params', 'pulses')
            
            
class RCSubLineEditForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields')
        count = kwargs.pop('count')
        line = kwargs.pop('line')
        super(RCSubLineEditForm, self).__init__(*args, **kwargs)
        for label, value in extra_fields.items():                           
            self.fields[label] = forms.CharField(initial=value,
                                                 widget=forms.TextInput(attrs={'name':'%s|%s|%s' % (count, line, label)}))


class RCImportForm(forms.Form):
    
    file_name = ExtFileField(extensions=['.racp', '.json', '.dat'])
    
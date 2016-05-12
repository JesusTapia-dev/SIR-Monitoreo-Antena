from django import forms
from django.utils.safestring import mark_safe
        
from .models import DeviceType, Device, Experiment, Campaign, Configuration, Location

FILE_FORMAT = (
                ('json', 'json'),
                )

DDS_FILE_FORMAT = (
                ('json', 'json'),
                ('text', 'dds')
                )

RC_FILE_FORMAT = (
                ('json', 'json'),
                ('text', 'racp'),
                ('binary', 'dat'),
                )

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

class DateRangepickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        start = attrs['start_date']
        end = attrs['end_date']      
        html = '''<div class="col-md-5 input-group date" style="float:inherit">
        <input class="form-control" id="id_start_date" name="start_date" placeholder="Start" title="" type="text" value="{}">
        <span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>
        </div>
        <div class="col-md-5 col-md-offset-2 input-group date" style="float:inherit">
        <input class="form-control" id="id_end_date" name="end_date" placeholder="End" title="" type="text" value="{}">
        <span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>
        </div>'''.format(start, end)
        return mark_safe(html)

class TimepickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        input_html = super(TimepickerWidget, self).render(name, value, attrs)
        html = '<div class="input-group time">'+input_html+'<span class="input-group-addon"><i class="glyphicon glyphicon-time"></i></span></div>'
        return mark_safe(html)

class CampaignForm(forms.ModelForm):
    
    experiments = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                 queryset=Experiment.objects.filter(template=True),
                                                 required=False)
    
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = DatepickerWidget(self.fields['start_date'].widget.attrs)
        self.fields['end_date'].widget = DatepickerWidget(self.fields['end_date'].widget.attrs)
        self.fields['description'].widget.attrs = {'rows': 2}
        
        if self.instance.pk:
            self.fields['experiments'].queryset |= self.instance.experiments.all()
    
    class Meta:
        model = Campaign
        exclude = ['']
    
         
class ExperimentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ExperimentForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = TimepickerWidget(self.fields['start_time'].widget.attrs)
        self.fields['end_time'].widget = TimepickerWidget(self.fields['end_time'].widget.attrs)
        
    class Meta:
        model = Experiment
        exclude = ['status']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ['']
        
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ['status']

class ConfigurationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ConfigurationForm, self).__init__(*args, **kwargs)
        
        if 'initial' in kwargs and 'experiment' in kwargs['initial'] and kwargs['initial']['experiment'] not in (0, '0'):
            self.fields['experiment'].widget.attrs['disabled'] = 'disabled'
    
    class Meta:
        model = Configuration
        exclude = ['type', 'created_date', 'programmed_date', 'parameters']
        
class DeviceTypeForm(forms.Form):
    device_type = forms.ChoiceField(choices=add_empty_choice(DeviceType.objects.all().order_by('name').values_list('id', 'name')))


class UploadFileForm(forms.Form):
    
    file = forms.FileField()

class DownloadFileForm(forms.Form):
    
    format = forms.ChoiceField(choices= ((0, 'json'),) )
    
    def __init__(self, device_type, *args, **kwargs):
        
        super(DownloadFileForm, self).__init__(*args, **kwargs)
        
        self.fields['format'].choices = FILE_FORMAT
        
        if device_type == 'dds':
            self.fields['format'].choices = DDS_FILE_FORMAT
        
        if device_type == 'rc':
            self.fields['format'].choices = RC_FILE_FORMAT
    
class OperationForm(forms.Form):
#     today = datetime.today()
    # -----Campaigns from this month------[:5]
    campaign = forms.ChoiceField(label="Campaign")
    
    def __init__(self, *args, **kwargs):
        
        if 'length' not in kwargs.keys():
            length = None
        else:
            length = kwargs['length']
        
            kwargs.pop('length')
        
        super(OperationForm, self).__init__(*args, **kwargs)
        self.fields['campaign'].choices=Campaign.objects.all().order_by('-start_date').values_list('id', 'name')[:length]
        

class OperationSearchForm(forms.Form):
    # -----ALL Campaigns------
    campaign = forms.ChoiceField(label="Campaign")
    
    def __init__(self, *args, **kwargs):
        super(OperationSearchForm, self).__init__(*args, **kwargs)
        self.fields['campaign'].choices=Campaign.objects.all().order_by('-start_date').values_list('id', 'name')
        

class NewForm(forms.Form):
    
    create_from = forms.ChoiceField(choices=((0, '-----'),
                                             (1, 'Empty (blank)'),
                                             (2, 'Template')))
    choose_template = forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        
        template_choices = kwargs.pop('template_choices', [])
        super(NewForm, self).__init__(*args, **kwargs)
        self.fields['choose_template'].choices = add_empty_choice(template_choices)
        

class FilterForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields', [])
        super(FilterForm, self).__init__(*args, **kwargs)
        
        for field in extra_fields:            
            if 'range_date' in field:
                self.fields[field] = forms.CharField(required=False)
                self.fields[field].widget = DateRangepickerWidget()
                if 'initial' in kwargs:
                    self.fields[field].widget.attrs = {'start_date':kwargs['initial'].get('start_date', ''),
                                                       'end_date':kwargs['initial'].get('end_date', '')}  
            elif 'template' in field:
                self.fields['template'] = forms.BooleanField(required=False)
            else:
                self.fields[field] = forms.CharField(required=False)
    
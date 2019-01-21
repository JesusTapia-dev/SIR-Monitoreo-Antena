import os
import json

from django import forms
from django.utils.safestring import mark_safe
from apps.main.models import Device
from apps.main.forms import add_empty_choice
from .models import RCConfiguration, RCLine, RCLineType, RCLineCode
from .widgets import KmUnitWidget, KmUnitHzWidget, KmUnitDcWidget, UnitKmWidget, DefaultWidget, CodesWidget, HiddenWidget, HCheckboxSelectMultiple

def create_choices_from_model(model, conf_id, all_choice=False):

    if model=='RCLine':
        instance = RCConfiguration.objects.get(pk=conf_id)
        choices =  [(line.pk, line.get_name()) for line in instance.get_lines(line_type__name='tx')]
        if all_choice:
            choices = add_empty_choice(choices, label='All')
    else:
        instance = globals()[model]
        choices = instance.objects.all().values_list('pk', 'name')

    return choices


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


class RCConfigurationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RCConfigurationForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)

        if instance and instance.pk:

            devices = Device.objects.filter(device_type__name='rc')
            if instance.experiment:
                self.fields['experiment'].widget.attrs['read_only'] = True
                #self.fields['experiment'].widget.choices = [(instance.experiment.id, instance.experiment)]
            self.fields['device'].widget.choices = [(device.id, device) for device in devices]
            self.fields['ipp'].widget = KmUnitHzWidget(attrs={'km2unit':instance.km2unit})
            self.fields['clock'].widget.attrs['readonly'] = True

        self.fields['time_before'].label = mark_safe(self.fields['time_before'].label)
        self.fields['time_after'].label = mark_safe(self.fields['time_after'].label)

        if 'initial' in kwargs and 'experiment' in kwargs['initial'] and kwargs['initial']['experiment'] not in (0, '0'):
            self.fields['experiment'].widget.attrs['readonly'] = True

    class Meta:
        model = RCConfiguration
        exclude = ('type', 'parameters', 'status', 'total_units', 'mix', 'author', 'hash')

    def clean(self):
        form_data = super(RCConfigurationForm, self).clean()

        if 'clock_divider' in form_data:
            if form_data['clock_divider']<1:
                self.add_error('clock_divider', 'Invalid Value')
            #else:
            #    if form_data['ipp']*(20./3*(form_data['clock_in']/form_data['clock_divider']))%10!=0:
            #        self.add_error('ipp', 'Invalid IPP units={}'.format(form_data['ipp']*(20./3*(form_data['clock_in']/form_data['clock_divider']))))

        return form_data

    def save(self, *args, **kwargs):
        conf = super(RCConfigurationForm, self).save(*args, **kwargs)
        conf.total_units = conf.ipp*conf.ntx*conf.km2unit
        conf.save()
        return conf


class RCMixConfigurationForm(forms.Form):

    clock_in = forms.CharField(widget=forms.HiddenInput())
    clock_divider = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField()
    experiment = forms.ChoiceField()
    mode = forms.ChoiceField(widget=forms.RadioSelect(),
                             choices=[(0, 'Parallel'), (1, 'Sequence')],
                             initial=0)
    operation = forms.ChoiceField(widget=forms.RadioSelect(),
                                  choices=[(0, 'OR'), (1, 'XOR'), (2, 'AND'), (3, 'NAND')],
                                  initial=1)
    delay = forms.CharField()
    mask = forms.MultipleChoiceField(
        choices=[(0, 'L1'),(1, 'L2'),(2, 'L3'),(3, 'L4'),(4, 'L5'),(5, 'L6'),(6, 'L7'),(7, 'L8'),
        (8, 'L9'),(9, 'L10'),(10, 'L11'),(11, 'L12'),(12, 'L13'),(13, 'L14'),(14, 'L15'),(15, 'L16')],
        widget=HCheckboxSelectMultiple())
    result = forms.CharField(required=False,
                             widget=forms.Textarea(attrs={'readonly':True, 'rows':5, 'class':'tabuled'}))

    def __init__(self, *args, **kwargs):
        confs = kwargs.pop('confs', [])
        if confs:
            km2unit = confs[0].km2unit
            clock_in = confs[0].clock_in
            clock_divider = confs[0].clock_divider
        else:
            km2unit = clock_in = clock_divider = 0
        super(RCMixConfigurationForm, self).__init__(*args, **kwargs)
        self.fields['experiment'].choices = [(conf.pk, '{} | {}'.format(conf.pk, conf.name)) for conf in confs]
        self.fields['delay'].widget = KmUnitWidget(attrs = {'km2unit':km2unit})
        self.fields['clock_in'].initial = clock_in
        self.fields['clock_divider'].initial = clock_divider


class RCLineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.extra_fields = kwargs.pop('extra_fields', [])
        super(RCLineForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs and 'line_type' in kwargs['initial']:
            line_type = RCLineType.objects.get(pk=kwargs['initial']['line_type'])

            if 'code_id' in kwargs['initial']:
                model_initial = kwargs['initial']['code_id']
            else:
                model_initial = 0

            params = json.loads(line_type.params)

            for label, value in self.extra_fields.items():
                if label=='params':
                    continue

                if 'model' in params[label]:
                    self.fields[label] = forms.ChoiceField(choices=create_choices_from_model(params[label]['model'],
                                                                                             kwargs['initial']['rc_configuration']),
                                                           initial=model_initial)


                else:
                    if label=='codes' and 'code_id' in kwargs['initial']:
                        self.fields[label] = forms.CharField(initial=RCLineCode.objects.get(pk=kwargs['initial']['code_id']).codes)
                    else:
                        self.fields[label] = forms.CharField(initial=value['value'])

                    if label=='codes':
                        self.fields[label].widget = CodesWidget()

        if self.data:
            line_type = RCLineType.objects.get(pk=self.data['line_type'])

            if 'code_id' in self.data:
                model_initial = self.data['code_id']
            else:
                model_initial = 0

            params = json.loads(line_type.params)

            for label, value in self.extra_fields.items():
                if label=='params':
                    continue

                if 'model' in params[label]:
                    self.fields[label] = forms.ChoiceField(choices=create_choices_from_model(params[label]['model'],
                                                                                             self.data['rc_configuration']),
                                                           initial=model_initial)


                else:
                    if label=='codes' and 'code' in self.data:
                        self.fields[label] = forms.CharField(initial=self.data['codes'])
                    else:
                        self.fields[label] = forms.CharField(initial=self.data[label])

                    if label=='codes':
                        self.fields[label].widget = CodesWidget()


    class Meta:
        model = RCLine
        fields = ('rc_configuration', 'line_type', 'channel')
        widgets = {
            'channel': forms.HiddenInput(),
        }


    def clean(self):

        form_data = self.cleaned_data
        if 'code' in self.data and self.data['TX_ref']=="0":
            self.add_error('TX_ref', 'Choose a valid TX reference')

        if RCLineType.objects.get(pk=self.data['line_type']).name=='mix':
            self.add_error('line_type', 'Invalid Line type')

        return form_data


    def save(self):
        line = super(RCLineForm, self).save()

        #auto add channel
        line.channel = RCLine.objects.filter(rc_configuration=line.rc_configuration).count()-1

        #auto add position for TX, TR & CODE
        if line.line_type.name in ('tx', ):
            line.position = RCLine.objects.filter(rc_configuration=line.rc_configuration, line_type=line.line_type).count()-1

        #save extra fields in params
        params = {}
        for label, value in self.extra_fields.items():
            if label=='params':
                params['params'] = []
            elif label=='codes':
                params[label] = [s for s in self.data[label].split('\r\n') if s]
            else:
                params[label] = self.data[label]
        line.params = json.dumps(params)
        line.save()
        return


class RCLineViewForm(forms.Form):

    def __init__(self, *args, **kwargs):

        extra_fields = kwargs.pop('extra_fields')
        line = kwargs.pop('line')
        subform = kwargs.pop('subform', False)
        super(RCLineViewForm, self).__init__(*args, **kwargs)

        if subform:
            params = json.loads(line.line_type.params)['params']
        else:
            params = json.loads(line.line_type.params)

        for label, value in extra_fields.items():

            if label=='params':
                continue
            if 'ref' in label:
                if value in (0, '0'):
                    value = 'All'
                else:
                    value = RCLine.objects.get(pk=value).get_name()
            elif label=='code':
                value = RCLineCode.objects.get(pk=value).name

            self.fields[label] = forms.CharField(initial=value)

            if 'widget' in params[label]:
                km2unit = line.rc_configuration.km2unit
                if params[label]['widget']=='km':
                    self.fields[label].widget = KmUnitWidget(attrs={'line':line, 'km2unit':km2unit, 'disabled':True})
                elif params[label]['widget']=='unit':
                    self.fields[label].widget = UnitKmWidget(attrs={'line':line, 'km2unit':km2unit, 'disabled':True})
                elif params[label]['widget']=='dc':
                    self.fields[label].widget = KmUnitDcWidget(attrs={'line':line, 'km2unit':km2unit, 'disabled':True})
                elif params[label]['widget']=='codes':
                    self.fields[label].widget = CodesWidget(attrs={'line':line, 'km2unit':km2unit, 'disabled':True})
            else:
                self.fields[label].widget = DefaultWidget(attrs={'disabled':True})


class RCLineEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        extra_fields = kwargs.pop('extra_fields', [])
        conf = kwargs.pop('conf', False)
        line = kwargs.pop('line')
        subform = kwargs.pop('subform', False)

        super(RCLineEditForm, self).__init__(*args, **kwargs)

        if subform is not False:
            params = json.loads(line.line_type.params)['params']
            count = subform
        else:
            params = json.loads(line.line_type.params)
            count = -1

        for label, value in extra_fields.items():

            if label in ('params',):
                continue
            if 'help' in params[label]:
                help_text = params[label]['help']
            else:
                help_text = ''

            if 'model' in params[label]:
                if line.line_type.name=='tr':
                    all_choice = True
                else:
                    all_choice = False
                self.fields[label] = forms.ChoiceField(choices=create_choices_from_model(params[label]['model'], conf.id, all_choice=all_choice),
                                            initial=value,
                                            widget=forms.Select(attrs={'name':'%s|%s|%s' % (count, line.id, label)}),
                                            help_text=help_text)

            else:
                self.fields[label] = forms.CharField(initial=value, help_text=help_text)

                if label in ('code', ):
                    self.fields[label].widget = HiddenWidget(attrs={'name':'%s|%s|%s' % (count, line.id, label)})

                elif 'widget' in params[label]:
                    km2unit = line.rc_configuration.km2unit
                    if params[label]['widget']=='km':
                        self.fields[label].widget = KmUnitWidget(attrs={'line':line, 'km2unit':km2unit, 'name':'%s|%s|%s' % (count, line.id, label)})
                    elif params[label]['widget']=='unit':
                        self.fields[label].widget = UnitKmWidget(attrs={'line':line, 'km2unit':km2unit, 'name':'%s|%s|%s' % (count, line.id, label)})
                    elif params[label]['widget']=='dc':
                        self.fields[label].widget = KmUnitDcWidget(attrs={'line':line, 'km2unit':km2unit, 'name':'%s|%s|%s' % (count, line.id, label)})
                    elif params[label]['widget']=='codes':
                        self.fields[label].widget = CodesWidget(attrs={'line':line, 'km2unit':km2unit, 'name':'%s|%s|%s' % (count, line.id, label)})
                else:
                    self.fields[label].widget = DefaultWidget(attrs={'line':line, 'name':'%s|%s|%s' % (count, line.id, label)})


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


class RCLineCodesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RCLineCodesForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            self.fields['code'] = forms.ChoiceField(choices=RCLineCode.objects.all().values_list('pk', 'name'),
                                                    initial=kwargs['initial']['code'])
        if 'instance' in kwargs:
            self.fields['code'] = forms.ChoiceField(choices=RCLineCode.objects.all().values_list('pk', 'name'),
                                                    initial=kwargs['instance'].pk)

        self.fields['codes'].widget = CodesWidget()


    class Meta:
        model = RCLineCode
        exclude = ('name',)

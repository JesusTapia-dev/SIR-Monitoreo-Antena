from django import forms
from .models import Device, Experiment, ExperimentTemplate

def add_empty_choice(choices, pos=0, label='-----'):
    if len(choices)>0:
        choices = list(choices)
        choices.insert(0, (0, label))
        return choices
    else:
        return [(0, label)]

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['name', 'alias', 'start_date', 'end_date']


class TemplatesForm(forms.Form):    
    template = forms.ChoiceField(choices=add_empty_choice(ExperimentTemplate.objects.all().values_list('id', 'experiment_detail__experiment__name')),                                   
                                  required=False)
    
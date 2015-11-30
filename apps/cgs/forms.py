from django import forms
from .models import CGSConfiguration

class CGSConfigurationForm(forms.ModelForm):
    #freq0.widget = te 
    def __init__(self, *args, **kwargs):
        #request = kwargs.pop('request')
        super(CGSConfigurationForm, self).__init__(*args, **kwargs)

    def clean(self):
        # Custom validation to force an integer when type of unit = "Unit"
        form_data = self.cleaned_data
        if (form_data['freq0'] or form_data['freq1'] or form_data['freq2'] or form_data['freq3'] < 0):
            raise forms.ValidationError("Please introduce positive Number")

        return form_data

    class Meta:
        model = CGSConfiguration
        #exclude = ('freqs', 'clk_in', 'mult','div',)
        exclude = ('freqs',)

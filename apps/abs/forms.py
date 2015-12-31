from django import forms
from .models import ABSConfiguration

class ABSConfigurationForm(forms.ModelForm):
    
    class Meta:
        model = ABSConfiguration
        fields = ('experiment',)

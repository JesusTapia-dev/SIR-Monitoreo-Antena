from django import forms
from .models import USRPConfiguration

class USRPConfigurationForm(forms.ModelForm):
    
    class Meta:
        model = USRPConfiguration
        fields = ('device',)

from django import forms
from .models import RCConfiguration

class RCConfigurationForm(forms.ModelForm):
    
    class Meta:
        model = RCConfiguration
        fields = ('experiment',)

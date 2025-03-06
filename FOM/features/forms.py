# features/forms.py

from django import forms
from .models import CommonFeature

class FeatureForm(forms.ModelForm):
    class Meta:
        model = CommonFeature
        fields = ['name', 'default_value', 'value_type', 'description']

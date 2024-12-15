# forms.py
from django import forms
from .models import Robot

class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['serial', 'model', 'version', 'created']

    def clean_model(self):
        model = self.cleaned_data.get('model')
        if not model.isalnum():
            raise forms.ValidationError("Model must be alphanumeric.")
        return model

    def clean_version(self):
        version = self.cleaned_data.get('version')
        if not version.isupper():
            raise forms.ValidationError("Version must be uppercase.")
        return version

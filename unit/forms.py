from django import forms
from .models import Unit

class UnitModelForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'code',
            'name',
        ]
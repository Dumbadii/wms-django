from django import forms
from .models import Unit, Department

class UnitModelForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'code',
            'name',
        ]

class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'code',
            'name',
        ]

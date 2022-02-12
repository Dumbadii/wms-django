from django import forms
from .models import Unit, Department, ItemType

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

class ItemTypeCreateModelForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = [
            # 'code',
            'name',
            'parent',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.fields['parent'].queryset.filter(parent=None)

class ItemTypeUpdateModelForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = [
            # 'code',
            'name',
        ]

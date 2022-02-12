from django import forms
from .models import Unit, Department, ItemType, ItemInfo

class UnitModelForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'code',
            'name',
            'unique_barcode'
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

class ItemInfoCreateModelForm(forms.ModelForm):
    class Meta:
        model = ItemInfo
        fields = [
            # 'code',
            'name',
            'specification',
            'type1',
            'type2',
            'brand',
            'unit',
            'price'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type1'].queryset = self.fields['type1'].queryset.filter(parent=None)
        self.fields['type2'].queryset = self.fields['type2'].queryset.none()

        if 'type1' in self.data:
            try:
                type1Id = int(self.data.get('type1'))
                self.fields['type2'].queryset = ItemType.objects.filter(parent=type1Id).order_by('code')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['type2'].queryset = self.instance.type1.type2_set.order_by('code')


class ItemInfoUpdateModelForm(forms.ModelForm):
    class Meta:
        model = ItemInfo
        fields = [
            # 'code',
            'name',
            'specification',
            'brand',
            'price'
        ]

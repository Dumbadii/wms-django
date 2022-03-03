from typing_extensions import Required
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, ValidationError, TextInput
from .models import StockinBasic, StockinDetail, StockoutBasic, StockoutDetail

class StockinDetailForm(ModelForm):
    class Meta:
        model = StockinDetail
        fields = [
            'item',
            'amount',
            'price'
        ]
# 
    def clean_amount(self):
        item = self.cleaned_data['item']
        data = self.cleaned_data['amount']
        if not item.unit.unique_barcode and data<1:
            raise ValidationError('单位"%s"数量需为整数' %(item.unit.name))
        return data

StockinDetailFormset = inlineformset_factory(
    StockinBasic,
    StockinDetail,
    form = StockinDetailForm
    )

class StockoutDetailForm(ModelForm):
    class Meta:
        model = StockoutDetail
        fields = (
            'barcode',
            'amount'
        )
        widgets = {
            'barcode': TextInput(),
        }

    def clean_amount(self):
        item = self.cleaned_data['item']
        data = self.cleaned_data['amount']
        if not item.unit.unique_barcode and data<1:
            raise ValidationError('单位"%s"数量需为整数' %(item.unit.name))
        return data


StockoutDetailFormset = inlineformset_factory(
    StockoutBasic,
    StockoutDetail,
    form = StockoutDetailForm
    )
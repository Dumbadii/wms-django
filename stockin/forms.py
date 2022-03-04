from django.db.models import F
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, ValidationError
from .models import StockinBasic, StockinDetail, StockoutBasic, StockoutDetail, StockbackBasic, StockbackDetail, Barcode

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

    def __init__(self, *args, **kwargs): 
        super(StockoutDetailForm, self).__init__(*args, **kwargs)
        # self.fields['barcode'].queryset = Barcode.objects.filter(amount_left__gt=0)

        
    def clean_amount(self):
        barcode = self.cleaned_data['barcode']
        data = self.cleaned_data['amount']
        if not self.instance.id:
            if not barcode.item.unit.unique_barcode and int(data)!=1:
                raise ValidationError('单位"%s"数量需为整数' %(barcode.item.unit.name))
            if data > barcode.amount_left:
                raise ValidationError('出库数量大于库存数')
        return data



StockoutDetailFormset = inlineformset_factory(
    StockoutBasic,
    StockoutDetail,
    form = StockoutDetailForm
    )

# stockback
class StockbackDetailForm(ModelForm):
    class Meta:
        model = StockbackDetail
        fields = (
            'barcode',
            'amount'
        )

    def __init__(self, *args, **kwargs): 
        super(StockbackDetailForm, self).__init__(*args, **kwargs)
        # self.fields['barcode'].queryset = Barcode.objects.filter(amount_left__lt=F('amount_init'))

        
    def clean_amount(self):
        barcode = self.cleaned_data['barcode']
        data = self.cleaned_data['amount']
        if not self.instance.id:
            if not barcode.item.unit.unique_barcode and int(data)!=1:
                raise ValidationError('单位"%s"数量需为整数' %(barcode.item.unit.name))
            if data > (barcode.amount_init-barcode.amount_left):
                raise ValidationError('回库数量大于出库数')
        return data



StockbackDetailFormset = inlineformset_factory(
    StockbackBasic,
    StockbackDetail,
    form = StockbackDetailForm
    )
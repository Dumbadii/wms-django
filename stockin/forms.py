from django.forms.models import inlineformset_factory
from django.forms import ModelForm, NumberInput, ValidationError
from .models import StockinBasic, StockinDetail, StockoutBasic, StockoutDetail, StockbackBasic, StockbackDetail, Barcode
from django.forms.widgets import Select

class StockinDetailForm(ModelForm):
    class Meta:
        model = StockinDetail
        fields = [
            'item',
            'amount',
            'price'
        ]
        widgets = {
            'amount': NumberInput(),
            'item': Select()
        }
# 
    def __init__(self, *args, **kwargs): 
        super(StockinDetailForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            barcodes = self.instance.barcodes.all()
            used_barcodes = list(filter(lambda x: (x.stockout_details.count()>0), barcodes))
            used_count = len(used_barcodes)
            self.fields['amount'].widget.attrs = {'min': used_count}

    def clean(self):
        cleaned_data=super().clean()
        print(cleaned_data)
        item = cleaned_data.get('item')
        amount = cleaned_data.get('amount')
        price = cleaned_data.get('price')
        pk = cleaned_data.get('id') 

        if item and amount and price:
            if not item.unit.unique_barcode and amount<1:
                raise ValidationError('单位"%s"数量需为整数' %(item.unit.name))
        else:
            raise ValidationError('all fields required')

        if pk:
            barcodes = self.instance.barcodes.all()
            out_count = len(list(filter(lambda x: (x.amount_init>x.amount_left), barcodes)))
            if out_count and item != self.instance.item:
                raise ValidationError('部分物品已出库，不允许修改')

        return cleaned_data

# StockinDetailFormset = inlineformset_factory(
    # StockinBasic,
    # StockinDetail,
    # form = StockinDetailForm
    # )

class StockinDetailFormset(
    inlineformset_factory(StockinBasic, StockinDetail, form=StockinDetailForm, extra=3)):
    def clean(self):
        super(StockinDetailFormset, self).clean()

        for form in self.forms:
            # if not form.is_valid():
                # continue
            pk = form.cleaned_data.get('id')
            dele = form.cleaned_data.get('DELETE')
            if pk and dele:
                barcodes = form.instance.barcodes.all()
                used_barcodes = list(filter(lambda x: (x.stockout_details.count()>0), barcodes))
                used_count = len(used_barcodes)
                if used_count>0:
                    raise ValidationError('入库单物品已使用，不能删除')

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
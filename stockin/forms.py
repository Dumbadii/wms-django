from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, ValidationError
from .models import StockinBasic, StockinDetail, StockoutBasic, StockoutDetail, StockbackBasic, StockbackDetail, Barcode,ItemInfo

class StockinDetailForm(ModelForm):
    class Meta:
        model = StockinDetail
        fields = [
            'item',
            'barcode_count',
            'amount',
            'price'
        ]

    def __init__(self, *args, **kwargs): 
        super(StockinDetailForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            used_count = self.instance.barcodes.filter(~Q(status=0)).count()
            in_count = self.instance.barcodes.filter(Q(status=0)|Q(status=2)).count()
            self.fields['barcode_count'].widget.attrs = {'min': used_count, 'max': self.instance.barcode_count}
            if self.instance.barcode_count > in_count:
                self.fields['item'].empty_label = None
                self.fields['item'].queryset = ItemInfo.objects.filter(id=self.instance.item.id)

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
                used_count = barcodes.filter(~Q(status=0)).count()
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

        
    # def clean_amount(self):
        # barcode = self.cleaned_data['barcode']
        # data = self.cleaned_data['amount']
        # if not self.instance.id:
            # if not barcode.item.unit.unique_barcode and int(data)!=1:
                # raise ValidationError('单位"%s"数量需为整数' %(barcode.item.unit.name))
            # if data > barcode.amount_left:
                # raise ValidationError('出库数量大于库存数')
        # return data



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
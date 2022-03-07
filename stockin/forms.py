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

# StockinDetailFormset = inlineformset_factory(
    # StockinBasic,
    # StockinDetail,
    # form = StockinDetailForm
    # )

class StockinDetailFormset(
    inlineformset_factory(StockinBasic, StockinDetail, form=StockinDetailForm, extra=3)):
    def clean(self):
        super(StockinDetailFormset, self).clean()

        items = []
        for form in self.forms:
            item = form.cleaned_data.get('item')

            if item in items:
                raise ValidationError('%s already used.' %(item))
            elif item != None:
                items.append(item)

class StockoutDetailForm(ModelForm):
    class Meta:
        model = StockoutDetail
        fields = (
            'barcode',
        )

    def __init__(self, *args, **kwargs):
        super(StockoutDetailForm, self).__init__(*args, **kwargs)
        self.fields['barcode'].queryset = Barcode.objects.filter(Q(status=0) | Q(status=2))
class StockoutDetailFormset(
    inlineformset_factory(StockoutBasic, StockoutDetail, form=StockoutDetailForm, extra=3)):
    def clean(self):
        super(StockoutDetailFormset, self).clean()

        barcodes = []
        for form in self.forms:
            barcode = form.cleaned_data.get('barcode')

            if barcode in barcodes:
                raise ValidationError('%s already used.' %(barcode))
            elif barcode != None:
                barcodes.append(barcode)

# stockback
class StockbackDetailForm(ModelForm):
    class Meta:
        model = StockbackDetail
        fields = (
            'barcode',
        )

StockbackDetailFormset = inlineformset_factory(
    StockbackBasic,
    StockbackDetail,
    form = StockbackDetailForm
    )

class StockinConfirmForm(ModelForm):
    class Meta:
        model = StockinBasic
        fields = ()

class StockoutConfirmForm(ModelForm):
    class Meta:
        model = StockoutBasic
        fields = ()

class StockbackConfirmForm(ModelForm):
    class Meta:
        model = StockbackBasic
        fields = ()
    
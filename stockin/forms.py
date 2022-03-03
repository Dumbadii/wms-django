from django.forms.models import inlineformset_factory, ModelForm
from .models import StockinBasic, StockinDetail 
# from params.models import ItemInfo

class StockinModelForm(ModelForm):
    class Meta:
        model = StockinDetail
        fields = [
            'item',
            'barcode_count',
            'amount',
            'price'
        ]

    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # self.fields['item'].queryset = self.fields['item'].queryset.none()
# 
        # if 'type1' in self.data:
            # try:
                # type1Id = int(self.data.get('type1'))
                # self.fields['type2'].queryset = ItemType.objects.filter(parent=type1Id).order_by('code')
            # except(ValueError, TypeError):
                # pass
        # elif self.instance.pk:
            # self.fields['type2'].queryset = self.instance.type1.type2_set.order_by('code')



StockinDetailFormset = inlineformset_factory(
    StockinBasic,
    StockinDetail,
    fields=(
        'item',
        'barcode_count',
        'amount',
        'price'
        )
    )

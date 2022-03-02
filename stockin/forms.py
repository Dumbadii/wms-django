from django.forms.models import inlineformset_factory
from .models import StockinBasic, StockinDetail 
# from params.models import ItemInfo

StockinDetailFormset = inlineformset_factory(
    StockinBasic,
    StockinDetail,
    fields=(
        # # 'item.type1',
        # # 'item.type2',
        'item',
        'barcode_count',
        'amount',
        'price'
        )
    )
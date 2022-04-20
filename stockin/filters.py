import django_filters
from .models import StockinBasic, StockoutBasic, StockbackBasic

class StockinFilterSet(django_filters.FilterSet):
    class Meta:
        model = StockinBasic
        fields = [
            'create_date',
            'code'
        ]

class StockoutFilterSet(django_filters.FilterSet):
    class Meta:
        model = StockoutBasic
        fields = [
            'create_date'
        ]

class StockbackFilterSet(django_filters.FilterSet):
    class Meta:
        model = StockbackBasic
        fields = [
            'create_date'
        ]
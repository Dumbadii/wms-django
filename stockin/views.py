from django.shortcuts import render
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from .models import StockinBasic, StockinDetail

# Create your views here.
class StockinDetailInline(InlineFormSetFactory):
    model = StockinDetail
    fields = ['item', 'barcode_count', 'amount', 'price']

class StockinCreateView(CreateWithInlinesView):
    model = StockinBasic
    inlines = [StockinDetailInline]
    fields = ['code', 'operator', 'memo']
    template_name = 'stockin_.html'

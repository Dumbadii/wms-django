from django.contrib import admin
from .models import (
  StockinBasic, 
  StockinDetail, 
  Barcode, 
  StockoutBasic, 
  StockoutDetail, 
  StockbackBasic, 
  StockbackDetail,
)

# Register your models here.
admin.site.register(StockinBasic)
admin.site.register(StockinDetail)
admin.site.register(Barcode)
admin.site.register(StockoutBasic)
admin.site.register(StockoutDetail)
admin.site.register(StockbackBasic)
admin.site.register(StockbackDetail)

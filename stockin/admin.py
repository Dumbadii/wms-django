from django.contrib import admin
from .models import StockinBasic, StockinDetail, Barcode

# Register your models here.
admin.site.register(StockinBasic)
admin.site.register(StockinDetail)
admin.site.register(Barcode)

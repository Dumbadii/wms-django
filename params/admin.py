from django.contrib import admin
from .models import (
  BarcodeStatus,
  Unit,
  Department,
  ItemType,
  ItemInfo,
)

# Register your models here.
admin.site.register(Unit)
admin.site.register(BarcodeStatus)
admin.site.register(Department)
admin.site.register(ItemType)
admin.site.register(ItemInfo)
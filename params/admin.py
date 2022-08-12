from django.contrib import admin
from .models import (
  BarcodeStatus,
  Unit,
  Department,
  ItemTypeParent,
  ItemTypeChild,
  ItemInfo,
)

# Register your models here.
admin.site.register(Unit)
admin.site.register(BarcodeStatus)
admin.site.register(Department)
admin.site.register(ItemTypeParent)
admin.site.register(ItemTypeChild)
admin.site.register(ItemInfo)

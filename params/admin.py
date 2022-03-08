from django.contrib import admin
from .models import ItemType, ItemInfo

# Register your models here.
admin.site.register(ItemType)
admin.site.register(ItemInfo)
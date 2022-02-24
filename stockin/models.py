from django.db import models
from django.urls import reverse
from django.conf import settings
from params.models import ItemInfo

class StockinBasic(models.Model):
    code = models.CharField(unique=True, max_length=12)
    create_date = models.TimeField(auto_now_add=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    memo = models.TextField(max_length=200)

    def get_absolute_url(self):
        return reverse("sotckin:stockin-basic-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("sotckin:stockin-basic-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("sotckin:stockin-basic-delete", kwargs={"pk": self.id})

    def __str__(self):
        return self.code

class StockinDetail(models.Model):
    basic = models.ForeignKey(StockinBasic, on_delete=models.PROTECT)
    item = models.ForeignKey(ItemInfo, on_delete=models.PROTECT)
    barcode_count = models.IntegerField()
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
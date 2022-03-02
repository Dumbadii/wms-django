from logging import PlaceHolder
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
        return reverse("stockin:stockin-info", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("stockin:stockin-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("stockin:stockin-delete", kwargs={"pk": self.id})

    def __str__(self):
        return self.code

class StockinDetail(models.Model):
    basic = models.ForeignKey(StockinBasic, related_name='details', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemInfo, related_name='stockin_details', on_delete=models.PROTECT)
    barcode_count = models.IntegerField()
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def list_barcodes(self):
        if self.barcode_count > 1:
            return '%s-%s' %(self.barcodes.all()[0].code, self.barcodes.all()[self.barcode_count-1].code)
        return self.barcodes.all()[0].code

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(StockinDetail, self).save(*args, **kwargs)
            pk = StockinDetail.objects.filter(basic=self.basic).aggregate(models.Max('id'))['id__max']

            max_code = Barcode.objects.filter(item=self.item).aggregate(models.Max('code'))['code__max']
            code_index = 0 if not max_code else int(max_code[-4:])
            for i in range(self.barcode_count):
                bc = Barcode(code = self.item.code + ('0000' + str(code_index+i+1))[-4:])
                bc.stockin_detail = StockinDetail.objects.get(pk=pk)
                bc.item = self.item
                bc.amount_init = 1 if not self.item.unit.unique_barcode else self.amount
                bc.amount_left = bc.amount_init
                bc.save()
        else:
            super(StockinDetail, self).save(*args, **kwargs)
 
class Barcode(models.Model):
    stockin_detail = models.ForeignKey(StockinDetail, related_name='barcodes', on_delete=models.PROTECT)
    item = models.ForeignKey(ItemInfo, related_name='barcodes', on_delete=models.PROTECT)
    code = models.CharField(unique=True, max_length=11)
    amount_init = models.DecimalField(max_digits=5, decimal_places=2)
    amount_left = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.code


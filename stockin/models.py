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
        return reverse("stock:stockin-info", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("stock:stockin-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("stock:stockin-delete", kwargs={"pk": self.id})

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
            self.barcode_count = 1 if self.item.unit.unique_barcode else int(self.amount)
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
        return '%s-%s-%s' %(self.code, self.item.name, self.amount_left)


class StockoutBasic(models.Model):
    code = models.CharField(unique=True, max_length=12)
    create_date = models.TimeField(auto_now_add=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stockouts_operator", on_delete=models.PROTECT)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stockouts_client", on_delete=models.PROTECT)
    memo = models.TextField(max_length=200)

    def get_absolute_url(self):
        return reverse("stock:stockout-info", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("stock:stockout-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("stock:stockout-delete", kwargs={"pk": self.id})

    def __str__(self):
        return self.code

class StockoutDetail(models.Model):
    basic = models.ForeignKey(StockoutBasic, related_name='details', on_delete=models.CASCADE)
    barcode = models.ForeignKey(Barcode, related_name='stockout_details', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk: #不让修改，只能新增（暂时）
            super(StockoutDetail, self).save(*args, **kwargs)

            bc = self.barcode
            bc.amount_left = bc.amount_init - bc.stockout_details.aggregate(models.Sum('amount'))['amount__sum']
            bc.save()

class StockbackBasic(models.Model):
    code = models.CharField(unique=True, max_length=12)
    create_date = models.TimeField(auto_now_add=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stockbacks_operator", on_delete=models.PROTECT)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stockbacks_client", on_delete=models.PROTECT)
    memo = models.TextField(max_length=200)

    def get_absolute_url(self):
        return reverse("stock:stockback-info", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("stock:stockback-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("stock:stockback-delete", kwargs={"pk": self.id})

    def __str__(self):
        return self.code

class StockbackDetail(models.Model):
    basic = models.ForeignKey(StockbackBasic, related_name='details', on_delete=models.CASCADE)
    barcode = models.ForeignKey(Barcode, related_name='stockback_details', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        super(StockbackDetail, self).save(*args, **kwargs)

        bc = self.barcode
        bc.amount_left = bc.amount_init + bc.stockback_details.aggregate(models.Sum('amount'))['amount__sum'] \
            - bc.stockout_details.aggregate(models.Sum('amount'))['amount__sum']
        bc.save()


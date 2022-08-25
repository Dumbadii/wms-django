from django.db import models
from django.urls import reverse
from django.conf import settings
from params.models import ItemInfo, BarcodeStatus,Department
from user.models import Employee
from datetime import datetime

class StockinBasic(models.Model):
    code = models.CharField(unique=True, max_length=11, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    vendor =models.CharField(max_length=50, null=True, blank=True)
    memo = models.TextField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            code_prefix = 'SI' + datetime.today().strftime('%y%m%d')
            objects = StockinBasic.objects.filter(code__startswith=code_prefix).all()
            if objects:
                max_code = objects.aggregate(models.Max('code'))['code__max']
                self.code = code_prefix + ('000' + str(int(max_code[-3:]) + 1))[-3:]
            else:
                self.code = code_prefix + '001'

        super(StockinBasic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("stock:stockin-info", kwargs={"pk": self.id})

    def get_pdf_url(self):
        return reverse("stock:stockin-pdf", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("stock:stockin-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("stock:stockin-delete", kwargs={"pk": self.id})

    def get_confirm_url(self):
        return reverse("stock:stockin-confirm", kwargs={"pk": self.id})

    def __str__(self):
        return '%s-%s' %(self.id,self.code)

class StockinDetail(models.Model):
    basic = models.ForeignKey(StockinBasic, related_name='details', on_delete=models.PROTECT)
    item = models.ForeignKey(ItemInfo, related_name='stockin_details', on_delete=models.PROTECT, null=False, blank=False)
    barcode_count = models.IntegerField()
    amount = models.DecimalField(max_digits=5, decimal_places=2,validators=[])
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def list_barcodes(self):
        if self.basic.confirmed:
            if self.barcode_count > 1:
                return '%s-%s' %(self.barcodes.all()[0].code, self.barcodes.all()[self.barcode_count-1].code[-4:])
            else:
                return self.barcodes.all()[0].code
        return 'no barcodes'
    
    def gen_barcode(self):
        self.barcodes.all().delete()
        max_code = Barcode.objects.filter(item=self.item).aggregate(models.Max('code'))['code__max']
        code_index = 0 if not max_code else int(max_code[-4:])
        for i in range(self.barcode_count):
            bc = Barcode(code = self.item.code + ('0000' + str(code_index+i+1))[-4:])
            bc.stockin_detail = self
            bc.item = self.item
            bc.amount = self.amount / self.barcode_count
            bc.save()
 
class Barcode(models.Model):
    stockin_detail = models.ForeignKey(StockinDetail, related_name='barcodes', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemInfo, related_name='barcodes', on_delete=models.PROTECT)
    code = models.CharField(unique=True, max_length=11)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    department = models.ForeignKey(Department, related_name='barcodes', on_delete=models.PROTECT, default=1)
    status = models.ForeignKey(BarcodeStatus, related_name='barcodes', on_delete=models.PROTECT,default=1)

    def __str__(self):
        return '%s-%s' %(self.code, self.item.name)


class StockoutBasic(models.Model):
    code = models.CharField(unique=True, max_length=12, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stockouts_operator", 
        on_delete=models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(Employee, related_name="stockouts", on_delete=models.PROTECT)
    department = models.ForeignKey(Department, related_name="stockouts", on_delete=models.PROTECT)
    memo = models.TextField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            code_prefix = 'SO' + datetime.today().strftime('%y%m%d')
            objects = StockoutBasic.objects.filter(code__startswith=code_prefix).all()
            if objects:
                max_code = objects.aggregate(models.Max('code'))['code__max']
                self.code = code_prefix + ('000' + str(int(max_code[-3:]) + 1))[-3:]
            else:
                self.code = code_prefix + '001'

        super(StockoutBasic, self).save(*args, **kwargs)

 
    def get_pdf_url(self):
        return reverse("stock:stockout-pdf", kwargs={"pk": self.id})

    def get_absolute_url(self):
        return reverse("stock:stockout-info", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("stock:stockout-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("stock:stockout-delete", kwargs={"pk": self.id})

    def get_confirm_url(self):
        return reverse("stock:stockout-confirm", kwargs={"pk": self.id})

    def __str__(self):
        return self.code

class StockoutDetail(models.Model):
    basic = models.ForeignKey(StockoutBasic, related_name='details', on_delete=models.CASCADE)
    barcode = models.ForeignKey(Barcode, related_name='stockout_details', on_delete=models.PROTECT)

class StockbackBasic(models.Model):
    code = models.CharField(unique=True, max_length=12, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stockbacks", 
        on_delete=models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(Employee, related_name="stockbacks", on_delete=models.PROTECT)
    department = models.ForeignKey(Department, related_name="stockbacks", on_delete=models.PROTECT)
    memo = models.TextField(max_length=200)
    confirmed = models.BooleanField(default=False)
 
    def save(self, *args, **kwargs):
        if self.pk is None:
            code_prefix = 'SB' + datetime.today().strftime('%y%m%d')
            objects = StockbackBasic.objects.filter(code__startswith=code_prefix).all()
            if objects:
                max_code = objects.aggregate(models.Max('code'))['code__max']
                self.code = code_prefix + ('000' + str(int(max_code[-3:]) + 1))[-3:]
            else:
                self.code = code_prefix + '001'

        super(StockbackBasic, self).save(*args, **kwargs)


    def get_pdf_url(self):
        return reverse("stock:stockback-pdf", kwargs={"pk": self.id})

    def get_absolute_url(self):
        return reverse("stock:stockback-info", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("stock:stockback-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("stock:stockback-delete", kwargs={"pk": self.id})

    def get_confirm_url(self):
        return reverse("stock:stockback-confirm", kwargs={"pk": self.id})

    def __str__(self):
        return self.code

class StockbackDetail(models.Model):
    basic = models.ForeignKey(StockbackBasic, related_name='details', on_delete=models.CASCADE)
    barcode = models.ForeignKey(Barcode, related_name='stockback_details', on_delete=models.PROTECT)

# stockdisabled-----------------------------
class StockdisableBasic(models.Model):
    code = models.CharField(unique=True, max_length=12, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stockdisables", 
        on_delete=models.PROTECT, null=True, blank=True)
    memo = models.TextField(max_length=200)
    confirmed = models.BooleanField(default=False)
 
    def save(self, *args, **kwargs):
        if self.pk is None:
            code_prefix = 'SD' + datetime.today().strftime('%y%m%d')
            objects = StockdisableBasic.objects.filter(code__startswith=code_prefix).all()
            if objects:
                max_code = objects.aggregate(models.Max('code'))['code__max']
                self.code = code_prefix + ('000' + str(int(max_code[-3:]) + 1))[-3:]
            else:
                self.code = code_prefix + '001'

        super(StockdisableBasic, self).save(*args, **kwargs)

class StockdisableDetail(models.Model):
    basic = models.ForeignKey(StockdisableBasic, related_name='details', on_delete=models.CASCADE)
    barcode = models.ForeignKey(Barcode, related_name='stockdisable_details', on_delete=models.PROTECT)

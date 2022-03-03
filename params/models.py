from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

UnitCodeReg = RegexValidator(r'^[0-9]{3}$', '3 digits requires')
# Create your models here.
class Unit(models.Model):
    code = models.CharField(unique=True, max_length=3, validators=[UnitCodeReg])
    name = models.TextField(max_length=10)
    unique_barcode = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("params:unit-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("params:unit-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("params:unit-delete", kwargs={"pk": self.id})

    def __str__(self):
        return '%s-%s' %(self.code, self.name)

DepartmentCodeReg = UnitCodeReg
class Department(models.Model):
    code = models.CharField(unique=True, max_length=3, validators=[DepartmentCodeReg])
    name = models.TextField(max_length=10)

    def get_absolute_url(self):
        return reverse("params:department-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("params:department-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("params:department-delete", kwargs={"pk": self.id})


ItemTypeReg = RegexValidator(r'^[A-Z][0-9]{0,3}$')
class ItemType(models.Model):
    code = models.CharField(unique=True, max_length=7, validators=[ItemTypeReg])
    name = models.TextField(max_length=10)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, default=0)

    def __unicode__(self):
        return u'%s-%s' %(self.code, self.name)

    def __str__(self):
        return '%s-%s' %(self.code, self.name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            max_code = ItemType.objects.filter(parent=self.parent).aggregate(models.Max('code'))['code__max']
            if not max_code:
                self.code = 'A' if self.parent == 0 else self.parent.code + '001'
            elif len(max_code) == 1:
                self.code = chr(ord(max_code[0]) + 1)
            else:
                self.code = max_code[:1] + ('000' + str(int(max_code[-3:]) + 1))[-3:]

        super(ItemType, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("params:itemtype-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("params:itemtype-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("params:itemtype-delete", kwargs={"pk": self.id})

ItemCodeReg = RegexValidator(r'^[A-Z][0-9]{6}$')
class ItemInfo(models.Model):
    code = models.CharField(unique=True, max_length=7, validators=[ItemCodeReg])
    name = models.CharField(unique=True, max_length=100)
    specification = models.TextField(max_length=500)
    type1 = models.ForeignKey(ItemType, on_delete=models.PROTECT, related_name='parent_type')
    type2 = models.ForeignKey(ItemType, on_delete=models.PROTECT, related_name='child_type')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.pk is None:
            max_code = ItemInfo.objects.filter(type2=self.type2).aggregate(models.Max('code'))['code__max']
            if not max_code:
                print('pk',self.type2.pk)
                max_code = ItemType.objects.filter(pk=self.type2.pk)[0].code
                self.code = max_code[:4] + '001'
            else:
                self.code = max_code[:4] + ('000' + str(int(max_code[-3:]) + 1))[-3:]

        super(ItemInfo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("params:iteminfo-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("params:iteminfo-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("params:iteminfo-delete", kwargs={"pk": self.id})

    def __str__(self):
        return '%s-%s' %(self.code, self.name)
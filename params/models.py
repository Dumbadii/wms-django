from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

# Create your models here.
class BarcodeStatus(models.Model):
    statusId = models.IntegerField(unique=True)
    statusName = models.TextField(max_length=10)
    def __str__(self):
        return '%s-%s' %(self.statusId, self.statusName)

UnitCodeReg = RegexValidator(r'^[0-9]{3}$', '3 digits requires')
# Create your models here.
class Unit(models.Model):
    class Meta:
        verbose_name_plural = '单位表'
    code = models.CharField(unique=True, max_length=3, validators=[UnitCodeReg], verbose_name='编号')
    name = models.TextField(max_length=10, verbose_name='名称')

    def __str__(self):
        return self.name

DepartmentCodeReg = UnitCodeReg
class Department(models.Model):
    class Meta:
        verbose_name_plural = '部门表'
    code = models.CharField(unique=True, max_length=3, validators=[DepartmentCodeReg], verbose_name='代码')
    name = models.TextField(max_length=10, verbose_name='名称')
    
    def __str__(self):
        return '%s-%s' %(self.code, self.name)


class ItemTypeParent(models.Model):
    class Meta:
        verbose_name_plural = '物品父类表'
    code = models.CharField(unique=True, max_length=1, null=True, blank=True, verbose_name='代码')
    name = models.TextField(max_length=10, verbose_name='名称')

    def __str__(self):
        return '%s-%s' %(self.code, self.name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            max_code = ItemTypeParent.objects.aggregate(models.Max('code'))['code__max']
            if not max_code:
                self.code = 'A'
            else:
                self.code = chr(ord(max_code[0]) + 1)

        super(ItemTypeParent, self).save(*args, **kwargs)


class ItemTypeChild(models.Model):
    class Meta:
        verbose_name_plural = '物品子类表'
    code = models.CharField(unique=True, max_length=7, null=True, blank=True, verbose_name='代码')
    name = models.TextField(max_length=10, verbose_name='名称')
    parent = models.ForeignKey(ItemTypeParent, on_delete=models.PROTECT, verbose_name='父类')

    def __str__(self):
        return '%s-%s' %(self.code, self.name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            max_code = ItemTypeChild.objects.filter(parent=self.parent).aggregate(models.Max('code'))['code__max']
            if not max_code:
                self.code = self.parent.code + '001'
            else:
                self.code = max_code[:1] + ('000' + str(int(max_code[-3:]) + 1))[-3:]

        super(ItemTypeChild, self).save(*args, **kwargs)


class ItemInfo(models.Model):
    class Meta:
        verbose_name_plural = '物品表'
    code = models.CharField(unique=True, max_length=7, null=True, blank=True, verbose_name='代码')
    name = models.CharField(unique=True, max_length=100, verbose_name='名称')
    specification = models.TextField(max_length=500, verbose_name='规格')
    # type1 = models.ForeignKey(ItemTypeParent, on_delete=models.PROTECT, related_name='parent_type')
    type2 = models.ForeignKey(ItemTypeChild, on_delete=models.PROTECT, related_name='items', verbose_name='分类')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='单位')
    brand = models.CharField(max_length=50, verbose_name='品牌')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='单价')

    def save(self, *args, **kwargs):
        if self.pk is None:
            max_code = ItemInfo.objects.filter(type2=self.type2).aggregate(models.Max('code'))['code__max']
            if not max_code:
                print('pk',self.type2.pk)
                max_code = ItemTypeChild.objects.filter(pk=self.type2.pk)[0].code
                self.code = max_code[:4] + '001'
            else:
                self.code = max_code[:4] + ('000' + str(int(max_code[-3:]) + 1))[-3:]

        super(ItemInfo, self).save(*args, **kwargs)

    def __str__(self):
        return '%s-%s-%s' %(self.code, self.name, self.unit.name)

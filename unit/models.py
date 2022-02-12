from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

UnitCodeReg = RegexValidator(r'^[0-9]{3}$', '3 digits requires')
# Create your models here.
class Unit(models.Model):
    code = models.CharField(unique=True, max_length=3, validators=[UnitCodeReg])
    name = models.TextField(max_length=10)

    def get_absolute_url(self):
        return reverse("unit:unit-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("unit:unit-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("unit:unit-delete", kwargs={"pk": self.id})

DepartmentCodeReg = UnitCodeReg
class Department(models.Model):
    code = models.CharField(unique=True, max_length=3, validators=[DepartmentCodeReg])
    name = models.TextField(max_length=10)

    def get_absolute_url(self):
        return reverse("department:department-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("department:department-update", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("department:department-delete", kwargs={"pk": self.id})


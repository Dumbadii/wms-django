from django.db import models
from django.contrib.auth.models import User
from params.models import Department

# Create your models here.
class Employee(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  department = models.ForeignKey(Department, related_name='employee',
    on_delete=models.CASCADE)

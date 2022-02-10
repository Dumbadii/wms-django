from django.db import models
from django.urls import reverse

# Create your models here.
class Unit(models.Model):
    code = models.CharField(max_length=3)
    name = models.TextField(max_length=10)

    def get_absolute_url(self):
        return reverse("unit-detail", kwargs={"id": self.id})


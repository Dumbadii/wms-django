# Generated by Django 3.2.12 on 2022-08-11 03:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0014_auto_20220420_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='code',
            field=models.CharField(max_length=3, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{3}$', '3 digits requires')], verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.TextField(max_length=10, verbose_name='名称'),
        ),
    ]

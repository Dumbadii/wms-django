# Generated by Django 3.2.12 on 2022-02-12 12:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0003_alter_itemtype_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='code',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator('^[A-Z][0-9]{0,3}$')]),
        ),
    ]

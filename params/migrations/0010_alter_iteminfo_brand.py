# Generated by Django 3.2.12 on 2022-02-22 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0009_iteminfo_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminfo',
            name='brand',
            field=models.CharField(max_length=50),
        ),
    ]

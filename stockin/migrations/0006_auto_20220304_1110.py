# Generated by Django 3.2.12 on 2022-03-04 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockin', '0005_stockoutbasic_stockoutdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barcode',
            name='amount_init',
        ),
        migrations.RemoveField(
            model_name='barcode',
            name='amount_left',
        ),
    ]
# Generated by Django 3.2.12 on 2022-04-23 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0014_auto_20220420_0421'),
        ('stockin', '0023_alter_stockoutbasic_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barcode',
            name='status',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='barcodes', to='params.barcodestatus'),
        ),
    ]

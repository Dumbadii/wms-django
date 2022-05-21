# Generated by Django 3.2.12 on 2022-05-16 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0014_auto_20220420_0421'),
        ('stockin', '0028_barcode_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barcode',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='barcodes', to='params.department'),
        ),
    ]

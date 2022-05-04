# Generated by Django 3.2.12 on 2022-05-01 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0014_auto_20220420_0421'),
        ('stockin', '0024_alter_barcode_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barcode',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='barcodes', to='params.barcodestatus'),
        ),
        migrations.AlterField(
            model_name='stockbackbasic',
            name='code',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
    ]

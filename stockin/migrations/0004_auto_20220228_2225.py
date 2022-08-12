# Generated by Django 3.2.12 on 2022-02-28 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockin', '0003_auto_20220228_2106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='barcode',
            old_name='amount',
            new_name='amount_init',
        ),
        migrations.AddField(
            model_name='barcode',
            name='amount_left',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
    ]

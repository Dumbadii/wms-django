# Generated by Django 3.2.12 on 2022-02-12 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0004_alter_itemtype_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='params.itemtype'),
        ),
    ]

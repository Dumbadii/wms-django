# Generated by Django 3.2.12 on 2022-02-12 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0002_itemtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='params.itemtype'),
        ),
    ]

# Generated by Django 3.2.12 on 2022-02-19 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0007_auto_20220219_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iteminfo',
            name='type',
        ),
        migrations.AddField(
            model_name='iteminfo',
            name='type1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='parent_type', to='params.itemtype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='iteminfo',
            name='type2',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='child_type', to='params.itemtype'),
            preserve_default=False,
        ),
    ]

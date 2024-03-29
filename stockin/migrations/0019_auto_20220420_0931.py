# Generated by Django 3.2.12 on 2022-04-20 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('params', '0014_auto_20220420_0421'),
        ('stockin', '0018_auto_20220420_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockoutbasic',
            name='client',
        ),
        migrations.AddField(
            model_name='stockoutbasic',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='stockouts', to='params.department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockoutbasic',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='stockouts', to='user.employee'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2.12 on 2022-03-08 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockin', '0013_remove_stockoutdetail_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockbackdetail',
            name='amount',
        ),
        migrations.AddField(
            model_name='stockbackbasic',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]

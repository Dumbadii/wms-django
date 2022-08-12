# Generated by Django 3.2.12 on 2022-02-12 03:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{3}$', '3 digits requires')])),
                ('name', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{3}$', '3 digits requires')])),
                ('name', models.TextField(max_length=10)),
            ],
        ),
    ]

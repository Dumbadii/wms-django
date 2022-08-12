# Generated by Django 3.2.12 on 2022-03-04 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stockin', '0007_auto_20220304_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockbackBasic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=12, unique=True)),
                ('create_date', models.TimeField(auto_now_add=True)),
                ('memo', models.TextField(max_length=200)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stockbacks_client', to=settings.AUTH_USER_MODEL)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stockbacks_operator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockbackDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('barcode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stockback_details', to='stockin.barcode')),
                ('basic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='stockin.stockbackbasic')),
            ],
        ),
    ]

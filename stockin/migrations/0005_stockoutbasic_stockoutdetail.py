# Generated by Django 3.2.12 on 2022-03-03 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stockin', '0004_auto_20220228_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockoutBasic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=12, unique=True)),
                ('create_date', models.TimeField(auto_now_add=True)),
                ('memo', models.TextField(max_length=200)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stockouts_client', to=settings.AUTH_USER_MODEL)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stockouts_operator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockoutDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('barcode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stockout_details', to='stockin.barcode')),
                ('basic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='stockin.stockoutbasic')),
            ],
        ),
    ]

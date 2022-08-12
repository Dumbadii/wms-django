# Generated by Django 3.2.12 on 2022-05-16 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0014_auto_20220420_0421'),
        ('user', '0003_alter_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='params.department'),
        ),
    ]

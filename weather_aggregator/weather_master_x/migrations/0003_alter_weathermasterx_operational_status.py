# Generated by Django 5.1.1 on 2024-09-28 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_master_x', '0002_alter_weathermasterx_operational_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weathermasterx',
            name='operational_status',
            field=models.CharField(choices=[('operational', 'operational'), ('maintenance', 'maintenance')], max_length=20),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_master_x', '0003_alter_weathermasterx_operational_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weathermasterx',
            name='humidity_percent',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='weathermasterx',
            name='pressure_hpa',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='weathermasterx',
            name='rain_mm',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='weathermasterx',
            name='temp_fahrenheit',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-28 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_master_x', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weathermasterx',
            name='operational_status',
            field=models.CharField(choices=[('o', 'operational'), ('m', 'maintenance')], max_length=20),
        ),
    ]

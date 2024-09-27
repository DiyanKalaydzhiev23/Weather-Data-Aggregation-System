from django.db import models

# Create your models here.

from django.db import models

class BulgarianMeteoProData(models.Model):
    station_id = models.CharField(
        max_length=50
    )

    city = models.CharField(
        max_length=100
    )

    latitude = models.FloatField()

    longitude = models.FloatField()

    timestamp = models.DateTimeField()  # ISO 8601 format

    temperature_celsius = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    humidity_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    wind_speed_kph = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    station_status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ]
    )

    raw_data = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['city', 'timestamp']),  # optimized for filtering city and ordering by timestamp
        ]
        ordering = ['timestamp']

    def __str__(self):
        return f"Station {self.station_id} in {self.city} recorded at {self.timestamp}"

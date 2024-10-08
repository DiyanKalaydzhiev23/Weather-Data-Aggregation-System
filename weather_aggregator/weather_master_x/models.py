from django.db import models

from weather_master_x.choices import StationStatusChoices


class WeatherMasterX(models.Model):
    station_identifier = models.CharField(
        max_length=50,
    )

    city_name = models.CharField(
        max_length=100,
    )

    lat = models.FloatField()

    lon = models.FloatField()

    recorded_at = models.DateTimeField()

    temp_fahrenheit = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    humidity_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    pressure_hpa = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    uv_index = models.IntegerField()

    rain_mm = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    operational_status = models.CharField(
        max_length=20,
        choices=StationStatusChoices.choices,
    )

    raw_data = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['city_name', 'recorded_at']),  # optimized for filtering city and ordering by timestamp
        ]
        ordering = ['recorded_at']

    def __str__(self):
        return f"Station {self.station_identifier} in {self.city_name} recorded at {self.recorded_at}"

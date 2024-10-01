from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from stations.managers import StationManager


class Station(models.Model):
    station_type = models.CharField(
        max_length=50
    )

    city = models.CharField(
        max_length=100
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.PositiveIntegerField()

    station_data = GenericForeignKey(
        'content_type',
        'object_id'
    )

    is_active = models.BooleanField(
        default=True
    )

    objects = StationManager()

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"Station {self.station_type} in {self.city}"

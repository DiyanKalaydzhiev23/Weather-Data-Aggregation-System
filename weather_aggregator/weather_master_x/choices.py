from django.db import models


class StationStatusChoices(models.TextChoices):
    OPERATIONAL = 'operational', 'operational'
    MAINTENANCE = 'maintenance', 'maintenance'

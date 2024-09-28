from django.contrib.contenttypes.models import ContentType
from stations.models import Station

class CreateStationMixin:
    """
    Mixin to automatically create a Station entry when a new weather station data record is created.
    """
    station_type = None  # Must be specified in the view using this mixin

    def get_station_type(self):
        if self.station_type:
            return self.station_type
        if self.queryset is not None:
            return self.queryset.model._meta.model_name
        raise NotImplementedError("View must define `station_type` or provide a queryset.")


    def perform_create(self, serializer):
        station_data_instance = serializer.save()
        station_type = self.get_station_type()

        station_data = serializer.get_station_data(station_data_instance)

        city = station_data.get('city')
        is_active = station_data.get('is_active')

        content_type = ContentType.objects.get_for_model(station_data_instance)

        Station.objects.create(
            station_type=station_type,
            city=city,
            content_type=content_type,
            object_id=station_data_instance.id,
            is_active=is_active
        )

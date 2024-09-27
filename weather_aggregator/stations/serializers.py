from abc import ABCMeta, abstractmethod
from rest_framework import serializers

DEFAULT_WEATHER_FIELDS = {
    'station_id': None,
    'city': None,
    'latitude': None,
    'longitude': None,
    'temperature_celsius': None,
    'humidity_percent': None,
    'wind_speed_kph': None,
    'pressure_hpa': None,
    'uv_index': None,
    'solar_radiation': None,
    'timestamp': None
}

class ABCSerializerMeta(ABCMeta, serializers.SerializerMetaclass):
    pass  # Solves the meta conflicts of Serializer and ABC


class BaseWeatherDataSerializer(serializers.Serializer, metaclass=ABCSerializerMeta):
    @abstractmethod
    def get_station_data(self, instance):
        pass

    def to_representation(self, instance):
        return_raw = self.context.get('return_raw_data', False)

        if return_raw:
            return instance.raw_data
        else:
            station_data = self.get_station_data(instance)
            return {**DEFAULT_WEATHER_FIELDS, **station_data}

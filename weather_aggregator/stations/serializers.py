from abc import ABCMeta, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import TypedDict, Optional
from rest_framework import serializers


class DefaultWeatherFields(TypedDict, total=False):
    station_id: Optional[str]
    city: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    temperature_celsius: Optional[Decimal]
    humidity_percent: Optional[Decimal]
    wind_speed_kph: Optional[Decimal]
    pressure_hpa: Optional[Decimal]
    uv_index: Optional[int]
    timestamp: Optional[datetime]
    is_active: Optional[bool]


DEFAULT_WEATHER_FIELDS: DefaultWeatherFields = {
    'station_id': None,
    'city': None,
    'latitude': None,
    'longitude': None,
    'temperature_celsius': None,
    'humidity_percent': None,
    'wind_speed_kph': None,
    'pressure_hpa': None,
    'uv_index': None,
    'timestamp': None,
    'is_active': None,
}

class ABCSerializerMeta(ABCMeta, serializers.SerializerMetaclass):
    def __new__(cls, name, bases, dct):
        abc_instance = ABCMeta.__new__(cls, name, bases, dct)
        serializer_instance = serializers.SerializerMetaclass.__new__(cls, name, bases, dct)
        return serializer_instance  # Solves the meta conflicts of Serializer and ABC


class BaseWeatherDataSerializer(serializers.Serializer, metaclass=ABCSerializerMeta):
    @abstractmethod
    def get_station_data(self, instance) -> DefaultWeatherFields:
        pass

    def create(self, validated_data):
        validated_data['raw_data'] = self.initial_data
        return super().create(validated_data)

    def to_representation(self, instance):
        return_raw = self.context.get('return_raw_data', False)

        if return_raw:
            return instance.raw_data
        else:
            station_data = self.get_station_data(instance)
            return {**DEFAULT_WEATHER_FIELDS, **station_data}

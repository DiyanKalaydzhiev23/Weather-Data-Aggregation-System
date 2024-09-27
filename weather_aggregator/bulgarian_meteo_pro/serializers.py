from rest_framework import serializers
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from stations.serializers import BaseWeatherDataSerializer


class BulgarianMeteoProDataSerializer(BaseWeatherDataSerializer, serializers.ModelSerializer):
    class Meta:
        model = BulgarianMeteoProData
        exclude = ('raw_data', )

    def get_station_data(self, instance):
        return {
            'station_id': instance.station_id,
            'city': instance.city,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'temperature_celsius': instance.temperature_celsius,
            'humidity_percent': instance.humidity_percent,
            'wind_speed_kph': instance.wind_speed_kph,
            'station_status': instance.station_status,
            'timestamp': instance.timestamp,
        }
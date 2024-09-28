from rest_framework import serializers
from stations.serializers import BaseWeatherDataSerializer
from weather_aggregator.utils import fahrenheit_to_celsius
from weather_master_x.choices import StationStatusChoices
from weather_master_x.models import WeatherMasterX


class WeatherMasterXSerializer(BaseWeatherDataSerializer, serializers.ModelSerializer):
    class Meta:
        model = WeatherMasterX
        exclude = ('raw_data', )

    def to_internal_value(self, data):
        # Flatten nested fields before validation
        location_data = data.get('location', {})
        coordinates = location_data.get('coordinates', {})
        readings_data = data.get('readings', {})

        # Update data to flatten the structure
        data['city_name'] = location_data.get('city_name')
        data['lat'] = coordinates.get('lat')
        data['lon'] = coordinates.get('lon')
        data['temp_fahrenheit'] = readings_data.get('temp_fahrenheit')
        data['humidity_percent'] = readings_data.get('humidity_percent')
        data['pressure_hpa'] = readings_data.get('pressure_hpa')
        data['uv_index'] = readings_data.get('uv_index')
        data['rain_mm'] = readings_data.get('rain_mm')

        return super().to_internal_value(data)

    def get_station_data(self, instance: WeatherMasterX):
        return {
            'station_id': instance.station_identifier,
            'city': instance.city_name,
            'latitude': instance.lat,
            'longitude': instance.lon,
            'temperature_celsius': fahrenheit_to_celsius(instance.temp_fahrenheit),
            'humidity_percent': instance.humidity_percent,
            'pressure_hpa': instance.pressure_hpa,
            'uv_index': instance.uv_index,
            'timestamp': instance.recorded_at,
            'is_active': instance.operational_status == StationStatusChoices.OPERATIONAL,
        }

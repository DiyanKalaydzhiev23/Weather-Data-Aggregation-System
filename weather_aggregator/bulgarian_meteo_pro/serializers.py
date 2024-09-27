from stations.serializers import BaseWeatherDataSerializer


class BulgarianMeteoProDataSerializer(BaseWeatherDataSerializer):
    def get_station_data(self, instance):
        return {
            'temperature_celsius': instance.temperature_celsius,
            'humidity_percent': instance.humidity_percent,
            'wind_speed_kph': instance.wind_speed_kph,
            'timestamp': instance.timestamp
        }

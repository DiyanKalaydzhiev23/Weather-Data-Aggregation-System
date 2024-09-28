from bulgarian_meteo_pro.models import BulgarianMeteoProData
from bulgarian_meteo_pro.serializers import BulgarianMeteoProDataSerializer
from weather_master_x.models import WeatherMasterX
from weather_master_x.serializers import WeatherMasterXSerializer

SERIALIZER_MAPPING = {
    BulgarianMeteoProData._meta.model_name.lower(): BulgarianMeteoProDataSerializer,
    WeatherMasterX._meta.model_name.lower(): WeatherMasterXSerializer,
}

class WeatherSerializerFactory:
    @staticmethod
    def get_serializer(station_instance):
        model_name = station_instance._meta.model_name.lower()
        serializer_class = SERIALIZER_MAPPING.get(model_name)

        if not serializer_class:
            raise ValueError(f"Serializer for station type '{model_name}' not found")

        return serializer_class

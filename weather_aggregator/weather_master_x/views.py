from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import CreateAPIView
from stations.mixins import CreateStationMixin
from weather_aggregator.utils import example_bad_request
from weather_master_x.models import WeatherMasterX
from weather_master_x.serializers import WeatherMasterXSerializer


@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "station_identifier": {"type": "string"},
                "location": {
                    "type": "object",
                    "properties": {
                        "city_name": {"type": "string"},
                        "coordinates": {
                            "type": "object",
                            "properties": {
                                "lat": {"type": "number"},
                                "lon": {"type": "number"}
                            },
                            "required": ["lat", "lon"]
                        }
                    },
                    "required": ["city_name", "coordinates"]
                },
                "recorded_at": {"type": "string", "format": "date-time"},
                "readings": {
                    "type": "object",
                    "properties": {
                        "temp_fahrenheit": {"type": "number"},
                        "humidity_percent": {"type": "number"},
                        "pressure_hpa": {"type": "number"},
                        "uv_index": {"type": "integer"},
                        "rain_mm": {"type": "number"}
                    },
                    "required": ["temp_fahrenheit", "humidity_percent"]
                },
                "operational_status": {"type": "string"}
            },
            "required": ["station_identifier", "location", "recorded_at", "readings", "operational_status"]
        }
    },
    responses={
        201: WeatherMasterXSerializer,
        400: OpenApiResponse(
            description="Validation Error",
            response=OpenApiTypes.OBJECT,
            examples=[
                example_bad_request,
            ]
        )
    }
)
class CreateWeatherDataView(CreateStationMixin, CreateAPIView):
    queryset = WeatherMasterX.objects.all()
    serializer_class = WeatherMasterXSerializer

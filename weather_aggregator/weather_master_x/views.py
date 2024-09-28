from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import CreateAPIView

from stations.mixins import CreateStationMixin
from weather_aggregator.utils import example_bad_request
from weather_master_x.models import WeatherMasterX
from weather_master_x.serializers import WeatherMasterXSerializer


@extend_schema(
    request=WeatherMasterXSerializer,
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

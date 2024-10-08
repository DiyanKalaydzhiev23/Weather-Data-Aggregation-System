from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import CreateAPIView
from stations.mixins import CreateStationMixin
from weather_aggregator.utils import example_bad_request
from .models import BulgarianMeteoProData
from .serializers import BulgarianMeteoProDataSerializer


@extend_schema(
    request=BulgarianMeteoProDataSerializer,
    responses={
        201: BulgarianMeteoProDataSerializer,
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
    queryset = BulgarianMeteoProData.objects.all()
    serializer_class = BulgarianMeteoProDataSerializer

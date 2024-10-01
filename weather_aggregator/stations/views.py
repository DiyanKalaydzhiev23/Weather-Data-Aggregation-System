from dataclasses import asdict

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from weather_aggregator.serializers_mapping import WeatherSerializerFactory
from .models import Station


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='raw',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Set to true to return raw data, otherwise normalized data will be returned.',
            required=False,
        )
    ]
)
@api_view(['GET'])
def get_aggregated_weather_data(request, city_name):
    return_raw_data = request.query_params.get('raw', 'false').lower() == 'true'
    aggregated_data = Station.objects.get_aggregated_weather_data(city_name, return_raw_data)

    if not aggregated_data:
        return Response(
            {"message": "No weather stations found for the specified city."},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(aggregated_data, status=status.HTTP_200_OK)

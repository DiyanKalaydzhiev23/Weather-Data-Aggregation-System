from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from weather_aggregator.serializers_mapping import WeatherSerializerFactory
from .models import Station


@api_view(['GET'])
def get_aggregated_weather_data(request, city_name):
    stations = Station.objects.filter(city__iexact=city_name).select_related('content_type')

    if not stations.exists():
        return Response(
            {"message": "No weather stations found for the specified city."},
            status=status.HTTP_404_NOT_FOUND
        )

    content_type_to_ids = {}
    content_type_to_model_class = {}

    for station in stations:
        content_type = station.content_type
        model_class = content_type.model_class()
        content_type_to_model_class[content_type.id] = model_class  # Cache the model class lookup

        if model_class not in content_type_to_ids:
            content_type_to_ids[model_class] = []

        content_type_to_ids[model_class].append(station.object_id)

    model_instances = {}
    for model_class, ids in content_type_to_ids.items():
        instances = model_class.objects.filter(id__in=ids)
        model_instances[model_class] = {instance.id: instance for instance in instances}

    aggregated_data = []
    for station in stations:
        station_model_class = content_type_to_model_class[station.content_type.id]
        station_instance = model_instances.get(station_model_class, {}).get(station.object_id)

        if not station_instance:
            continue

        try:
            serializer_class = WeatherSerializerFactory.get_serializer(station_instance)
        except ValueError:
            continue

        serializer = serializer_class(station_instance)
        aggregated_data.append(serializer.data)

    if not aggregated_data:
        return Response({"message": "No data available for the specified city."}, status=status.HTTP_404_NOT_FOUND)

    return Response(aggregated_data, status=status.HTTP_200_OK)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import BulgarianMeteoProData
from .serializers import BulgarianMeteoProDataSerializer

@api_view(['POST'])
def create_weather_data(request):
    serializer = BulgarianMeteoProDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_weather_data_by_city(request, city_name):
    weather_data = BulgarianMeteoProData.objects.filter(city=city_name).order_by('timestamp')
    serializer = BulgarianMeteoProDataSerializer(weather_data, many=True)
    return Response(serializer.data)

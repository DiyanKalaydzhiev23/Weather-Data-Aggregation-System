from django.urls import path
from stations import views

urlpatterns = (
    path('weather-data/<str:city_name>', views.get_aggregated_weather_data, name='get_city_weather_data'),
)
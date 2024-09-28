from django.urls import path
from . import views

urlpatterns = [
    path('weather-data/', views.CreateWeatherDataView.as_view(), name='create_weather_data_weather_master_x'),
]

from django.shortcuts import resolve_url
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from stations.models import Station
from weather_master_x.models import WeatherMasterX

class GetAggregatedWeatherDataTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Set up a sample weather station of type "BulgarianMeteoProData"
        self.bulgarian_content_type = ContentType.objects.get_for_model(BulgarianMeteoProData)
        self.bulgarian_station_data = BulgarianMeteoProData.objects.create(
            station_id="BG-001",
            city="Sofia",
            latitude=42.6977,
            longitude=23.3219,
            temperature_celsius=21.0,
            humidity_percent=60.0,
            wind_speed_kph=10.0,
            station_status="active",
            timestamp="2024-09-27T10:00:00Z",
            raw_data={"some_key": "some_value"}
        )

        Station.objects.create(
            station_type="BulgarianMeteoProData",
            city="Sofia",
            content_type=self.bulgarian_content_type,
            object_id=self.bulgarian_station_data.id,
            is_active=True
        )

        # Set up a sample weather station of type "WeatherMasterX"
        self.weather_master_content_type = ContentType.objects.get_for_model(WeatherMasterX)
        self.weather_master_data = WeatherMasterX.objects.create(
            station_identifier="WX-1234",
            city_name="Sofia",
            lat=42.1354,
            lon=24.7453,
            temp_fahrenheit=75.2,
            humidity_percent=58.0,
            pressure_hpa=1012.3,
            uv_index=4,
            rain_mm=1.2,
            operational_status="operational",
            recorded_at="2024-09-27T10:30:00Z",
            raw_data={"some_other_key": "some_other_value"}
        )

        Station.objects.create(
            station_type="WeatherMasterX",
            city="Sofia",
            content_type=self.weather_master_content_type,
            object_id=self.weather_master_data.id,
            is_active=True
        )

    def test_get_aggregated_weather_data_normalized(self):
        """Test getting aggregated weather data in normalized format"""
        response = self.client.get(resolve_url('get_city_weather_data', city_name='Sofia'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        self.assertIn("temperature_celsius", response.data[0])
        self.assertIn("humidity_percent", response.data[0])

    def test_get_aggregated_weather_data_raw(self):
        """Test getting aggregated weather data in raw format"""
        response = self.client.get(resolve_url('get_city_weather_data', city_name='Sofia'), {"raw": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        self.assertIn("some_key", response.data[0])
        self.assertNotIn("temperature_celsius", response.data[0])

    def test_get_aggregated_weather_data_city_not_found(self):
        """Test getting aggregated weather data for a city that has no stations"""
        response = self.client.get(resolve_url('get_city_weather_data', city_name='Varna'))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"message": "No weather stations found for the specified city."})



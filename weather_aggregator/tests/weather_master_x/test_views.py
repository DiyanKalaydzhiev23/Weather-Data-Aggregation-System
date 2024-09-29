from django.shortcuts import resolve_url
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from weather_master_x.models import WeatherMasterX
from stations.models import Station


class CreateWeatherMasterXDataTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "station_identifier": "WX-1234",
            "location": {
                "city_name": "Plovdiv",
                "coordinates": {
                    "lat": 42.1354,
                    "lon": 24.7453
                }
            },
            "recorded_at": "2024-09-27T10:20:45Z",
            "readings": {
                "temp_fahrenheit": 73.4,
                "humidity_percent": 58.0,
                "pressure_hpa": 1012.3,
                "uv_index": 5,
                "rain_mm": 0.0
            },
            "operational_status": "operational"
        }
        self.invalid_payload = {
            "station_identifier": "WX-INVALID",
            "location": {
                "city_name": "",
                "coordinates": {
                    "lat": "invalid",  # Invalid value for latitude
                }
            },
            "recorded_at": "invalid-date",  # Incorrect datetime format
            "readings": {
                "temp_fahrenheit": "invalid",  # Should be a float
                "humidity_percent": 58.0,
                "pressure_hpa": 1012.3,
                "uv_index": "invalid",  # Should be an integer
                "rain_mm": 0.0
            },
            "operational_status": "operational"
        }

    def test_create_weather_master_x_data_success(self):
        """Test creating WeatherMasterX data successfully"""
        response = self.client.post(
            resolve_url('create_weather_data_weather_master_x'),
            data=self.valid_payload,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WeatherMasterX.objects.count(), 1)
        self.assertEqual(Station.objects.count(), 1)

        # Ensure the Station record is created correctly
        station = Station.objects.first()
        self.assertEqual(station.city, self.valid_payload["location"]["city_name"])
        self.assertEqual(station.station_type, "weathermasterx")
        self.assertEqual(station.is_active, True)

    def test_create_weather_master_x_data_invalid_payload(self):
        """Test creating WeatherMasterX data with invalid payload"""
        response = self.client.post(
            resolve_url('create_weather_data_weather_master_x'),
            data=self.invalid_payload,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("city_name", response.data)
        self.assertIn("recorded_at", response.data)

    def test_create_weather_master_x_data_station_not_created_on_error(self):
        """Test that no Station entry is created when there is a validation error"""
        response = self.client.post(
            resolve_url('create_weather_data_weather_master_x'),
            data=self.invalid_payload,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Ensure no Station or WeatherMasterX objects are created
        self.assertEqual(WeatherMasterX.objects.count(), 0)
        self.assertEqual(Station.objects.count(), 0)

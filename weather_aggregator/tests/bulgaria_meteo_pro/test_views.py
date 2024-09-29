from django.shortcuts import resolve_url
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from stations.models import Station


class CreateWeatherDataTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "station_id": "BG-STATION-001",
            "city": "Sofia",
            "latitude": 42.6977,
            "longitude": 23.3219,
            "timestamp": "2024-09-27T10:15:30Z",
            "temperature_celsius": 22.5,
            "humidity_percent": 65.0,
            "wind_speed_kph": 14.3,
            "station_status": "active"
        }
        self.invalid_payload = {
            "station_id": "BG-STATION-002",
            "city": "",  # Missing city name to trigger validation error
            "latitude": "invalid",  # Invalid latitude to trigger validation error
            "timestamp": "invalid-date",  # Invalid date format
            "temperature_celsius": 22.5,
            "humidity_percent": 65.0,
            "wind_speed_kph": 14.3,
            "station_status": "inactive"
        }

    def test_create_weather_data_success(self):
        """Test creating a weather data entry successfully"""
        response = self.client.post(
            resolve_url('create_weather_data_bulgarian_meteo_pro'),
            data=self.valid_payload,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BulgarianMeteoProData.objects.count(), 1)
        self.assertEqual(Station.objects.count(), 1)

        # Ensure the Station record is created properly
        station = Station.objects.first()
        self.assertEqual(station.city, self.valid_payload["city"])
        self.assertEqual(station.station_type, "bulgarianmeteoprodata")
        self.assertEqual(station.is_active, True)

    def test_create_weather_data_invalid_payload(self):
        """Test creating a weather data entry with invalid payload"""
        response = self.client.post(
            resolve_url('create_weather_data_bulgarian_meteo_pro'),
            data=self.invalid_payload,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("city", response.data)
        self.assertIn("latitude", response.data)
        self.assertIn("timestamp", response.data)

    def test_create_weather_data_station_not_created_on_error(self):
        """Test no Station entry is created when there is a validation error"""
        response = self.client.post(
            resolve_url('create_weather_data_bulgarian_meteo_pro'),
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Ensure no Station or BulgarianMeteoProData objects are created
        self.assertEqual(BulgarianMeteoProData.objects.count(), 0)
        self.assertEqual(Station.objects.count(), 0)


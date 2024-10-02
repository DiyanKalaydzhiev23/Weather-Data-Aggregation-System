# Steps to Add a New Weather Station to the Project

This guide provides all the necessary steps for adding a new weather station to the existing Django project. 
Every new weather station type is treated as a separate application within the project, each with its own unique model, serializer, and API endpoint for data creation.

## Step 1: Create a New Django App for the Weather Station

1. Use the following command to create a new Django app:
   ```sh
   python manage.py startapp <new_station_name>
   ```
2. Add the new app to the `INSTALLED_APPS` in `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       '<new_station_name>',
       ...
   ]
   ```

## Step 2: Define the Model for the Weather Station

1. In the new app (`<new_station_name>`), create the model for the new station in `models.py`:
   ```python
   from django.db import models
   from weather_master_x.choices import StationStatusChoices

   class NewStationData(models.Model):
       station_id = models.CharField(max_length=50)
       city = models.CharField(max_length=100)
       latitude = models.FloatField()
       longitude = models.FloatField()
       timestamp = models.DateTimeField()
       temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)
       # Add more fields based on the station's capabilities

       raw_data = models.JSONField()

       class Meta:
           indexes = [
               models.Index(fields=['city', 'timestamp']),
           ]
           ordering = ['timestamp']

       def __str__(self):
           return f"Station {self.station_id} in {self.city} recorded at {self.timestamp}"
   ```

## Step 3: Create a Serializer for the Weather Station

1. In the `<new_station_name>` app, create a new serializer in `serializers.py`:
   ```python
   from rest_framework import serializers
   from stations.serializers import BaseWeatherDataSerializer, DefaultWeatherFields
   from .models import NewStationData

   class NewStationDataSerializer(BaseWeatherDataSerializer, serializers.ModelSerializer):
       class Meta:
           model = NewStationData
           exclude = ('raw_data', )

       def get_station_data(self, instance: NewStationData) -> DefaultWeatherFields:
           return {
               'station_id': instance.station_id,
               'city': instance.city,
               'latitude': instance.latitude,
               'longitude': instance.longitude,
               'temperature_celsius': instance.temperature_celsius,
               # Add more fields as required for this specific station type
               'timestamp': instance.timestamp,
               'is_active': instance.station_status == 'active',
           }
   ```

   - Make sure that the new serializer inherits from `BaseWeatherDataSerializer`.
   - Implement the `get_station_data` method to return the data in the standardized format, following the signature defined in `BaseWeatherDataSerializer`.

## Step 4: Add the Serializer to the Factory

1. Open the `weather_aggregator/serializers_mapping.py` file.
2. Add the new model and serializer class to the `SERIALIZER_MAPPING` in the `WeatherSerializerFactory`:
   ```python
   from <new_station_name>.models import NewStationData
   from <new_station_name>.serializers import NewStationDataSerializer

   SERIALIZER_MAPPING = {
       ...
       NewStationData._meta.model_name.lower(): NewStationDataSerializer,
       ...
   }
   ```
3. This step allows the system to determine the appropriate serializer for the new station when aggregating data.

## Step 5: Create an Endpoint for Posting Data to the New Station

1. In the `<new_station_name>` app, create a new view in `views.py` to handle the POST request for creating new weather data:
   ```python
   from rest_framework.generics import CreateAPIView
   from stations.mixins import CreateStationMixin
   from .models import NewStationData
   from .serializers import NewStationDataSerializer

   class CreateNewStationDataView(CreateStationMixin, CreateAPIView):
       queryset = NewStationData.objects.all()
       serializer_class = NewStationDataSerializer
   ```
2. Register the endpoint in `urls.py` of the `<new_station_name>` app:
   ```python
   from django.urls import path
   from .views import CreateNewStationDataView

   urlpatterns = [
       path('new-station-data/', CreateNewStationDataView.as_view(), name='create_new_station_data'),
   ]
   ```
3. Add the URL path to the project's root URL configuration.

## Step 6: Test the Endpoint

1. Use Swagger (available at `/api/docs/` for superusers) or tools like Postman to test the endpoint.
2. Ensure that the data is being saved properly and that the data is also being recorded in the main `Station` model.

## Step 7: Update Tests

1. Create test cases for the new station model, serializer, and endpoint.
2. Place the test cases in the `/tests/` folder (which is outside of the app folders) following the project convention.
3. Run tests using Django’s test framework to ensure everything works as expected:
   ```sh
   python manage.py test
   ```

## Step 8: Smile

- **Congrats!** You just added a station.

---

## Summary
- **Create a new app**: Start with a new Django app for each station.
- **Define model**: Create a model that matches the station's data structure.
- **Serializer**: Inherit from `BaseWeatherDataSerializer` and implement the required methods.
- **Factory**: Update the `WeatherSerializerFactory` with the new station model and serializer.
- **Endpoint**: Define a new `CreateAPIView` endpoint to accept new data for the station.
- **Testing**: Update and create test cases for the new station type.

By following these steps, the project maintains consistency across different weather stations while providing the flexibility to add new ones seamlessly.


---

<div style="display: flex">
  <a href="../README.md">
    <svg width="20" height="20" fill="blue" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Capa_1" width="800px" height="800px" viewBox="0 0 495.398 495.398" xml:space="preserve">
    <g>
        <g>
            <g>
                <path d="M487.083,225.514l-75.08-75.08V63.704c0-15.682-12.708-28.391-28.413-28.391c-15.669,0-28.377,12.709-28.377,28.391     v29.941L299.31,37.74c-27.639-27.624-75.694-27.575-103.27,0.05L8.312,225.514c-11.082,11.104-11.082,29.071,0,40.158     c11.087,11.101,29.089,11.101,40.172,0l187.71-187.729c6.115-6.083,16.893-6.083,22.976-0.018l187.742,187.747     c5.567,5.551,12.825,8.312,20.081,8.312c7.271,0,14.541-2.764,20.091-8.312C498.17,254.586,498.17,236.619,487.083,225.514z"/>
                <path d="M257.561,131.836c-5.454-5.451-14.285-5.451-19.723,0L72.712,296.913c-2.607,2.606-4.085,6.164-4.085,9.877v120.401     c0,28.253,22.908,51.16,51.16,51.16h81.754v-126.61h92.299v126.61h81.755c28.251,0,51.159-22.907,51.159-51.159V306.79     c0-3.713-1.465-7.271-4.085-9.877L257.561,131.836z"/>
            </g>
        </g>
    </g>
    </svg>
  </a>
 <a style="margin-left: 10px" href="../README.md">Home</a>
</div>


---
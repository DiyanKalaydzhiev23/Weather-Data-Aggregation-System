# Mixins for Weather Data Handling

## Overview

This document explains the usage and purpose of mixins in our weather data application. Mixins are used to add reusable 
functionality to the views, specifically focusing on creating related records in the `Station` model when new weather data is added.

### CreateStationMixin

The `CreateStationMixin` is designed to handle the automatic creation of a `Station` entry when a new weather station data record is created. It ensures that every piece of weather data added to the system has a corresponding entry in the central `Station` model, which allows for easy management and querying of different station types.

### Key Features of `CreateStationMixin`

#### 1. Automatic Creation of Station Entries
The mixin intercepts the `perform_create` method, allowing it to create a related `Station` record whenever a new weather data instance is saved.

- **Station Type**: The `station_type` is optionally specified in the view to identify which type of station is being created. By default, is extracted from the queryset
- **City and Status**: It extracts fields such as the city and operational status from the newly created instance.

#### Example Usage

Here's how you would use `CreateStationMixin` in a view:

```python
class CreateWeatherDataView(CreateStationMixin, CreateAPIView):
    queryset = BulgarianMeteoProData.objects.all()
    serializer_class = BulgarianMeteoProDataSerializer
```

---

# WeatherSerializerFactory

The `WeatherSerializerFactory` is designed to dynamically provide the appropriate serializer class for different types of weather station data. 
It ensures flexibility when adding new weather stations, minimizing changes to the main data retrieval or aggregation logic.

## Purpose
The `WeatherSerializerFactory` allows the system to dynamically determine the correct serializer for different types of weather 
stations by looking at the model type of the instance provided.

## Implementation Details

- **SERIALIZER_MAPPING**: The factory maintains a `SERIALIZER_MAPPING` dictionary that maps model names to their corresponding serializer classes.
This mapping ensures that each weather station type has a specific serializer that handles its data appropriately.

```python
SERIALIZER_MAPPING = {
    BulgarianMeteoProData._meta.model_name.lower(): BulgarianMeteoProDataSerializer,
    WeatherMasterX._meta.model_name.lower(): WeatherMasterXSerializer,
}
```

The `SERIALIZER_MAPPING` dictionary uses the model name in lowercase as the key and the corresponding serializer class as the value. This ensures that the factory can handle different types of stations with minimal manual effort.

## Key Method

### `get_serializer(station_instance)`
This method is the core function that returns the appropriate serializer class for a given model instance.

- **Parameters**: 
  - `station_instance` (the weather station model instance)
  
- **Returns**: 
  - The serializer class that matches the instance type.
  
- **Raises**: 
  - `ValueError` if no appropriate serializer can be found for the given instance.

Example of the method:

```python
class WeatherSerializerFactory:
    @staticmethod
    def get_serializer(station_instance):
        model_name = station_instance._meta.model_name.lower()
        serializer_class = SERIALIZER_MAPPING.get(model_name)

        if not serializer_class:
            raise ValueError(f"Serializer for station type '{model_name}' not found")

        return serializer_class
```

## Usage Example
Here is an example of how the `WeatherSerializerFactory` is used to get the appropriate serializer for a given weather station instance:

```python
from weather_aggregator.serializers_mapping import WeatherSerializerFactory
from .models import Station

def get_aggregated_weather_data(city_name):
    stations = Station.objects.filter(city__iexact=city_name)

    aggregated_data = []

    for station in stations:
        station_model = station.content_type.model_class()
        station_instance = station_model.objects.get(id=station.object_id)

        # Get the appropriate serializer using the factory
        try:
            serializer_class = WeatherSerializerFactory.get_serializer(station_instance)
        except ValueError:
            continue

        serializer = serializer_class(station_instance)
        aggregated_data.append(serializer.data)

    return aggregated_data
```

---

#### Next Page: [Project Setup](./project_setup.md)

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

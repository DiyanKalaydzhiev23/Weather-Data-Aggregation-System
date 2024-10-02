# Weather Data Aggregation System - Serializers Documentation

## Overview

The serializers in this project are responsible for transforming weather data into consistent formats that can be easily consumed by the API, 
regardless of the data source. The use of an abstract base serializer (`BaseWeatherDataSerializer`) ensures that all derived serializers for different weather stations share a common structure, while allowing flexibility for each station's specific needs.

The main components covered are:

- **`DefaultWeatherFields`**: A `TypedDict` to define the default schema for weather data fields.
- **`BaseWeatherDataSerializer`**: An abstract base class that standardizes the weather data format.
- **Custom Serialization Logic**: Handling raw and normalized data through methods like `to_representation`.

---

## Default Weather Fields - `DefaultWeatherFields`

### **`DefaultWeatherFields`**

`DefaultWeatherFields` is a `TypedDict` that defines the standard fields expected in all weather data. 
These fields represent the default structure for any weather data and are used in the `BaseWeatherDataSerializer` to ensure consistency across different station types.

| Field                | Type               | Description                                        |
| -------------------- | ------------------ | -------------------------------------------------- |
| `station_id`         | `Optional[str]`    | Unique identifier for the weather station.         |
| `city`               | `Optional[str]`    | Name of the city where the station is located.     |
| `latitude`           | `Optional[float]`  | Latitude of the station's location.                |
| `longitude`          | `Optional[float]`  | Longitude of the station's location.               |
| `temperature_celsius`| `Optional[Decimal]`| Temperature in degrees Celsius.                    |
| `humidity_percent`   | `Optional[Decimal]`| Humidity as a percentage.                          |
| `wind_speed_kph`     | `Optional[Decimal]`| Wind speed in kilometers per hour.                 |
| `pressure_hpa`       | `Optional[float]`  | Atmospheric pressure in hectopascals.              |
| `uv_index`           | `Optional[int]`    | UV index at the time of recording.                 |
| `timestamp`          | `Optional[datetime]` | The date and time when the data was recorded.     |
| `is_active`          | `Optional[bool]`   | Whether the station is currently operational.      |

### **Usage Example**:

```python
# Example of default weather fields
DEFAULT_WEATHER_FIELDS: DefaultWeatherFields = {
    'station_id': None,
    'city': None,
    'latitude': None,
    'longitude': None,
    'temperature_celsius': None,
    'humidity_percent': None,
    'wind_speed_kph': None,
    'pressure_hpa': None,
    'uv_index': None,
    'timestamp': None,
    'is_active': None,
}

```
---

# Abstract Base Serializer - BaseWeatherDataSerializer

## BaseWeatherDataSerializer

`BaseWeatherDataSerializer` is an abstract base class that all weather station serializers inherit from. 
It provides a standardized structure for weather data and handles both raw and normalized representations.

- **Metaclass**: Uses `ABCSerializerMeta` to resolve conflicts between Python's `ABCMeta` and DRF's `SerializerMetaclass`.
- **Standardization**: Ensures all derived serializers return a consistent set of weather data fields.
- **Extensibility**: Allows new weather station serializers to easily be added with custom logic while maintaining a consistent API structure.

---

## Attributes and Methods

### Metaclass: `ABCSerializerMeta`

The `ABCSerializerMeta` combines `ABCMeta` and `serializers.SerializerMetaclass` to handle potential metaclass conflicts.

### `create(self, validated_data)`

- **Purpose**: Overrides the default `create` method to add raw data to the validated data before saving.
- **Parameters**:
  - `validated_data`: Dictionary of validated data.
- **Functionality**:
  - Adds `raw_data` to `validated_data`, storing the original input received by the API.
- **Example**:

```python
def create(self, validated_data):
    validated_data['raw_data'] = self.initial_data
    return super().create(validated_data)
```

### `to_representation(self, instance)`

**Purpose**: Defines how the data should be serialized when responding to a request.

**Parameters**:
- `instance`: The model instance to be serialized.

**Functionality**:
- Checks if the data should be returned in its raw format based on the context (`return_raw_data`).
- If raw data is requested, returns the `raw_data` from the model instance.
- If normalized data is requested, calls `get_station_data(instance)` to retrieve the station-specific data, merged with `DEFAULT_WEATHER_FIELDS`.

**Example**:

```python
def to_representation(self, instance):
    return_raw = self.context.get('return_raw_data', False)

    if return_raw:
        return instance.raw_data
    else:
        station_data = self.get_station_data(instance)
        return {**DEFAULT_WEATHER_FIELDS, **station_data}
```

### `get_station_data(self, instance)`

**Purpose**: Abstract method that must be implemented by all child serializers to extract station-specific data from the model instance.

**Parameters**:

- `instance`: The model instance from which to extract data.

**Functionality**:

- Each subclass must provide its own implementation for extracting station-specific fields while matching the signature of the method.

# Usage Example

- You can look at the `BulgarianMeteoProSerilizer`

---

#### Next Page: [Managers](./managers.md)

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

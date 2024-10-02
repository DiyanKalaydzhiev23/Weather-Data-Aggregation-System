# Weather Data Aggregation System - Models Documentation

## Overview

The Weather Data Aggregation System consists of several models that represent different types of weather stations and their corresponding weather data. These models are designed to handle data from different weather stations and aggregate them in a consistent way, allowing flexibility to add new station types without making extensive changes to the core logic.

The main components are:

- **Station Model**: A generic model to represent all weather stations.
- **Individual Station Models**: Specific models for different types of weather stations like `BulgarianMeteoProData` and `WeatherMasterX`.
- **Custom Fields and Generic Relationships**: Use of generic foreign keys to maintain flexibility.

---

## Station Model

### **Station**

The `Station` model represents a generic weather station. This model acts as an abstraction that links to specific station data using Django’s ContentType framework.

| Field           | Type              | Description                                               |
| --------------- | ----------------- | --------------------------------------------------------- |
| `station_type`  | `CharField`       | Type of station (e.g., "BulgarianMeteoPro", "WeatherMasterX"). |
| `city`          | `CharField`       | Name of the city where the station is located.            |
| `content_type`  | `ForeignKey`      | Links to the ContentType of the specific station model.   |
| `object_id`     | `PositiveIntegerField` | ID of the linked object instance in the specific station model. |
| `station_data`  | `GenericForeignKey` | Generic relation to the specific station data instance.    |
| `is_active`     | `BooleanField`    | Whether the station is currently active. Default is `True`. |

### **Meta Options**
- **Indexes**: 
  - `content_type` and `object_id` to improve the efficiency of querying the related station data.
- **String Representation (`__str__`)**:
  - Returns a formatted string indicating the `station_type` and `city` for readability.

### **Usage Example**:
```python
# Example of creating a Station instance
content_type = ContentType.objects.get_for_model(BulgarianMeteoProData)
station = Station.objects.create(
    station_type='BulgarianMeteoPro',
    city='Sofia',
    content_type=content_type,
    object_id=1,
    is_active=True
)
```

```python
# Assume you want to get the weather data for a specific station
station = Station.objects.get(station_type='bulgarianmeteopro', city='Sofia')

# Retrieve the specific model instance related to this station
content_type = station.content_type
model_class = content_type.model_class()  # Get the associated model class (in this case, BulgarianMeteoProData)
instance = model_class.objects.get(id=station.object_id)

# Print the weather data (can also access any field of the instance)
print(f"Weather Data for Station ID {instance.station_id}:")
print(f"Temperature: {instance.temperature_celsius}°C")
print(f"Humidity: {instance.humidity_percent}%")
print(f"Wind Speed: {instance.wind_speed_kph} kph")

```

---

#### Next Page: [Serializers](./serializers.md)

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
# Custom Manager Documentation

## Overview

This documentation explains the functionality of the custom manager designed for the weather station system.
The focus is on the custom methods, especially the `get_aggregated_weather_data` logic, which plays a crucial role in aggregating data across different station types.

---

### Custom Weather Station Manager

The custom manager provides an abstraction to handle the complex operations involving multiple types of weather stations. By using Django's model manager capabilities, it allows more organized querying and aggregation of data across different weather stations, ensuring better code reuse and maintainability.

#### Key Methods

#### `get_aggregated_weather_data(city_name, return_raw_data=False)`

**Purpose**:  
Aggregates weather data for a specified city, regardless of the station type. The method can return either the normalized weather data or the raw data based on the input parameters.

**Parameters**:
- `city_name` (str): The name of the city for which to aggregate weather data.
- `return_raw_data` (bool, optional): Determines whether to return raw or normalized weather data. Defaults to `False`.

**Workflow**:
1. **Filter Stations**:
   The method starts by filtering the `Station` model to find all stations that match the provided `city_name`. 
   
```python
   stations = Station.objects.filter(city__iexact=city_name).select_related('content_type')
```

2. **Map Content Types to IDs**: 
    The manager then iterates over the filtered stations to group them by content type. 
    This step ensures that queries are minimized by collecting IDs for each station type.
    - `content_type_to_ids is` used to group station model classes and their respective IDs.
    - `content_type_to_model_class` is a cache to store the model class corresponding to each content type.
```python
    content_type_to_ids = {}
    content_type_to_model_class = {}
    
    for station in stations:
        content_type = station.content_type
        model_class = content_type.model_class()
        content_type_to_model_class[content_type.id] = model_class
    
        if model_class not in content_type_to_ids:
            content_type_to_ids[model_class] = []
    
        content_type_to_ids[model_class].append(station.object_id)
```

3. **Fetch Instances in Bulk**:
    Instead of querying each station's data individually, which would result in multiple database hits (O(n) queries), the method groups the station IDs by their model class and performs bulk queries.
    - The instances are then stored in `model_instances` for easy retrieval during data aggregation.

```python
model_instances = {}
for model_class, ids in content_type_to_ids.items():
    instances = model_class.objects.filter(id__in=ids)
    model_instances[model_class] = {instance.id: instance for instance in instances}
```

4. **Aggregate Data**: 
   For each station, the method retrieves the corresponding instance from model_instances and attempts to serialize the data using the appropriate serializer.
   - The `WeatherSerializerFactory` is used to determine the correct serializer for each station instance.
   - The serialized data is appended to the `aggregated_data` list.

```python
aggregated_data = []
for station in stations:
    station_model_class = content_type_to_model_class[station.content_type.id]
    station_instance = model_instances.get(station_model_class, {}).get(station.object_id)

    if not station_instance:
        continue

    try:
        serializer_class = WeatherSerializerFactory.get_serializer(station_instance)
    except ValueError:
        continue

    serializer = serializer_class(station_instance, context={'return_raw_data': return_raw_data})
    aggregated_data.append(serializer.data)
```

5. **Return Response**: 
   Finally, if no aggregated data is available, a `404 Not Found` response is returned. 
   Otherwise, the aggregated weather data is returned.

```python
if not aggregated_data:
    return Response({"message": "No data available for the specified city."}, status=status.HTTP_404_NOT_FOUND)

return Response(aggregated_data, status=status.HTTP_200_OK)
```

#### Next Page: [Mixins](./mixins.md)

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

# Documentation

### Project Overview

The goal of this project was to create an API to manage weather data from multiple types of weather stations, ensuring that data aggregation is consistent and accessible. 
The solution is designed to handle data from different types of stations, with each station potentially having a different structure and different data types, while allowing for easy integration of new station types.

---

## Contents

### Setup Tutorials

- [Project Setup](docs/project_setup.md)
- [Add Station](docs/add_station_tutorial.md)

---

### Key parts
- [Models](docs/models.md)
- [Serializers](docs/serializers.md)
- [Managers](docs/managers.md)
- [Mixins](docs/mixins.md)

---

### Key Components

1. Weather Data Models
   - We have individual models for each station type (e.g., `BulgarianMeteoProData`, `WeatherMasterX`).
   - Each model represents the specific fields provided by that station in both a normalized format and their raw format (in order to keep data as-is).
   - The `Station` model acts as a generic representation of the **various types of stations**, utilizing a **Generic Foreign Key** (via Django’s ContentType framework) to dynamically link to specific station models.
     - This allows for flexibility when a city changes its weather station and when we want to **retrieve aggregated data** for a city, regardless of the station.
    
2. Custom Manager for Aggregated Data
   - A **custom manager** was used in the Station model to **handle the complex aggregation logic** for querying and combining weather data from **different station types**.
  
3. Custom Serializers for Data Normalization
   - Since each station type may have a unique structure, custom serializers were created for each station model.
   - A base serializer (`BaseWeatherDataSerializer`) was designed to ensure consistency and to enforce normalization across all data being returned via the method `get_static_data`.
     The `get_station()` method was used to handle this, so regardless of the station type, the endpoint returns the data in a **consistent** structure.

4. CreateStationMixin for Automatic Station Creation
   - We added a mixin (`CreateStationMixin`) to ensure that every time new weather data is created for a specific station type, a corresponding record is created in the `Station` model.
   - This ensures a unified way of managing station data and guarantees that every weather data record has a corresponding station entry.

5. Flexible Data Handling and API Endpoint
   - The main aggregation endpoint (`get_aggregated_weather_data`) was designed to retrieve data for a specific city, regardless of the station type.
   - Users can request either raw or normalized data using a query parameter (`?raw=true`). This adds flexibility, allowing clients to decide how they want to consume the data.
  
6. Swagger Integration for Documentation
   - **Swagger/OpenAPI** integration using `drf-spectacular` was used to document the API.

---

### Justification of Design Decisions

##### Modular Architecture
- Each weather station is implemented as a separate Django app. This approach ensures separation of concerns, easier testing, and future maintainability.

##### Inheritance-Based Serializers
- A base serializer (`BaseWeatherDataSerializer`) is used to enforce consistency across all weather station serializers. It provides a unified API structure and ensures that each serializer follows a standard representation.

##### Factory Pattern for Serializer Resolution
- The `WeatherSerializerFactory` is used to dynamically determine the appropriate serializer for each station. This reduces the need for if-else statements and keeps the code more extensible as new stations are added.

##### Use of Generic Relationships
- The `Station` model utilizes Django’s ContentType framework to store data across multiple weather station types. This provides a flexible way to link the generic station model to multiple station-specific models.

##### Data Normalization vs. Raw Data Representation
- The decision to provide both raw and normalized data responses ensures that the API is flexible for different client needs, supporting both standard analysis and debugging use-cases.


---

from django.contrib.auth.decorators import user_passes_test
from drf_spectacular.utils import OpenApiExample


example_bad_request = OpenApiExample(
    name="Validation Error Example",
    value={
        "station_id": ["This field is required."],
        "temperature_celsius": ["Ensure this value is greater than or equal to 0."]
    },
    description="Example of a validation error response"
)


def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)


def fahrenheit_to_celsius(fahrenheit: float):
    return (fahrenheit - 32) / 1.8
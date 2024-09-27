from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from weather_aggregator.utils import superuser_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', superuser_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    path('bulgarian_meteo_pro/', include('bulgarian_meteo_pro.urls')),
]

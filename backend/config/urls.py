from django.contrib import admin
from django.urls import path, include
from apps.stations.views import AdminOverviewView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/weather/', include('apps.prediction.urls')),
    path('api/admin/dashboard-stats/', AdminOverviewView.as_view(), name='admin-dashboard-stats'),

    # ! Swagger/OpenAPI URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Autres URLs
]
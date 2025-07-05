from django.contrib import admin
from django.urls import path, include
from apps.stations.views import AdminOverviewView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/weather/', include('apps.prediction.urls')),
    path('api/admin/dashboard-stats/', AdminOverviewView.as_view(), name='admin-dashboard-stats'),

    # Autres URLs
]
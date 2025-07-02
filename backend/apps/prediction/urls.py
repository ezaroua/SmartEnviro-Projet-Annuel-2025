from django.urls import path
from .views import WeatherAPIView, WeatherDailyForIAModelAPIView

urlpatterns = [
    path('', WeatherAPIView.as_view(), name='weather-api'),
    path('weather-daily/', WeatherDailyForIAModelAPIView.as_view(), name='weather-daily'),
]

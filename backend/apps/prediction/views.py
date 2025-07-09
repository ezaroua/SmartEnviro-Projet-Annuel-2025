import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.openapi import OpenApiTypes

@extend_schema(
    summary="Get weather data",
    description="Retrieve general weather data (current, hourly, daily precipitation) for dashboard indicators and 7-day chart",
    tags=["Weather"],
    parameters=[
        OpenApiParameter(
            name="lat",
            description="Latitude coordinate",
            type=OpenApiTypes.FLOAT,
            location=OpenApiParameter.QUERY,
            required=True
        ),
        OpenApiParameter(
            name="lon",
            description="Longitude coordinate",
            type=OpenApiTypes.FLOAT,
            location=OpenApiParameter.QUERY,
            required=True
        )
    ]
)
class WeatherAPIView(APIView):
    """
    Vue pour récupérer les données météo générales (actuelle, horaire, précipitations du jour).
    Utilisée pour les indicateurs et le graphique des 7 jours.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")

        if not lat or not lon:
            return Response({"error": True, "reason": "Latitude et longitude requises"}, status=400)

        # URL pour les données météo générales (current_weather, hourly, daily precipitation_sum)
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"  # <-- Assurez-vous que lat et lon sont ici
            f"&current_weather=true" 
            f"&hourly=relative_humidity_2m" 
            f"&daily=precipitation_sum" 
            f"&timezone=auto"
            f"&forecast_days=7"
        )

        try:
            print(f"DEBUG Django API (WeatherAPIView): Appel Open-Meteo URL: {url}")
            res = requests.get(url)
            res.raise_for_status() 
            data = res.json()
            print(f"DEBUG Django API (WeatherAPIView): Réponse JSON brute d'Open-Meteo: {data}")
            return Response(data)

        except requests.exceptions.RequestException as e:
            print(f"ERREUR Django API (WeatherAPIView): Échec de la requête Open-Meteo: {e}")
            return Response({"error": True, "reason": f"Erreur de communication avec l'API météo externe: {e}"}, status=500)
        except Exception as e:
            print(f"ERREUR Django API (WeatherAPIView): Erreur inattendue: {str(e)}")
            return Response({"error": True, "reason": str(e)}, status=500)


@extend_schema(
    summary="Get daily weather data for AI model",
    description="Retrieve comprehensive daily weather data specifically for AI model predictions",
    tags=["Weather"],
    parameters=[
        OpenApiParameter(
            name="lat",
            description="Latitude coordinate",
            type=OpenApiTypes.FLOAT,
            location=OpenApiParameter.QUERY,
            required=True
        ),
        OpenApiParameter(
            name="lon",
            description="Longitude coordinate",
            type=OpenApiTypes.FLOAT,
            location=OpenApiParameter.QUERY,
            required=True
        )
    ]
)
class WeatherDailyForIAModelAPIView(APIView):
    """
    Vue pour récupérer les données météo journalières complètes spécifiquement pour le modèle IA.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")

        if not lat or not lon:
            return Response({"error": True, "reason": "Latitude et longitude requises"}, status=400)

        # URL pour les données météo journalières complètes pour le modèle IA
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"  # <-- Assurez-vous que lat et lon sont ici
            f"&daily="
            f"weathercode,"
            f"temperature_2m_max,temperature_2m_min,"
            f"apparent_temperature_max,apparent_temperature_min,"
            f"sunrise,sunset,daylight_duration,sunshine_duration,"
            f"uv_index_max,uv_index_clear_sky_max,"
            f"rain_sum,showers_sum,snowfall_sum,precipitation_sum,"
            f"precipitation_hours,precipitation_probability_max,"
            f"windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,"
            f"shortwave_radiation_sum,et0_fao_evapotranspiration" 
            f"&timezone=auto"
            f"&forecast_days=7"
        )

        try:
            print(f"DEBUG Django API (WeatherDailyForIAModelAPIView): Appel Open-Meteo URL: {url}")
            res = requests.get(url)
            res.raise_for_status() 
            data = res.json()
            print(f"DEBUG Django API (WeatherDailyForIAModelAPIView): Réponse JSON brute d'Open-Meteo: {data}")
            return Response(data)

        except requests.exceptions.RequestException as e:
            print(f"ERREUR Django API (WeatherDailyForIAModelAPIView): Échec de la requête Open-Meteo: {e}")
            return Response({"error": True, "reason": f"Erreur de communication avec l'API météo externe: {e}"}, status=500)
        except Exception as e:
            print(f"ERREUR Django API (WeatherDailyForIAModelAPIView): Erreur inattendue: {str(e)}")
            return Response({"error": True, "reason": str(e)}, status=500)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import requests

class WeatherAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Récupération des coordonnées depuis les paramètres
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")

        if not lat or not lon:
            return Response({"error": True, "reason": "Latitude et longitude requises"}, status=400)

        # URL de l'API Open-Meteo avec toutes les données nécessaires
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=relative_humidity_2m"
            f"&daily=precipitation_sum"
            f"&timezone=auto"
            f"&forecast_days=7"
        )

        try:
            print(f"Appel API pour lat={lat}, lon={lon}")
            print(f"URL: {url}")
            
            res = requests.get(url)
            data = res.json()
            
            print(f"Réponse API reçue: {len(str(data))} caractères")
            print(f"Météo actuelle: {data.get('current_weather', {})}")
            print(f"Précipitations quotidiennes: {data.get('daily', {}).get('precipitation_sum', [])}")
            
            return Response(data)

        except Exception as e:
            print(f"Erreur API: {str(e)}")
            return Response({"error": True, "reason": str(e)}, status=500)
        

        # Endpoint utilisé pour le MODELE IA
class WeatherDailyForIAModelAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")

        if not lat or not lon:
            return Response({"error": True, "reason": "Latitude et longitude requises"}, status=400)

        # URL avec TOUS les paramètres de Daily Weather Variables
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
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
            print(f"Appel MODELE IA lat={lat}, lon={lon}")
            print(f"URL: {url}")

            res = requests.get(url)
            data = res.json()

            print(f"Réponse API reçue pour IA: {len(str(data))} caractères")
            return Response(data)

        except Exception as e:
            print(f"Erreur API: {str(e)}")
            return Response({"error": True, "reason": str(e)}, status=500)
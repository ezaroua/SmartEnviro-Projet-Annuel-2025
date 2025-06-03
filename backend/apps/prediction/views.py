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
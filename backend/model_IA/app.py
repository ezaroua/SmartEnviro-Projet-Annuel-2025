import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, request, jsonify
import joblib
import pandas as pd
from backend.model_IA.preprocessing import preprocess_data

app = Flask(__name__)

# Chemin relatif pour accéder au dossier models depuis le dossier backend
models_dir = os.path.join("..","..","models")

# Charger le modèle et le scaler
model = joblib.load(os.path.join(models_dir, 'best_xgboost_weather_model.joblib'))
scaler = joblib.load(os.path.join(models_dir, 'weather_scaler.joblib'))

# Définis les colonnes de caractéristiques attendues par ton modèle
feature_columns = [
    "weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max",
    "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration",
    "uv_index_max", "uv_index_clear_sky_max", "rain_sum", "showers_sum", "snowfall_sum",
    "precipitation_sum", "precipitation_hours", "wind_speed_10m_max", "wind_gusts_10m_max",
    "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"
]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données de la requête
        data = request.json

        # Prétraiter les données
        df_processed = preprocess_data(data, scaler, feature_columns)

        # Faire une prédiction
        predictions = model.predict(df_processed)

        # Retourner les prédictions
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

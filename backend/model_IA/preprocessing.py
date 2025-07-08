import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime 

# --- Fonctions de prétraitement ---

def create_simple_features_for_prediction(df_input):
    """
    Crée les features essentielles pour une prédiction à partir des données brutes de l'API.
    Convertit les timestamps en valeurs numériques (secondes depuis minuit)
    et ajoute le jour de l'année, jour de la semaine, mois.
    """
    print(f"DEBUG PREPROCESSING: create_simple_features_for_prediction - df_input shape: {df_input.shape}, columns: {df_input.columns.tolist()}")
    df_processed = df_input.copy()

    # Convertir 'time' en datetime pour extraire des features
    if 'time' in df_processed.columns:
        df_processed['time'] = pd.to_datetime(df_processed['time'])
        df_processed['day_of_year'] = df_processed['time'].dt.dayofyear
        df_processed['day_of_week'] = df_processed['time'].dt.dayofweek
        df_processed['month'] = df_processed['time'].dt.month
        print(f"DEBUG PREPROCESSING: Ajouté day_of_year, day_of_week, month.")
    
    # Convertir 'sunrise' et 'sunset' en secondes depuis minuit
    if 'sunrise' in df_processed.columns: 
        df_processed['sunrise_seconds'] = df_processed['sunrise'].apply(
            lambda x: datetime.fromisoformat(x.replace('Z', '+00:00')).hour * 3600 + 
                      datetime.fromisoformat(x.replace('Z', '+00:00')).minute * 60
        )
        print(f"DEBUG PREPROCESSING: Converti 'sunrise' en 'sunrise_seconds'.")

    if 'sunset' in df_processed.columns: 
        df_processed['sunset_seconds'] = df_processed['sunset'].apply(
            lambda x: datetime.fromisoformat(x.replace('Z', '+00:00')).hour * 3600 + 
                      datetime.fromisoformat(x.replace('Z', '+00:00')).minute * 60
        )
        print(f"DEBUG PREPROCESSING: Converti 'sunset' en 'sunset_seconds'.")

    return df_processed

def preprocess_data_for_prediction(data_dict, scaler, expected_feature_columns):
    print(f"DEBUG PREPROCESSING: --- Début preprocess_data_for_prediction ---")
    print(f"DEBUG PREPROCESSING: data_dict keys: {data_dict.keys()}")
    
    df = pd.DataFrame([data_dict])
    print(f"DEBUG PREPROCESSING: Après pd.DataFrame([data_dict]) - df shape: {df.shape}, colonnes: {df.columns.tolist()}")

    # --- ÉTAPE CLÉ : RENOMMER LES COLONNES POUR CORRESPONDRE AUX FEATURES ATTENDUES ---
    # Créer un dictionnaire de mapping des noms de colonnes de l'API vers les noms de features du modèle
    # Ceci est basé sur les noms dans votre CSV d'entraînement et les noms de l'API Open-Meteo
    column_mapping = {
        'weathercode': 'weather_code (wmo code)',
        'temperature_2m_max': 'temperature_2m_max (°C)',
        'temperature_2m_min': 'temperature_2m_min (°C)',
        'apparent_temperature_max': 'apparent_temperature_max (°C)',
        'apparent_temperature_min': 'apparent_temperature_min (°C)',
        'daylight_duration': 'daylight_duration (s)',
        'sunshine_duration': 'sunshine_duration (s)',
        'uv_index_max': 'uv_index_max ()',
        'uv_index_clear_sky_max': 'uv_index_clear_sky_max ()',
        'rain_sum': 'rain_sum (mm)',
        'showers_sum': 'showers_sum (mm)',
        'snowfall_sum': 'snowfall_sum (cm)',
        'precipitation_sum': 'precipitation_sum (mm)',
        'precipitation_hours': 'precipitation_hours (h)',
        'precipitation_probability_max': 'precipitation_probability_max (%)',
        'windspeed_10m_max': 'wind_speed_10m_max (km/h)',
        'windgusts_10m_max': 'wind_gusts_10m_max (km/h)',
        'winddirection_10m_dominant': 'wind_direction_10m_dominant (°)',
        'shortwave_radiation_sum': 'shortwave_radiation_sum (MJ/m²)',
        'et0_fao_evapotranspiration': 'et0_fao_evapotranspiration (mm)',
        # Les features de date/heure générées n'ont pas besoin de mapping ici
        # car elles sont créées avec les bons noms dans create_simple_features_for_prediction
        'day_of_year': 'day_of_year',
        'day_of_week': 'day_of_week',
        'month': 'month',
        'sunrise_seconds': 'sunrise_seconds',
        'sunset_seconds': 'sunset_seconds',
        # Si vous avez inclus latitude/longitude dans le modèle, ajoutez-les ici aussi
        'latitude': 'latitude', # Si cette colonne est dans expected_feature_columns
        'longitude': 'longitude' # Si cette colonne est dans expected_feature_columns
    }

    # Appliquer le renommage
    df.rename(columns=column_mapping, inplace=True)
    print(f"DEBUG PREPROCESSING: df après renommage: {df.shape}, colonnes: {df.columns.tolist()}")


    # Création des features de date/heure et transformation des colonnes
    df = create_simple_features_for_prediction(df)
    print(f"DEBUG PREPROCESSING: Après create_simple_features_for_prediction - df shape: {df.shape}, colonnes: {df.columns.tolist()}")

    # Supprimer les colonnes originales de date/heure qui ont été transformées
    # Note: Ces noms sont les noms originaux de l'API, pas les noms avec unités
    cols_to_drop_after_feature_creation = ['time', 'sunrise', 'sunset'] 
    df = df.drop(columns=[col for col in cols_to_drop_after_feature_creation if col in df.columns])
    print(f"DEBUG PREPROCESSING: Supprimé les colonnes originales de date/heure: {cols_to_drop_after_feature_creation}. df shape: {df.shape}, colonnes: {df.columns.tolist()}")


    # Liste des colonnes de précipitation à supprimer (basé sur l'API Django)
    # Assurez-vous que ces noms correspondent aux noms RENOMMÉS si vous les avez renommés
    precip_cols_to_remove = [
        'rain_sum (mm)', 'showers_sum (mm)', 'snowfall_sum (cm)',
        'precipitation_sum (mm)', 'precipitation_hours (h)',
        'precipitation_probability_max (%)' 
    ]
    
    cols_before_precip_drop = df.columns.tolist()
    df = df.drop(columns=[col for col in precip_cols_to_remove if col in df.columns])
    print(f"DEBUG PREPROCESSING: Après suppression des colonnes de précipitation - df shape: {df.shape}, colonnes: {df.columns.tolist()}")
    if set(cols_before_precip_drop) == set(df.columns.tolist()):
        print("DEBUG PREPROCESSING: Aucune colonne de précipitation n'a été trouvée ou supprimée.")

    # Gestion des valeurs manquantes (remplir avec 0)
    df = df.fillna(0)
    print(f"DEBUG PREPROCESSING: Après df.fillna(0) - df shape: {df.shape}")


    # Encodage One-Hot pour les colonnes catégorielles (uniquement 'weather_code (wmo code)' si c'est une catégorie)
    categorical_cols = []
    # Le nom de la colonne 'weathercode' est maintenant 'weather_code (wmo code)' après renommage
    if 'weather_code (wmo code)' in df.columns and pd.api.types.is_object_dtype(df['weather_code (wmo code)']):
        categorical_cols.append('weather_code (wmo code)')

    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    print(f"DEBUG PREPROCESSING: Après pd.get_dummies - df_encoded shape: {df_encoded.shape}, colonnes: {df_encoded.columns.tolist()}")
    
    # Align columns with expected_feature_columns and fill missing with 0
    final_df = df_encoded.reindex(columns=expected_feature_columns, fill_value=0)
    
    print(f"DEBUG PREPROCESSING: final_df (avant scaling):")
    print(final_df) 
    print(f"DEBUG PREPROCESSING: final_df columns: {final_df.columns.tolist()}")
    print(f"DEBUG PREPROCESSING: final_df shape: {final_df.shape}")

    # Assurez-vous que toutes les colonnes sont numériques avant le scaling
    for col in final_df.columns:
        if final_df[col].dtype == bool: 
            final_df[col] = final_df[col].astype(int)
        elif not pd.api.types.is_numeric_dtype(final_df[col]):
            print(f"DEBUG PREPROCESSING: Conversion de la colonne non numérique '{col}' en numérique (remplie de 0 si échec).")
            final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0) 

    final_df = final_df.fillna(0) 

    df_scaled = scaler.transform(final_df)
    print(f"DEBUG PREPROCESSING: df_scaled après scaler.transform: {df_scaled.shape}")
    print(f"DEBUG PREPROCESSING: --- Fin preprocess_data_for_prediction ---")

    return df_scaled

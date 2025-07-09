import pandas as pd
import numpy as np
import joblib
import pickle
from flask import Flask, request, jsonify

# 1. Enregistrer les modèles entraînés
def save_models(rf_model, xgb_model, scaler, filepath_prefix="models/"):
    """
    Enregistre les modèles et le scaler pour une utilisation ultérieure.
    """
    # Créer le dossier si nécessaire
    import os
    os.makedirs(filepath_prefix, exist_ok=True)
    
    # Enregistrer les modèles avec joblib (plus efficace pour les modèles scikit-learn)
    joblib.dump(rf_model, f"{filepath_prefix}random_forest_model.joblib")
    joblib.dump(xgb_model, f"{filepath_prefix}xgboost_model.joblib")
    joblib.dump(scaler, f"{filepath_prefix}scaler.joblib")
    
    print(f"Modèles et scaler enregistrés dans {filepath_prefix}")

# 2. Charger les modèles enregistrés
def load_models(filepath_prefix="models/"):
    """
    Charge les modèles et le scaler enregistrés.
    """
    rf_model = joblib.load(f"{filepath_prefix}random_forest_model.joblib")
    xgb_model = joblib.load(f"{filepath_prefix}xgboost_model.joblib")
    scaler = joblib.load(f"{filepath_prefix}scaler.joblib")
    
    return rf_model, xgb_model, scaler

# 3. Tester le modèle sur un nouveau jeu de données CSV
def test_on_new_data(filepath, rf_model, xgb_model, scaler):
    """
    Teste les modèles sur un nouveau jeu de données CSV.
    """
    # Charger les nouvelles données
    df = pd.read_csv(filepath)
    
    # Prétraitement (similaire à celui de l'entraînement)
    df_processed = preprocess_for_prediction(df, scaler)
    
    # Faire des prédictions
    rf_predictions = rf_model.predict(df_processed)
    xgb_predictions = xgb_model.predict(df_processed)
    
    # Ajouter les prédictions au DataFrame original
    df['RF_Prediction'] = rf_predictions
    df['XGB_Prediction'] = xgb_predictions
    
    # Convertir les prédictions numériques en étiquettes lisibles
    df['RF_Prediction_Label'] = df['RF_Prediction'].map({0: 'No', 1: 'Yes'})
    df['XGB_Prediction_Label'] = df['XGB_Prediction'].map({0: 'No', 1: 'Yes'})
    
    return df

# 4. Prétraitement pour les nouvelles données (sans la cible)
def preprocess_for_prediction(df, scaler):
    """
    Prétraite de nouvelles données pour la prédiction.
    """
    # Gérer les valeurs manquantes (remplacement par la moyenne ou le mode au lieu de dropna)
    # Pour les colonnes numériques
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mean())
    
    # Pour les colonnes catégorielles
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if col != 'Date' and df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode()[0])
    
    # Supprimer la colonne Date
    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])
    
    # Supprimer la colonne cible si elle existe
    if 'RainTomorrow' in df.columns:
        df = df.drop(columns=['RainTomorrow'])
    
    # Encoder les variables catégorielles
    df_encoded = pd.get_dummies(df, drop_first=True)
    
    # Gérer les nouvelles catégories ou les catégories manquantes
    # (Cela peut nécessiter de stocker les colonnes utilisées lors de l'entraînement)
    
    # Appliquer le scaling
    df_scaled = scaler.transform(df_encoded)
    
    return df_scaled

# 5. Créer une API Flask pour le modèle
def create_flask_app(rf_model, xgb_model, scaler):
    """
    Crée une API Flask pour servir les prédictions du modèle.
    """
    app = Flask(__name__)
    
    @app.route('/predict', methods=['POST'])
    def predict():
        try:
            # Récupérer les données JSON de la requête
            data = request.json
            
            # Convertir en DataFrame
            df = pd.DataFrame(data)
            
            # Prétraiter les données
            df_processed = preprocess_for_prediction(df, scaler)
            
            # Faire des prédictions
            rf_prediction = rf_model.predict(df_processed)
            xgb_prediction = xgb_model.predict(df_processed)
            
            # Calculer la probabilité
            rf_proba = rf_model.predict_proba(df_processed)[:, 1]
            xgb_proba = xgb_model.predict_proba(df_processed)[:, 1]
            
            # Préparer la réponse
            response = {
                'rf_prediction': rf_prediction.tolist(),
                'rf_prediction_label': ['Yes' if p == 1 else 'No' for p in rf_prediction],
                'rf_probability': rf_proba.tolist(),
                'xgb_prediction': xgb_prediction.tolist(),
                'xgb_prediction_label': ['Yes' if p == 1 else 'No' for p in xgb_prediction],
                'xgb_probability': xgb_proba.tolist()
            }
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return app

# Exemple d'utilisation
if __name__ == "__main__":
    # 1. Modifier votre fonction main pour renvoyer également le scaler
    # dans votre script original
    
    # Supposons que vous avez déjà entraîné vos modèles
    from modelprojetannuel import main
    rf_model, xgb_model = main("C:/Users/romai/Documents/Cours ESGI/IABD S2/Spark Streaming/weatherAUS.csv")
    
    # Pour sauvegarder les modèles, vous aurez besoin du scaler
    # Vous pouvez soit modifier votre script original pour renvoyer le scaler,
    # soit recréer le scaler ici
    
    # Exemple de sauvegarde (si vous avez le scaler)
    # save_models(rf_model, xgb_model, scaler)
    
    # Exemple de test sur de nouvelles données
    # new_predictions = test_on_new_data("chemin/vers/nouvelles_donnees.csv", rf_model, xgb_model, scaler)
    
    # Exemple de création d'une API
    # app = create_flask_app(rf_model, xgb_model, scaler)
    # app.run(debug=True, host='0.0.0.0', port=5001)
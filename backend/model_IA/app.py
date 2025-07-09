import sys
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Importe la fonction de prétraitement depuis le module preprocessing local
from preprocessing import preprocess_data_for_prediction

app = Flask(__name__)
CORS(app) # Active CORS pour permettre les requêtes depuis le front-end

# Chemin vers le r  épertoire des modèles
# Pour Docker, les modèles seront dans le dossier models local
models_dir = os.path.join("models")

# Chargement du modèle, du scaler et des noms des features au démarrage de l'application
try:
    model = joblib.load(os.path.join(models_dir, 'simplified_xgboost_weather_model.joblib'))
    scaler = joblib.load(os.path.join(models_dir, 'simplified_weather_scaler.joblib'))
    # Charge la liste des noms de colonnes finales attendues par le modèle
    expected_feature_columns = pd.read_csv(os.path.join(models_dir, 'simplified_weather_features.csv'))['feature'].tolist()
    print("Modèle, scaler et features simplifiés chargés avec succès.")
except FileNotFoundError as e:
    # Gère l'erreur si un fichier n'est pas trouvé
    print(f"Erreur au chargement des ressources : {e}. Assurez-vous que les fichiers sont dans {models_dir}")
    sys.exit(1) # Quitte l'application si les fichiers essentiels sont manquants

@app.route('/predict', methods=['POST'])
def predict():
    """
    Point d'API pour la prédiction de pluie.
    Reçoit les données météo brutes du front-end et retourne une probabilité de pluie.
    """
    try:
        data = request.json # Récupère les données JSON envoyées par le front-end
        
        # DEBUG: Affiche les données brutes reçues
        print(f"DEBUG App.py: Données reçues pour prédiction: {data}")

        # Prétraite les données en utilisant la fonction dédiée
        # C'est ici que le formatage et la transformation des données se produisent
        df_processed = preprocess_data_for_prediction(data, scaler, expected_feature_columns)

        # Effectue la prédiction de probabilité avec le modèle chargé
        # [:, 1] récupère la probabilité de la classe positive (pluie = 1)
        prediction_probability = model.predict_proba(df_processed)[:, 1]

        # Retourne la probabilité sous forme de réponse JSON
        # [0] car prediction_probability est un tableau numpy avec un seul élément
        return jsonify({'prediction_probability': prediction_probability.tolist()[0]})
        
    except Exception as e:
        # Gère toute erreur survenant pendant le processus de prédiction
        import traceback
        traceback.print_exc() # Affiche la trace complète de l'erreur dans la console du serveur
        return jsonify({'error': str(e), 'details': 'Erreur interne du serveur lors de la prédiction'}), 500 # Retourne une erreur 500

if __name__ == '__main__':
    # Lance l'application Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
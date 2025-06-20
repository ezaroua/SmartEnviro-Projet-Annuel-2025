import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import xgboost as xgb

# 1. Chargement des données
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

# 2. Prétraitement des données
def preprocess_data(df):
    # Convertir la variable cible avant tout autre traitement
    y = df['RainTomorrow'].map({'No': 0, 'Yes': 1})  # Target (conversion en 0 et 1)

    # Suppression des valeurs manquantes
    df = df.dropna()

    # Garder l'index des lignes après dropna pour y correspondant
    y = y[df.index]

    # Supprimer la colonne Date et la cible
    df = df.drop(columns=['Date', 'RainTomorrow'])

    # Convertir les variables catégorielles en variables numériques
    df_encoded = pd.get_dummies(df, drop_first=True)

    # Normalisation des données
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_encoded)

    return X_scaled, y

# 3. Séparation des données en train/test
def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

# 4a. Entraînement du modèle RandomForest
def train_rf_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# 4b. Entraînement du modèle XGBoost
def train_xgb_model(X_train, y_train):
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train, y_train)
    return model

# 5. Évaluation du modèle
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("ROC AUC Score:", roc_auc_score(y_test, y_prob))

# 6. Prédiction sur de nouvelles données
def predict(model, new_data):
    probabilities = model.predict_proba(new_data)[:, 1]
    return probabilities

# Utilisation complète
def main(filepath):
    df = load_data(filepath)
    X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    print("Training RandomForest Model...")
    rf_model = train_rf_model(X_train, y_train)
    evaluate_model(rf_model, X_test, y_test)

    print("\nTraining XGBoost Model...")
    xgb_model = train_xgb_model(X_train, y_train)
    evaluate_model(xgb_model, X_test, y_test)

    return rf_model, xgb_model

if __name__ == "__main__":
    rf_model, xgb_model = main("C:/Users/romai/Documents/Cours ESGI/IABD S2/Spark Streaming/weatherAUS.csv")
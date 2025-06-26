import pandas as pd

def preprocess_data(data, scaler, feature_columns):
    # Convertir les données en DataFrame
    df = pd.DataFrame([data])

    # Assure-toi que toutes les colonnes nécessaires sont présentes
    for column in feature_columns:
        if column not in df.columns:
            df[column] = 0  # ou une autre valeur par défaut appropriée

    # Supprimer les colonnes non nécessaires si elles existent
    if 'time' in df.columns:
        df = df.drop(columns=['time'])

    # Gérer les valeurs manquantes
    df = df.dropna()

    # Encodage des variables catégorielles
    df_encoded = pd.get_dummies(df, drop_first=True)

    # Assure-toi que toutes les colonnes attendues par le scaler sont présentes
    missing_cols = set(scaler.get_feature_names_out()) - set(df_encoded.columns)
    for col in missing_cols:
        df_encoded[col] = 0

    # Assure-toi que les colonnes sont dans le bon ordre
    df_encoded = df_encoded[scaler.get_feature_names_out()]

    # Appliquer le scaler
    df_scaled = scaler.transform(df_encoded)

    return df_scaled



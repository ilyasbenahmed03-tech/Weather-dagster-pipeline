import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sqlalchemy import create_engine

def train_and_predict(df_stats):
    """
    Modele IA : Random Forest Regressor.
    Predition de la temperature pour le lendemain.
    """
    #  3 jours pour l'entrainement
    if len(df_stats) < 3:
        return None

    df = df_stats.copy()

    # On utilise la colonne temp_moyenne generee par l'asset precedent
    target_col = 'temp_moyenne' if 'temp_moyenne' in df.columns else 'temp_mean'

    feature_names = ['day_index']
    df['day_index'] = np.arange(len(df))

    # X = caracteristiques, y = cible
    X = df[feature_names]
    y = df[target_col].values

    # Configuration du modele
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Prediction pour le jour suivant
    next_day_df = pd.DataFrame([[len(df)]], columns=feature_names)
    prediction = model.predict(next_day_df)[0]

    # Calcul de la marge d'erreur (MAE)
    y_pred_train = model.predict(X)
    error_margin = mean_absolute_error(y, y_pred_train)

    # Creation du DataFrame de sortie
    df_result = pd.DataFrame({
        'prediction_date': [pd.Timestamp.now().normalize() + pd.Timedelta(days=1)],
        'predicted_temp_mean': [round(float(prediction), 2)],
        'error_margin': [round(float(error_margin), 2)],
        'model_used': ['RandomForestRegressor'],
        'execution_status': ['SUCCESS']
    })

    return df_result


# --- BLOC DE TEST MANUEL ---
if __name__ == "__main__":
    # Donnees de test
    data_test = pd.DataFrame({
        'temp_moyenne': [12.5, 14.0, 13.8, 15.2, 16.5]
    })

    print("--- Lancement du test ML ---")
    resultat = train_and_predict(data_test)
    print(resultat)

    # Test d'ecriture sur le port 5433 (Postgres local)
    try:
        # Note : Dans Docker, l'app utilise db_postgres:5432
        db_password = os.getenv("POSTGRES_PASSWORD", "change_me")
        engine = create_engine(f"postgresql://postgres:{db_password}@127.0.0.1:5433/postgres")
        resultat.to_sql('weather_predictions', engine, if_exists='replace', index=False)
        print("\nSUCCES : Table weather_predictions creee !")
    except Exception as e:
        print(f"\nERREUR DE CONNEXION : {e}")
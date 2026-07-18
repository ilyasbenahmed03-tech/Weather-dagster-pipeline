import requests
import pandas as pd
import numpy as np
import os
import sys
from sqlalchemy import create_engine
from dagster import (
    asset, DailyPartitionsDefinition, AssetSelection,
    define_asset_job, ScheduleDefinition, sensor, RunRequest
)

# Gestion du path pour l'import de ml.py
sys.path.append(os.path.dirname(__file__))
from ml import train_and_predict

# 1. CONFIGURATION DES PARTITIONS (Debut au 01/05/2026)
daily_partitions = DailyPartitionsDefinition(start_date="2026-05-01")


# --1
@asset(partitions_def=daily_partitions, group_name="weather_pipeline")
def raw_weather_data(context):
    partition_date = context.partition_key
    context.log.info(f"Extraction API pour : {partition_date}")

    # Appel API Open-Meteo pour Lyon
    url = f"https://api.open-meteo.com/v1/forecast?latitude=45.75&longitude=4.85&hourly=temperature_2m&start_date={partition_date}&end_date={partition_date}"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        context.log.error(f"Erreur API : {response.status_code}")
        raise Exception(f"API Error: {response.status_code}")

    return pd.DataFrame(response.json()['hourly'])


# --2
@asset(deps=[raw_weather_data], partitions_def=daily_partitions, group_name="weather_pipeline")
def cleaned_weather_data(context, raw_weather_data):
    df = raw_weather_data.copy()
    df['time'] = pd.to_datetime(df['time'])
    df = df.rename(columns={"temperature_2m": "temp_celsius"})
    cleaned_df = df[['time', 'temp_celsius']].dropna()

    context.log.info(f"Nettoyage termine : {len(cleaned_df)} points conserves.")
    return cleaned_df


# --3
@asset(deps=[cleaned_weather_data], partitions_def=daily_partitions, group_name="weather_pipeline")
def daily_weather_stats(context, cleaned_weather_data):
    df = cleaned_weather_data.copy()
    df.set_index('time', inplace=True)

    # Agregation par jour : moyenne, min et max
    df_daily = df.resample('D').agg({'temp_celsius': ['mean', 'min', 'max']})
    df_daily.columns = ['temp_moyenne', 'temp_min', 'temp_max']

    result = df_daily.reset_index().round(2)
    context.log.info(f"Stats calculees pour {context.partition_key}")
    return result


# --4
@asset(deps=[daily_weather_stats], group_name="weather_pipeline")
def weather_prediction(context, daily_weather_stats):
    context.log.info("Calcul de la prediction Random Forest...")
    return train_and_predict(daily_weather_stats)


# --5 postgres
# Utilisation du nom 'db_postgres' pour communiquer entre containers
@asset(deps=[daily_weather_stats], partitions_def=daily_partitions, group_name="weather_pipeline")
def weather_to_postgres(context, daily_weather_stats):
    db_password = os.getenv("POSTGRES_PASSWORD")
    engine = create_engine(f"postgresql://postgres:{db_password}@db_postgres:5433/postgres")
    daily_weather_stats.to_sql('weather_daily_metrics', engine, if_exists='append', index=False)
    context.log.info("Donnees inserees dans weather_daily_metrics.")
    return "OK"


@asset(deps=[weather_prediction], group_name="weather_pipeline")
def predictions_to_postgres(context, weather_prediction):
    if weather_prediction is None: return "Pas de donnees"

    db_password = os.getenv("POSTGRES_PASSWORD")
    engine = create_engine(f"postgresql://postgres:{db_password}@db_postgres:5433/postgres")
    weather_prediction.to_sql('weather_predictions', engine, if_exists='replace', index=False)
    context.log.info("Table weather_predictions mise a jour.")
    return "OK"


# -AUTOMATION
weather_job = define_asset_job(
    name="weather_pipeline_job",
    selection=AssetSelection.groups("weather_pipeline")
)

# Planification quotidienne a minuit
weather_schedule = ScheduleDefinition(job=weather_job, cron_schedule="0 0 * * *")


@sensor(job=weather_job)
def watch_input_file_sensor():
    # Detection de fichiers dans le dossier input pour declencher le pipeline
    folder_path = "/app/input" # Chemin  Docker
    if not os.path.exists(folder_path): os.makedirs(folder_path)

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for filename in files:
        yield RunRequest(run_key=filename)
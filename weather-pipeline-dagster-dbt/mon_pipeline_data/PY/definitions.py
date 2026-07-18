from dagster import Definitions, load_assets_from_modules, sensor, RunRequest, SkipReason
import requests
from . import assets

all_assets = load_assets_from_modules([assets])

# Définition  Sensor
@sensor(job=assets.weather_job)
def api_availability_sensor():
    try:
        response = requests.head("https://api.open-meteo.com/v1/forecast", timeout=5)
        if response.status_code == 200:
            yield RunRequest()
        else:
            yield SkipReason(f"L'API répond avec le code {response.status_code}")
    except Exception as e:
        yield SkipReason(f"Erreur de connexion : {str(e)}")

# L'objet unique qui regroupe TOUT
defs = Definitions(
    assets=all_assets,
    jobs=[assets.weather_job],
    schedules=[assets.weather_schedule],
    sensors=[api_availability_sensor],
)
import pandas as pd
import pytest
import sys
import os
import numpy as np


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mon_pipeline_data.assets import cleaned_weather_data, daily_weather_stats


def test_cleaned_weather_data_logic():
    """
    Test de la couche SILVER : Vérifie le renommage et le typage.
    """

    df_raw = pd.DataFrame({
        "time": ["2026-05-01T00:00", "2026-05-01T01:00"],
        "temperature_2m": [15.0, 25.0]
    })

    # la fonction
    df_cleaned = cleaned_weather_data(df_raw)

    #  Vérifications (Assertions)
    assert "temp_celsius" in df_cleaned.columns  #  le renommage
    assert len(df_cleaned) == 2  # Vérifie qu'on n'a pas perdu de lignes
    assert pd.api.types.is_datetime64_any_dtype(df_cleaned['time'])  # le type date


def test_daily_weather_stats_logic():
    """
    Test de la couche GOLD : Vérifie l'agrégation (Moyenne/Min/Max).
    """

    df_silver = pd.DataFrame({
        "time": pd.to_datetime(["2026-05-01 10:00", "2026-05-01 14:00"]),
        "temp_celsius": [10.0, 20.0]
    })

    # Exécution
    df_gold = daily_weather_stats(df_silver)

    # Vérifications
    # On vérifie que la moyenne est bien de 15.0
    assert df_gold['temp_moyenne'].iloc[0] == 15.0
    assert df_gold['temp_min'].iloc[0] == 10.0
    assert df_gold['temp_max'].iloc[0] == 20.0
    # Vérifie que l'index  sous forme de colonne 'time'
    assert 'time' in df_gold.columns


def test_empty_data_handling():
    """Vérifie que le code ne plante pas avec un DataFrame vide."""
    df_empty = pd.DataFrame({"time": [], "temperature_2m": []})
    result = cleaned_weather_data(df_empty)
    assert len(result) == 0
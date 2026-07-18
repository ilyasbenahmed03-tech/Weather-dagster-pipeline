# Transformations dbt — Couche Silver/Gold Météo Lyon

Ce projet dbt transforme les données météo brutes (couche Bronze, insérées par le pipeline Dagster dans PostgreSQL) en statistiques journalières exploitables pour l'aide à la décision et la visualisation.

## Modèle

- **`daily_weather_stats`** : agrège les relevés horaires (`weather_hourly`) en statistiques quotidiennes (température moyenne, min, max) par jour.

Ce modèle fait partie du pipeline global décrit dans [`../mon_pipeline_data/README.md`](../mon_pipeline_data/README.md) : Dagster extrait et charge les données brutes, puis dbt les transforme directement dans PostgreSQL (approche ELT).

## Utilisation

Prérequis : `dbt-postgres` installé et un profil `mon_projet_dbt` configuré dans `~/.dbt/profiles.yml` pointant vers la base PostgreSQL du projet.

```bash
dbt run    # exécute les transformations
dbt test   # lance les tests de qualité de données (si définis)
```

## Structure

```
DBT/
├── models/
│   ├── sources.yml           # Déclaration de la source (table weather_hourly)
│   └── daily_weather_stats.sql
├── dbt_project.yml
└── ...                       # dossiers standard dbt (macros, seeds, snapshots, tests)
```

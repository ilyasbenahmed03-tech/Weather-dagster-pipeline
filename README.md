# 🌦️ Weather Data Pipeline — Dagster + dbt + PostgreSQL + Power BI

Pipeline de données météo complet (module **4DATAPROCESSING**) : extraction via l'API Open-Meteo, orchestration Dagster, transformation SQL avec dbt (architecture Bronze/Silver/Gold), prédiction ML, et restitution via un dashboard Power BI.

Projet réalisé en binôme : **Ilyas Benahmed & Mahmoud Qzibar**.

## 🏗️ Architecture globale

```
Open-Meteo API (Lyon)
        ↓
  Extraction (Asset Dagster)
        ↓
  PostgreSQL — Couche Bronze (données brutes)
        ↓
  dbt — Transformations SQL
        ↓
  PostgreSQL — Couches Silver & Gold (données enrichies)
        ↓
  ┌───────────────────────────┐
  │ ML (Random Forest)        │
  │ Prédiction température J+1│
  └───────────────────────────┘
        ↓
  Rapports (matplotlib) & Dashboard Power BI
```

## 📁 Organisation du dépôt

Ce dépôt regroupe deux sous-projets complémentaires :

- **[`mon_pipeline_data/`](mon_pipeline_data/README.md)** — Le pipeline Dagster (extraction API, chargement PostgreSQL, ML, tests, Docker). Voir le README dédié pour l'installation complète.
- **[`DBT/`](DBT/README.md)** — Les modèles dbt qui transforment les données brutes en statistiques journalières (couche Silver/Gold).

Un dashboard Power BI (`mon_pipeline_data/DOC/Projet_Meteo_Lyon.pbix`) et un export PDF sont fournis en complément pour l'aide à la décision.

## 🚀 Démarrage rapide

Voir les instructions détaillées dans [`mon_pipeline_data/README.md`](mon_pipeline_data/README.md) (Docker Compose, variables d'environnement, tests) et [`DBT/README.md`](DBT/README.md) (exécution des transformations dbt).

## 🛠️ Stack technique

Dagster · dbt · PostgreSQL · Docker · Python (Pandas, Scikit-learn) · Power BI

## 👤 Auteurs

Ilyas Benahmed & Mahmoud Qzibar — Master Ingénierie Data, SUPINFO Lyon

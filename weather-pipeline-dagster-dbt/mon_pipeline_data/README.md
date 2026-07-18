Pipeline de Données Météo Lyon - Orchestration Dagster
Ce projet a été réalisé dans le cadre du module 4DATAPROCESSING. L'objectif est de mettre en place une pipeline ETL/ELT complète, de l'extraction de données brutes via API jusqu'à l'aide à la décision .

## Architecture

```
Open-Meteo API (Lyon)
        ↓
    Extraction (Asset Dagster)
        ↓
    PostgreSQL - Couche Bronze (Données brutes)
        ↓
    dbt - Transformations SQL
        ↓
    PostgreSQL - Couches Silver & Gold (Données enrichies)
        ↓
    ┌─────────────────────────────┐
    │  ML (Random Forest)          │
    │  Prédiction Temp J+1         │
    └─────────────────────────────┘
        ↓
    Rapports & Visualisations
```

1. Choix de Conception
Nous avons opté pour une approche Modern Data Stack conteneurisée pour garantir la portabilité et la robustesse du système :

* Orchestration (Dagster) : Contrairement à Airflow, Dagster nous permet une gestion par "Assets", facilitant le suivi du lignage des données et la réexécution partielle en cas d'erreur.

* Transformation (dbt & SQL) : dbt est utilisé pour transformer les données directement dans notre base de données.

* Stockage (PostgreSQL) : Une base de données relationnelle robuste pour centraliser les données météo et les résultats du modèle ML.

* Intelligence Artificielle : Intégration d'un modèle Random Forest Regressor pour prédire les températures .

* Conteneurisation (Docker) : L'intégralité de l'infrastructure (Base de données + Orchestrateur) est isolée dans des conteneurs pour simplifier le déploiement.

2. Structure du Pipeline Dagster
Le pipeline implémente les fonctionnalités clés demandées dans le cahier des charges :

* Assets : Chaque étape (extraction API, chargement Postgres, entraînement ML) est définie comme un asset avec ses propres dépendances.

* Schedules : Le pipeline est planifié pour s'exécuter automatiquement chaque jour à minuit.

* Sensors : Un capteur surveille le répertoire `/input`  tout nouveau fichier déposé déclenche instantanément un run du pipeline.

* Monitoring : Utilisation des logs natifs de Dagster et de l'interface de lignage pour le débogage en temps réel.

3. Installation et Lancement
Prérequis

* Docker & Docker Compose installés.
*  Python 3.10+ pour exécuter les scripts de visualisation en local.
Déploiement rapide

1. Cloner le dépôt et se rendre à la racine du projet.
2. Créer le fichier d'environnement : `cp .env.example .env` puis définir un mot de passe PostgreSQL dans `.env`.
3. Lancer l'infrastructure via Docker :
Bash

```
docker-compose up --build

```

3. Accéder aux outils :
   * Interface Dagster : `http://localhost:3000`
   * Base de données Postgres : Port `5433` (identifiants définis dans ton fichier `.env`, voir `.env.example`).

4. Tests et Fiabilité
La fiabilité du code est assurée par une suite de tests unitaires :

* Outil : `pytest`.
* Portée : Validation des schémas de données et des transformations critiques.

* Résultat : 3 tests majeurs validés avec succès (Extraction, Transformation, Prédiction).

5. Aide à la Décision et Visualisation
Le projet propose deux supports pour l'exploitation des données :

1. Rapports Automatisés (Python) : Le script `visualisation.py` génère des graphiques d'analyse de tendances (températures horaires et quotidiennes).

2. Dashboard Interactif (Power BI) .

Binôme : Ilyas BENAHMED & Mahmoud Qzibar 

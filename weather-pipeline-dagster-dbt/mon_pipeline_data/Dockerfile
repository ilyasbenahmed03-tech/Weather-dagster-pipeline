# ETAPE 1 : Image de base Python
FROM python:3.10-slim

# ETAPE 2 : Dossier de travail dans le container
WORKDIR /app

# ETAPE 3 : Dependances systeme pour PostgreSQL
# Necessaire pour compiler psycopg2 et autres outils
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ETAPE 4 : Installation des libs Python
# On utilise le cache Docker pour gagner du temps au build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ETAPE 5 : Copie du code source
# Copie locale vers le dossier /app du container
COPY . .

# ETAPE 6 : Port pour l'interface web
EXPOSE 3000

# ETAPE 7 : Lancement de Dagster
# On ecoute sur 0.0.0.0 pour permettre l'acces depuis l'exterieur
CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]
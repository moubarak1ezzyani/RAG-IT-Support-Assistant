# 1. Image de base
FROM python:3.12-slim

# 2. Dossier de travail
WORKDIR /app

# 3. Variables d'environnement pour optimiser Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# --- AJOUT CRUCIAL ---
# Cela garantit que Python trouve tes dossiers "db" et "app" peu importe où il se trouve
ENV PYTHONPATH=/app 

# 4. Installation des dépendances système (PostgreSQL driver)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Copie et installation des librairies Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copie du code source
COPY . .

# 7. Lancement de l'application
# On lance le module 'app.main' depuis la racine
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
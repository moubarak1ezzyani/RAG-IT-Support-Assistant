# 1. Image de base
FROM python:3.12-slim

# 2. Dossier de travail
WORKDIR /app

# 3. Variables d'environnement pour optimiser Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 4. Installation des dépendances système (PostgreSQL driver & build tools)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Copie et installation des librairies Python
COPY requirements.txt .

# --- OPTIMIZATION START ---
# We explicitly install the CPU version of torch FIRST.
# This prevents 'requirements.txt' from downloading the massive Nvidia version later.
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# --- OPTIMIZATION END ---

# Now install the rest. Pip will see 'torch' is already installed and skip the heavy download.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copie du code source
COPY . .

# 7. Lancement de l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# RAG-IT-Support-Assistant
A reliable RAG-powered assistant for IT technicians to query procedures, incidents, and FAQs from PDF documentation.

## 📂 File Tree & Naming Convention
```Plaintext
RAG-IT-Support/
│
├── .github/
│   └── workflows/
│       └── ci_cd.yml          # Pipeline GitHub Actions (Test, Build, Lint)
│
├── app/                       # Cœur du code applicatif
│   ├── api/                   # Tout ce qui concerne FastAPI
│   │   ├── __init__.py
│   │   ├── endpoints.py       # Tes routes (POST /query, POST /auth, etc.)
│   │   └── dependencies.py    # Vérification token JWT, accès DB
│   │
│   ├── core/                  # Configuration globale
│   │   ├── config.py          # Variables d'env (URL DB, Clés API)
│   │   └── security.py        # Logique de hashage MDP et génération JWT
│   │
│   ├── db/                    # Base de données PostgreSQL
│   │   ├── database.py        # Connexion SQLAlchemy
│   │   ├── models.py          # Tables (Users, Queries)
│   │   └── schemas.py         # Modèles Pydantic (validation des données)
│   │
│   ├── ml/                    # Partie Machine Learning (Non supervisé)
│   │   ├── clustering.py      # Script KMeans pour regrouper les questions
│   │   └── mlflow_utils.py    # Fonctions pour logger les métriques MLflow
│   │
│   ├── rag/                   # Le cerveau (Pipeline LangChain)
│   │   ├── ingestion.py       # Chargement PDF -> Split -> ChromaDB
│   │   ├── embeddings.py      # Configuration du modèle HuggingFace
│   │   └── chain.py           # La chaîne RetrievalQA + Prompt
│   │
│   └── main.py                # Point d'entrée de l'application (lancement FastAPI)
│
├── data/                      # Stockage des données locales
│   ├── raw/                   # Mets ton PDF ici (ex: support_it.pdf)
│   └── chroma_db/             # Dossier où Chroma va stocker les vecteurs
│
├── k8s/                       # Fichiers pour Kubernetes (Minikube/Lens)
│   ├── deployment.yaml        # Configuration du Pod/Deployment
│   ├── service.yaml           # Exposition du service
│   └── postgres-k8s.yaml      # (Optionnel) Si tu mets la DB dans K8s aussi
│
├── tests/                     # Tests unitaires
│   ├── test_api.py
│   └── test_rag.py
│
├── .env                       # Tes mots de passe et clés (NE PAS COMMIT SUR GIT)
├── .gitignore                 # Pour ignorer .env, venv, pycache, data/chroma_db
├── docker-compose.yml         # Pour lancer App + Postgres + MLflow en local
├── Dockerfile                 # Pour construire l'image de ton API
├── requirements.txt           # Liste des librairies (fastapi, langchain, torch...)
└── README.md                  # Documentation du projet
```

## 🌿 GitHub Branch Strategy (Git Flow)
![alt text](image.png)
``
feat/data-ingestion
feat/vector-db
feat/rag
feat/backend
feat/db-postgres
feat/ml-flow-tracking
feat/ml-flow-registry
feat/ci-cd
feat/deploy
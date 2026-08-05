![CI](https://github.com/hdmanoach/recette-api/actions/workflows/ci.yml/badge.svg)

# Recette API

Une API REST pour gérer des recettes de cuisine, construite avec FastAPI.

🔗 **Démo en ligne** : https://recette-api-l2r6.onrender.com/docs  

🔗 **Frontend associé** : https://recette-frontend-five.vercel.app ([code source](https://github.com/hdmanoach/recette-frontend))

💾 **Base de données** : Supabase PostgreSQL (gratuit, permanent) — maintenue active par un cron job sur `/health`.

## Fonctionnalités

- CRUD complet sur les recettes (Create, Read, Update, Delete, + création en lot)
- Authentification par JWT (inscription, connexion)
- Chaque recette appartient à un utilisateur ; seul le propriétaire peut la modifier/supprimer
- Limitation anti-bruteforce sur les tentatives de connexion
- Journalisation de toutes les requêtes en base, consultable via `/logs`
- Validation avancée des données (Pydantic)
- Pagination et filtres (titre, ingrédient, temps de préparation)
- Base de données persistante : Supabase PostgreSQL en production, SQLite en local
- Endpoint `/health` pour vérifier la connexion DB et garder Supabase actif (cron job)
- Tests automatisés et isolés (Pytest)
- Linting automatique (Ruff)
- Conteneurisation (Docker)
- CI/CD avec GitHub Actions (lint, tests, build Docker)
- Déploiement automatique (Render)

## Installation

```bash
git clone https://github.com/hdmanoach/recette-api.git
cd recette-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Crée un fichier `.env` à la racine :
```bash
SECRET_KEY=une-cle-secrete-generee-aleatoirement
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000
# Optionnel — si absent, SQLite est utilisé automatiquement
# DATABASE_URL=postgresql://user:password@host:port/dbname
```
Génère une clé secrète avec :
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Lancer le serveur

```bash
uvicorn main:app --reload
```

L'API est accessible sur `http://127.0.0.1:8000`
Documentation interactive (Swagger) : `http://127.0.0.1:8000/docs`

## Endpoints principaux

| Méthode | Route                | Auth requise | Description                        |
|---------|-----------------------|:---:|-------------------------------------|
| GET     | `/`                    |  | Message de bienvenue                |
| GET     | `/health`              |  | Vérification santé + ping DB (cron) |
| POST    | `/register`            |  | Créer un compte utilisateur         |
| POST    | `/login`               |  | Se connecter, obtenir un token JWT  |
| GET     | `/recipes`             |  | Lister les recettes (filtres, pagination) |
| GET     | `/recipes/{id}`        |  | Récupérer une recette par son id    |
| POST    | `/recipes`             | ✅ | Créer une recette                   |
| POST    | `/recipes/bulk`        | ✅ | Créer plusieurs recettes            |
| PUT     | `/recipes/{id}`        | ✅ | Modifier une recette (propriétaire) |
| DELETE  | `/recipes/{id}`        | ✅ | Supprimer une recette (propriétaire)|
| GET     | `/logs`                | ✅ | Consulter le journal des requêtes   |

## Lancer les tests

```bash
pytest
```

## Vérifier le style du code

```bash
ruff check .
```

## Lancer avec Docker

```bash
docker build -t recette-api .
docker run -p 8000:8000 -v $(pwd)/data:/app/data recette-api
```

## Structure du projet
```bash
recette-api/
├── main.py # Point d'entrée : config app, CORS, middleware, routers
├── database.py # Configuration de la base de données
├── models.py # Modèles Pydantic et SQLAlchemy
├── security.py # JWT, hash de mot de passe, anti-bruteforce
├── middleware.py # Journalisation des requêtes
├── routers/
│ ├── auth.py # /register, /login
│ ├── recipes.py # CRUD recettes
│ └── logs.py # /logs
├── test_main.py # Tests automatisés
├── requirements.txt
├── pyproject.toml # Configuration de Ruff
├── Dockerfile
└── .github/workflows/ci.yml # Pipeline CI/CD
```

## Déploiement en production

### Architecture
```
Vercel (frontend) → Render (API FastAPI) → Supabase (PostgreSQL)
                                         ↑
                              cron-job.org (ping /health toutes les 72h)
```

### Variables d'environnement sur Render
| Variable | Valeur |
|---|---|
| `DATABASE_URL` | URI **pooler** Supabase (port `6543`, pas `5432`) |
| `SECRET_KEY` | Clé secrète JWT |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `CORS_ORIGINS` | `http://localhost:3000,https://recette-frontend-five.vercel.app` |

> ⚠️ **Important** : utiliser l'URI **Connection Pooling (Session)** de Supabase, pas la connexion directe. Render free ne supporte pas IPv6, et la connexion directe Supabase résout en IPv6.
```
## Auteur

**Manoach HOSSOU DODO** — [LinkedIn](https://www.linkedin.com/in/hdmanoach/)

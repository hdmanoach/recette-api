![CI](https://github.com/hdmanoach/recette-api/actions/workflows/ci.yml/badge.svg)

# Recette API

Une API REST simple pour gérer des recettes de cuisine, construite avec FastAPI.

## Fonctionnalités

- CRUD complet sur les recettes (Create, Read, Update, Delete)
- Base de données persistante (SQLite + SQLAlchemy)
- Tests automatisés et isolés avec Pytest
- Linting automatique avec Ruff
- CI/CD avec GitHub Actions (lint + tests à chaque push)

## Installation

```bash
git clone https://github.com/hdmanoach/recette-api.git
cd recette-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Lancer le serveur

```bash
uvicorn main:app --reload
```

L'API est accessible sur `http://127.0.0.1:8000`
Documentation interactive (Swagger) : `http://127.0.0.1:8000/docs`

## Endpoints

| Méthode | Route                | Description                        |
|---------|-----------------------|-------------------------------------|
| GET     | `/`                    | Message de bienvenue                |
| POST    | `/recipes`             | Créer une recette                   |
| POST    | `/recipes/bulk`        | Créer plusieurs recettes en une fois|
| GET     | `/recipes`             | Lister toutes les recettes          |
| GET     | `/recipes/{id}`        | Récupérer une recette par son id    |
| PUT     | `/recipes/{id}`        | Modifier une recette                |
| DELETE  | `/recipes/{id}`        | Supprimer une recette               |

## Lancer les tests

```bash
pytest
```

## Vérifier le style du code

```bash
ruff check .
```

## Structure du projet

recette-api/
├── main.py # Points d'entrée de l'API (endpoints)
├── models.py # Modèles Pydantic et SQLAlchemy
├── database.py # Configuration de la base de données
├── test_main.py # Tests automatisés
├── requirements.txt # Dépendances Python
├── pyproject.toml # Configuration de Ruff
└── .github/workflows/ci.yml # Pipeline CI/CD

## Auteur

**Manoach HOSSOU DODO** — [LinkedIn](https://www.linkedin.com/in/hdmanoach/)

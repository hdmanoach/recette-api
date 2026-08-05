import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Utilisation d'une base SQLite en mémoire pour une isolation et une vitesse maximales
from sqlalchemy.pool import StaticPool

from database import Base
from main import app
from security import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture pour configurer proprement la base de données avant CHAQUE test
@pytest.fixture(name="db_session")
def fixture_db_session():
    # Crée les tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Surcharge de la dépendance FastAPI
    def override_get_db():
        try:
            yield db
        finally:
            pass  # Géré par la fixture

    app.dependency_overrides[get_db] = override_get_db

    yield db

    # Nettoyage après le test
    db.close()
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(name="client")
def fixture_client(db_session):
    """Fournit un client de test qui bénéficie de la base de données propre."""
    return TestClient(app)


# --- Tests unitaires ---


def test_bienvenue(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue dans l'API Recettes"}


def test_create_recipe(client):
    # Enregistrement de l'utilisateur
    client.post(
        "/register", json={"username": "testuser", "password": "testpass123"}
    )

    # Connexion pour obtenir le jeton JWT
    login_response = client.post(
        "/login", json={"username": "testuser", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]

    recipe = {
        "id": 100,
        "title": "Test Recipe",
        "ingredients": ["Ingredient 1", "Ingredient 2"],
        "instructions": ["Instruction 1", "Instruction 2"],
        "prep_time": 30,
        "servings": 4,
    }

    # Publication de la recette avec l'en-tête d'authentification
    response = client.post(
        "/recipes",
        json=recipe,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Recipe"


def test_get_recipes(client):
    # Grâce à l'isolation, cette base de données est vide (0 recette)
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == {"recipes": [], "total": 0}


def test_get_recipe(client):
    response = client.get("/recipes/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Recette introuvable"}

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)

def test_bienvenue():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue dans l'API Recettes"}

def test_get_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == {"recipes": []}

def test_get_recipe():
    response = client.get("/recipes/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Recette introuvable"}

def test_create_recipe():
    recipe = {"id": 100, "title": "Test Recipe", "ingredients": ["Ingredient 1", "Ingredient 2"], "instructions": ["Instruction 1", "Instruction 2"], "prep_time": 30, "servings": 4}
    response = client.post("/recipes", json=recipe)
    assert response.status_code == 200
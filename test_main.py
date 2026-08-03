from fastapi.testclient import TestClient

from main import app

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
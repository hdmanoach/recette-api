from fastapi import FastAPI, HTTPException

from models import Recipe

app = FastAPI()
recipes = []  # Liste pour stocker les recettes
@app.get("/")
def bienvenue():
    return {"message": "Bienvenue dans l'API Recettes"}


@app.post("/recipes")
def create_recipe(recipe: Recipe):
    recipes.append(recipe)
    return recipe

@app.post("/recipes/bulk")
def create_recipes(new_recipes: list[Recipe]):
    recipes.extend(new_recipes)
    return recipes

@app.get("/recipes")
def get_recipes():
    return {"recipes": recipes}

@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    for recipe in recipes:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recette introuvable")

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    for recipe in recipes:
        if recipe.id == recipe_id:
            recipes.remove(recipe)
            return {"message": "Recette supprimée"}
    raise HTTPException(status_code=404, detail="Recette introuvable")

@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, recipe: Recipe):
    for r in recipes:
        if r.id == recipe_id:
            r.title = recipe.title
            r.ingredients = recipe.ingredients
            r.instructions = recipe.instructions
            r.prep_time = recipe.prep_time
            r.servings = recipe.servings
            return r
    raise HTTPException(status_code=404, detail="Recette introuvable")
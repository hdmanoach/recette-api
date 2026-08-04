from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Recipe, RecipeDB

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def bienvenue():
    return {"message": "Bienvenue dans l'API Recettes"}


@app.post("/recipes")
def create_recipe(recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = RecipeDB(
        id=recipe.id,
        title=recipe.title,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        servings=recipe.servings,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
@app.post("/recipes/bulk")
def create_recipes(new_recipes: list[Recipe], db: Session = Depends(get_db)):
    db_recipes = []
    for recipe in new_recipes:
        db_recipe = RecipeDB(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            prep_time=recipe.prep_time,
            servings=recipe.servings,
        )
        db.add(db_recipe)
        db_recipes.append(db_recipe)
    db.commit()
    return db_recipes

@app.get("/recipes")
def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(RecipeDB).all()
    return {"recipes": recipes}

@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recette introuvable")
    return recipe

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recette introuvable")
    db.delete(recipe)
    db.commit()
    return {"message": "Recette supprimée"}

@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recette introuvable")
    db_recipe.title = recipe.title
    db_recipe.ingredients = recipe.ingredients
    db_recipe.instructions = recipe.instructions
    db_recipe.prep_time = recipe.prep_time
    db_recipe.servings = recipe.servings
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
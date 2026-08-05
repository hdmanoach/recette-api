from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Recipe, RecipeDB, UserDB
from security import get_current_user, get_db

router = APIRouter(tags=["recipes"])


@router.get("/recipes")
def get_recipes(
    skip: int = 0,
    limit: int = 10,
    title: str | None = None,
    max_prep_time: int | None = None,
    ingredient: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(RecipeDB)
    if title:
        query = query.filter(RecipeDB.title.ilike(f"%{title}%"))
    if max_prep_time:
        query = query.filter(RecipeDB.prep_time <= max_prep_time)

    results = query.all()

    if ingredient:
        results = [
            r for r in results
            if any(ingredient.lower() in i.lower() for i in r.ingredients)
        ]

    return {"recipes": results[skip: skip + limit], "total": len(results)}


@router.post("/recipes/bulk")
def create_recipes(
    new_recipes: list[Recipe],
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    db_recipes = []
    for recipe in new_recipes:
        db_recipe = RecipeDB(
            title=recipe.title,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            prep_time=recipe.prep_time,
            servings=recipe.servings,
            owner_id=current_user.id,
        )
        db.add(db_recipe)
        db_recipes.append(db_recipe)
    db.commit()
    return db_recipes


@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recette introuvable")
    return recipe


@router.post("/recipes")
def create_recipe(
    recipe: Recipe,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    db_recipe = RecipeDB(
        title=recipe.title,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        servings=recipe.servings,
        owner_id=current_user.id,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.delete("/recipes/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recette introuvable")
    if recipe.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à supprimer cette recette")
    db.delete(recipe)
    db.commit()
    return {"message": "Recette supprimée"}


@router.put("/recipes/{recipe_id}")
def update_recipe(
    recipe_id: int,
    recipe: Recipe,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    db_recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recette introuvable")
    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à modifier cette recette")
    db_recipe.title = recipe.title
    db_recipe.ingredients = recipe.ingredients
    db_recipe.instructions = recipe.instructions
    db_recipe.prep_time = recipe.prep_time
    db_recipe.servings = recipe.servings
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
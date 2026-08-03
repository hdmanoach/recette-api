"""
    Ce qu'on veut modéliser
    
    Une recette basique, avec par exemple :
        id : identifiant unique
        title : titre de la recette
        ingredients : liste d'ingrédients
        instructions : les étapes de préparation
        prep_time : temps de préparation (en minutes)
        servings : nombre de personnes
"""
from pydantic import BaseModel

class Recipe(BaseModel):
    id: int
    title: str
    ingredients: list[str]
    instructions: list[str]
    prep_time: int
    servings: int
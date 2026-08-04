"""
Ce qu'on veut modéliser

Une recette basique, avec par exemple :
    id : identifiant unique
    title : titre de la recette
    ingredients : liste d'ingrédients
    instructions : les étapes de préparation
    prep_time : temps de préparation (en minutes)
    servings : nombre de personnes
    
Règles qu'on va ajouter
    title → ne doit pas être vide
    prep_time → doit être strictement positif (> 0)
    servings → doit être entre 1 et 20
    ingredients → doit contenir au moins 1 élément
    instructions → doit contenir au moins 1 élément
"""
from pydantic import BaseModel, Field
from sqlalchemy import JSON, Column, Integer, String

from database import Base


class Recipe(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    ingredients: list[str] = Field(..., min_length=1)
    instructions: list[str] = Field(..., min_length=1)
    prep_time: int = Field(..., gt=0)
    servings: int = Field(..., ge=1, le=20)

"""
    ... → signifie "champ obligatoire" (pas de valeur par défaut)
    min_length=1 → au moins 1 caractère (pour title) ou 1 élément (pour les listes)
    gt=0 → greater than 0 (strictement positif)
    ge=1, le=20 → greater or equal 1, less or equal 20 (entre 1 et 20 inclus)
"""

class RecipeDB(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    ingredients = Column(JSON, nullable=False)
    instructions = Column(JSON, nullable=False)
    prep_time = Column(Integer, nullable=False)
    servings = Column(Integer, nullable=False)
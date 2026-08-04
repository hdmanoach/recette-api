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
from sqlalchemy import JSON, Column, Integer, String

from database import Base


class Recipe(BaseModel):
    id: int
    title: str
    ingredients: list[str]
    instructions: list[str]
    prep_time: int
    servings: int


class RecipeDB(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    ingredients = Column(JSON)
    instructions = Column(JSON)
    prep_time = Column(Integer)
    servings = Column(Integer)
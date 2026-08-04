"""
engine → le point d'entrée vers ta base (ici un simple fichier recettes.db créé automatiquement)
connect_args={"check_same_thread": False} → spécifique à SQLite, nécessaire car FastAPI peut utiliser plusieurs threads
SessionLocal → une "usine" à sessions — chaque requête API va ouvrir sa propre session pour parler à la base
Base → la classe dont hériteront tes futurs modèles de table (RecipeDB)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

os.makedirs("data", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/recettes.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
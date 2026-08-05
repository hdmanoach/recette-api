"""
engine → le point d'entrée vers ta base (ici un simple fichier recettes.db créé automatiquement)
connect_args={"check_same_thread": False} → spécifique à SQLite, nécessaire car FastAPI peut utiliser plusieurs threads
SessionLocal → une "usine" à sessions — chaque requête API va ouvrir sa propre session pour parler à la base
Base → la classe dont hériteront tes futurs modèles de table (RecipeDB)
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Render fournit parfois une URL commençant par "postgres://",
    # mais SQLAlchemy exige "postgresql://"
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)
else:
    os.makedirs("data", exist_ok=True)
    DATABASE_URL = "sqlite:///./data/recettes.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
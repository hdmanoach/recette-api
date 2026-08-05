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
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from database import Base

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

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
    owner_id = Column(Integer, ForeignKey("users.id"))

"""
    Explication
    pwd_context → l'outil qui va hasher/vérifier les mots de passe avec l'algorithme bcrypt
    UserDB → la table SQL réelle. username est unique=True → impossible d'avoir deux comptes avec le même nom
    UserCreate → ce que le client envoie pour s'inscrire (nom d'utilisateur + mot de passe en clair, qu'on va hasher avant de stocker)
    UserLogin → ce que le client envoie pour se connecter
    UserOut → ce qu'on renvoie au client — remarque qu'il n'y a pas de mot de passe ici, jamais ! On ne renvoie jamais le hash, même, par sécurité
    from_attributes = True → permet à Pydantic de lire directement un objet SQLAlchemy (comme UserDB) pour le convertir en UserOut
"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


from pydantic import (  # ajoute ConfigDict à l'import existant
    BaseModel,
    ConfigDict,
    Field,
)


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    method = Column(String)
    path = Column(String)
    status_code = Column(Integer)
    username = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
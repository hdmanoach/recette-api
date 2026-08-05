import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import Base, engine
from middleware import LoggingMiddleware
from routers import auth, logs, recipes

# Charger les variables du fichier .env
load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Récupérer la chaîne du .env et la transformer en liste Python
cors_origins_raw = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:3000,https://recette-frontend-five.vercel.app"
)
origins = [origin.strip() for origin in cors_origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Utilise la liste dynamique issue du .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(logs.router)


@app.get("/")
def bienvenue():
    return {"message": "Bienvenue dans l'API Recettes"}

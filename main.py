import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from middleware import LoggingMiddleware
from routers import auth, logs, recipes

# Charger les variables du fichier .env
load_dotenv()

app = FastAPI()

# Créer toutes les tables dans la base PostgreSQL (ou SQLite en local)
print(f"[startup] Tables enregistrées : {list(Base.metadata.tables.keys())}")
Base.metadata.create_all(bind=engine)
print("[startup] create_all terminé avec succès")

# Récupérer la chaîne du .env et la transformer en liste Python
cors_origins_raw = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:3000,https://recette-frontend-five.vercel.app"
)
origins = [origin.strip() for origin in cors_origins_raw.split(",")]

# IMPORTANT : l'ordre compte ! Starlette exécute les middlewares en LIFO.
# LoggingMiddleware est ajouté en premier → il s'exécute en dernier (à l'intérieur).
# CORSMiddleware est ajouté en dernier → il s'exécute en premier (à l'extérieur).
# Ainsi, les headers CORS sont TOUJOURS présents, même si le logging crashe.
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Utilise la liste dynamique issue du .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(logs.router)


@app.get("/")
def bienvenue():
    return {"message": "Bienvenue dans l'API Recettes"}


@app.get("/health")
def health_check():
    """Endpoint de santé — utilisé par le cron job pour garder Supabase actif."""
    from sqlalchemy import text
    from sqlalchemy.exc import SQLAlchemyError

    from database import SessionLocal

    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError:
        return {"status": "error", "database": "disconnected"}
    finally:
        db.close()

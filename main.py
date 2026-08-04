from fastapi import FastAPI

from database import Base, engine
from middleware import LoggingMiddleware
from routers import auth, logs, recipes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(LoggingMiddleware)

app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(logs.router)


@app.get("/")
def bienvenue():
    return {"message": "Bienvenue dans l'API Recettes"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import (
    UserCreate,
    UserDB,
    UserLogin,
    UserOut,
    create_access_token,
    hash_password,
    verify_password,
)
from security import (
    LOCKOUT_DURATION_MINUTES,
    clear_failed_attempts,
    get_db,
    is_locked_out,
    register_failed_attempt,
)

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà pris")

    db_user = UserDB(
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    if is_locked_out(credentials.username):
        raise HTTPException(
            status_code=429,
            detail=f"Trop de tentatives échouées. Réessayez dans {LOCKOUT_DURATION_MINUTES} minutes.",
        )

    user = db.query(UserDB).filter(UserDB.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        register_failed_attempt(credentials.username)
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")

    clear_failed_attempts(credentials.username)
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
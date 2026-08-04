from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import SessionLocal
from models import ALGORITHM, SECRET_KEY, UserDB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserDB:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=401,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user


MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

failed_login_attempts: dict[str, list[datetime]] = {}


def is_locked_out(username: str) -> bool:
    attempts = failed_login_attempts.get(username, [])
    now = datetime.now(timezone.utc)
    recent_attempts = [a for a in attempts if now - a < timedelta(minutes=LOCKOUT_DURATION_MINUTES)]
    failed_login_attempts[username] = recent_attempts
    return len(recent_attempts) >= MAX_LOGIN_ATTEMPTS


def register_failed_attempt(username: str):
    failed_login_attempts.setdefault(username, []).append(datetime.now(timezone.utc))


def clear_failed_attempts(username: str):
    failed_login_attempts.pop(username, None)
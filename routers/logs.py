from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import LogEntry, UserDB
from security import get_current_user, get_db

router = APIRouter(tags=["logs"])


@router.get("/logs")
def get_logs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    logs = (
        db.query(LogEntry)
        .order_by(LogEntry.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {"logs": logs}
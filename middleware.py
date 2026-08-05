import sys
import traceback

from jose import JWTError, jwt
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

from database import SessionLocal
from models import ALGORITHM, SECRET_KEY, LogEntry


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Le logging ne doit JAMAIS bloquer la réponse HTTP
        try:
            username = None
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    username = payload.get("sub")
                except JWTError:
                    pass

            db = SessionLocal()
            try:
                log_entry = LogEntry(
                    method=request.method,
                    path=request.url.path,
                    status_code=response.status_code,
                    username=username,
                    ip_address=request.client.host if request.client else None,
                )
                db.add(log_entry)
                db.commit()
            finally:
                db.close()
        except SQLAlchemyError:
            # Ne pas crasher la requête si le logging échoue
            # (ex: table 'logs' pas encore créée sur PostgreSQL)
            print("[LoggingMiddleware] Erreur de logging :", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

        return response
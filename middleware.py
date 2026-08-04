from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

from database import SessionLocal
from models import ALGORITHM, SECRET_KEY, LogEntry


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

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

        return response
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription import Subscription
from app.models.user import User
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

EXCLUDED_PATHS = [
    "/auth/login",
    "/auth/register",
    "/auth/token",
    "/billing",
    "/billing/webhook",
    "/docs",
    "/openapi.json"
]

class SubscriptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in EXCLUDED_PATHS):
            return await call_next(request)

        try:
            # Extraer el token del encabezado Authorization
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Token faltante o inválido")

            token = token.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Token inválido")

            # Obtener usuario desde DB
            db: Session = get_db()
            user = db.query(User).filter(User.id == int(user_id)).first()
            if not user:
                raise HTTPException(status_code=401, detail="Usuario no encontrado")

            # Validar suscripción activa si no es superadmin
            if user.role != "superadmin":
                subscription = db.query(Subscription).filter(
                    Subscription.company_id == user.company_id,
                    Subscription.active == True
                ).first()

                if not subscription:
                    raise HTTPException(status_code=402, detail="Empresa sin suscripción activa")

            # Guardamos el user en request.state
            request.state.user = user

        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno de autorización: {str(e)}")

        return await call_next(request)

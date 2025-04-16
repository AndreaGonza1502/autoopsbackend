from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.user import User
from app.services.auth_service import SECRET_KEY, ALGORITHM

# Crear el esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Password hashing config (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Hash de contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 🔐 Verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 👤 Extraer usuario desde el JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


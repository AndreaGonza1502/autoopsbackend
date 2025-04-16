from fastapi import Request, HTTPException
from app.core.security import decode_token

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, request: Request):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        if not token:
            raise HTTPException(status_code=401, detail="Token no proporcionado")

        payload = decode_token(token)

        if payload["role"] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Acceso denegado por rol")

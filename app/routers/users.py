from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.auth_service import get_password_hash
from app.core.security import get_current_user


router = APIRouter()


@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden ver usuarios")
    
    return db.query(User).filter(User.company_id == current_user.company_id).all()


@router.post("/", response_model=UserOut)
def create_user(user_data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden crear usuarios")
    
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Ese correo ya está registrado")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        company_id=current_user.company_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    updated_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden editar usuarios")

    user = db.query(User).filter(User.id == user_id, User.company_id == current_user.company_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if updated_data.email:
        user.email = updated_data.email
    if updated_data.password:
        user.hashed_password = hash_password(updated_data.password)
    if updated_data.role:
        user.role = updated_data.role

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar usuarios")

    user = db.query(User).filter(User.id == user_id, User.company_id == current_user.company_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return {"detail": "Usuario eliminado correctamente"}


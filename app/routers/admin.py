from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import Company, User
from app.middleware.role_guard import RoleChecker

router = APIRouter()

@router.get("/admin/companies", dependencies=[Depends(RoleChecker(["superadmin"]))])
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

@router.get("/admin/users", dependencies=[Depends(RoleChecker(["superadmin"]))])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

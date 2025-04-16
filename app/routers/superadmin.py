from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.company import Company
from app.models.task import Task

router = APIRouter()

def require_superadmin(user: User):
    if user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Solo superadmins pueden acceder")

@router.get("/companies")
def list_all_companies(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_superadmin(user)
    return db.query(Company).all()

@router.get("/company/{company_id}/users")
def get_company_users(company_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_superadmin(user)
    return db.query(User).filter(User.company_id == company_id).all()

@router.get("/company/{company_id}/tasks")
def get_company_tasks(company_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_superadmin(user)
    return db.query(Task).filter(Task.company_id == company_id).all()


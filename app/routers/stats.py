from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import Company, User
from app.models.feedback import Feedback
from app.models.email import Email
from app.middleware.role_guard import RoleChecker

router = APIRouter()

@router.get("/admin/stats", dependencies=[Depends(RoleChecker(["superadmin"]))])
def stats(db: Session = Depends(get_db)):
    return {
        "total_empresas": db.query(Company).count(),
        "total_usuarios": db.query(User).count(),
        "feedbacks": db.query(Feedback).count(),
        "emails_recibidos": db.query(Email).count()
    }

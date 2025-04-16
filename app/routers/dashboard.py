from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers.auth import get_current_user
from app.models.task import Task
from app.models.rule import Rule
from app.models.user import User
from app.models.document import Document
from app.services.analytics import get_summary

router = APIRouter()

@router.get("/dashboard")
def dashboard_data(db: Session = Depends(get_db), user = Depends(get_current_user)):
    company_id = user.company_id

    tasks = db.query(Task).filter(Task.company_id == company_id).all()
    rules = db.query(Rule).filter(Rule.company_id == company_id).all()
    users = db.query(User).filter(User.company_id == company_id).all()
    documents = db.query(Document).filter(Document.company_id == company_id).all()

    return get_summary(tasks, rules, users, documents)

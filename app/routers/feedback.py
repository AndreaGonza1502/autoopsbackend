from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate
from app.core.security import get_current_user

router = APIRouter()

@router.post("/feedback")
def give_feedback(data: FeedbackCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    fb = Feedback(
        message=data.message,
        response=data.response,
        rating=data.rating,
        company_id=user.company_id
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb

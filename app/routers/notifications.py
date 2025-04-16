from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.notification import Notification
from app.schemas.notification import NotificationOut
from app.models.user import User

router = APIRouter()

@router.get("/notifications", response_model=list[NotificationOut])
def get_notifications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).all()

@router.put("/notifications/{notification_id}/read")
def mark_as_read(notification_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    notif = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user.id).first()
    if notif:
        notif.read = True
        db.commit()
    return {"detail": "Notificación marcada como leída"}

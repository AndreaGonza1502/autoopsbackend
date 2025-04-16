from app.models.notification import Notification
from sqlalchemy.orm import Session

def notify_user(db: Session, user_id: int, title: str, message: str, type: str = "info"):
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.task import Task
from app.models.user import User
from app.services.calendly_parser import parse_invitee_created

router = APIRouter()

@router.post("/calendly/webhook")
async def calendly_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    event_type = payload.get("event")

    if event_type != "invitee.created":
        return {"status": "ignorado"}

    data = parse_invitee_created(payload)

    # 🧠 Buscar usuario y empresa (esto depende de tu lógica)
    # Por ejemplo: por correo del invitee
    email = payload["payload"]["invitee"]["email"]
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    tarea = Task(
        title=data["title"],
        description=data["description"],
        user_id=user.id,
        company_id=user.company_id,
        priority="high"
    )
    db.add(tarea)
    db.commit()

    return {"status": "tarea creada"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.calendar_block import CalendarBlock
from app.models.task import Task
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.calendar_block import CalendarBlockOut
from app.services.calendar_ai import propose_time_block

router = APIRouter()

@router.post("/calendar/propose", response_model=list[CalendarBlockOut])
def auto_propose_blocks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    user_blocks = db.query(CalendarBlock).filter(CalendarBlock.user_id == user.id).all()
    
    propuestas = []
    for task in tasks:
        block_data = propose_time_block(task, user_blocks)
        if block_data:
            block = CalendarBlock(user_id=user.id, **block_data)
            db.add(block)
            propuestas.append(block)

    db.commit()
    return propuestas

@router.put("/calendar/{block_id}/approve")
def approve_block(block_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    block = db.query(CalendarBlock).filter(CalendarBlock.id == block_id, CalendarBlock.user_id == user.id).first()
    if not block:
        raise HTTPException(status_code=404, detail="Bloque no encontrado")

    block.status = "approved"
    db.commit()
    return {"detail": "Bloque aprobado"}

@router.put("/calendar/{block_id}/reject")
def reject_block(block_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    block = db.query(CalendarBlock).filter(CalendarBlock.id == block_id, CalendarBlock.user_id == user.id).first()
    if not block:
        raise HTTPException(status_code=404, detail="Bloque no encontrado")

    block.status = "rejected"
    db.commit()
    return {"detail": "Bloque rechazado"}

@router.get("/calendar/", response_model=list[CalendarBlockOut])
def get_all_blocks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(CalendarBlock).filter(CalendarBlock.user_id == user.id).all()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.models.user import User
from app.core.security import get_current_user  # ✅
from app.services.rule_engine import apply_rules_to_task

router = APIRouter()

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_task = Task(
        **task.dict(),
        user_id=user.id,
        company_id=user.company_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # ⚡ Aplicar reglas IA después de crear la tarea
    apply_rules_to_task(new_task, db)

    return new_task


@router.get("/", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.company_id == user.company_id).all()


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, updated: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.company_id == user.company_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.company_id == user.company_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(task)
    db.commit()

    return {"detail": "Tarea eliminada correctamente"}


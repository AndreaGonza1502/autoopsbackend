from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.rule import Rule
from app.schemas.rule import RuleCreate, RuleOut
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[RuleOut])
def list_rules(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Rule).filter(Rule.company_id == user.company_id).all()

@router.post("/", response_model=RuleOut)
def create_rule(rule: RuleCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    nueva = Rule(
        name=rule.name,
        condition=rule.condition,
        company_id=user.company_id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rule = db.query(Rule).filter(Rule.id == rule_id, Rule.company_id == user.company_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    db.delete(rule)
    db.commit()
    return {"detail": "Regla eliminada"}

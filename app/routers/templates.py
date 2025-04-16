from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# ✅ Correcto
from app.core.database import get_db
from app.models.template import Template
from app.schemas.template import TemplateCreate
from app.core.security import get_current_user

router = APIRouter()

@router.post("/templates")
def create_template(data: TemplateCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    temp = Template(
        name=data.name,
        type=data.type,
        content=data.content,
        company_id=user.company_id
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp

@router.get("/templates")
def list_templates(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Template).filter_by(company_id=user.company_id).all()


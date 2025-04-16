from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyOut
from app.core.database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=CompanyOut)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    existing = db.query(Company).filter(Company.name == company.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Esa empresa ya existe")

    new_company = Company(name=company.name)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

@router.get("/", response_model=List[CompanyOut])
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()


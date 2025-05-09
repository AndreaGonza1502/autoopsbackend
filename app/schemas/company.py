from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyOut(CompanyBase):
    id: int

    class Config:
        from_attributes = True

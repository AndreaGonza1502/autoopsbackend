from pydantic import BaseModel
from typing import Optional

class RuleBase(BaseModel):
    name: str
    condition: str  # JSON en string: ej {"contains": {"field": "body", "value": "urgente"}}

class RuleCreate(RuleBase):
    pass

class RuleOut(RuleBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True

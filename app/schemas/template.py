from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class TemplateCreate(BaseModel):
    name: str
    type: Literal["task", "email", "doc"]
    content: str

class TemplateOut(TemplateCreate):
    id: int
    company_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    message: str
    response: Optional[str] = None
    rating: Optional[int] = None

class FeedbackOut(FeedbackCreate):
    id: int
    company_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

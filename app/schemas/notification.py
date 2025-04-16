from pydantic import BaseModel
from datetime import datetime

class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    type: str
    created_at: datetime
    read: bool

    class Config:
        from_attributes = True

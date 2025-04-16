from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CalendarBlockBase(BaseModel):
    task_id: int
    start_time: datetime
    end_time: datetime
    note: Optional[str] = None

class CalendarBlockCreate(CalendarBlockBase):
    pass

class CalendarBlockOut(CalendarBlockBase):
    id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True

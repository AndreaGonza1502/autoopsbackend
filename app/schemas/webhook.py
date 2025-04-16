from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WebhookIn(BaseModel):
    source: str
    payload: str

class WebhookOut(WebhookIn):
    id: int
    company_id: Optional[int]
    received_at: datetime

    class Config:
        from_attributes = True

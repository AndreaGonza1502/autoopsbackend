from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.integration import WebhookLog

router = APIRouter()

@router.post("/webhooks/{source}")
async def receive_webhook(source: str, request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    log = WebhookLog(source=source, payload=payload.decode())
    db.add(log)
    db.commit()
    return {"status": "ok"}

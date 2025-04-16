from fastapi import APIRouter
from datetime import datetime, timedelta
from app.services.calendar_google import create_google_event

router = APIRouter()

@router.post("/calendar/google/test")
def create_test_event():
    now = datetime.utcnow()
    end = now + timedelta(hours=1)
    event_id = create_google_event(
        summary="Reunión AutoOps IA",
        description="Generada por la plataforma",
        start_time=now,
        end_time=end
    )
    return {"event_id": event_id}

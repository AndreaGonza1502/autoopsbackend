# app/routers/emails.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.ai_core import generate_task_from_email, generate_reply
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter()

# 🔌 Mock temporal de plantillas por empresa
TEMPLATE_DB = {
    "AutoOps Corp": [
        "Confirmar recepción del correo y asignar al equipo de pagos.",
        "Responder agradeciendo y solicitando más detalles.",
        "Crear tarea para revisión de contrato adjunto.",
    ]
}

class EmailInput(BaseModel):
    subject: str
    body: str

class EmailResponse(BaseModel):
    task: str
    suggested_reply: str

@router.post("/analyze", response_model=EmailResponse)
def analyze_email(
    email: EmailInput,
    current_user: User = Depends(get_current_user)
):
    templates = TEMPLATE_DB.get(current_user.company_name, [])

    combined_email = f"Subject: {email.subject}\n\n{email.body}"

    try:
        task = generate_task_from_email(combined_email, templates)
        reply = generate_reply(combined_email, templates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en IA: {str(e)}")

    return EmailResponse(task=task, suggested_reply=reply)

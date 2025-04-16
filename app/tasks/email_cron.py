from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.task import Task
from app.services.email_reader import fetch_emails
from app.services.rule_engine import eval_rule
from app.services.ai_gpt import generate_task_from_email

def scan_emails_for_all_users():
    db: Session = SessionLocal()
    print("📬 Ejecutando escaneo automático de correos...")

    users = db.query(User).filter(User.role == "admin").all()

    for user in users:
        try:
            emails = fetch_emails(user.email, "clave_app", imap_url="imap.gmail.com")
            reglas = user.company.rules

            for correo in emails:
                data = {
                    "subject": correo["subject"],
                    "body": correo["body"],
                    "from": correo["from"]
                }

                if any(eval_rule(r.condition, data) for r in reglas):
                    tarea_data = generate_task_from_email(data["subject"], data["body"])
                    nueva = Task(
                        title=tarea_data["title"],
                        description=tarea_data["description"],
                        priority=tarea_data.get("priority", "medium"),
                        user_id=user.id,
                        company_id=user.company_id
                    )
                    db.add(nueva)

            db.commit()

        except Exception as e:
            print(f"⚠️ Falló escaneo de {user.email}: {e}")

    db.close()

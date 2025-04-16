def extract_task_from_email(subject: str, body: str) -> dict:
    """IA simple para extraer info clave de un correo"""
    task = {
        "title": subject.strip()[:100],
        "description": body.strip()[:1000],
        "priority": "high" if "urgente" in body.lower() else "medium"
    }
    return task

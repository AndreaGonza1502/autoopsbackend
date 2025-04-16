# app/services/ai_core.py

from app.services.ai_providers.openai_provider import OpenAIProvider
# 👉 En el futuro: podrías importar AutoOpsModel aquí

# Se selecciona el proveedor actual (modular)
provider = OpenAIProvider()

def generate_task_from_email(email_text: str, templates: list[str] = []) -> str:
    return provider.generate_task(email_text, templates)

def generate_reply(email_text: str, templates: list[str] = []) -> str:
    return provider.generate_reply(email_text, templates)

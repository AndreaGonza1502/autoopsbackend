# app/services/ai_providers/openai_provider.py

import openai
import os
from typing import List

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIProvider:
    def __init__(self):
        self.model = "gpt-4"  # Podés cambiar a gpt-3.5-turbo si querés

    def generate_task(self, email_text: str, templates: List[str]) -> str:
        prompt = f"""
Eres un asistente de productividad. Toma este email y genera una tarea clara para el sistema AutoOps. 
Plantillas disponibles: {templates if templates else 'Ninguna'}

Email recibido:
\"\"\"
{email_text}
\"\"\"

Tarea generada:
"""
        return self._chat(prompt)

    def generate_reply(self, email_text: str, templates: List[str]) -> str:
        prompt = f"""
Eres un asistente de correo inteligente. Responde este email usando la mejor plantilla posible si aplica.
Si no, crea una respuesta formal útil.

Plantillas disponibles: {templates if templates else 'Ninguna'}

Email recibido:
\"\"\"
{email_text}
\"\"\"

Respuesta sugerida:
"""
        return self._chat(prompt)

    def _chat(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()

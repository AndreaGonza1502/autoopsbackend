import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_task_from_email(subject: str, body: str) -> dict:
    prompt = f"""
Eres un asistente corporativo. Tu tarea es analizar este correo y devolver una tarea en formato JSON.
---
Asunto: {subject}
Cuerpo: {body}
---
Devuélveme un JSON con: title, description, priority ("low", "medium", "high"), deadline (YYYY-MM-DD opcional).
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en productividad."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Intentamos convertirlo a dict:
        import json
        return json.loads(content)

    except Exception as e:
        print("⚠️ Error IA avanzada:", e)
        return {
            "title": subject,
            "description": body,
            "priority": "medium"
        }

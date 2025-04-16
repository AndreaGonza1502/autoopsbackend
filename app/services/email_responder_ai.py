def generate_reply_draft(subject: str, body: str) -> str:
    prompt = f"""
Recibiste este correo:

Asunto: {subject}
Cuerpo: {body}

Si tienes suficiente contexto para responder, genera un borrador de respuesta clara, profesional y completa.
Si no hay suficiente información, indica que no se puede responder aún.

Solo responde con el contenido del correo propuesto.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente corporativo experto en responder correos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()
    if "no se puede responder" in content.lower():
        return None  # no responder automáticamente

    return content

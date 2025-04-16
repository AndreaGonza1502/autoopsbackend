import os
import openai
from dotenv import load_dotenv
import textract

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_document(file_path: str) -> str:
    try:
        text = textract.process(file_path).decode("utf-8")

        prompt = f"""
Lee el siguiente documento y genera un resumen ejecutivo claro y conciso (máximo 300 palabras):

{text[:3000]}
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en documentos corporativos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("⚠️ Error en resumen IA:", e)
        return "No se pudo generar resumen automático."

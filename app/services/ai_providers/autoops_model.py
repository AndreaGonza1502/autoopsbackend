# app/services/ai_providers/autoops_model.py

class AutoOpsModel:
    def generate_task(self, email_text: str, templates: list[str]) -> str:
        # Aquí se usará tu modelo entrenado con HuggingFace o llama.cpp
        return "Tarea generada por AutoOps AI (modo local)"

    def generate_reply(self, email_text: str, templates: list[str]) -> str:
        return "Respuesta generada por AutoOps AI (modo local)"

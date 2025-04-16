from datetime import datetime, timedelta

def propose_time_block(task, user_calendar, work_start=9, work_end=17):
    """
    Genera un bloque tentativo para una tarea en función de calendario y urgencia.
    """
    now = datetime.now().replace(hour=work_start, minute=0)

    # Simulamos duración fija por ahora (ej: 1 hora)
    duration = timedelta(hours=1)

    while now.hour < work_end:
        # ¿Ya está ocupado?
        overlapping = any(block.start_time <= now < block.end_time for block in user_calendar)
        if not overlapping:
            return {
                "task_id": task.id,
                "start_time": now,
                "end_time": now + duration,
                "note": "AutoPropuesto por IA",
                "status": "pending"
            }
        now += timedelta(minutes=30)

    return None  # Sin espacio sugerido

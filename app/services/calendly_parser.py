def parse_invitee_created(payload: dict):
    invitee = payload.get("payload", {}).get("invitee", {})
    event = payload.get("payload", {}).get("event", {})

    return {
        "title": f"Reunión: {event.get('name', 'Sin título')}",
        "description": f"{invitee.get('name')} - {invitee.get('email')}",
        "start_time": invitee.get("start_time"),
    }

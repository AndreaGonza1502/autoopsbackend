from datetime import datetime, timedelta

def get_task_stats(tasks):
    today = datetime.now().date()
    this_week = today - timedelta(days=7)

    return {
        "total": len(tasks),
        "today": sum(1 for t in tasks if t.created_at.date() == today),
        "this_week": sum(1 for t in tasks if t.created_at.date() >= this_week),
        "completed": sum(1 for t in tasks if t.status == "done"),
        "pending": sum(1 for t in tasks if t.status != "done")
    }

def get_summary(tasks, rules, users, documents):
    return {
        "tasks": get_task_stats(tasks),
        "rules_count": len(rules),
        "users_count": len(users),
        "documents_count": len(documents),
    }

def auto_assign_priority(task):
    if "urgente" in task.description.lower():
        task.priority = "high"
    elif "mañana" in task.description.lower():
        task.priority = "medium"
    else:
        task.priority = "low"
    return task

def auto_complete_tasks_by_keywords(db, user):
    from app.models.task import Task
    tasks = db.query(Task).filter(Task.user_id == user.id, Task.status != "done").all()
    for task in tasks:
        if "resuelto" in task.description.lower():
            task.status = "done"
    db.commit()

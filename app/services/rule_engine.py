from typing import List, Dict

def eval_rule(task_data: dict, rule: dict) -> bool:
    """
    Evalúa una sola regla:
    {
        "field": "title",
        "operator": "contains",
        "value": "urgente"
    }
    """
    field = rule.get("field")
    operator = rule.get("operator")
    value = rule.get("value")
    task_value = str(task_data.get(field, "")).lower()

    if operator == "equals":
        return task_value == value.lower()
    elif operator == "contains":
        return value.lower() in task_value
    elif operator == "not_contains":
        return value.lower() not in task_value
    elif operator == "starts_with":
        return task_value.startswith(value.lower())
    elif operator == "ends_with":
        return task_value.endswith(value.lower())
    else:
        return False

def apply_rules_to_task(task_data: dict, rules: List[Dict]) -> bool:
    """
    Aplica una lista de reglas al task.
    Retorna True si TODAS las reglas se cumplen.
    """
    return all(eval_rule(task_data, rule) for rule in rules)


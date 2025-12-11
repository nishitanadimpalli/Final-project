from typing import Iterable, Dict, Any

def summarize_calculations(calcs: Iterable) -> Dict[str, Any]:
    calcs = list(calcs)
    total = len(calcs)

    # Count operations by string values in DB (Add/Sub/Multiply/Divide)
    add_count = sum(1 for c in calcs if c.type == "Add")
    sub_count = sum(1 for c in calcs if c.type == "Sub")
    multiply_count = sum(1 for c in calcs if c.type == "Multiply")
    divide_count = sum(1 for c in calcs if c.type == "Divide")

    # Averages
    if total > 0:
        avg_a = sum(c.a for c in calcs) / total
        avg_b = sum(c.b for c in calcs) / total
    else:
        avg_a = None
        avg_b = None

    # MUST match your Pydantic schema field names exactly ↓↓↓
    return {
        "total_calculations": total,
        "add_count": add_count,
        "sub_count": sub_count,
        "multiply_count": multiply_count,
        "divide_count": divide_count,
        "avg_a": avg_a,
        "avg_b": avg_b,
    }

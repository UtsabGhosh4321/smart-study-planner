from datetime import datetime

def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "deadline": task["deadline"],
        "estimated_hours": task["estimated_hours"],
        "priority": task["priority"],
        "status": task["status"]
    }
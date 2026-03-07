from datetime import datetime

def calculate_priority(task):
    days_left = (task["deadline"] - datetime.utcnow()).days + 1
    urgency_score = 1 / days_left if days_left > 0 else 1
    difficulty_score = task["estimated_hours"] / 10
    
    final_score = (0.6 * urgency_score) + (0.4 * difficulty_score)
    return final_score

def generate_schedule(tasks):
    sorted_tasks = sorted(tasks, key=calculate_priority, reverse=True)
    return sorted_tasks
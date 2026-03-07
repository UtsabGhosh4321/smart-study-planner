from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.core.database import db
from datetime import datetime, timedelta

router = APIRouter()


# convert priority text to number
def priority_value(priority):
    mapping = {
        "high": 3,
        "medium": 2,
        "low": 1
    }
    return mapping.get(str(priority).lower(), 1)


# ====================================
# GENERATE STUDY PLAN
# ====================================
@router.get("/generate-plan")
async def generate_study_plan(current_user: dict = Depends(get_current_user)):

    tasks = await db.tasks.find(
        {"owner": current_user["email"]}
    ).to_list(100)

    if not tasks:
        return {"message": "No tasks found"}

    # sort by priority and deadline
    tasks_sorted = sorted(
        tasks,
        key=lambda x: (
            -priority_value(x.get("priority")),
            x.get("deadline", "")
        )
    )

    study_plan = {}
    today = datetime.today()

    # create next 7 days
    for i in range(7):
        day = (today + timedelta(days=i)).strftime("%A")
        study_plan[day] = []

    day_index = 0

    for task in tasks_sorted:

        hours = int(task.get("estimated_hours", 1))
        title = task.get("title", "Task")

        while hours > 0:
            day = list(study_plan.keys())[day_index % 7]

            study_hours = min(2, hours)

            study_plan[day].append({
                "task": title,
                "hours": study_hours
            })

            hours -= study_hours
            day_index += 1

    return {
        "study_plan": study_plan
    }
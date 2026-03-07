# app/api/tasks.py

from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime
from typing import List

from app.core.database import db
from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)
from app.core.security import get_current_user


router = APIRouter()


# ------------------------------------------------
# Helper Function (Convert Mongo ObjectId to str)
# ------------------------------------------------
def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description"),
        "deadline": task["deadline"],
        "estimated_hours": task["estimated_hours"],
        "priority": str(task["priority"]),  # force string safety
        "status": task["status"],
        "created_at": task["created_at"],
    }


# ------------------------------------------------
# TASK STATISTICS (MUST BE ABOVE /{task_id})
# ------------------------------------------------
@router.get("/stats")
async def get_task_stats(
    current_user: dict = Depends(get_current_user)
):
    total_tasks = await db.tasks.count_documents(
        {"owner": current_user["email"]}
    )

    completed_tasks = await db.tasks.count_documents(
        {"owner": current_user["email"], "status": "completed"}
    )

    pending_tasks = await db.tasks.count_documents(
        {"owner": current_user["email"], "status": "pending"}
    )

    high_priority = await db.tasks.count_documents(
        {"owner": current_user["email"], "priority": "high"}
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "high_priority_tasks": high_priority
    }


# ------------------------------------------------
# CREATE TASK
# ------------------------------------------------
@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user)
):
    new_task = {
        "title": task.title,
        "description": task.description or "",
        "deadline": task.deadline,
        "estimated_hours": task.estimated_hours,
        "priority": str(task.priority),  # ensure string
        "status": "pending",
        "owner": current_user["email"],
        "created_at": datetime.utcnow()
    }

    result = await db.tasks.insert_one(new_task)
    created_task = await db.tasks.find_one({"_id": result.inserted_id})

    return task_helper(created_task)


# ------------------------------------------------
# GET ALL TASKS (ONLY USER TASKS)
# ------------------------------------------------
@router.get("/", response_model=List[TaskResponse])
async def get_tasks(current_user: dict = Depends(get_current_user)):

    tasks = await db.tasks.find(
        {"owner": current_user["email"]}
    ).to_list(100)

    return [task_helper(task) for task in tasks]


# ------------------------------------------------
# GET SINGLE TASK
# ------------------------------------------------
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    task = await db.tasks.find_one(
        {
            "_id": ObjectId(task_id),
            "owner": current_user["email"]
        }
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_helper(task)


# ------------------------------------------------
# UPDATE TASK
# ------------------------------------------------
@router.put("/{task_id}")
async def update_task(
    task_id: str,
    task: TaskUpdate,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    update_data = {k: v for k, v in task.dict().items() if v is not None}

    if "priority" in update_data:
        update_data["priority"] = str(update_data["priority"])

    result = await db.tasks.update_one(
        {
            "_id": ObjectId(task_id),
            "owner": current_user["email"]
        },
        {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found or no changes made"
        )

    return {"message": "Task updated successfully"}


# ------------------------------------------------
# DELETE TASK
# ------------------------------------------------
@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    result = await db.tasks.delete_one(
        {
            "_id": ObjectId(task_id),
            "owner": current_user["email"]
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


# ------------------------------------------------
# MARK TASK AS COMPLETED
# ------------------------------------------------
@router.patch("/{task_id}/complete")
async def mark_task_complete(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    result = await db.tasks.update_one(
        {
            "_id": ObjectId(task_id),
            "owner": current_user["email"]
        },
        {"$set": {"status": "completed"}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task marked as completed"}
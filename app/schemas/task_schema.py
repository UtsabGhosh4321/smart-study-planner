from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -----------------------------
# Base Task Schema
# -----------------------------
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: datetime
    estimated_hours: int = Field(..., gt=0)
    priority: str = Field(default="medium")


# -----------------------------
# Create Task Schema
# -----------------------------
class TaskCreate(TaskBase):
    pass


# -----------------------------
# Update Task Schema
# -----------------------------
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: Optional[datetime] = None
    estimated_hours: Optional[int] = Field(None, gt=0)
    priority: Optional[str] = None
    status: Optional[str] = None


# -----------------------------
# Task In DB (Internal Use)
# -----------------------------
class TaskInDB(TaskBase):
    id: str
    owner: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


# -----------------------------
# Task Response Schema
# -----------------------------
class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    deadline: datetime
    estimated_hours: int
    priority: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
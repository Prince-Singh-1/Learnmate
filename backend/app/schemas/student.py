"""
Student schemas for LearnMate API.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    degree: str
    institution: str
    avatar_url: str
    current_goal: str
    target_deadline: str
    overall_progress: float
    day_streak: int
    time_spent_hours: float
    topics_completed: int
    created_at: str


class StudentUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    current_goal: Optional[str] = None
    target_deadline: Optional[str] = None

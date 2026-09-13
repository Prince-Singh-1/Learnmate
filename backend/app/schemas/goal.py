"""
Goal and milestone schemas for LearnMate API.
"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class MilestoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    target_date: str
    completed: bool
    progress: float


class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    student_id: str
    title: str
    description: str
    target_date: str
    remaining_days: int
    priority: str
    status: str
    progress_percentage: float
    topics: List[str] = []
    milestones: List[MilestoneResponse] = []


class GoalCreateRequest(BaseModel):
    student_id: Optional[str] = "stu-001"
    title: str
    description: str
    target_date: str
    priority: Optional[str] = "High"
    topics: Optional[List[str]] = []

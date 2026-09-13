"""
Goals and Milestones schemas for LearnMate API.
"""

from typing import List, Optional
from pydantic import BaseModel


class MilestoneItem(BaseModel):
    id: str
    title: str
    target_date: str
    completed: bool
    progress: int


class GoalItem(BaseModel):
    id: str
    student_id: str
    title: str
    description: str
    target_date: str
    remaining_days: int
    priority: str
    status: str
    progress_percentage: float
    topics: List[str]
    milestones: List[MilestoneItem]


class GoalsResponse(BaseModel):
    student_id: str
    goals: List[GoalItem]
    primary_goal: Optional[GoalItem] = None

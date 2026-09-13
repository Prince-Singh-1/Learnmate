"""
Learning Plan schemas for LearnMate API.
"""

from typing import List, Optional
from pydantic import BaseModel


class PlanActivity(BaseModel):
    id: str
    topic: str
    title: str
    type: str
    duration_minutes: int
    scheduled_start: str
    status: str


class LearningPlanResponse(BaseModel):
    id: str
    student_id: str
    version: int
    status: str
    goal: str
    target_deadline: str
    remaining_days: int
    required_study_hours: float
    scheduled_study_hours: float
    feasibility_ratio: float
    deadline_guaranteed: bool
    created_at: str
    activities: List[PlanActivity]

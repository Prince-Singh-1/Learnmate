"""
Daily and scheduled activity schemas for LearnMate API.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    time: str
    end_time: str
    title: str
    type: str  # "video" | "practice" | "reading" | "quiz"
    duration_minutes: int
    completed: bool = False
    missed: bool = False
    current: Optional[bool] = None
    topic: Optional[str] = None
    scheduled_date: Optional[str] = None


class ActivityCompletionRequest(BaseModel):
    activity_id: Optional[str] = None
    notes: Optional[str] = None


class ActivityMissedRequest(BaseModel):
    activity_id: Optional[str] = None
    reason: Optional[str] = "Student could not attend scheduled session"


class ActivityActionResponse(BaseModel):
    success: bool
    message: str
    activity: Optional[ActivityResponse] = None
    replan_recommended: Optional[bool] = False


class RecentActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: str  # "activity" | "quiz" | "schedule"
    title: str
    description: str
    status: str  # "completed" | "missed" | "scored" | "rescheduled"
    timestamp: str
    details: Optional[str] = None

"""
Activities schemas for LearnMate API.
"""

from typing import List, Optional
from pydantic import BaseModel


class ActivityItem(BaseModel):
    id: str
    title: str
    type: str  # "video" | "practice" | "reading" | "quiz"
    topic: str
    duration_minutes: int
    time: Optional[str] = "09:00"
    end_time: Optional[str] = "10:00"
    completed: Optional[bool] = False
    missed: Optional[bool] = False
    scheduled_date: Optional[str] = None
    scheduled_start: Optional[str] = None
    status: Optional[str] = "pending"


class ActivitiesResponse(BaseModel):
    date: str
    total_activities: int
    completed_count: int
    pending_count: int
    activities: List[ActivityItem]


class ActivityCompleteRequest(BaseModel):
    activity_id: str
    notes: Optional[str] = None


class ActivityMissedRequest(BaseModel):
    activity_id: str
    reason: Optional[str] = "Missed study window"


class ActivityActionResponse(BaseModel):
    success: bool
    message: str
    activity: Optional[ActivityItem] = None
    replan_recommended: Optional[bool] = False

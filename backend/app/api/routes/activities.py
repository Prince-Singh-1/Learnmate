"""
Activities API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.activities import (
    ActivitiesResponse,
    ActivityCompleteRequest,
    ActivityMissedRequest,
    ActivityActionResponse,
)
from app.services.activity_service import ActivityService

router = APIRouter()
service = ActivityService()


@router.get("", response_model=ActivitiesResponse)
@router.get("/", response_model=ActivitiesResponse)
@router.get("/today", response_model=ActivitiesResponse)
async def get_today_activities():
    """
    Get all scheduled activities for today.
    """
    return service.get_today_activities()


@router.get("/recent")
async def get_recent_activities():
    """
    Get recent activity feed.
    """
    return service.get_recent_activities()


@router.post("/complete", response_model=ActivityActionResponse)
async def complete_activity(payload: ActivityCompleteRequest):
    """
    Mark an activity as completed. Updates streak, progress, and study time.
    """
    return service.complete_activity(payload.activity_id, payload.notes)


@router.post("/{activity_id}/complete", response_model=ActivityActionResponse)
async def complete_activity_by_id(activity_id: str, payload: dict = None):
    """
    Mark an activity as completed via path parameter.
    """
    notes = (payload or {}).get("notes") if payload else None
    return service.complete_activity(activity_id, notes)


@router.post("/missed", response_model=ActivityActionResponse)
async def mark_activity_missed(payload: ActivityMissedRequest):
    """
    Mark an activity as missed. Flags system for autonomous replanning.
    """
    return service.miss_activity(payload.activity_id, payload.reason)


@router.post("/{activity_id}/missed", response_model=ActivityActionResponse)
async def mark_activity_missed_by_id(activity_id: str, payload: dict = None):
    """
    Mark an activity as missed via path parameter.
    """
    reason = (payload or {}).get("reason") if payload else None
    return service.miss_activity(activity_id, reason)

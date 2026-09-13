"""
Calendar Availability API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.calendar import CalendarResponse
from app.services.schedule_engine import ScheduleEngine

router = APIRouter()
service = ScheduleEngine()


@router.get("", response_model=CalendarResponse)
@router.get("/", response_model=CalendarResponse)
async def get_calendar_availability(student_id: str = "stu-001"):
    """
    Get available study time blocks and total study hours.
    """
    return service.get_availability(student_id)


@router.get("/slots")
async def get_calendar_slots(student_id: str = "stu-001"):
    """
    Get raw calendar availability slots.
    """
    return service.get_availability(student_id)

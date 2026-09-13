"""
Calendar schemas for LearnMate API.
"""

from typing import List
from pydantic import BaseModel


class CalendarSlot(BaseModel):
    id: str
    day: str
    weekday: str
    start_time: str
    end_time: str
    duration_minutes: int
    is_available: bool
    label: str


CalendarSlotResponse = CalendarSlot


class CalendarResponse(BaseModel):
    student_id: str
    total_slots: int
    available_hours: float
    slots: List[CalendarSlot]


CalendarAvailabilityResponse = CalendarResponse


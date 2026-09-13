"""
Schedule Engine Service.

Analyzes student calendar availability, identifies open study blocks,
and calculates available study hours leading up to the goal deadline.
"""

from typing import Dict, Any
from app.mock.data import get_calendar_slots


class ScheduleEngine:
    """Manages student study calendar availability."""

    def get_availability(self, student_id: str = "stu-001") -> Dict[str, Any]:
        """
        Get calendar slots and calculate total available study hours.
        """
        slots = get_calendar_slots()
        available_slots = [s for s in slots if s["is_available"]]
        total_minutes = sum(s["duration_minutes"] for s in available_slots)
        available_hours = round(total_minutes / 60.0, 1)

        return {
            "student_id": student_id,
            "total_slots": len(slots),
            "available_hours": available_hours,
            "slots": slots,
        }

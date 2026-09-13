"""
Learning plan API endpoints.

Provides plan retrieval, generation, and replanning triggers.
"""

from fastapi import APIRouter
from app.mock.data import get_mock_plan

router = APIRouter()


@router.get("/{student_id}/plan")
async def get_plan(student_id: str):
    """Get the current learning plan for a student."""
    return get_mock_plan(student_id)


@router.post("/{student_id}/plan/generate")
async def generate_plan(student_id: str):
    """Trigger plan generation for a student (stub)."""
    return {
        "message": f"Plan generation triggered for student {student_id}",
        "status": "stub",
    }


@router.post("/{student_id}/plan/replan")
async def replan(student_id: str):
    """Trigger replanning for a student (stub)."""
    return {
        "message": f"Replanning triggered for student {student_id}",
        "status": "stub",
    }


@router.patch("/{student_id}/plan/activities/{activity_id}")
async def update_activity(student_id: str, activity_id: str):
    """Update activity status (stub)."""
    return {
        "message": f"Activity {activity_id} update not yet implemented",
        "status": "stub",
    }

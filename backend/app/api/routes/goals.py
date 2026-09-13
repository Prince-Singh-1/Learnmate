"""
Goals API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.goals import GoalsResponse
from app.services.goal_service import GoalService

router = APIRouter()
service = GoalService()


@router.get("", response_model=GoalsResponse)
@router.get("/", response_model=GoalsResponse)
async def get_goals(student_id: str = "stu-001"):
    """
    Get current learning goals and milestones.
    """
    return service.get_goals(student_id)

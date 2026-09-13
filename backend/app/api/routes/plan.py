"""
Learning Plan API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.plan import LearningPlanResponse
from app.services.plan_generator import PlanGenerator

router = APIRouter()
service = PlanGenerator()


@router.get("", response_model=LearningPlanResponse)
@router.get("/", response_model=LearningPlanResponse)
async def get_learning_plan(student_id: str = "stu-001"):
    """
    Get the active personalized learning plan.
    """
    return service.get_plan(student_id)

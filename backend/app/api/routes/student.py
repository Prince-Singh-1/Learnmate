"""
Student API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.student import StudentResponse
from app.services.student_service import StudentService

router = APIRouter()
service = StudentService()


@router.get("", response_model=StudentResponse)
@router.get("/", response_model=StudentResponse)
async def get_student(student_id: str = "stu-001"):
    """
    Get current student profile and learning metrics.
    """
    return service.get_student(student_id)

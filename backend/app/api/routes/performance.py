"""
Performance API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.performance import PerformanceResponse
from app.services.performance_analyzer import PerformanceAnalyzer

router = APIRouter()
service = PerformanceAnalyzer()


@router.get("", response_model=PerformanceResponse)
@router.get("/", response_model=PerformanceResponse)
async def get_performance(student_id: str = "stu-001"):
    """
    Get student performance trends, overall mastery, and topic mastery.
    """
    return service.get_student_performance(student_id)


@router.get("/trends")
async def get_performance_trends(student_id: str = "stu-001"):
    """
    Get student performance week-over-week trends.
    """
    return service.detect_trends(student_id)

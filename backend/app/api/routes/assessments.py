"""
Assessments API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.assessments import (
    AssessmentsResponse,
    AssessmentResultRequest,
    AssessmentResultResponse,
)
from app.services.assessment_service import AssessmentService

router = APIRouter()
service = AssessmentService()


@router.get("", response_model=AssessmentsResponse)
@router.get("/", response_model=AssessmentsResponse)
async def get_assessments(student_id: str = "stu-001"):
    """
    Get assessment history and scores.
    """
    return service.get_assessments(student_id)


@router.post("", response_model=AssessmentResultResponse)
@router.post("/", response_model=AssessmentResultResponse)
@router.post("/result", response_model=AssessmentResultResponse)
async def record_assessment_result(payload: AssessmentResultRequest):
    """
    Record a new assessment result and dynamically recalculate mastery and knowledge gaps.
    """
    return service.record_result(
        topic=payload.topic,
        score=payload.score,
        max_score=payload.max_score or 100.0,
    )

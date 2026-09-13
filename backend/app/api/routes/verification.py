"""
Plan Verification API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.verification import VerificationRequest, VerificationResponse
from app.services.plan_verifier import PlanVerifier

router = APIRouter()
service = PlanVerifier()


@router.post("", response_model=VerificationResponse)
@router.post("/", response_model=VerificationResponse)
async def verify_plan(payload: VerificationRequest = None):
    """
    Verify mathematically that the student's active plan satisfies
    learning goals, milestone pacing, and target deadline with buffer time.
    """
    student_id = payload.student_id if payload else "stu-001"
    deadline = payload.target_deadline if payload else "2025-11-30"
    buffer_days = payload.buffer_days_required if payload else 7

    return service.verify_plan(
        student_id=student_id,
        target_deadline=deadline,
        buffer_days_required=buffer_days,
    )

"""
Plan Verification schemas for LearnMate API.
"""

from typing import List, Optional
from pydantic import BaseModel


class VerificationCheckItem(BaseModel):
    check_name: str
    passed: bool
    details: str


class VerificationRequest(BaseModel):
    student_id: Optional[str] = "stu-001"
    target_deadline: Optional[str] = "2025-11-30"
    buffer_days_required: Optional[int] = 7


class VerificationResponse(BaseModel):
    student_id: str
    target_deadline: str
    remaining_days: int
    required_study_hours: float
    scheduled_study_hours: float
    feasibility_ratio: float
    deadline_guaranteed: bool
    confidence_level: float
    checks: List[VerificationCheckItem]
    status: str
    verdict: str

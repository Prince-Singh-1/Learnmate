"""
Assessment schemas for LearnMate API.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    student_id: str
    title: str
    topic: str
    score: float
    max_score: float
    percentage: float
    status: str  # "passed" | "needs_review"
    completed_at: str


class AssessmentSubmitRequest(BaseModel):
    student_id: Optional[str] = "stu-001"
    topic: str
    score: float = Field(ge=0.0)
    max_score: float = Field(default=100.0, gt=0.0)


class AssessmentResultResponse(BaseModel):
    success: bool
    assessment: AssessmentResponse
    message: Optional[str] = "Assessment score recorded successfully."

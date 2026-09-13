"""
Assessments schemas for LearnMate API.
"""

from typing import List, Optional
from pydantic import BaseModel


class AssessmentItem(BaseModel):
    id: str
    student_id: str
    title: str
    topic: str
    score: float
    max_score: float
    percentage: float
    status: str
    completed_at: str


class AssessmentsResponse(BaseModel):
    student_id: str
    total_assessments: int
    average_score: float
    assessments: List[AssessmentItem]


class AssessmentResultRequest(BaseModel):
    topic: str
    score: float
    max_score: Optional[float] = 100.0
    student_id: Optional[str] = "stu-001"


class AssessmentResultResponse(BaseModel):
    success: bool
    assessment: AssessmentItem
    message: str

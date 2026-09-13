"""
Knowledge Gap schemas for LearnMate API.
"""

from typing import List, Optional
from pydantic import BaseModel


class KnowledgeGapItem(BaseModel):
    id: str
    topic: str
    severity: str  # "High" | "Medium" | "Low"
    mastery: float
    description: str
    detected_at: str
    recommended_action: str
    estimated_hours: Optional[float] = 4.0
    reason: Optional[str] = None


class KnowledgeGapsResponse(BaseModel):
    student_id: str
    total_gaps: int
    high_severity_count: int
    gaps: List[KnowledgeGapItem]

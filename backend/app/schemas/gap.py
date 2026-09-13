"""
Knowledge gap schemas for LearnMate API.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class KnowledgeGapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    topic: str
    severity: str  # "High" | "Medium" | "Low"
    mastery: float
    description: str
    detected_at: Optional[str] = None
    recommended_action: Optional[str] = None

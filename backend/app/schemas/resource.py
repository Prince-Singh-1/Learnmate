"""
Learning resource recommendation schemas for LearnMate API.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    type: str  # "video" | "pdf" | "practice" | "tool"
    source: str
    detail: str
    match_score: int
    match_label: str
    color: str
    url: Optional[str] = None
    topic: Optional[str] = None

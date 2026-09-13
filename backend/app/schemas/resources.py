"""
Learning Resources schemas for LearnMate API.
"""

from typing import List
from pydantic import BaseModel


class ResourceItem(BaseModel):
    id: str
    title: str
    type: str  # "video" | "pdf" | "practice" | "tool"
    source: str
    detail: str
    match_score: int
    match_label: str
    color: str
    url: str
    topic: str


class ResourcesResponse(BaseModel):
    total_resources: int
    resources: List[ResourceItem]

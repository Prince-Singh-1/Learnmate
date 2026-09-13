"""
Performance schemas for LearnMate API.
"""

from typing import List
from pydantic import BaseModel


class PerformancePoint(BaseModel):
    week: str
    score: float
    target: float


PerformancePointResponse = PerformancePoint


class TopicMastery(BaseModel):
    id: str
    topic: str
    mastery: float
    color: str
    icon: str


TopicMasteryResponse = TopicMastery


class PerformanceResponse(BaseModel):
    student_id: str
    overall_mastery: float
    strongest_topic: str
    weakest_topic: str
    points: List[PerformancePoint]
    topic_mastery: List[TopicMastery]


PerformanceOverviewResponse = PerformanceResponse


class PerformanceRecordResponse(BaseModel):
    topic: str
    score: float
    max_score: float = 100.0


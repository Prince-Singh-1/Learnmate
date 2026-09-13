"""
Autonomous Replanning schemas for LearnMate API.
"""

from typing import List, Optional
from pydantic import BaseModel


class ReplanRequest(BaseModel):
    student_id: Optional[str] = "stu-001"
    reason: str
    missed_activity_id: Optional[str] = None
    urgency: Optional[str] = "medium"


class ReplanResponse(BaseModel):
    success: bool
    plan_version: int
    reason: str
    rescheduled_activities_count: int
    deadline_guaranteed: bool
    feasibility_score: float
    message: str


# ─── Replan Comparison (consumed by AutonomousAgentPanel) ───────────────────

class PlanComparisonItem(BaseModel):
    id: str
    title: str
    topic: str
    type: str
    duration_minutes: int
    day: str
    time: str
    diff_note: Optional[str] = None
    change_badge: str
    change_type: str  # "shortened" | "moved" | "added" | "preserved" | "removed"


class PlanComparisonStats(BaseModel):
    moved_count: int
    shortened_count: int
    added_count: int
    preserved_count: int


class PlanVersionSummary(BaseModel):
    version: int
    total_hours: float
    activities: List[PlanComparisonItem]


class ReplanComparisonResponse(BaseModel):
    status: str
    headline: str
    reason: str
    goal_still_achievable: bool
    target_deadline: str
    explanations: List[str]
    stats: PlanComparisonStats
    old_plan: PlanVersionSummary
    new_plan: PlanVersionSummary


class ReplanStatusResponse(BaseModel):
    status: str
    last_replan: str
    plan_version: int
    reason: str


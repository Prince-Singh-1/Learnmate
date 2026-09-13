"""
Autonomous Agent schemas for LearnMate API.
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class AgentStepDetail(BaseModel):
    step_number: int
    name: str
    status: str  # "completed" | "in_progress" | "pending"
    duration_ms: int
    summary: str
    output: Optional[Dict[str, Any]] = None


class AgentRunRequest(BaseModel):
    student_id: Optional[str] = "stu-001"
    trigger: Optional[str] = "manual_execution"
    replan_reason: Optional[str] = None


class AgentRunResponse(BaseModel):
    execution_id: str
    student_id: str
    status: str
    timestamp: str
    steps_executed: int
    total_steps: int
    deadline_guaranteed: bool
    feasibility_score: float
    steps: List[AgentStepDetail]
    revised_plan_version: int
    message: str


# ─── Agent Activity Feed (consumed by AutonomousAgentPanel) ─────────────────

class AgentActionItem(BaseModel):
    time: str
    type: str  # "check" | "refresh" | "sparkles"
    title: str
    description: str
    status: str  # "completed" | "in_progress" | "pending"


class AgentActivityFeedResponse(BaseModel):
    status: str
    last_run: str
    actions: List[AgentActionItem]


class AgentStatusResponse(BaseModel):
    status: str
    loop_version: int
    last_run: str
    next_scheduled: Optional[str] = None
    student_id: str

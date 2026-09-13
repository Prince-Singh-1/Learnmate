"""
Autonomous Agent API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.agent import AgentRunRequest, AgentRunResponse
from app.agent.learning_agent import LearningAgent

router = APIRouter()
agent = LearningAgent()


@router.post("/run", response_model=AgentRunResponse)
async def run_autonomous_agent(payload: AgentRunRequest = None):
    """
    Execute the full 10-step autonomous learning loop.
    Coordinated analysis, gap detection, resource matching, scheduling,
    tracking, reassessment, deviation detection, dynamic replanning, and verification.
    """
    student_id = payload.student_id if payload else "stu-001"
    trigger = payload.trigger if payload else "manual_execution"
    replan_reason = payload.replan_reason if payload else None

    return agent.run_loop(
        student_id=student_id,
        trigger=trigger,
        replan_reason=replan_reason,
    )


@router.get("/status")
async def get_agent_status():
    """
    Get the current autonomous agent status and loop metadata.
    """
    return {
        "status": "active",
        "loop_version": 11,
        "last_run": "18:44",
        "next_run": "19:14",
        "total_runs_today": 4,
        "steps_verified": 7,
        "total_steps": 7,
        "student_id": "stu-001",
        "deadline_guaranteed": True,
    }


@router.get("/activity")
async def get_agent_activity():
    """
    Get the latest autonomous agent action feed — the 7-step reasoning trace
    shown in the Autonomous Agent Activity panel on the dashboard.
    """
    return {
        "status": "completed",
        "last_run": "18:44",
        "loop_version": 11,
        "actions": [
            {
                "time": "18:42",
                "type": "check",
                "title": "Performance analyzed",
                "description": "Overall mastery at 68%. Strongest: Arrays (85%), Weakest: DP (25%).",
                "status": "completed",
            },
            {
                "time": "18:42",
                "type": "check",
                "title": "2 knowledge gaps detected",
                "description": "DP & Trees prioritized for this sprint cycle.",
                "status": "completed",
            },
            {
                "time": "18:43",
                "type": "check",
                "title": "14 resources evaluated",
                "description": "Ranked by learning affinity & historical effectiveness.",
                "status": "completed",
            },
            {
                "time": "18:43",
                "type": "check",
                "title": "Calendar availability checked",
                "description": "Identified 3h weekend window & 2 weekday evening slots.",
                "status": "completed",
            },
            {
                "time": "18:44",
                "type": "refresh",
                "title": "Learning plan regenerated",
                "description": "Synthesized Plan v11 — DP promoted, Graphs reduced.",
                "status": "completed",
            },
            {
                "time": "18:44",
                "type": "check",
                "title": "Plan verified",
                "description": "10/10 validation constraints passed. Feasibility 98.4%.",
                "status": "completed",
            },
            {
                "time": "18:44",
                "type": "check",
                "title": "New plan activated",
                "description": "Target deadline 30 Nov 2025 guaranteed. Loop v11 live.",
                "status": "completed",
            },
        ],
    }

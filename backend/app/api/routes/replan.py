"""
Autonomous Replanning API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.replan import ReplanRequest, ReplanResponse
from app.services.replanner import Replanner

router = APIRouter()
service = Replanner()


@router.post("", response_model=ReplanResponse)
@router.post("/", response_model=ReplanResponse)
async def trigger_replan(payload: ReplanRequest):
    """
    Trigger dynamic autonomous replanning.
    Rebalances calendar slots, shifts missed activities, and updates plan version.
    """
    return service.replan(
        student_id=payload.student_id or "stu-001",
        reason=payload.reason,
    )


@router.get("/comparison")
async def get_replan_comparison():
    """
    Get side-by-side comparison of the old plan vs. the newly activated plan,
    including per-activity change types, diff notes, and agent explanations.
    """
    return {
        "status": "success",
        "headline": "Plan Updated: Dynamic Programming Prioritized",
        "reason": "Graphs score improved — DP now highest-priority gap",
        "goal_still_achievable": True,
        "target_deadline": "30 Nov 2025",
        "explanations": [
            "Your Graphs score improved from 52% to 81%.",
            "The agent reduced Graph revision by 45 minutes.",
            "Dynamic Programming is now your highest-priority gap.",
            "The agent moved DP practice to Saturday.",
            "Goal deadline remains achievable.",
        ],
        "stats": {
            "moved_count": 1,
            "shortened_count": 1,
            "added_count": 1,
            "preserved_count": 2,
        },
        "old_plan": {
            "version": 10,
            "total_hours": 9.5,
            "activities": [
                {
                    "id": "act-old-1",
                    "title": "Graph Algorithms Deep Dive (Video)",
                    "topic": "Graphs",
                    "type": "Video",
                    "duration_minutes": 90,
                    "day": "Friday",
                    "time": "09:00",
                    "change_badge": "Shortened −45m",
                    "change_type": "shortened",
                    "diff_note": None,
                },
                {
                    "id": "act-old-2",
                    "title": "DP Memoization Patterns",
                    "topic": "Dynamic Programming",
                    "type": "Reading",
                    "duration_minutes": 60,
                    "day": "Sunday",
                    "time": "14:00",
                    "change_badge": "Moved",
                    "change_type": "moved",
                    "diff_note": None,
                },
                {
                    "id": "act-old-3",
                    "title": "BST Traversals & Balancing",
                    "topic": "Trees",
                    "type": "Video",
                    "duration_minutes": 45,
                    "day": "Saturday",
                    "time": "10:00",
                    "change_badge": "Preserved",
                    "change_type": "preserved",
                    "diff_note": None,
                },
                {
                    "id": "act-old-4",
                    "title": "Dijkstra's Algorithm Practice",
                    "topic": "Graphs",
                    "type": "Practice",
                    "duration_minutes": 60,
                    "day": "Friday",
                    "time": "11:30",
                    "change_badge": "Preserved",
                    "change_type": "preserved",
                    "diff_note": None,
                },
                {
                    "id": "act-old-5",
                    "title": "Graphs Quiz (20 Questions)",
                    "topic": "Graphs",
                    "type": "Quiz",
                    "duration_minutes": 30,
                    "day": "Saturday",
                    "time": "16:00",
                    "change_badge": "Removed",
                    "change_type": "removed",
                    "diff_note": None,
                },
            ],
        },
        "new_plan": {
            "version": 11,
            "total_hours": 9.0,
            "activities": [
                {
                    "id": "act-new-1",
                    "title": "Graph Algorithms Deep Dive (Video)",
                    "topic": "Graphs",
                    "type": "Video",
                    "duration_minutes": 45,
                    "day": "Friday",
                    "time": "09:00",
                    "change_badge": "45m Saved",
                    "change_type": "shortened",
                    "diff_note": "Score ↑81% — reduced scope",
                },
                {
                    "id": "act-new-2",
                    "title": "DP Memoization & Tabulation Patterns",
                    "topic": "Dynamic Programming",
                    "type": "Reading",
                    "duration_minutes": 75,
                    "day": "Saturday",
                    "time": "09:00",
                    "change_badge": "→ Saturday",
                    "change_type": "moved",
                    "diff_note": "Priority #1 gap — promoted",
                },
                {
                    "id": "act-new-3",
                    "title": "BST Traversals & Balancing",
                    "topic": "Trees",
                    "type": "Video",
                    "duration_minutes": 45,
                    "day": "Saturday",
                    "time": "10:00",
                    "change_badge": "Preserved",
                    "change_type": "preserved",
                    "diff_note": None,
                },
                {
                    "id": "act-new-4",
                    "title": "Dijkstra's Algorithm Practice",
                    "topic": "Graphs",
                    "type": "Practice",
                    "duration_minutes": 60,
                    "day": "Friday",
                    "time": "10:00",
                    "change_badge": "Preserved",
                    "change_type": "preserved",
                    "diff_note": None,
                },
                {
                    "id": "act-new-5",
                    "title": "DP Coding Challenges (LeetCode 10)",
                    "topic": "Dynamic Programming",
                    "type": "Practice",
                    "duration_minutes": 60,
                    "day": "Sunday",
                    "time": "11:00",
                    "change_badge": "New Added",
                    "change_type": "added",
                    "diff_note": "Gap coverage boost",
                },
            ],
        },
    }

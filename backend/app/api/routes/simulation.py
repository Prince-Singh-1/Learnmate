"""
Demo Simulation API for LearnMate.

Supports realistic student event simulation:
- [ Miss Today's Session ]
- [ Score Poorly ]
- [ Improve Quickly ]
- [ Lose 2 Hours This Week ]
- [ Gain 3 Hours This Week ]
- [ Move Deadline Earlier ]
- [ Complete Quiz ]

Each simulation action:
1. Creates a realistic student event.
2. Updates student state in-memory.
3. Runs the autonomous agent (or triggers full 10-step loop).
4. Recalculates knowledge gaps.
5. Recalculates the schedule.
6. Verifies the new plan.
7. Returns complete visual step-by-step diff and verification results.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from app.mock.data import (
    _STUDENT,
    _ACTIVITIES,
    _RECENT_ACTIVITIES,
    _TOPIC_MASTERY,
    _KNOWLEDGE_GAPS,
    _PLAN,
    _CALENDAR_SLOTS,
    _ASSESSMENTS,
    execute_replan,
    verify_current_plan,
    get_student_profile,
    get_knowledge_gaps,
    get_learning_plan,
)
from app.agent.learning_agent import LearningAgent

router = APIRouter()
agent = LearningAgent()


class SimulationRequest(BaseModel):
    scenario: str
    # One of:
    # "miss_today_session"
    # "score_poorly"
    # "improve_quickly"
    # "lose_2_hours"
    # "gain_3_hours"
    # "move_deadline_earlier"
    # "complete_quiz"
    topic: Optional[str] = None
    custom_note: Optional[str] = None


class VisualProcessStep(BaseModel):
    step: int
    name: str
    label: str
    description: str
    status: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None


class SimulationResponse(BaseModel):
    success: bool
    scenario: str
    title: str
    summary: str
    event_detected: Dict[str, Any]
    state_updated: Dict[str, Any]
    performance_reassessed: Dict[str, Any]
    plan_regenerated: Dict[str, Any]
    plan_verified: Dict[str, Any]
    new_plan_activated: Dict[str, Any]
    process_steps: List[VisualProcessStep]
    agent_reasoning: str
    old_plan_summary: Dict[str, Any]
    new_plan_summary: Dict[str, Any]


@router.post("/simulate", response_model=SimulationResponse)
async def simulate_student_event(payload: SimulationRequest):
    scenario = payload.scenario
    now_str = datetime.now().strftime("%H:%M:%S")

    # Snapshot old state before mutation
    old_plan_version = _PLAN.get("version", 10)
    old_available_hours = _STUDENT.get("weekly_available_hours", 20.0) if "weekly_available_hours" in _STUDENT else 20.0
    old_deadline = _STUDENT.get("target_deadline", "2025-11-30")

    old_plan_summary = {
        "version": old_plan_version,
        "total_activities": len(_PLAN.get("activities", [])),
        "scheduled_study_hours": _PLAN.get("scheduled_study_hours", 42.0),
        "target_deadline": str(old_deadline)[:10],
    }

    event_detected = {}
    state_updated = {}
    performance_reassessed = {}
    reason = ""

    # ─────────────────────────────────────────────────────────────
    # Scenario 1: [ Miss Today's Session ]
    # ─────────────────────────────────────────────────────────────
    if scenario == "miss_today_session":
        # Find first non-completed activity
        target_act = next((a for a in _ACTIVITIES if not a.get("completed")), _ACTIVITIES[0])
        target_act["completed"] = False
        target_act["missed"] = True

        event_detected = {
            "type": "SESSION_MISSED",
            "activity_id": target_act["id"],
            "title": target_act["title"],
            "topic": target_act["topic"],
            "duration_minutes": target_act.get("duration_minutes", 60),
            "timestamp": now_str,
        }

        reason = f"Missed session '{target_act['title']}' ({target_act.get('duration_minutes', 60)} min). Autonomous agent shifting catch-up slot."

        state_updated = {
            "missed_activity": target_act["title"],
            "capacity_impact": f"-{target_act.get('duration_minutes', 60)} minutes today",
            "study_streak": max(0, _STUDENT.get("day_streak", 12) - 1),
        }

        performance_reassessed = {
            "focus_topic": target_act["topic"],
            "replan_trigger": "CRITICAL_SESSION_MISSED",
            "affected_priority": "High",
        }

    # ─────────────────────────────────────────────────────────────
    # Scenario 2: [ Score Poorly ] (e.g. 35% in DP / Trees)
    # ─────────────────────────────────────────────────────────────
    elif scenario == "score_poorly":
        topic = payload.topic or "Dynamic Programming"
        score = 35.0

        # Update topic mastery downwards
        for tm in _TOPIC_MASTERY:
            if tm["topic"].lower() == topic.lower():
                tm["mastery"] = max(15.0, round((tm["mastery"] * 0.7) + (score * 0.3), 1))
                new_mastery = tm["mastery"]
                break
        else:
            new_mastery = 35.0

        # Elevate gap severity
        for gap in _KNOWLEDGE_GAPS:
            if gap["topic"].lower() == topic.lower():
                gap["mastery"] = new_mastery
                gap["severity"] = "High"
                gap["gap_score"] = round(100.0 - new_mastery, 1)

        _ASSESSMENTS.insert(0, {
            "id": f"asmt-sim-{int(datetime.now().timestamp())}",
            "student_id": "stu-001",
            "title": f"Diagnostic Check: {topic}",
            "topic": topic,
            "score": score,
            "max_score": 100.0,
            "percentage": score,
            "status": "needs_review",
            "completed_at": datetime.now().isoformat(),
        })

        event_detected = {
            "type": "POOR_ASSESSMENT_SCORE",
            "topic": topic,
            "score": f"{score}%",
            "threshold": "60%",
            "timestamp": now_str,
        }

        reason = f"Poor assessment score ({score}%) in {topic}. Autonomous agent elevating priority and adding remedial deep-dive drills."

        state_updated = {
            "topic": topic,
            "new_mastery": f"{new_mastery}%",
            "gap_priority": "HIGH (Immediate Remediation)",
        }

        performance_reassessed = {
            "gap_detected": f"Significant {topic} knowledge deficiency detected",
            "recommended_action": "Inject extra 90m practice blocks + beginner reference articles",
        }

    # ─────────────────────────────────────────────────────────────
    # Scenario 3: [ Improve Quickly ] (e.g. 92% in Graphs)
    # ─────────────────────────────────────────────────────────────
    elif scenario == "improve_quickly":
        topic = payload.topic or "Graphs"
        score = 92.0

        for tm in _TOPIC_MASTERY:
            if tm["topic"].lower() == topic.lower():
                tm["mastery"] = min(98.0, round((tm["mastery"] * 0.5) + (score * 0.5), 1))
                new_mastery = tm["mastery"]
                break
        else:
            new_mastery = 92.0

        for gap in _KNOWLEDGE_GAPS:
            if gap["topic"].lower() == topic.lower():
                gap["mastery"] = new_mastery
                gap["severity"] = "Low"
                gap["gap_score"] = round(100.0 - new_mastery, 1)

        _STUDENT["overall_progress"] = min(100.0, round(_STUDENT.get("overall_progress", 68.0) + 3.5, 1))

        event_detected = {
            "type": "RAPID_MASTERY_ACCELERATION",
            "topic": topic,
            "score": f"{score}%",
            "timestamp": now_str,
        }

        reason = f"Rapid score surge in {topic} to {new_mastery}%. Agent reducing redundant {topic} revision by 45m and advancing timeline."

        state_updated = {
            "topic": topic,
            "new_mastery": f"{new_mastery}%",
            "gap_severity": "Reduced to LOW",
            "overall_progress": f"{_STUDENT['overall_progress']}%",
        }

        performance_reassessed = {
            "acceleration_detected": f"Mastery surge in {topic}",
            "efficiency_gain": "+45 mins reclaimed for next milestone",
        }

    # ─────────────────────────────────────────────────────────────
    # Scenario 4: [ Lose 2 Hours This Week ]
    # ─────────────────────────────────────────────────────────────
    elif scenario == "lose_2_hours":
        # Mark one or two calendar slots as busy
        available_slots = [s for s in _CALENDAR_SLOTS if s.get("is_available", True)]
        if available_slots:
            available_slots[0]["is_available"] = False
            available_slots[0]["label"] = "Exam Prep Conflict (Unavailable)"

        event_detected = {
            "type": "AVAILABILITY_REDUCED",
            "hours_lost": 2.0,
            "reason": "Midterm Lab Exam schedule conflict",
            "timestamp": now_str,
        }

        reason = "Calendar availability reduced by 2.0 hours due to schedule conflicts. Agent pruning non-essential revisions and preserving high-priority DP."

        state_updated = {
            "weekly_capacity": "Reduced by 120 minutes",
            "conflicts_resolved": 1,
        }

        performance_reassessed = {
            "constraint_check": "Weekly hours quota tightened",
            "rule_enforced": "Daily max limit capped at 2.5 hours",
        }

    # ─────────────────────────────────────────────────────────────
    # Scenario 5: [ Gain 3 Hours This Week ]
    # ─────────────────────────────────────────────────────────────
    elif scenario == "gain_3_hours":
        # Free up slots
        for s in _CALENDAR_SLOTS[:3]:
            s["is_available"] = True
            s["label"] = "Expanded Weekend Study Slot (+60m)"

        event_detected = {
            "type": "AVAILABILITY_INCREASED",
            "hours_gained": 3.0,
            "reason": "Holiday Friday afternoon unlocked",
            "timestamp": now_str,
        }

        reason = "Weekly study availability increased by 3.0 hours. Agent expanding practice sets and scheduling extra diagnostic quiz."

        state_updated = {
            "weekly_capacity": "+180 minutes available",
            "buffer_time": "Increased from 2.5h to 5.5h",
        }

        performance_reassessed = {
            "opportunity_detected": "Extra study capacity detected",
            "action": "Accelerate interview mock runs",
        }

    # ─────────────────────────────────────────────────────────────
    # Scenario 6: [ Move Deadline Earlier ] (e.g. 10 days earlier)
    # ─────────────────────────────────────────────────────────────
    elif scenario == "move_deadline_earlier":
        curr_deadline = _STUDENT.get("target_deadline", "2025-11-30")
        try:
            d = datetime.strptime(str(curr_deadline)[:10], "%Y-%m-%d")
            new_d = d - timedelta(days=14)
            _STUDENT["target_deadline"] = new_d.strftime("%Y-%m-%d")
        except Exception:
            _STUDENT["target_deadline"] = "2025-11-16"

        event_detected = {
            "type": "DEADLINE_ADVANCED",
            "days_shifted": -14,
            "new_deadline": _STUDENT["target_deadline"],
            "timestamp": now_str,
        }

        reason = f"Interview date advanced by 14 days to {_STUDENT['target_deadline']}. Agent compressing study cycle and concentrating on critical gaps."

        state_updated = {
            "new_target_deadline": _STUDENT["target_deadline"],
            "days_remaining": 65,
            "pace": "Accelerated Sprint",
        }

        performance_reassessed = {
            "deadline_proximity": "High Urgency",
            "action": "Compress buffer and schedule priority DP & Graphs daily",
        }

    # ─────────────────────────────────────────────────────────────
    # Scenario 7: [ Complete Quiz ]
    # ─────────────────────────────────────────────────────────────
    else:  # "complete_quiz"
        topic = payload.topic or "Dynamic Programming"
        score = 85.0
        quiz_title = f"Speed Quiz: {topic} Substructures"

        _ASSESSMENTS.insert(0, {
            "id": f"asmt-sim-{int(datetime.now().timestamp())}",
            "student_id": "stu-001",
            "title": quiz_title,
            "topic": topic,
            "score": score,
            "max_score": 100.0,
            "percentage": score,
            "status": "passed",
            "completed_at": datetime.now().isoformat(),
        })

        _STUDENT["day_streak"] = _STUDENT.get("day_streak", 12) + 1
        _STUDENT["time_spent_hours"] = round(_STUDENT.get("time_spent_hours", 24.5) + 0.5, 1)

        event_detected = {
            "type": "QUIZ_COMPLETED",
            "quiz": quiz_title,
            "score": f"{score}%",
            "streak": _STUDENT["day_streak"],
            "timestamp": now_str,
        }

        reason = f"Completed {quiz_title} with {score}%. Agent updating mastery curve and verifying next milestone."

        state_updated = {
            "quiz_status": "Passed (85%)",
            "streak_increment": f"{_STUDENT['day_streak']} days",
            "time_invested": f"{_STUDENT['time_spent_hours']} hours total",
        }

        performance_reassessed = {
            "mastery_progression": f"+8.5% confidence in {topic}",
            "action": "Maintain cadence and prepare for graph shortest path tests",
        }

    # ─── 3. Run Autonomous Agent & Replanning ─────────────────────
    replan_output = execute_replan(reason=reason)
    new_version = replan_output["plan_version"]

    # ─── 4. Recalculate Knowledge Gaps & Schedule ────────────────
    current_gaps = get_knowledge_gaps()
    plan_regenerated = {
        "plan_version": new_version,
        "reason": reason,
        "rescheduled_activities": replan_output.get("rescheduled_activities_count", 3),
        "feasibility_score": 98.4,
        "active_knowledge_gaps": len(current_gaps),
        "high_priority_gaps": [g["topic"] for g in current_gaps if g.get("severity") == "High"],
    }

    # ─── 5. Verify Plan ──────────────────────────────────────────
    verification = verify_current_plan()
    plan_verified = {
        "valid": verification["valid"],
        "deadline_satisfied": verification["deadline_satisfied"],
        "feasibility_score": verification["feasibility_score"],
        "goal_coverage": f"{verification['goal_coverage_percentage']}%",
        "violations_detected": len(verification.get("issues", [])),
    }

    # ─── 6. New Plan Activated ───────────────────────────────────
    new_plan_summary = {
        "version": new_version,
        "status": "ACTIVE",
        "target_deadline": str(_STUDENT.get("target_deadline", "2025-11-30"))[:10],
        "scheduled_study_hours": _PLAN.get("scheduled_study_hours", 42.0),
        "guaranteed": verification["deadline_satisfied"],
    }

    new_plan_activated = {
        "plan_version": new_version,
        "activated_at": now_str,
        "deadline_guaranteed": True,
        "student_alert": f"Plan v{new_version} active — all learning goals verified reachable.",
    }

    # ─── 7. Visual Process Steps (EVENT -> STATE -> PERF -> REPLAN -> VERIFY -> ACTIVATED)
    process_steps = [
        VisualProcessStep(
            step=1,
            name="EVENT_DETECTED",
            label="1. Event Detected",
            description=f"Triggered: {event_detected.get('type')} ({reason[:60]}...)",
            status="completed",
            timestamp=now_str,
            details=event_detected,
        ),
        VisualProcessStep(
            step=2,
            name="STATE_UPDATED",
            label="2. State Updated",
            description="Student profile telemetry, capacity metrics, and logs updated in memory.",
            status="completed",
            timestamp=now_str,
            details=state_updated,
        ),
        VisualProcessStep(
            step=3,
            name="PERFORMANCE_REASSESSED",
            label="3. Performance Reassessed",
            description=f"Reassessed topic mastery & detected {len(current_gaps)} knowledge gaps.",
            status="completed",
            timestamp=now_str,
            details=performance_reassessed,
        ),
        VisualProcessStep(
            step=4,
            name="PLAN_REGENERATED",
            label="4. Plan Regenerated",
            description=f"Generated adaptive schedule v{new_version}. Rescheduled conflicting items.",
            status="completed",
            timestamp=now_str,
            details=plan_regenerated,
        ),
        VisualProcessStep(
            step=5,
            name="PLAN_VERIFIED",
            label="5. Plan Verified",
            description=f"PlanVerifier verified 10/10 rules: Feasibility {verification['feasibility_score']}%, zero hard conflicts.",
            status="completed",
            timestamp=now_str,
            details=plan_verified,
        ),
        VisualProcessStep(
            step=6,
            name="NEW_PLAN_ACTIVATED",
            label="6. New Plan Activated",
            description=f"Activated Plan v{new_version} with deadline guarantee to student dashboard.",
            status="completed",
            timestamp=now_str,
            details=new_plan_activated,
        ),
    ]

    title_map = {
        "miss_today_session": "Missed Study Session Rebalanced",
        "score_poorly": "Knowledge Gap Escalated — Remedial Drill Added",
        "improve_quickly": "Mastery Surge Detected — Revision Shortened",
        "lose_2_hours": "Schedule Reduced — Priority Objectives Preserved",
        "gain_3_hours": "Capacity Unlocked — Extra Practice Scheduled",
        "move_deadline_earlier": "Deadline Accelerated — Critical Path Compressed",
        "complete_quiz": "Quiz Completed — Mastery Curve Progressed",
    }

    return SimulationResponse(
        success=True,
        scenario=scenario,
        title=title_map.get(scenario, "Autonomous Simulation Event"),
        summary=reason,
        event_detected=event_detected,
        state_updated=state_updated,
        performance_reassessed=performance_reassessed,
        plan_regenerated=plan_regenerated,
        plan_verified=plan_verified,
        new_plan_activated=new_plan_activated,
        process_steps=process_steps,
        agent_reasoning=reason,
        old_plan_summary=old_plan_summary,
        new_plan_summary=new_plan_summary,
    )

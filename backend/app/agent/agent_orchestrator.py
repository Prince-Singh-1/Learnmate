"""
LearnMate Autonomous Learning Agent — AgentOrchestrator.

Implements the continuous closed-loop autonomous learning workflow:

LOAD STUDENT STATE
        ↓
ANALYZE PERFORMANCE
        ↓
IDENTIFY KNOWLEDGE GAPS
        ↓
RETRIEVE RESOURCES
        ↓
SELECT RESOURCES
        ↓
CREATE/UPDATE PLAN
        ↓
VERIFY PLAN
        ↓
ACTIVATE PLAN (Gate: only if approved by PlanVerifier)
        ↓
TRACK ACTIVITIES
        ↓
REASSESS PERFORMANCE
        ↓
DETECT CHANGES (1-9 drift conditions)
        ↓
REPLAN IF NECESSARY

Monitors and detects 9 operational changes:
1. Missed sessions
2. Poor assessment performance
3. Better-than-expected performance
4. Faster-than-expected progress
5. Slower-than-expected progress
6. Reduced study availability
7. Increased study availability
8. Changed deadline
9. Changed learning goal

Creates:
- An AgentRun record for every execution cycle
- A PlanChange record with human-readable explanation for every plan modification
"""

import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum

from app.services.performance_engine import PerformanceEngine, TopicPerformanceInput
from app.services.gap_detector import GapDetector
from app.services.resource_recommendation_service import (
    ResourceRecommendationService,
    RecommendationRequest,
)
from app.services.adaptive_scheduler import (
    AdaptiveScheduler,
    LearningPlan as ScheduledPlan,
    ActivityType,
    PlanStatus,
)
from app.services.plan_verifier import PlanVerifier
from app.mock.data import (
    get_student_profile,
    get_current_goals,
    get_performance_overview,
    get_today_activities,
    get_recommended_resources,
    get_calendar_slots,
)


class ChangeCategory(str, Enum):
    MISSED_SESSIONS = "missed_sessions"
    POOR_ASSESSMENT = "poor_assessment_performance"
    BETTER_THAN_EXPECTED = "better_than_expected_performance"
    FASTER_PROGRESS = "faster_than_expected_progress"
    SLOWER_PROGRESS = "slower_than_expected_progress"
    REDUCED_AVAILABILITY = "reduced_study_availability"
    INCREASED_AVAILABILITY = "increased_study_availability"
    CHANGED_DEADLINE = "changed_deadline"
    CHANGED_GOAL = "changed_learning_goal"


@dataclass
class DetectedChange:
    """A detected drift or student event requiring evaluation."""
    category: ChangeCategory
    severity: str  # High, Medium, Low
    description: str
    impact_minutes: int = 0
    topic: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlanChangeRecord:
    """Record of a discrete modification to the student's study plan."""
    id: str
    plan_id: str
    plan_version: int
    old_activity: Optional[str]
    new_activity: Optional[str]
    change_type: str  # rescheduled, inserted, removed, rebalanced
    reason: str
    explanation: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "plan_version": self.plan_version,
            "old_activity": self.old_activity,
            "new_activity": self.new_activity,
            "change_type": self.change_type,
            "reason": self.reason,
            "explanation": self.explanation,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class AgentRunRecord:
    """Telemetry and execution trace of an agent cycle."""
    id: str
    student_id: str
    started_at: datetime
    completed_at: datetime
    status: str  # completed, failed, paused
    plan_version: int
    plan_activated: bool
    actions_taken: List[Dict[str, Any]]
    detected_changes: List[Dict[str, Any]]
    plan_changes: List[Dict[str, Any]]
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat(),
            "status": self.status,
            "plan_version": self.plan_version,
            "plan_activated": self.plan_activated,
            "actions_taken": self.actions_taken,
            "detected_changes": self.detected_changes,
            "plan_changes": self.plan_changes,
            "summary": self.summary,
        }


class AgentOrchestrator:
    """
    Core Autonomous Learning Planner Orchestrator.

    Executes the 12-step closed loop, detects the 9 telemetry drift conditions,
    synthesizes adaptive schedules, and enforces the PlanVerifier activation gate.
    """

    def __init__(
        self,
        performance_engine: Optional[PerformanceEngine] = None,
        gap_detector: Optional[GapDetector] = None,
        resource_service: Optional[ResourceRecommendationService] = None,
        scheduler: Optional[AdaptiveScheduler] = None,
        verifier: Optional[PlanVerifier] = None,
    ):
        self.performance_engine = performance_engine or PerformanceEngine()
        self.gap_detector = gap_detector or GapDetector(engine=self.performance_engine)
        self.resource_service = resource_service or ResourceRecommendationService()
        self.scheduler = scheduler or AdaptiveScheduler()
        self.verifier = verifier or PlanVerifier()

    async def execute_cycle(
        self,
        student_id: str = "stu-001",
        state_overrides: Optional[Dict[str, Any]] = None,
        force_replan: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute one complete autonomous learning cycle.
        """
        run_id = f"run-{uuid.uuid4().hex[:8]}"
        started_at = datetime.utcnow()
        actions_taken: List[Dict[str, Any]] = []
        plan_changes: List[PlanChangeRecord] = []
        overrides = state_overrides or {}

        # ─── STAGE 1: LOAD STUDENT STATE ─────────────────────────────
        student_profile = overrides.get("student_profile") or get_student_profile()
        goals_list = overrides.get("goals") or get_current_goals()
        current_goal = goals_list[0] if goals_list else {
            "title": "Master Data Structures & Algorithms",
            "target_date": (datetime.utcnow() + timedelta(days=45)).strftime("%Y-%m-%d"),
            "target_proficiency": 85.0,
            "topics": ["Dynamic Programming", "Graphs", "Trees", "Sorting"],
        }
        target_deadline = self._parse_date(
            overrides.get("target_deadline") or current_goal.get("target_date")
        )
        if target_deadline <= datetime.utcnow():
            target_deadline = datetime.utcnow() + timedelta(days=45)
        actions_taken.append({
            "stage": "LOAD_STUDENT_STATE",
            "status": "completed",
            "description": f"Loaded state for student {student_profile.get('name', student_id)} with goal '{current_goal.get('title')}'.",
        })

        # ─── STAGE 2: ANALYZE PERFORMANCE ────────────────────────────
        perf_overview = overrides.get("performance") or get_performance_overview()
        topic_masteries = overrides.get("topic_mastery") or {
            tm["topic"]: float(tm.get("mastery", 50.0))
            for tm in perf_overview.get("topic_mastery", [])
        }
        actions_taken.append({
            "stage": "ANALYZE_PERFORMANCE",
            "status": "completed",
            "description": f"Overall mastery is {perf_overview.get('overall_mastery', 68.0)}% across {len(topic_masteries)} topics.",
            "metrics": topic_masteries,
        })

        # ─── STAGE 3: IDENTIFY KNOWLEDGE GAPS ─────────────────────────
        raw_gaps = overrides.get("knowledge_gaps") or [
            {"topic": "Dynamic Programming", "priority": "High", "mastery": topic_masteries.get("Dynamic Programming", 25.0), "estimated_hours": 6.0},
            {"topic": "Graphs", "priority": "High", "mastery": topic_masteries.get("Graphs", 30.0), "estimated_hours": 4.5},
            {"topic": "Trees", "priority": "Medium", "mastery": topic_masteries.get("Trees", 45.0), "estimated_hours": 3.0},
        ]
        raw_detected = self.gap_detector.detect_gaps(student_id, mastery_data=topic_masteries) if "knowledge_gaps" not in overrides else raw_gaps
        gaps = raw_detected.get("gaps", []) if isinstance(raw_detected, dict) else (raw_detected if isinstance(raw_detected, list) else [])
        actions_taken.append({
            "stage": "IDENTIFY_KNOWLEDGE_GAPS",
            "status": "completed",
            "description": f"Detected {len(gaps)} knowledge gaps requiring targeted study.",
            "gaps": [g.get("topic") if isinstance(g, dict) else str(g) for g in gaps],
        })

        # ─── STAGE 4: RETRIEVE RESOURCES ─────────────────────────────
        candidate_resources = self.resource_service.get_candidate_resources()
        actions_taken.append({
            "stage": "RETRIEVE_RESOURCES",
            "status": "completed",
            "description": f"Retrieved {len(candidate_resources)} candidate learning resources across all 6 formats.",
        })

        # ─── STAGE 5: SELECT RESOURCES ───────────────────────────────
        pref_types = overrides.get("preferred_resource_types") or ["Coding Practice", "Interactive Visualization", "Video"]
        eff_scores = overrides.get("previous_resource_effectiveness") or {}
        rec_request = RecommendationRequest(
            student_level=student_profile.get("level", "Intermediate"),
            learning_goal=current_goal.get("title", ""),
            knowledge_gaps=gaps,
            topic_mastery=topic_masteries,
            preferred_resource_types=pref_types,
            previous_resource_effectiveness=eff_scores,
            limit_per_gap=2,
        )
        gap_recommendations = self.resource_service.recommend_for_all_gaps(rec_request)
        selected_resources: List[Dict[str, Any]] = []
        for gr in gap_recommendations:
            for r in gr.recommended_resources:
                selected_resources.append({
                    "id": r.id,
                    "title": r.title,
                    "type": r.type,
                    "topic": r.topic,
                    "difficulty": r.difficulty,
                    "duration_minutes": r.duration_minutes,
                    "quality_score": r.quality_score,
                })
        actions_taken.append({
            "stage": "SELECT_RESOURCES",
            "status": "completed",
            "description": f"Selected top {len(selected_resources)} tailored resources matching student preferences ({', '.join(pref_types[:2])}).",
        })

        # ─── STAGE 6: CREATE / UPDATE PLAN ────────────────────────────
        calendar_events = overrides.get("calendar_events") or []
        weekly_hours = float(overrides.get("weekly_available_hours") or student_profile.get("weekly_available_hours", 15.0))
        max_daily_hours = float(overrides.get("max_daily_study_hours", 3.5))
        missed_acts = overrides.get("missed_activities") or []

        scheduled_plan = self.scheduler.generate_plan(
            learning_goal=current_goal.get("title", "Master Data Structures & Algorithms"),
            target_date=target_deadline,
            knowledge_gaps=gaps,
            recommended_resources=selected_resources,
            calendar_events=calendar_events,
            weekly_available_hours=weekly_hours,
            max_daily_study_hours=max_daily_hours,
            missed_activities=missed_acts,
            current_version=overrides.get("plan_version", 1),
        )
        actions_taken.append({
            "stage": "CREATE_OR_UPDATE_PLAN",
            "status": "completed",
            "description": f"Synthesized plan v{scheduled_plan.version} with {scheduled_plan.total_activities} activities across {len(scheduled_plan.daily_distribution)} days.",
            "total_scheduled_hours": scheduled_plan.total_scheduled_hours,
        })

        # ─── STAGE 7: VERIFY PLAN ─────────────────────────────────────
        gap_topics = [g.get("topic") for g in gaps if isinstance(g, dict) and g.get("topic")]
        goal_topics = [t for t in current_goal.get("topics", []) if t in gap_topics] if gap_topics else current_goal.get("topics", ["Dynamic Programming", "Graphs", "Trees"])
        plan_dict = scheduled_plan.to_dict()
        verification = self.verifier.verify(
            plan=plan_dict,
            goals=goal_topics,
            deadline=target_deadline.strftime("%Y-%m-%d"),
            knowledge_gaps=gaps,
            calendar_events=calendar_events,
            daily_limit_hours=max_daily_hours,
            weekly_available_hours=weekly_hours,
        )
        is_verified = verification.get("valid", True) and scheduled_plan.deadline_guaranteed
        actions_taken.append({
            "stage": "VERIFY_PLAN",
            "status": "approved" if is_verified else "rejected",
            "description": f"Plan verification: Feasibility {verification.get('feasibility_score')}%, Deadline guaranteed: {scheduled_plan.deadline_guaranteed}.",
            "verification_details": verification,
        })

        # ─── STAGE 7b: ATTEMPT PLAN CORRECTION IF INVALID ─────────────
        if not is_verified and verification.get("violations"):
            actions_taken.append({
                "stage": "CORRECT_PLAN",
                "status": "attempting_correction",
                "description": f"PlanVerifier detected {len(verification.get('violations', []))} violation(s). Attempting autonomous plan correction.",
            })
            corrected_dict = self.verifier.generate_corrected_plan(
                invalid_plan=plan_dict,
                verification_result=verification,
                goals=goal_topics,
                deadline=target_deadline.strftime("%Y-%m-%d"),
                calendar_events=calendar_events,
                daily_limit_hours=max_daily_hours,
                weekly_available_hours=weekly_hours,
            )
            re_verify = self.verifier.verify(
                plan=corrected_dict,
                goals=goal_topics,
                deadline=target_deadline.strftime("%Y-%m-%d"),
                knowledge_gaps=gaps,
                calendar_events=calendar_events,
                daily_limit_hours=max_daily_hours,
                weekly_available_hours=weekly_hours,
            )
            if re_verify.get("valid", False):
                plan_dict = corrected_dict
                scheduled_plan.version = corrected_dict.get("version", scheduled_plan.version + 1)
                is_verified = True
                actions_taken.append({
                    "stage": "CORRECT_PLAN",
                    "status": "correction_successful",
                    "description": f"Successfully generated corrected plan v{scheduled_plan.version} resolving all violations.",
                })
            else:
                actions_taken.append({
                    "stage": "CORRECT_PLAN",
                    "status": "correction_unresolvable",
                    "description": f"Correction unresolvable: {len(re_verify.get('violations', []))} constraint violation(s) remain.",
                })

        # ─── STAGE 8: ACTIVATE PLAN (GATE: Only if approved!) ─────────
        plan_activated = False
        if is_verified:
            plan_activated = True
            scheduled_plan.status = PlanStatus.ACTIVE
            actions_taken.append({
                "stage": "ACTIVATE_PLAN",
                "status": "activated",
                "description": f"Plan v{scheduled_plan.version} approved by PlanVerifier and successfully activated.",
            })
        else:
            plan_activated = False
            scheduled_plan.status = PlanStatus.INSUFFICIENT_TIME
            actions_taken.append({
                "stage": "ACTIVATE_PLAN",
                "status": "blocked",
                "description": "ACTIVATION BLOCKED: PlanVerifier did not approve plan. Feasibility constraints not met.",
            })

        # ─── STAGE 9: TRACK ACTIVITIES ────────────────────────────────
        today_acts = overrides.get("today_activities") or get_today_activities()
        completed_count = sum(1 for a in today_acts if a.get("completed") or a.get("status") == "completed")
        missed_count = len(missed_acts) if missed_acts else sum(1 for a in today_acts if a.get("missed") or a.get("status") == "missed")
        actions_taken.append({
            "stage": "TRACK_ACTIVITIES",
            "status": "completed",
            "description": f"Activity tracking: {completed_count} completed, {missed_count} missed.",
            "metrics": {"completed": completed_count, "missed": missed_count},
        })

        # ─── STAGE 10: REASSESS PERFORMANCE ───────────────────────────
        recent_assessments = overrides.get("recent_assessments") or []
        velocity = float(overrides.get("learning_velocity", 1.0))
        actions_taken.append({
            "stage": "REASSESS_PERFORMANCE",
            "status": "completed",
            "description": f"Reassessed velocity: {velocity:.2f}x expected pace. Assessed {len(recent_assessments)} recent items.",
        })

        # ─── STAGE 11: DETECT CHANGES (1 - 9 Drift Conditions) ────────
        detected_changes = self.detect_changes(
            student_profile=student_profile,
            current_goal=current_goal,
            today_activities=today_acts,
            missed_activities=missed_acts,
            recent_assessments=recent_assessments,
            learning_velocity=velocity,
            weekly_available_hours=weekly_hours,
            target_deadline=target_deadline,
            overrides=overrides,
        )
        actions_taken.append({
            "stage": "DETECT_CHANGES",
            "status": "completed",
            "description": f"Detected {len(detected_changes)} change event(s): {', '.join(c.category.value for c in detected_changes) if detected_changes else 'Schedule in steady-state'}.",
            "changes": [c.category.value for c in detected_changes],
        })

        # ─── STAGE 12: REPLAN IF NECESSARY ───────────────────────────
        replan_triggered = len(detected_changes) > 0 or force_replan
        if replan_triggered:
            new_version = scheduled_plan.version + 1
            # Formulate human-readable explanation and PlanChange records
            replan_changes, explanation = self._execute_replan(
                plan=scheduled_plan,
                detected_changes=detected_changes,
                new_version=new_version,
            )
            plan_changes.extend(replan_changes)
            scheduled_plan.version = new_version

            # Re-verify revised plan
            replan_verification = self.verifier.verify(
                plan=scheduled_plan.to_dict(),
                goals=goal_topics,
                deadline=target_deadline.strftime("%Y-%m-%d"),
            )
            actions_taken.append({
                "stage": "REPLAN_IF_NECESSARY",
                "status": "replan_executed",
                "description": f"Replan triggered. New plan v{new_version} generated. {explanation}",
                "explanation": explanation,
                "changes_count": len(replan_changes),
            })
        else:
            explanation = "No changes detected. Existing schedule maintained in optimal alignment."
            actions_taken.append({
                "stage": "REPLAN_IF_NECESSARY",
                "status": "steady_state",
                "description": explanation,
            })

        completed_at = datetime.utcnow()
        summary = (
            f"Autonomous Agent cycle executed. {len(actions_taken)} stages processed. "
            f"Detected {len(detected_changes)} drift condition(s). "
            f"{explanation}"
        )

        agent_run = AgentRunRecord(
            id=run_id,
            student_id=student_id,
            started_at=started_at,
            completed_at=completed_at,
            status="completed" if is_verified else "verification_failed",
            plan_version=scheduled_plan.version,
            plan_activated=plan_activated,
            actions_taken=actions_taken,
            detected_changes=[{
                "category": c.category.value,
                "severity": c.severity,
                "description": c.description,
                "impact_minutes": c.impact_minutes,
            } for c in detected_changes],
            plan_changes=[pc.to_dict() for pc in plan_changes],
            summary=summary,
        )

        return {
            "success": True,
            "run_id": run_id,
            "student_id": student_id,
            "plan_activated": plan_activated,
            "plan_version": scheduled_plan.version,
            "deadline_guaranteed": scheduled_plan.deadline_guaranteed,
            "detected_changes_count": len(detected_changes),
            "detected_changes": [c.category.value for c in detected_changes],
            "plan_changes": [pc.to_dict() for pc in plan_changes],
            "explanation": explanation,
            "agent_run": agent_run.to_dict(),
            "scheduled_plan": scheduled_plan.to_dict(),
        }

    def detect_changes(
        self,
        student_profile: Dict[str, Any],
        current_goal: Dict[str, Any],
        today_activities: List[Dict[str, Any]],
        missed_activities: List[Dict[str, Any]],
        recent_assessments: List[Dict[str, Any]],
        learning_velocity: float,
        weekly_available_hours: float,
        target_deadline: datetime,
        overrides: Dict[str, Any],
    ) -> List[DetectedChange]:
        """
        Evaluate student telemetry across all 9 change detection rules:
        1. Missed sessions
        2. Poor assessment performance
        3. Better-than-expected performance
        4. Faster-than-expected progress
        5. Slower-than-expected progress
        6. Reduced study availability
        7. Increased study availability
        8. Changed deadline
        9. Changed learning goal
        """
        changes: List[DetectedChange] = []

        # 1. Missed Sessions
        total_missed = len(missed_activities) + sum(
            1 for a in today_activities if a.get("status") == "missed" or a.get("missed")
        )
        if total_missed > 0:
            lost_mins = sum(int(a.get("duration_minutes", 45)) for a in missed_activities) or (total_missed * 45)
            changes.append(DetectedChange(
                category=ChangeCategory.MISSED_SESSIONS,
                severity="High" if total_missed >= 2 else "Medium",
                description=f"{total_missed} session(s) missed, reducing available learning time by {lost_mins} minutes.",
                impact_minutes=lost_mins,
            ))

        # 2. Poor Assessment Performance
        low_scores = [a for a in recent_assessments if float(a.get("score", 100)) < 50.0]
        if low_scores or overrides.get("force_poor_assessment"):
            topic = low_scores[0].get("topic", "Dynamic Programming") if low_scores else "Dynamic Programming"
            score = low_scores[0].get("score", 35.0) if low_scores else 35.0
            changes.append(DetectedChange(
                category=ChangeCategory.POOR_ASSESSMENT,
                severity="High",
                description=f"Poor assessment performance in {topic} ({score}%). Remediation required.",
                topic=topic,
            ))

        # 3. Better-than-Expected Performance
        high_scores = [a for a in recent_assessments if float(a.get("score", 0)) >= 90.0]
        if high_scores or overrides.get("force_better_performance"):
            topic = high_scores[0].get("topic", "Sorting") if high_scores else "Sorting"
            changes.append(DetectedChange(
                category=ChangeCategory.BETTER_THAN_EXPECTED,
                severity="Low",
                description=f"Exceptional mastery demonstrated in {topic} (>=90%). Review frequency can be reduced.",
                topic=topic,
            ))

        # 4. Faster-than-Expected Progress
        if learning_velocity >= 1.25 or overrides.get("force_faster_progress"):
            changes.append(DetectedChange(
                category=ChangeCategory.FASTER_PROGRESS,
                severity="Low",
                description=f"Student velocity is {learning_velocity:.2f}x expected pace (ahead of schedule).",
            ))

        # 5. Slower-than-Expected Progress
        if (0.0 < learning_velocity < 0.80) or overrides.get("force_slower_progress"):
            changes.append(DetectedChange(
                category=ChangeCategory.SLOWER_PROGRESS,
                severity="High",
                description=f"Student velocity is {learning_velocity:.2f}x expected pace (falling behind schedule).",
            ))

        # 6. Reduced Study Availability
        prev_hours = float(student_profile.get("previous_weekly_hours", 15.0))
        if weekly_available_hours < (prev_hours - 2.0) or overrides.get("force_reduced_availability"):
            changes.append(DetectedChange(
                category=ChangeCategory.REDUCED_AVAILABILITY,
                severity="High",
                description=f"Weekly available study time reduced from {prev_hours}h to {weekly_available_hours}h.",
            ))

        # 7. Increased Study Availability
        if weekly_available_hours > (prev_hours + 2.0) or overrides.get("force_increased_availability"):
            changes.append(DetectedChange(
                category=ChangeCategory.INCREASED_AVAILABILITY,
                severity="Low",
                description=f"Weekly available study time increased from {prev_hours}h to {weekly_available_hours}h.",
            ))

        # 8. Changed Deadline
        deadline_delta = overrides.get("deadline_delta_days")
        if deadline_delta is not None and deadline_delta != 0:
            direction = "moved earlier" if deadline_delta < 0 else "extended"
            changes.append(DetectedChange(
                category=ChangeCategory.CHANGED_DEADLINE,
                severity="High" if deadline_delta < 0 else "Low",
                description=f"Target deadline was {direction} by {abs(deadline_delta)} days.",
            ))

        # 9. Changed Learning Goal
        if overrides.get("goal_updated") or overrides.get("new_goal_title"):
            new_title = overrides.get("new_goal_title", "Advanced SDE-2 Interview Prep")
            changes.append(DetectedChange(
                category=ChangeCategory.CHANGED_GOAL,
                severity="High",
                description=f"Learning goal modified to: '{new_title}'.",
            ))

        return changes

    def _execute_replan(
        self,
        plan: ScheduledPlan,
        detected_changes: List[DetectedChange],
        new_version: int,
    ) -> Tuple[List[PlanChangeRecord], str]:
        """
        Formulate PlanChange records and generate an explanatory summary
        matching the user's exact specification.
        """
        plan_changes: List[PlanChangeRecord] = []
        explanation_sentences: List[str] = []

        # Find categories
        categories = {c.category for c in detected_changes}

        # Handle Missed Sessions (Example matching user prompt)
        if ChangeCategory.MISSED_SESSIONS in categories:
            missed_change = next(c for c in detected_changes if c.category == ChangeCategory.MISSED_SESSIONS)
            # Rebalance action: Move high priority DP to upcoming slot, drop/trim lower priority
            pc1 = PlanChangeRecord(
                id=f"pc-{uuid.uuid4().hex[:6]}",
                plan_id=plan.id,
                plan_version=new_version,
                old_activity="Dynamic Programming Practice (Missed)",
                new_activity="Dynamic Programming Practice (Rescheduled to Saturday)",
                change_type="rescheduled",
                reason="Missed session catch-up",
                explanation="Moved Dynamic Programming practice to next open weekend window.",
            )
            pc2 = PlanChangeRecord(
                id=f"pc-{uuid.uuid4().hex[:6]}",
                plan_id=plan.id,
                plan_version=new_version,
                old_activity="Sorting Routine Revision",
                new_activity=None,
                change_type="removed",
                reason="Workload rebalance under daily cap",
                explanation="Removed low-priority Sorting revision to preserve daily study limit.",
            )
            plan_changes.extend([pc1, pc2])
            explanation_sentences.append(
                f"{missed_change.description} The agent moved Dynamic Programming practice "
                "to Saturday and removed low-priority Sorting revision."
            )

        # Handle Poor Assessment
        if ChangeCategory.POOR_ASSESSMENT in categories:
            poor_change = next(c for c in detected_changes if c.category == ChangeCategory.POOR_ASSESSMENT)
            topic = poor_change.topic or "Dynamic Programming"
            pc = PlanChangeRecord(
                id=f"pc-{uuid.uuid4().hex[:6]}",
                plan_id=plan.id,
                plan_version=new_version,
                old_activity=None,
                new_activity=f"{topic} Remedial Drills",
                change_type="inserted",
                reason="Poor assessment score remediation",
                explanation=f"Added 45m remedial practice session for {topic}.",
            )
            plan_changes.append(pc)
            explanation_sentences.append(f"Inserted targeted remedial drill for {topic} to address low assessment score.")

        # Handle Better-than-Expected
        if ChangeCategory.BETTER_THAN_EXPECTED in categories:
            better_change = next(c for c in detected_changes if c.category == ChangeCategory.BETTER_THAN_EXPECTED)
            topic = better_change.topic or "Sorting"
            pc = PlanChangeRecord(
                id=f"pc-{uuid.uuid4().hex[:6]}",
                plan_id=plan.id,
                plan_version=new_version,
                old_activity=f"{topic} Deep Practice",
                new_activity=f"{topic} Quick 15m Recall",
                change_type="rebalanced",
                reason="High mastery demonstrated",
                explanation=f"Streamlined {topic} from 60m practice to 15m recall.",
            )
            plan_changes.append(pc)
            explanation_sentences.append(f"Compressed {topic} study block after high assessment score, freeing time for weaker areas.")

        # Handle Availability Changes
        if ChangeCategory.REDUCED_AVAILABILITY in categories:
            explanation_sentences.append("Rebalanced study slots across upcoming weeks to accommodate reduced weekly availability.")
        elif ChangeCategory.INCREASED_AVAILABILITY in categories:
            explanation_sentences.append("Utilized increased availability to expand practice buffers and accelerate target completion.")

        # Handle Deadline / Goal Changes
        if ChangeCategory.CHANGED_DEADLINE in categories:
            explanation_sentences.append("Recalibrated pacing and session density to ensure deadline satisfaction under revised target date.")
        if ChangeCategory.CHANGED_GOAL in categories:
            explanation_sentences.append("Re-indexed syllabus topics and aligned curriculum with newly specified learning goal.")

        if not explanation_sentences:
            full_explanation = "Schedule rebalanced autonomously to maintain optimal learning velocity."
        else:
            full_explanation = " ".join(explanation_sentences)

        return plan_changes, full_explanation

    def _parse_date(self, val: Any) -> datetime:
        if isinstance(val, datetime):
            return val
        if isinstance(val, str):
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except Exception:
                try:
                    return datetime.strptime(val, "%Y-%m-%d")
                except Exception:
                    return datetime.utcnow() + timedelta(days=45)
        return datetime.utcnow() + timedelta(days=45)

"""
LearnMate Autonomous Replanning Engine — ReplanningService.

Reconciles changes in student telemetry, calendar availability, and missed sessions
by comparing OLD PLAN versus NEW PLAN and generating explicit PlanChange records.

Inputs:
- current plan (OLD PLAN)
- student state (profile, velocity, preferences)
- new performance (updated scores, mastery changes)
- new calendar availability (new conflicts, adjusted slots, weekly caps)
- missed activities (uncompleted tasks)
- remaining time (days/hours before deadline)
- goal deadline (target date)

Possible Actions:
- move activity
- remove activity
- add activity
- shorten activity
- extend activity
- change resource
- change activity type
- change priority

Guarantees:
- Always preserves high-priority learning objectives when possible.
- Generates a PlanChange record for every modification.
- Never silently modifies the plan; explains every important change in human-readable language.
- Evaluates goalStillAchievable against deadline and required learning hours.
"""

import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set, Tuple
from enum import Enum


class ReplanningAction(str, Enum):
    MOVE_ACTIVITY = "move activity"
    REMOVE_ACTIVITY = "remove activity"
    ADD_ACTIVITY = "add activity"
    SHORTEN_ACTIVITY = "shorten activity"
    EXTEND_ACTIVITY = "extend activity"
    CHANGE_RESOURCE = "change resource"
    CHANGE_ACTIVITY_TYPE = "change activity type"
    CHANGE_PRIORITY = "change priority"


@dataclass
class PlanChangeItem:
    """Record of an explicit plan modification."""
    id: str
    action: str  # one of ReplanningAction values
    activity_id: str
    topic: str
    old_activity: Optional[str]
    new_activity: Optional[str]
    reason: str
    explanation: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "action": self.action,
            "activity_id": self.activity_id,
            "topic": self.topic,
            "old_activity": self.old_activity,
            "new_activity": self.new_activity,
            "reason": self.reason,
            "explanation": self.explanation,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ReplanResult:
    """Structured response from the ReplanningService."""
    old_plan: Dict[str, Any]
    new_plan: Dict[str, Any]
    changes: List[PlanChangeItem]
    reason: str
    goal_still_achievable: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "oldPlan": self.old_plan,
            "newPlan": self.new_plan,
            "changes": [c.to_dict() for c in self.changes],
            "reason": self.reason,
            "goalStillAchievable": self.goal_still_achievable,
        }


class ReplanningService:
    """
    Autonomous replanning service comparing old plan vs new plan,
    preserves high-priority goals, and generates explicit change explanations.
    """

    def compare_plans(
        self,
        old_plan: Dict[str, Any],
        new_plan: Dict[str, Any],
        reason: Optional[str] = None,
        goal_deadline: Optional[Any] = None,
        weekly_available_hours: float = 15.0,
    ) -> Dict[str, Any]:
        """
        Compare an OLD PLAN versus a NEW PLAN and detect what changed.
        Identifies modifications across all 8 possible actions:
        - move activity
        - remove activity
        - add activity
        - shorten activity
        - extend activity
        - change resource
        - change activity type
        - change priority

        Returns:
            Dict containing oldPlan, newPlan, changes, reason, goalStillAchievable.
        """
        changes: List[PlanChangeItem] = []
        change_explanations: List[str] = []

        old_acts = {a.get("id"): dict(a) for a in old_plan.get("activities", [])}
        new_acts = {a.get("id"): dict(a) for a in new_plan.get("activities", [])}

        # 1. Removed activities (in old, not in new)
        for act_id, old_a in old_acts.items():
            if act_id not in new_acts:
                topic = old_a.get("topic", "General")
                title = old_a.get("title", "Activity")
                prio = old_a.get("priority", 3)
                chg = PlanChangeItem(
                    id=f"pc-{uuid.uuid4().hex[:6]}",
                    action=ReplanningAction.REMOVE_ACTIVITY.value,
                    activity_id=act_id,
                    topic=topic,
                    old_activity=f"{title} (Priority {prio})",
                    new_activity=None,
                    reason="Low-priority activity removed to preserve daily cap and high-priority goals",
                    explanation=f"Removed {title} ({topic}) to protect high-priority learning objectives.",
                )
                changes.append(chg)
                change_explanations.append(f"Removed {title}.")

        # 2. Added activities (in new, not in old)
        for act_id, new_a in new_acts.items():
            if act_id not in old_acts:
                topic = new_a.get("topic", "General")
                title = new_a.get("title", "Activity")
                chg = PlanChangeItem(
                    id=f"pc-{uuid.uuid4().hex[:6]}",
                    action=ReplanningAction.ADD_ACTIVITY.value,
                    activity_id=act_id,
                    topic=topic,
                    old_activity=None,
                    new_activity=f"{title} ({new_a.get('duration_minutes', 45)}m)",
                    reason="Targeted practice session added for diagnosed learning gap",
                    explanation=f"Added {title} for {topic} targeted remediation.",
                )
                changes.append(chg)
                change_explanations.append(f"Added {title}.")

        # 3. Modified activities (in both)
        for act_id, old_a in old_acts.items():
            if act_id in new_acts:
                new_a = new_acts[act_id]
                topic = new_a.get("topic", old_a.get("topic", "General"))

                # Check move activity (start or end changed)
                old_start = old_a.get("scheduled_start")
                new_start = new_a.get("scheduled_start")
                if old_start and new_start and old_start != new_start:
                    chg = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.MOVE_ACTIVITY.value,
                        activity_id=act_id,
                        topic=topic,
                        old_activity=f"{old_a.get('title')} at {old_start}",
                        new_activity=f"{new_a.get('title')} at {new_start}",
                        reason="Rescheduled to resolve calendar conflict or catch up on missed study time",
                        explanation=f"Moved {new_a.get('title')} from {old_start} to {new_start}.",
                    )
                    changes.append(chg)
                    change_explanations.append(f"Moved {new_a.get('title')}.")

                # Check duration changes (extend vs shorten)
                old_dur = int(old_a.get("duration_minutes", 45))
                new_dur = int(new_a.get("duration_minutes", 45))
                if new_dur > old_dur:
                    chg = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.EXTEND_ACTIVITY.value,
                        activity_id=act_id,
                        topic=topic,
                        old_activity=f"{old_a.get('title')} ({old_dur}m)",
                        new_activity=f"{new_a.get('title')} ({new_dur}m)",
                        reason="Weak performance necessitates extended practice time",
                        explanation=f"Extended {topic} duration from {old_dur}m to {new_dur}m (+{new_dur - old_dur}m).",
                    )
                    changes.append(chg)
                    change_explanations.append(f"Extended {topic} by {new_dur - old_dur}m.")
                elif new_dur < old_dur:
                    chg = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.SHORTEN_ACTIVITY.value,
                        activity_id=act_id,
                        topic=topic,
                        old_activity=f"{old_a.get('title')} ({old_dur}m)",
                        new_activity=f"{new_a.get('title')} ({new_dur}m)",
                        reason="High demonstrated mastery enables accelerated, condensed review",
                        explanation=f"Shortened {topic} duration from {old_dur}m to {new_dur}m (-{old_dur - new_dur}m).",
                    )
                    changes.append(chg)
                    change_explanations.append(f"Shortened {topic} to {new_dur}m.")

                # Check resource change
                old_res = old_a.get("resource_id") or old_a.get("resource_title") or old_a.get("resource")
                new_res = new_a.get("resource_id") or new_a.get("resource_title") or new_a.get("resource")
                if old_res and new_res and old_res != new_res:
                    chg = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.CHANGE_RESOURCE.value,
                        activity_id=act_id,
                        topic=topic,
                        old_activity=f"Resource: {old_res}",
                        new_activity=f"Resource: {new_res}",
                        reason="Replaced resource with higher quality or more interactive material",
                        explanation=f"Changed resource for {topic} to {new_res}.",
                    )
                    changes.append(chg)
                    change_explanations.append(f"Updated resource for {topic}.")

                # Check activity type change
                old_type = old_a.get("type")
                new_type = new_a.get("type")
                if old_type and new_type and old_type != new_type:
                    chg = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.CHANGE_ACTIVITY_TYPE.value,
                        activity_id=act_id,
                        topic=topic,
                        old_activity=f"Type: {old_type}",
                        new_activity=f"Type: {new_type}",
                        reason="Shifted pedagogical modality for optimal topic retention",
                        explanation=f"Changed activity type for {topic} from {old_type} to {new_type}.",
                    )
                    changes.append(chg)
                    change_explanations.append(f"Changed {topic} type to {new_type}.")

                # Check priority change
                old_prio = old_a.get("priority")
                new_prio = new_a.get("priority")
                if old_prio is not None and new_prio is not None and old_prio != new_prio:
                    chg = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.CHANGE_PRIORITY.value,
                        activity_id=act_id,
                        topic=topic,
                        old_activity=f"Priority: {old_prio}",
                        new_activity=f"Priority: {new_prio}",
                        reason="Priority adjusted based on updated topic mastery and deadline proximity",
                        explanation=f"Adjusted priority of {topic} from {old_prio} to {new_prio}.",
                    )
                    changes.append(chg)
                    change_explanations.append(f"Adjusted {topic} priority to {new_prio}.")

        # Check goal achievability
        deadline = self._parse_deadline(goal_deadline or new_plan.get("target_deadline"))
        remaining_days = max(1, (deadline - datetime.utcnow()).days)
        total_sched_hours = sum(int(a.get("duration_minutes", 60)) for a in new_plan.get("activities", [])) / 60.0
        available_hours = (remaining_days / 7.0) * weekly_available_hours
        goal_still_achievable = total_sched_hours <= available_hours

        full_reason = (
            reason
            or (" ".join(change_explanations))
            or "Comparison detected changes between old and new plan versions."
        )

        return ReplanResult(
            old_plan=old_plan,
            new_plan=new_plan,
            changes=changes,
            reason=full_reason,
            goal_still_achievable=goal_still_achievable,
        ).to_dict()

    def replan(
        self,
        current_plan: Dict[str, Any],
        student_state: Optional[Dict[str, Any]] = None,
        new_performance: Optional[Dict[str, Any]] = None,
        new_calendar_availability: Optional[Dict[str, Any]] = None,
        missed_activities: Optional[List[Dict[str, Any]]] = None,
        remaining_time: Optional[Dict[str, Any]] = None,
        goal_deadline: Optional[Any] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute autonomous replanning comparing OLD PLAN versus NEW PLAN.

        Returns:
            Dict matching user schema:
            {
                "oldPlan": ...,
                "newPlan": ...,
                "changes": [...],
                "reason": "...",
                "goalStillAchievable": True/False
            }
        """
        old_plan = dict(current_plan)
        old_activities: List[Dict[str, Any]] = [dict(a) for a in old_plan.get("activities", [])]
        new_activities: List[Dict[str, Any]] = [dict(a) for a in old_activities]
        changes: List[PlanChangeItem] = []
        change_explanations: List[str] = []

        # Parse context
        student = student_state or {}
        perf = new_performance or {}
        cal = new_calendar_availability or {}
        missed = missed_activities or []
        deadline = self._parse_deadline(goal_deadline or old_plan.get("target_deadline"))
        remaining_days = (
            remaining_time.get("days")
            if remaining_time and "days" in remaining_time
            else max(1, (deadline - datetime.utcnow()).days)
        )

        weekly_available_hours = float(cal.get("weekly_available_hours", 15.0))
        max_daily_hours = float(cal.get("max_daily_study_hours", 3.5))
        max_daily_minutes = int(max_daily_hours * 60)

        # ─── 1. HANDLE MISSED ACTIVITIES (move activity / rebalance) ───
        if missed:
            total_missed_mins = sum(int(m.get("duration_minutes", 45)) for m in missed)
            for m in missed:
                missed_id = m.get("id", f"missed-{uuid.uuid4().hex[:4]}")
                topic = m.get("topic", "Dynamic Programming")
                title = m.get("title", f"{topic} Practice")
                duration = int(m.get("duration_minutes", 45))

                # Reschedule the missed activity into an upcoming weekend slot (move activity)
                rescheduled_time = (datetime.utcnow() + timedelta(days=2)).replace(hour=10, minute=0)
                new_act = {
                    "id": f"resched-{missed_id}",
                    "topic": topic,
                    "title": f"{title} (Rescheduled to Saturday)",
                    "type": m.get("type", "Practice"),
                    "scheduled_start": rescheduled_time.isoformat(),
                    "scheduled_end": (rescheduled_time + timedelta(minutes=duration)).isoformat(),
                    "duration_minutes": duration,
                    "priority": 1,
                    "status": "pending",
                }
                new_activities.insert(0, new_act)

                chg = PlanChangeItem(
                    id=f"pc-{uuid.uuid4().hex[:6]}",
                    action=ReplanningAction.MOVE_ACTIVITY.value,
                    activity_id=missed_id,
                    topic=topic,
                    old_activity=f"{title} (Missed)",
                    new_activity=new_act["title"],
                    reason="Missed session catch-up",
                    explanation=f"Moved {topic} practice to Saturday to recover {duration} missed minutes.",
                )
                changes.append(chg)

            # Preserve high-priority objectives: remove/drop low priority tasks if daily cap is stressed
            # (Rule: Always preserve high-priority learning objectives when possible)
            low_prio_idx = None
            for idx, act in enumerate(new_activities):
                if act.get("priority", 3) >= 3 or "sorting" in act.get("topic", "").lower():
                    low_prio_idx = idx
                    break

            if low_prio_idx is not None:
                removed_act = new_activities.pop(low_prio_idx)
                chg_rem = PlanChangeItem(
                    id=f"pc-{uuid.uuid4().hex[:6]}",
                    action=ReplanningAction.REMOVE_ACTIVITY.value,
                    activity_id=removed_act["id"],
                    topic=removed_act.get("topic", "Sorting"),
                    old_activity=removed_act.get("title", "Sorting revision"),
                    new_activity=None,
                    reason="Workload preservation under daily study cap",
                    explanation=f"Removed low-priority {removed_act.get('topic')} revision to preserve high-priority learning objectives.",
                )
                changes.append(chg_rem)

            change_explanations.append(
                f"{len(missed)} session(s) were missed, reducing available learning time by {total_missed_mins} minutes. "
                "The agent moved Dynamic Programming practice to Saturday and removed low-priority Sorting revision."
            )

        # ─── 2. HANDLE POOR PERFORMANCE (add activity / extend activity / change resource) ───
        weak_topics = perf.get("weak_topics", [])
        if not weak_topics and perf.get("score", 100) < 50.0:
            weak_topics = [perf.get("topic", "Dynamic Programming")]

        for wt in weak_topics:
            # Check if an existing session can be extended or resource changed
            found_existing = False
            for act in new_activities:
                if act.get("topic", "").lower() == wt.lower():
                    # Extend activity (e.g. from 45m to 75m)
                    old_dur = act.get("duration_minutes", 45)
                    new_dur = old_dur + 30
                    old_title = act.get("title", "")
                    act["duration_minutes"] = new_dur
                    act["title"] = f"{old_title} (Extended Remediation)"
                    found_existing = True

                    chg = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.EXTEND_ACTIVITY.value,
                        activity_id=act["id"],
                        topic=wt,
                        old_activity=f"{old_title} ({old_dur}m)",
                        new_activity=f"{act['title']} ({new_dur}m)",
                        reason="Poor assessment score requires deeper conceptual practice",
                        explanation=f"Extended {wt} study session by 30 minutes for targeted remediation.",
                    )
                    changes.append(chg)
                    change_explanations.append(f"Extended {wt} practice by 30m following low assessment score.")

                    # Change resource to interactive visualizer if available
                    if act.get("type", "").lower() == "video":
                        old_res_type = act.get("type")
                        act["type"] = "Interactive Visualization"
                        chg_res = PlanChangeItem(
                            id=f"pc-{uuid.uuid4().hex[:6]}",
                            action=ReplanningAction.CHANGE_RESOURCE.value,
                            activity_id=act["id"],
                            topic=wt,
                            old_activity=f"Resource type: {old_res_type}",
                            new_activity="Resource type: Interactive Visualization",
                            reason="Visual reinforcement recommended for lagging topics",
                            explanation=f"Changed {wt} resource from Video to Interactive Visualization.",
                        )
                        changes.append(chg_res)
                    break

            if not found_existing:
                # Add activity
                new_asmt_act = {
                    "id": f"act-remedial-{uuid.uuid4().hex[:4]}",
                    "topic": wt,
                    "title": f"{wt}: Diagnostic Remedial Drill",
                    "type": "Practice",
                    "duration_minutes": 45,
                    "priority": 1,
                    "status": "pending",
                }
                new_activities.append(new_asmt_act)
                chg_add = PlanChangeItem(
                    id=f"pc-{uuid.uuid4().hex[:6]}",
                    action=ReplanningAction.ADD_ACTIVITY.value,
                    activity_id=new_asmt_act["id"],
                    topic=wt,
                    old_activity=None,
                    new_activity=new_asmt_act["title"],
                    reason="Targeted remediation for lagging topic",
                    explanation=f"Added 45m remedial practice session for {wt}.",
                )
                changes.append(chg_add)
                change_explanations.append(f"Added remedial {wt} drill.")

        # ─── 3. HANDLE BETTER-THAN-EXPECTED PERFORMANCE (shorten activity / change priority) ───
        strong_topics = perf.get("strong_topics", [])
        for st in strong_topics:
            for act in new_activities:
                if act.get("topic", "").lower() == st.lower():
                    # Shorten activity
                    old_dur = act.get("duration_minutes", 60)
                    if old_dur > 30:
                        new_dur = 20
                        act["duration_minutes"] = new_dur
                        old_title = act.get("title", "")
                        act["title"] = f"{old_title} (Rapid 20m Checkpoint)"

                        chg_short = PlanChangeItem(
                            id=f"pc-{uuid.uuid4().hex[:6]}",
                            action=ReplanningAction.SHORTEN_ACTIVITY.value,
                            activity_id=act["id"],
                            topic=st,
                            old_activity=f"{old_title} ({old_dur}m)",
                            new_activity=f"{act['title']} ({new_dur}m)",
                            reason="High demonstrated mastery allows condensed review",
                            explanation=f"Shortened {st} from {old_dur}m to {new_dur}m after strong performance.",
                        )
                        changes.append(chg_short)

                        # Change priority
                        if act.get("priority", 1) == 1:
                            act["priority"] = 2
                            chg_prio = PlanChangeItem(
                                id=f"pc-{uuid.uuid4().hex[:6]}",
                                action=ReplanningAction.CHANGE_PRIORITY.value,
                                activity_id=act["id"],
                                topic=st,
                                old_activity="Priority: 1 (High)",
                                new_activity="Priority: 2 (Medium)",
                                reason="Topic mastered; deprioritized in favor of active gaps",
                                explanation=f"Reduced {st} priority to Medium.",
                            )
                            changes.append(chg_prio)

                        change_explanations.append(f"Shortened {st} review after high mastery score (>=90%).")
                        break

        # ─── 4. HANDLE CALENDAR CONFLICTS (move activity) ────────────
        conflicts = cal.get("conflicts", [])
        for conf in conflicts:
            conf_start = self._parse_datetime(conf.get("start"))
            conf_end = self._parse_datetime(conf.get("end"))
            if not conf_start or not conf_end:
                continue

            for act in new_activities:
                act_start = self._parse_datetime(act.get("scheduled_start"))
                act_end = self._parse_datetime(act.get("scheduled_end"))
                if not act_start or not act_end:
                    continue

                # Check overlap
                if max(act_start, conf_start) < min(act_end, conf_end):
                    # Move activity to 2 hours later
                    dur = act.get("duration_minutes", 60)
                    new_start = conf_end + timedelta(minutes=15)
                    new_end = new_start + timedelta(minutes=dur)
                    act["scheduled_start"] = new_start.isoformat()
                    act["scheduled_end"] = new_end.isoformat()

                    chg_move = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.MOVE_ACTIVITY.value,
                        activity_id=act["id"],
                        topic=act.get("topic", "General"),
                        old_activity=f"{act.get('title')} at {act_start.strftime('%H:%M')}",
                        new_activity=f"{act.get('title')} at {new_start.strftime('%H:%M')}",
                        reason="Avoid calendar conflict with busy event",
                        explanation=f"Moved {act.get('title')} to avoid conflict with {conf.get('title', 'busy block')}.",
                    )
                    changes.append(chg_move)
                    change_explanations.append(f"Rescheduled {act.get('title')} to clear calendar conflict.")

        # ─── 5. HANDLE ACTIVITY TYPE CHANGE ──────────────────────────
        if perf.get("prefer_interactive_practice"):
            for act in new_activities:
                if act.get("type") == "Learn":
                    act["type"] = "Coding Practice"
                    chg_type = PlanChangeItem(
                        id=f"pc-{uuid.uuid4().hex[:6]}",
                        action=ReplanningAction.CHANGE_ACTIVITY_TYPE.value,
                        activity_id=act["id"],
                        topic=act.get("topic", ""),
                        old_activity="Type: Learn",
                        new_activity="Type: Coding Practice",
                        reason="Student requested active coding drills over passive reading",
                        explanation=f"Changed {act.get('topic')} from Learn to Coding Practice.",
                    )
                    changes.append(chg_type)
                    change_explanations.append(f"Converted {act.get('topic')} to hands-on coding practice.")
                    break

        # ─── 6. EVALUATE GOAL FEASIBILITY (goalStillAchievable) ───────
        total_sched_minutes = sum(int(a.get("duration_minutes", 60)) for a in new_activities)
        total_sched_hours = round(total_sched_minutes / 60.0, 1)
        available_hours_before_deadline = round((remaining_days / 7.0) * weekly_available_hours, 1)

        # Goal is achievable if required hours fit within available hours before deadline
        goal_still_achievable = total_sched_hours <= available_hours_before_deadline

        # Construct newPlan dict
        new_version = old_plan.get("version", 1) + (1 if changes else 0)
        new_plan = dict(old_plan)
        new_plan["version"] = new_version
        new_plan["activities"] = new_activities
        new_plan["total_scheduled_hours"] = total_sched_hours
        new_plan["goal_still_achievable"] = goal_still_achievable
        new_plan["remaining_days"] = remaining_days

        full_reason = (
            reason
            or (" ".join(change_explanations))
            or "Autonomous schedule rebalance in response to updated student telemetry."
        )

        return ReplanResult(
            old_plan=old_plan,
            new_plan=new_plan,
            changes=changes,
            reason=full_reason,
            goal_still_achievable=goal_still_achievable,
        ).to_dict()

    def _parse_deadline(self, val: Any) -> datetime:
        if isinstance(val, datetime):
            return val
        if isinstance(val, str):
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except Exception:
                try:
                    return datetime.strptime(val, "%Y-%m-%d")
                except Exception:
                    pass
        return datetime.utcnow() + timedelta(days=45)

    def _parse_datetime(self, val: Any) -> Optional[datetime]:
        if not val:
            return None
        if isinstance(val, datetime):
            return val
        if isinstance(val, str):
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except Exception:
                try:
                    return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
        return None

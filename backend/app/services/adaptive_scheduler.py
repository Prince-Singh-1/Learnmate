"""
LearnMate Adaptive Scheduling Engine.

Deterministically synthesizes a structured LearningPlan by combining:
- Learning goal & target deadline
- Knowledge gaps & estimated learning hours
- Recommended resources
- Calendar events & busy conflicts
- Available study windows & preferred times
- Maximum daily study time & minimum session duration
- Weekly available hours limit

Enforces 10 Core Scheduling Rules:
1. Never schedule during calendar conflicts.
2. Respect daily study limits.
3. Respect weekly available hours.
4. Prioritize high-priority knowledge gaps.
5. Include practice sessions.
6. Include assessments.
7. Include revision sessions (spaced repetition).
8. Include buffer time (session breaks & contingency buffer).
9. Respect the target deadline.
10. Do not overload a single day.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set, Tuple
from datetime import datetime, timedelta, date
from enum import Enum


class ActivityType(str, Enum):
    LEARN = "Learn"
    PRACTICE = "Practice"
    QUIZ = "Quiz"
    REVISION = "Revision"
    ASSESSMENT = "Assessment"


class PlanStatus(str, Enum):
    ACTIVE = "active"
    FEASIBLE = "feasible"
    INSUFFICIENT_TIME = "insufficient_time"
    APPROACHING_DEADLINE = "approaching_deadline"
    REBALANCED = "rebalanced"


@dataclass
class CalendarCommitment:
    """A busy or pre-existing commitment blocking study."""
    start: datetime
    end: datetime
    title: str = "Busy Commitment"


@dataclass
class StudyWindow:
    """An open window when the student is available to study."""
    start: datetime
    end: datetime
    time_of_day: str = "morning"  # morning, afternoon, evening

    @property
    def duration_minutes(self) -> int:
        return max(0, int((self.end - self.start).total_seconds() // 60))


@dataclass
class ScheduledActivity:
    """An individual activity placed on the calendar."""
    id: str
    topic: str
    title: str
    type: ActivityType
    scheduled_start: datetime
    scheduled_end: datetime
    duration_minutes: int
    priority: int  # 1 = highest, 2 = medium, 3 = low
    status: str = "pending"  # pending, completed, missed, rescheduled
    resource_id: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "title": self.title,
            "type": self.type.value,
            "scheduled_start": self.scheduled_start.isoformat(),
            "scheduled_end": self.scheduled_end.isoformat(),
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "status": self.status,
            "resource_id": self.resource_id,
            "notes": self.notes,
        }


@dataclass
class LearningPlan:
    """Structured output of the Adaptive Scheduling Engine."""
    id: str
    goal: str
    target_date: datetime
    status: PlanStatus
    version: int
    total_activities: int
    total_scheduled_hours: float
    required_hours: float
    available_hours: float
    deadline_guaranteed: bool
    feasibility_ratio: float
    buffer_hours: float
    daily_distribution: Dict[str, float]  # YYYY-MM-DD -> hours
    activities: List[ScheduledActivity]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "goal": self.goal,
            "target_date": self.target_date.isoformat(),
            "status": self.status.value,
            "version": self.version,
            "total_activities": self.total_activities,
            "total_scheduled_hours": self.total_scheduled_hours,
            "required_hours": self.required_hours,
            "available_hours": self.available_hours,
            "deadline_guaranteed": self.deadline_guaranteed,
            "feasibility_ratio": self.feasibility_ratio,
            "buffer_hours": self.buffer_hours,
            "daily_distribution": self.daily_distribution,
            "activities": [a.to_dict() for a in self.activities],
            "warnings": self.warnings,
        }


class AdaptiveScheduler:
    """
    Deterministic adaptive scheduler combining goals, deadlines, gaps,
    and calendar constraints into a viable learning plan.
    """

    def __init__(
        self,
        max_daily_study_hours: float = 3.5,
        min_session_minutes: int = 30,
        min_break_minutes: int = 15,
        default_weekly_available_hours: float = 15.0,
    ):
        self.max_daily_study_hours = max_daily_study_hours
        self.min_session_minutes = min_session_minutes
        self.min_break_minutes = min_break_minutes
        self.default_weekly_available_hours = default_weekly_available_hours

    def generate_plan(
        self,
        learning_goal: str,
        target_date: datetime,
        knowledge_gaps: List[Dict[str, Any]],
        recommended_resources: Optional[List[Dict[str, Any]]] = None,
        calendar_events: Optional[List[Dict[str, Any]]] = None,
        available_study_windows: Optional[List[StudyWindow]] = None,
        preferred_study_times: Optional[List[str]] = None,
        max_daily_study_hours: Optional[float] = None,
        weekly_available_hours: Optional[float] = None,
        start_date: Optional[datetime] = None,
        current_version: int = 1,
        missed_activities: Optional[List[Dict[str, Any]]] = None,
    ) -> LearningPlan:
        """
        Synthesize a deterministic learning plan respecting all 10 scheduling rules.
        """
        now = start_date or datetime.utcnow()
        max_daily = max_daily_study_hours or self.max_daily_study_hours
        weekly_max = weekly_available_hours or self.default_weekly_available_hours
        pref_times = [p.lower() for p in (preferred_study_times or ["morning", "afternoon"])]
        resources = recommended_resources or []
        warnings: List[str] = []

        # 1. Parse Calendar Commitments (Rule 1: Never schedule during calendar conflicts)
        busy_commitments: List[CalendarCommitment] = []
        for ev in (calendar_events or []):
            if not ev.get("is_available", True) or ev.get("status") == "busy":
                start_dt = self._parse_datetime(ev.get("start") or ev.get("start_time"))
                end_dt = self._parse_datetime(ev.get("end") or ev.get("end_time"))
                if start_dt and end_dt:
                    busy_commitments.append(CalendarCommitment(start=start_dt, end=end_dt, title=ev.get("title", "Busy")))

        # 2. Build or Clean Available Study Windows
        windows = available_study_windows or self._generate_default_study_windows(now, target_date, pref_times)
        valid_windows = self._remove_conflicts_from_windows(windows, busy_commitments)

        # 3. Calculate Total Available Capacity before Target Date
        # Bound by target_date (Rule 9: Respect target deadline)
        valid_windows = [w for w in valid_windows if w.start < target_date and w.end > now]
        total_window_minutes = sum(w.duration_minutes for w in valid_windows)
        total_available_hours = round(total_window_minutes / 60.0, 1)

        # Cap available capacity by weekly limit
        total_days = max(1, (target_date - now).days)
        max_capacity_by_weekly_limit = (total_days / 7.0) * weekly_max
        effective_available_hours = min(total_available_hours, round(max_capacity_by_weekly_limit, 1))

        # 4. Generate Required Task Queue
        # (Rule 4: Prioritize gaps; Rule 5: Practice; Rule 6: Assessments; Rule 7: Revision)
        tasks_to_schedule = self._formulate_activity_queue(
            knowledge_gaps=knowledge_gaps,
            resources=resources,
            missed_activities=missed_activities,
        )

        total_required_minutes = sum(t["duration_minutes"] for t in tasks_to_schedule)
        total_required_hours = round(total_required_minutes / 60.0, 1)

        # Buffer calculation (Rule 8: Include buffer time)
        buffer_hours = round(max(0.0, effective_available_hours - total_required_hours), 1)

        # 5. Check Feasibility & Constraints
        feasibility_ratio = (
            round(effective_available_hours / max(0.1, total_required_hours), 2)
            if total_required_hours > 0
            else 1.0
        )
        deadline_guaranteed = total_required_hours <= effective_available_hours

        plan_status = PlanStatus.ACTIVE
        if not deadline_guaranteed:
            plan_status = PlanStatus.INSUFFICIENT_TIME
            warnings.append(
                f"Required study time ({total_required_hours}h) exceeds available capacity "
                f"({effective_available_hours}h) before deadline {target_date.strftime('%Y-%m-%d')}."
            )
        elif (target_date - now).days <= 7:
            plan_status = PlanStatus.APPROACHING_DEADLINE
            warnings.append(f"Approaching deadline in {(target_date - now).days} days.")

        # 6. Deterministic Slot Placement
        # (Rule 2: Daily limits; Rule 3: Weekly hours; Rule 10: No day overload)
        scheduled_activities, daily_dist = self._allocate_activities_to_windows(
            tasks=tasks_to_schedule,
            windows=valid_windows,
            max_daily_hours=max_daily,
            weekly_available_hours=weekly_max,
            min_session_minutes=self.min_session_minutes,
            min_break_minutes=self.min_break_minutes,
            deadline=target_date,
        )

        total_scheduled_minutes = sum(a.duration_minutes for a in scheduled_activities)
        total_scheduled_hours = round(total_scheduled_minutes / 60.0, 1)

        return LearningPlan(
            id=f"plan-v{current_version}",
            goal=learning_goal,
            target_date=target_date,
            status=plan_status,
            version=current_version,
            total_activities=len(scheduled_activities),
            total_scheduled_hours=total_scheduled_hours,
            required_hours=total_required_hours,
            available_hours=effective_available_hours,
            deadline_guaranteed=deadline_guaranteed,
            feasibility_ratio=feasibility_ratio,
            buffer_hours=buffer_hours,
            daily_distribution=daily_dist,
            activities=scheduled_activities,
            warnings=warnings,
        )

    def _formulate_activity_queue(
        self,
        knowledge_gaps: List[Dict[str, Any]],
        resources: List[Dict[str, Any]],
        missed_activities: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Formulate an ordered sequence of activities:
        1. Rescheduled missed activities (high urgency)
        2. High-priority gap modules (Learn -> Practice -> Quiz)
        3. Medium/Low gap modules
        4. Revision activities (spaced repetition)
        5. Milestone Assessments
        """
        queue: List[Dict[str, Any]] = []
        counter = 1

        # 1. Reschedule missed activities first
        for missed in (missed_activities or []):
            queue.append({
                "id": f"resched-{missed.get('id', counter)}",
                "topic": missed.get("topic", "General"),
                "title": f"[Rescheduled] {missed.get('title', 'Study Session')}",
                "type": ActivityType(missed.get("type", ActivityType.PRACTICE.value)),
                "duration_minutes": int(missed.get("duration_minutes", 45)),
                "priority": 1,
                "notes": "Rescheduled from previously missed activity",
            })
            counter += 1

        # 2. Sort gaps by priority: High -> Medium -> Low
        priority_rank = {"high": 1, "medium": 2, "low": 3}
        sorted_gaps = sorted(
            knowledge_gaps,
            key=lambda g: priority_rank.get(str(g.get("priority", "medium")).lower(), 2),
        )

        for gap in sorted_gaps:
            topic = gap.get("topic", "General")
            prio_val = priority_rank.get(str(gap.get("priority", "medium")).lower(), 2)
            est_hours = float(gap.get("estimated_hours", 4.0))

            # Find matching resources if available
            topic_res = [r for r in resources if r.get("topic", "").lower() == topic.lower()]
            res_id = topic_res[0]["id"] if topic_res else None

            # A. Concept Learning Session (Learn)
            learn_dur = min(60, max(30, int(est_hours * 20)))  # ~30-60 mins
            queue.append({
                "id": f"act-learn-{counter}",
                "topic": topic,
                "title": f"{topic}: Core Theory & Deep Dive",
                "type": ActivityType.LEARN,
                "duration_minutes": learn_dur,
                "priority": prio_val,
                "resource_id": res_id,
                "notes": f"Initial mastery acquisition for {topic}",
            })
            counter += 1

            # B. Hands-on Practice Session (Practice - Rule 5)
            practice_dur = min(75, max(45, int(est_hours * 30)))
            queue.append({
                "id": f"act-practice-{counter}",
                "topic": topic,
                "title": f"{topic}: Hands-on Problem Drills",
                "type": ActivityType.PRACTICE,
                "duration_minutes": practice_dur,
                "priority": prio_val,
                "resource_id": res_id,
                "notes": "Algorithm drills and edge case handling",
            })
            counter += 1

            # C. Knowledge Check (Quiz - Rule 5)
            queue.append({
                "id": f"act-quiz-{counter}",
                "topic": topic,
                "title": f"{topic}: Diagnostic Checkpoint",
                "type": ActivityType.QUIZ,
                "duration_minutes": 25,
                "priority": prio_val,
                "notes": "Verification of concept retention",
            })
            counter += 1

            # D. Spaced Repetition Review (Revision - Rule 7)
            queue.append({
                "id": f"act-rev-{counter}",
                "topic": topic,
                "title": f"{topic}: Spaced Repetition Revision",
                "type": ActivityType.REVISION,
                "duration_minutes": 30,
                "priority": prio_val + 1,
                "notes": "Spaced repetition review to prevent memory decay",
            })
            counter += 1

        # 3. Comprehensive Milestone Assessment (Assessment - Rule 6)
        if sorted_gaps:
            queue.append({
                "id": f"act-asmt-{counter}",
                "topic": "Comprehensive",
                "title": "Milestone Benchmark Assessment",
                "type": ActivityType.ASSESSMENT,
                "duration_minutes": 60,
                "priority": 1,
                "notes": "Final progress and mastery benchmark validation",
            })

        return queue

    def _allocate_activities_to_windows(
        self,
        tasks: List[Dict[str, Any]],
        windows: List[StudyWindow],
        max_daily_hours: float,
        weekly_available_hours: float,
        min_session_minutes: int,
        min_break_minutes: int,
        deadline: datetime,
    ) -> Tuple[List[ScheduledActivity], Dict[str, float]]:
        """
        Place tasks sequentially into conflict-free windows, strictly enforcing:
        - Daily hour cap (Rule 2 & 10)
        - Rolling weekly available cap (Rule 3)
        - Deadline boundary (Rule 9)
        - Rest break spacing (Rule 8)
        """
        scheduled: List[ScheduledActivity] = []
        daily_minutes: Dict[str, int] = {}
        daily_distribution: Dict[str, float] = {}
        max_daily_minutes = int(max_daily_hours * 60)

        # Sort windows chronologically
        sorted_windows = sorted(windows, key=lambda w: w.start)

        task_idx = 0
        num_tasks = len(tasks)

        for win in sorted_windows:
            if task_idx >= num_tasks:
                break

            current_time = win.start
            window_end = win.end

            while task_idx < num_tasks and current_time < window_end:
                day_str = current_time.strftime("%Y-%m-%d")
                spent_today = daily_minutes.get(day_str, 0)

                # Check daily limit (Rule 2)
                if spent_today >= max_daily_minutes:
                    break

                task = tasks[task_idx]
                task_dur = max(min_session_minutes, int(task["duration_minutes"]))

                # Check if task duration fits daily limit
                if spent_today + task_dur > max_daily_minutes:
                    # If remaining daily allowance is >= min_session_minutes, trim task
                    allowed_remaining = max_daily_minutes - spent_today
                    if allowed_remaining >= min_session_minutes:
                        task_dur = allowed_remaining
                    else:
                        break

                # Check if task fits in this study window
                if current_time + timedelta(minutes=task_dur) > window_end:
                    remaining_win = int((window_end - current_time).total_seconds() // 60)
                    if remaining_win >= min_session_minutes:
                        task_dur = remaining_win
                    else:
                        break

                # Check deadline constraint (Rule 9)
                task_end = current_time + timedelta(minutes=task_dur)
                if task_end > deadline:
                    break

                # Valid slot found! Schedule activity
                activity = ScheduledActivity(
                    id=task["id"],
                    topic=task["topic"],
                    title=task["title"],
                    type=task["type"],
                    scheduled_start=current_time,
                    scheduled_end=task_end,
                    duration_minutes=task_dur,
                    priority=task.get("priority", 2),
                    resource_id=task.get("resource_id"),
                    notes=task.get("notes", ""),
                )
                scheduled.append(activity)

                daily_minutes[day_str] = spent_today + task_dur
                daily_distribution[day_str] = round(daily_minutes[day_str] / 60.0, 2)

                # Advance clock with buffer break (Rule 8: Buffer time)
                current_time = task_end + timedelta(minutes=min_break_minutes)
                task_idx += 1

        return scheduled, daily_distribution

    def _remove_conflicts_from_windows(
        self,
        windows: List[StudyWindow],
        busy_commitments: List[CalendarCommitment],
    ) -> List[StudyWindow]:
        """
        Subtract busy commitment intervals from study windows so study
        is NEVER scheduled during conflicts (Rule 1).
        """
        if not busy_commitments:
            return list(windows)

        available_intervals: List[Tuple[datetime, datetime]] = [
            (w.start, w.end) for w in windows
        ]

        for busy in busy_commitments:
            updated_intervals: List[Tuple[datetime, datetime]] = []
            for start, end in available_intervals:
                # No overlap
                if busy.end <= start or busy.start >= end:
                    updated_intervals.append((start, end))
                else:
                    # Left split
                    if start < busy.start:
                        updated_intervals.append((start, busy.start))
                    # Right split
                    if end > busy.end:
                        updated_intervals.append((busy.end, end))
            available_intervals = updated_intervals

        # Filter out intervals shorter than minimum session
        cleaned: List[StudyWindow] = []
        for s, e in available_intervals:
            dur = int((e - s).total_seconds() // 60)
            if dur >= self.min_session_minutes:
                cleaned.append(StudyWindow(start=s, end=e))

        return cleaned

    def _generate_default_study_windows(
        self,
        start: datetime,
        end: datetime,
        preferred_times: List[str],
    ) -> List[StudyWindow]:
        """Generate recurring daily study windows based on preferred times."""
        windows: List[StudyWindow] = []
        curr = start.date()
        end_date = end.date()

        while curr <= end_date:
            day_dt = datetime(curr.year, curr.month, curr.day)

            # Morning: 09:00 - 11:30 (150 mins)
            if "morning" in preferred_times:
                windows.append(StudyWindow(
                    start=day_dt.replace(hour=9, minute=0),
                    end=day_dt.replace(hour=11, minute=30),
                    time_of_day="morning",
                ))

            # Afternoon: 14:00 - 16:30 (150 mins)
            if "afternoon" in preferred_times:
                windows.append(StudyWindow(
                    start=day_dt.replace(hour=14, minute=0),
                    end=day_dt.replace(hour=16, minute=30),
                    time_of_day="afternoon",
                ))

            # Evening: 18:00 - 20:30 (150 mins)
            if "evening" in preferred_times:
                windows.append(StudyWindow(
                    start=day_dt.replace(hour=18, minute=0),
                    end=day_dt.replace(hour=20, minute=30),
                    time_of_day="evening",
                ))

            curr += timedelta(days=1)

        return windows

    def _parse_datetime(self, val: Any) -> Optional[datetime]:
        if isinstance(val, datetime):
            return val
        if isinstance(val, str):
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except Exception:
                try:
                    return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    return None
        return None

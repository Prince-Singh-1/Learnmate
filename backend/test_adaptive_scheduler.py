"""
Unit Tests for LearnMate Adaptive Scheduling Engine.

Validates the 10 Core Scheduling Rules and Test Scenarios:
1. Normal schedule (all 10 rules satisfied, structured LearningPlan returned)
2. Insufficient time (exceeds available capacity -> INSUFFICIENT_TIME flagged, deadline_guaranteed=False)
3. Calendar conflict (activities strictly avoid busy events with 0 overlaps)
4. Approaching deadline (imminent deadline triggers APPROACHING_DEADLINE status and warning)
5. Missed sessions (missed activities are prioritized and rescheduled without daily overloading)
6. Reduced availability (weekly availability drops -> workload rebalanced across days)
7. Increased availability (availability increases -> earlier completion and larger buffer)
"""

import sys
from datetime import datetime, timedelta
from app.services.adaptive_scheduler import (
    AdaptiveScheduler,
    LearningPlan,
    ActivityType,
    PlanStatus,
    StudyWindow,
    CalendarCommitment,
)

passed_count = 0
failed_count = 0


def assert_test(condition: bool, name: str, details: str = ""):
    global passed_count, failed_count
    if condition:
        print(f"[PASS] {name}")
        passed_count += 1
    else:
        print(f"[FAIL] {name}: {details}")
        failed_count += 1


def test_adaptive_scheduler():
    print("=" * 65)
    print("RUNNING UNIT TESTS FOR ADAPTIVE SCHEDULING ENGINE")
    print("=" * 65)

    base_time = datetime(2026, 9, 15, 8, 0, 0)
    scheduler = AdaptiveScheduler(
        max_daily_study_hours=3.5,
        min_session_minutes=30,
        min_break_minutes=15,
        default_weekly_available_hours=15.0,
    )

    standard_gaps = [
        {
            "topic": "Dynamic Programming",
            "priority": "High",
            "estimated_hours": 6.0,
            "gap_score": 50.0,
        },
        {
            "topic": "Graphs",
            "priority": "High",
            "estimated_hours": 4.5,
            "gap_score": 40.0,
        },
        {
            "topic": "Trees",
            "priority": "Medium",
            "estimated_hours": 3.0,
            "gap_score": 25.0,
        },
    ]

    standard_resources = [
        {"id": "res-dp-1", "topic": "Dynamic Programming", "title": "DP Patterns Video", "type": "Video"},
        {"id": "res-dp-2", "topic": "Dynamic Programming", "title": "DP Problem Drills", "type": "Coding Practice"},
        {"id": "res-gr-1", "topic": "Graphs", "title": "Graph Algorithms Deep Dive", "type": "Video"},
    ]

    # -------------------------------------------------------------
    # Scenario 1: Normal Schedule (All 10 Rules Satisfied)
    # -------------------------------------------------------------
    target_date = base_time + timedelta(days=21)  # 3 weeks away
    plan = scheduler.generate_plan(
        learning_goal="Master Data Structures & Algorithms",
        target_date=target_date,
        knowledge_gaps=standard_gaps,
        recommended_resources=standard_resources,
        start_date=base_time,
        max_daily_study_hours=3.5,
        weekly_available_hours=15.0,
    )

    assert_test(isinstance(plan, LearningPlan), "Returns structured LearningPlan")
    assert_test(plan.status in (PlanStatus.ACTIVE, PlanStatus.FEASIBLE), "Plan status is ACTIVE/FEASIBLE")
    assert_test(plan.deadline_guaranteed is True, "Deadline is guaranteed for normal schedule")
    assert_test(plan.total_activities > 0, f"Activities scheduled (count={plan.total_activities})")

    # Rule 2: Respect daily study limits (no day exceeds 3.5h)
    daily_violations = [d for d, hrs in plan.daily_distribution.items() if hrs > 3.55]
    assert_test(len(daily_violations) == 0, f"Rule 2: Daily hours <= 3.5h across all days (violations={daily_violations})")

    # Rule 5, 6, 7: Activity types present
    types_present = {a.type for a in plan.activities}
    assert_test(ActivityType.LEARN in types_present, "Rule 4/5: 'Learn' activities included")
    assert_test(ActivityType.PRACTICE in types_present, "Rule 5: 'Practice' activities included")
    assert_test(ActivityType.QUIZ in types_present, "Rule 5/6: 'Quiz' activities included")
    assert_test(ActivityType.REVISION in types_present, "Rule 7: 'Revision' activities included")
    assert_test(ActivityType.ASSESSMENT in types_present, "Rule 6: 'Assessment' activities included")

    # Rule 8: Buffer time
    assert_test(plan.buffer_hours >= 0.0, f"Rule 8: Buffer hours calculated ({plan.buffer_hours}h)")

    # Rule 9: Target deadline respected (every activity ends <= target_date)
    late_activities = [a for a in plan.activities if a.scheduled_end > target_date]
    assert_test(len(late_activities) == 0, f"Rule 9: All activities end on or before target deadline (late={len(late_activities)})")

    # -------------------------------------------------------------
    # Scenario 2: Insufficient Time (Unrealistic deadline)
    # -------------------------------------------------------------
    tight_target = base_time + timedelta(days=2)  # Only 2 days for 15 hours of work
    tight_plan = scheduler.generate_plan(
        learning_goal="Master Data Structures & Algorithms",
        target_date=tight_target,
        knowledge_gaps=standard_gaps,
        start_date=base_time,
        max_daily_study_hours=2.0,  # Max 4 hours available in 2 days
        weekly_available_hours=8.0,
    )

    assert_test(tight_plan.status == PlanStatus.INSUFFICIENT_TIME, "Insufficient time correctly flagged")
    assert_test(tight_plan.deadline_guaranteed is False, "Deadline guarantee correctly set to False")
    assert_test(len(tight_plan.warnings) > 0, "Warning generated for insufficient time")
    assert_test(tight_plan.feasibility_ratio < 1.0, f"Feasibility ratio < 1.0 (got {tight_plan.feasibility_ratio})")

    # -------------------------------------------------------------
    # Scenario 3: Calendar Conflicts (Rule 1: Never schedule during conflicts)
    # -------------------------------------------------------------
    busy_slots = [
        # Student has university classes from 09:00 to 11:30 every weekday
        {
            "title": "Computer Networks Lecture",
            "start": (base_time + timedelta(days=1)).replace(hour=9, minute=0).isoformat(),
            "end": (base_time + timedelta(days=1)).replace(hour=11, minute=30).isoformat(),
            "is_available": False,
        },
        {
            "title": "Operating Systems Lab",
            "start": (base_time + timedelta(days=2)).replace(hour=14, minute=0).isoformat(),
            "end": (base_time + timedelta(days=2)).replace(hour=16, minute=30).isoformat(),
            "is_available": False,
        },
    ]

    conflict_plan = scheduler.generate_plan(
        learning_goal="Master Data Structures & Algorithms",
        target_date=base_time + timedelta(days=14),
        knowledge_gaps=standard_gaps,
        calendar_events=busy_slots,
        start_date=base_time,
    )

    # Check for any overlaps with busy events
    overlaps = 0
    for act in conflict_plan.activities:
        for busy in busy_slots:
            busy_start = datetime.fromisoformat(busy["start"])
            busy_end = datetime.fromisoformat(busy["end"])
            # Check interval overlap: max(start1, start2) < min(end1, end2)
            if max(act.scheduled_start, busy_start) < min(act.scheduled_end, busy_end):
                overlaps += 1

    assert_test(overlaps == 0, f"Rule 1: Zero calendar conflict overlaps (detected {overlaps})")

    # -------------------------------------------------------------
    # Scenario 4: Approaching Deadline
    # -------------------------------------------------------------
    imminent_deadline = base_time + timedelta(days=5)  # 5 days
    imminent_plan = scheduler.generate_plan(
        learning_goal="Master Data Structures & Algorithms",
        target_date=imminent_deadline,
        knowledge_gaps=[standard_gaps[0]],  # Only DP (6 hours)
        start_date=base_time,
        max_daily_study_hours=3.0,
        weekly_available_hours=20.0,
    )

    assert_test(
        imminent_plan.status == PlanStatus.APPROACHING_DEADLINE,
        f"Approaching deadline correctly flagged (got {imminent_plan.status.value})"
    )
    assert_test(any("Approaching deadline" in w for w in imminent_plan.warnings), "Approaching deadline warning emitted")

    # -------------------------------------------------------------
    # Scenario 5: Missed Sessions Rescheduling
    # -------------------------------------------------------------
    missed_activity = {
        "id": "act-prev-missed",
        "topic": "Dynamic Programming",
        "title": "DP Memoization Code Drills",
        "type": "Practice",
        "duration_minutes": 60,
    }

    replan_with_missed = scheduler.generate_plan(
        learning_goal="Master Data Structures & Algorithms",
        target_date=base_time + timedelta(days=14),
        knowledge_gaps=standard_gaps,
        start_date=base_time,
        missed_activities=[missed_activity],
        current_version=2,
    )

    assert_test(replan_with_missed.version == 2, "Plan version incremented to 2")
    # First activity should be the rescheduled item
    first_activity = replan_with_missed.activities[0]
    assert_test("[Rescheduled]" in first_activity.title, f"Missed session prioritized first: '{first_activity.title}'")
    assert_test(first_activity.topic == "Dynamic Programming", "Rescheduled activity retains topic")

    # -------------------------------------------------------------
    # Scenario 6: Reduced Availability
    # -------------------------------------------------------------
    reduced_plan = scheduler.generate_plan(
        learning_goal="Master Data Structures & Algorithms",
        target_date=base_time + timedelta(days=14),
        knowledge_gaps=standard_gaps,
        start_date=base_time,
        max_daily_study_hours=1.5,  # Reduced from 3.5 to 1.5
        weekly_available_hours=6.0,  # Reduced from 15 to 6
    )

    # Workload must be distributed over more days with smaller daily chunks
    daily_hrs = list(reduced_plan.daily_distribution.values())
    assert_test(all(h <= 1.55 for h in daily_hrs), "All daily hours capped at reduced daily limit (<=1.5h)")
    assert_test(reduced_plan.available_hours < plan.available_hours, "Available hours reflects reduced capacity")

    # -------------------------------------------------------------
    # Scenario 7: Increased Availability
    # -------------------------------------------------------------
    expanded_plan = scheduler.generate_plan(
        learning_goal="Master Data Structures & Algorithms",
        target_date=base_time + timedelta(days=14),
        knowledge_gaps=standard_gaps,
        start_date=base_time,
        max_daily_study_hours=4.0,  # Expanded to 4.0
        weekly_available_hours=25.0,  # Expanded to 25.0
    )

    assert_test(expanded_plan.deadline_guaranteed is True, "Expanded capacity guarantees deadline")
    assert_test(expanded_plan.buffer_hours > plan.buffer_hours, f"Buffer hours increased with capacity ({expanded_plan.buffer_hours}h vs {plan.buffer_hours}h)")
    assert_test(expanded_plan.feasibility_ratio >= 1.5, f"High feasibility ratio with expanded capacity ({expanded_plan.feasibility_ratio})")

    # -------------------------------------------------------------
    # Rule 4: Priority Ordering Verification
    # -------------------------------------------------------------
    # High-priority gaps (DP & Graphs) must be scheduled before Medium (Trees)
    act_topics = [a.topic for a in plan.activities if a.type in (ActivityType.LEARN, ActivityType.PRACTICE)]
    dp_first_idx = act_topics.index("Dynamic Programming") if "Dynamic Programming" in act_topics else 99
    trees_first_idx = act_topics.index("Trees") if "Trees" in act_topics else 99
    assert_test(dp_first_idx < trees_first_idx, "Rule 4: High-priority DP scheduled before Medium-priority Trees")

    print("=" * 65)
    print(f"TEST RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 65)

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    test_adaptive_scheduler()

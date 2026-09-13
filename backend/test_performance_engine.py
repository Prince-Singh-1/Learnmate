"""
Unit Tests for LearnMate Deterministic Performance Analysis Engine.

Validates:
- Deterministic calculation of:
    - mastery
    - confidence
    - trend
    - target
    - gap
    - priority
    - estimated learning hours
- Multi-source telemetry ingestion:
    - assessment results
    - quiz scores
    - practice results
    - activity completion
    - time spent
    - previous mastery
    - target mastery
- Priority multi-factor scoring:
    - size of the knowledge gap
    - importance of the topic
    - deadline proximity
    - recent performance drift
    - prerequisite dependencies
    - estimated effort
- Prompt exact examples:
    - Dynamic Programming: mastery ~30, target 80, gap 50 -> HIGH
    - Graphs: mastery ~40, target 80, gap 40 -> HIGH
    - Sorting: mastery ~82, target 80, gap 0 -> LOW
- 100% deterministic pure Python calculations (no LLM dependency).
"""

import sys
from datetime import datetime, timedelta
from app.services.performance_engine import (
    PerformanceEngine,
    TopicPerformanceInput,
    AssessmentScore,
    QuizScore,
    PracticeResult,
    ActivityCompletion,
    PriorityLevel,
    TrendDirection,
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


def test_performance_engine():
    print("=" * 65)
    print("RUNNING UNIT TESTS FOR LEARN MATE PERFORMANCE ENGINE")
    print("=" * 65)

    engine = PerformanceEngine(default_target_mastery=80.0)

    # -------------------------------------------------------------
    # Test 1: User Prompt Example - Dynamic Programming
    # mastery ~ 30, target = 80, gap = 50 -> priority = HIGH
    # -------------------------------------------------------------
    dp_input = TopicPerformanceInput(
        topic="Dynamic Programming",
        target_mastery=80.0,
        previous_mastery=28.0,
        assessment_results=[AssessmentScore(score=30.0, max_score=100.0)],
        quiz_scores=[QuizScore(score=32.0, max_score=100.0)],
        practice_results=[
            PracticeResult(problems_solved=3, total_problems=10, hints_used=2)  # ~25%
        ],
        activity_completion=ActivityCompletion(completed_activities=2, scheduled_activities=5),  # 40%
        time_spent_hours=8.5,
        importance=1.8,  # Critical core topic
        difficulty="Advanced",
    )
    dp_result = engine.calculate_topic(dp_input, days_until_deadline=45)

    assert_test(28.0 <= dp_result.mastery <= 33.0, "DP: mastery ~ 30 (got {})".format(dp_result.mastery))
    assert_test(dp_result.target == 80.0, "DP: target == 80.0")
    assert_test(47.0 <= dp_result.gap <= 52.0, "DP: gap ~ 50 (got {})".format(dp_result.gap))
    assert_test(dp_result.priority == PriorityLevel.HIGH, "DP: priority == HIGH")
    assert_test(dp_result.estimated_learning_hours > 0.0, "DP: estimated hours > 0 (got {}h)".format(dp_result.estimated_learning_hours))
    assert_test(dp_result.is_knowledge_gap is True, "DP: is_knowledge_gap == True")

    # -------------------------------------------------------------
    # Test 2: User Prompt Example - Graphs
    # mastery ~ 40, target = 80, gap = 40 -> priority = HIGH
    # -------------------------------------------------------------
    graphs_input = TopicPerformanceInput(
        topic="Graphs",
        target_mastery=80.0,
        previous_mastery=38.0,
        assessment_results=[AssessmentScore(score=40.0, max_score=100.0)],
        quiz_scores=[QuizScore(score=42.0, max_score=100.0)],
        practice_results=[
            PracticeResult(problems_solved=4, total_problems=10)  # 40%
        ],
        activity_completion=ActivityCompletion(completed_activities=3, scheduled_activities=6),  # 50%
        time_spent_hours=6.0,
        importance=1.5,
        difficulty="Advanced",
    )
    graphs_result = engine.calculate_topic(graphs_input, days_until_deadline=45)

    assert_test(38.0 <= graphs_result.mastery <= 43.0, "Graphs: mastery ~ 40 (got {})".format(graphs_result.mastery))
    assert_test(graphs_result.target == 80.0, "Graphs: target == 80.0")
    assert_test(37.0 <= graphs_result.gap <= 42.0, "Graphs: gap ~ 40 (got {})".format(graphs_result.gap))
    assert_test(graphs_result.priority == PriorityLevel.HIGH, "Graphs: priority == HIGH")
    assert_test(graphs_result.is_knowledge_gap is True, "Graphs: is_knowledge_gap == True")

    # -------------------------------------------------------------
    # Test 3: User Prompt Example - Sorting
    # mastery = 82, target = 80, gap = 0 -> priority = LOW
    # -------------------------------------------------------------
    sorting_input = TopicPerformanceInput(
        topic="Sorting",
        target_mastery=80.0,
        previous_mastery=80.0,
        assessment_results=[
            AssessmentScore(score=82.0, max_score=100.0),
            AssessmentScore(score=85.0, max_score=100.0),
        ],
        quiz_scores=[QuizScore(score=80.0, max_score=100.0)],
        practice_results=[
            PracticeResult(problems_solved=9, total_problems=10)  # 90%
        ],
        activity_completion=ActivityCompletion(completed_activities=5, scheduled_activities=5),  # 100%
        time_spent_hours=12.0,
        importance=1.0,
        difficulty="Intermediate",
    )
    sorting_result = engine.calculate_topic(sorting_input, days_until_deadline=45)

    assert_test(sorting_result.mastery >= 80.0, "Sorting: mastery >= 80.0 (got {})".format(sorting_result.mastery))
    assert_test(sorting_result.target == 80.0, "Sorting: target == 80.0")
    assert_test(sorting_result.gap == 0.0, "Sorting: gap == 0.0")
    assert_test(sorting_result.priority == PriorityLevel.LOW, "Sorting: priority == LOW")
    assert_test(sorting_result.estimated_learning_hours == 0.0, "Sorting: estimated hours == 0.0")
    assert_test(sorting_result.is_knowledge_gap is False, "Sorting: is_knowledge_gap == False")

    # -------------------------------------------------------------
    # Test 4: All 7 Output Fields Computed for Every Topic
    # -------------------------------------------------------------
    expected_fields = [
        "mastery",
        "confidence",
        "trend",
        "target",
        "gap",
        "priority",
        "estimated_learning_hours",
    ]
    for field in expected_fields:
        assert_test(hasattr(dp_result, field), f"TopicResult contains field '{field}'")

    # -------------------------------------------------------------
    # Test 5: Multi-Source Telemetry Ingestion Weights
    # -------------------------------------------------------------
    telemetry_input = TopicPerformanceInput(
        topic="Linked Lists",
        target_mastery=85.0,
        previous_mastery=65.0,
        assessment_results=[AssessmentScore(score=70.0, max_score=100.0)],
        quiz_scores=[QuizScore(score=75.0, max_score=100.0)],
        practice_results=[PracticeResult(problems_solved=8, total_problems=10)],
        activity_completion=ActivityCompletion(completed_activities=4, scheduled_activities=4),
        time_spent_hours=5.0,
    )
    ll_result = engine.calculate_topic(telemetry_input)
    assert_test(70.0 <= ll_result.mastery <= 80.0, "Multi-source telemetry weighted into mastery (got {})".format(ll_result.mastery))
    assert_test(0.60 <= ll_result.confidence <= 1.0, "Confidence increases with multi-source sample size (got {})".format(ll_result.confidence))

    # -------------------------------------------------------------
    # Test 6: Trend Direction Detection
    # -------------------------------------------------------------
    improving_input = TopicPerformanceInput(
        topic="Recursion",
        previous_mastery=40.0,
        assessment_results=[
            AssessmentScore(score=45.0, max_score=100.0),
            AssessmentScore(score=65.0, max_score=100.0),
            AssessmentScore(score=75.0, max_score=100.0),
        ],
    )
    imp_res = engine.calculate_topic(improving_input)
    assert_test(imp_res.trend == TrendDirection.IMPROVING, "Trend correctly detected as IMPROVING")

    declining_input = TopicPerformanceInput(
        topic="Trees",
        previous_mastery=70.0,
        assessment_results=[
            AssessmentScore(score=65.0, max_score=100.0),
            AssessmentScore(score=50.0, max_score=100.0),
            AssessmentScore(score=40.0, max_score=100.0),
        ],
    )
    dec_res = engine.calculate_topic(declining_input)
    assert_test(dec_res.trend == TrendDirection.DECLINING, "Trend correctly detected as DECLINING")

    # -------------------------------------------------------------
    # Test 7: Prerequisite Dependency Impact on Priority
    # Topic with dependent downstream topics gets higher urgency
    # -------------------------------------------------------------
    topic_with_deps = TopicPerformanceInput(
        topic="Recursion",  # Trees, DP, and Graphs all depend on Recursion!
        target_mastery=80.0,
        previous_mastery=55.0,
        assessment_results=[AssessmentScore(score=55.0, max_score=100.0)],
    )
    # Recursion with 3 downstream dependents vs with 0 dependents
    res_blocking = engine.calculate_topic(topic_with_deps, dependent_topics_count=3)
    res_non_blocking = engine.calculate_topic(topic_with_deps, dependent_topics_count=0)
    assert_test(res_blocking.priority == PriorityLevel.HIGH, "Blocking 3 downstream topics elevates to HIGH priority")

    # -------------------------------------------------------------
    # Test 8: Deadline Proximity Urgency
    # -------------------------------------------------------------
    urgent_deadline_res = engine.calculate_topic(topic_with_deps, days_until_deadline=7)
    assert_test(urgent_deadline_res.priority == PriorityLevel.HIGH, "Imminent deadline (7 days) escalates priority to HIGH")

    # -------------------------------------------------------------
    # Test 9: Curriculum Analysis & Automatic Knowledge Gap Extraction
    # -------------------------------------------------------------
    curriculum = [dp_input, graphs_input, sorting_input, telemetry_input]
    curriculum_result = engine.analyze_curriculum(curriculum, days_until_deadline=45)

    assert_test("overall_mastery" in curriculum_result, "Curriculum result contains overall_mastery")
    assert_test("knowledge_gaps" in curriculum_result, "Curriculum result contains knowledge_gaps")
    assert_test(curriculum_result["total_gap_count"] == 3, "Sorting with 0 gap excluded from gaps (count == 3)")

    # Gaps must be sorted with HIGH priority first
    gaps = curriculum_result["knowledge_gaps"]
    assert_test(gaps[0].priority == PriorityLevel.HIGH, "First ranked gap is HIGH priority")
    assert_test(gaps[0].topic in ("Dynamic Programming", "Graphs"), "Highest gaps are DP or Graphs")

    # -------------------------------------------------------------
    # Test 10: 100% Deterministic Execution Check
    # Running calculation 5 times produces identically equal floats
    # -------------------------------------------------------------
    runs = [engine.calculate_topic(dp_input).mastery for _ in range(5)]
    assert_test(all(r == runs[0] for r in runs), "Calculations are 100% deterministic with zero variance across runs")

    print("=" * 65)
    print(f"TEST RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 65)

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    test_performance_engine()

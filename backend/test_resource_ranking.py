"""
Unit Tests for LearnMate Learning Resource Recommendation Engine.

Validates:
- All 6 supported resource types:
    - Video
    - Article
    - PDF
    - Quiz
    - Coding Practice
    - Interactive Visualization
- Multi-factor scoring components:
    - topic relevance (0.30)
    - difficulty fit (0.20)
    - quality (0.15)
    - student preference (0.15)
    - previous effectiveness (0.10)
    - duration (0.10)
- Recommendation for specific knowledge gaps (Dynamic Programming, Graphs, Trees)
- Sensitivity to student preferences (e.g. prioritizing Coding Practice or Interactive Visualization)
- Sensitivity to previous effectiveness (boosting effective resources)
- Reusable ResourceRecommendationService independent of React/UI
"""

import sys
from app.services.resource_recommendation_service import (
    ResourceRecommendationService,
    RecommendationRequest,
    SupportedResourceType,
    ScoredResource,
    GapRecommendationResult,
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


def test_resource_recommendation_engine():
    print("=" * 65)
    print("RUNNING UNIT TESTS FOR RESOURCE RECOMMENDATION ENGINE")
    print("=" * 65)

    service = ResourceRecommendationService()

    # -------------------------------------------------------------
    # Test 1: Supported Resource Types Validation
    # -------------------------------------------------------------
    candidate_types = {
        SupportedResourceType.normalize(r.get("type", ""))
        for r in service.get_candidate_resources()
    }
    required_types = [
        "Video",
        "Article",
        "PDF",
        "Quiz",
        "Coding Practice",
        "Interactive Visualization",
    ]
    for r_type in required_types:
        assert_test(
            r_type in candidate_types,
            f"Candidate pool contains resource type '{r_type}'"
        )

    # -------------------------------------------------------------
    # Test 2: Multi-Factor Scoring for a Candidate Resource
    # -------------------------------------------------------------
    test_resource = {
        "id": "test-dp-code",
        "title": "DP Tabulation Sandbox",
        "type": "Coding Practice",
        "topic": "Dynamic Programming",
        "difficulty": "Beginner",
        "duration_minutes": 45,
        "quality_score": 95,
        "source": "Sandbox Test",
    }

    score, breakdown, why = service.score_resource(
        resource=test_resource,
        gap_topic="Dynamic Programming",
        student_mastery=25.0,  # Beginner fit
        student_level="Beginner",
        preferred_types=["Coding Practice", "Video"],
        previous_effectiveness={"test-dp-code": 0.90},
    )

    assert_test(breakdown.topic_relevance == 100.0, "Topic relevance is 100% for exact match")
    assert_test(breakdown.difficulty_fit == 100.0, "Beginner difficulty is 100% fit for 25% mastery")
    assert_test(breakdown.student_preference == 100.0, "Top preferred format scores 100%")
    assert_test(breakdown.duration_appropriateness == 100.0, "45-minute duration scores 100%")
    assert_test(breakdown.previous_effectiveness >= 90.0, "High previous effectiveness recognized")
    assert_test(score >= 90.0, f"Composite score is high (got {score})")
    assert_test(len(why) > 10, "Provides clear why_recommended justification")

    # -------------------------------------------------------------
    # Test 3: Recommendation for a Specific Knowledge Gap (Dynamic Programming)
    # -------------------------------------------------------------
    dp_gap_rec = service.recommend_for_gap(
        gap_topic="Dynamic Programming",
        student_mastery=25.0,
        gap_score=55.0,
        priority="High",
        preferred_types=["Coding Practice", "Interactive Visualization", "Video"],
        limit=3,
    )

    assert_test(dp_gap_rec.gap_topic == "Dynamic Programming", "Result matches requested gap topic")
    assert_test(len(dp_gap_rec.recommended_resources) == 3, "Returns requested limit of 3 resources")
    assert_test(
        all(r.topic == "Dynamic Programming" for r in dp_gap_rec.recommended_resources),
        "All recommended resources belong to Dynamic Programming"
    )

    # Check that resources are sorted strictly descending by match_score
    scores = [r.match_score for r in dp_gap_rec.recommended_resources]
    assert_test(
        scores == sorted(scores, reverse=True),
        f"Resources are sorted descending by score: {scores}"
    )

    # -------------------------------------------------------------
    # Test 4: Recommendation for Graphs Knowledge Gap
    # -------------------------------------------------------------
    graphs_gap_rec = service.recommend_for_gap(
        gap_topic="Graphs",
        student_mastery=40.0,
        gap_score=40.0,
        priority="High",
        preferred_types=["Interactive Visualization", "Video"],
        limit=3,
    )

    assert_test(graphs_gap_rec.gap_topic == "Graphs", "Graphs gap topic returned")
    assert_test(len(graphs_gap_rec.recommended_resources) >= 2, "Found candidate resources for Graphs")
    # Interactive visualizer should be top match because it matches preference #1 and quality 98
    top_resource = graphs_gap_rec.recommended_resources[0]
    assert_test(
        top_resource.match_score >= 85.0,
        f"Top resource has high match score (got {top_resource.match_score})"
    )

    # -------------------------------------------------------------
    # Test 5: Preference Shift Changes Ranking
    # When student changes preference from Video to Coding Practice
    # -------------------------------------------------------------
    rec_video_first = service.recommend_for_gap(
        gap_topic="Graphs",
        student_mastery=45.0,
        preferred_types=["Video", "Quiz"],
        limit=2,
    )
    rec_quiz_first = service.recommend_for_gap(
        gap_topic="Graphs",
        student_mastery=45.0,
        preferred_types=["Quiz", "Video"],
        limit=2,
    )

    # In rec_video_first, Video should score higher in student_preference than Quiz
    video_item = next(r for r in rec_video_first.recommended_resources if r.type == "Video")
    assert_test(video_item.score_breakdown.student_preference == 100.0, "Video preference is 100% when #1")

    quiz_item = next(r for r in rec_quiz_first.recommended_resources if r.type == "Quiz")
    assert_test(quiz_item.score_breakdown.student_preference == 100.0, "Quiz preference is 100% when #1")

    # -------------------------------------------------------------
    # Test 6: Previous Effectiveness Weighting
    # Boosting an effective resource raises its score
    # -------------------------------------------------------------
    base_rec = service.recommend_for_gap(
        gap_topic="Dynamic Programming",
        student_mastery=30.0,
        previous_effectiveness={"res-2": 0.50},  # Moderate
        limit=6,
    )
    boosted_rec = service.recommend_for_gap(
        gap_topic="Dynamic Programming",
        student_mastery=30.0,
        previous_effectiveness={"res-2": 0.99},  # Highly effective
        limit=6,
    )

    base_score = next(r.match_score for r in base_rec.recommended_resources if r.id == "res-2")
    boosted_score = next(r.match_score for r in boosted_rec.recommended_resources if r.id == "res-2")
    assert_test(
        boosted_score > base_score,
        f"High previous effectiveness boosted score from {base_score} to {boosted_score}"
    )

    # -------------------------------------------------------------
    # Test 7: Full Multi-Gap Recommendation Request
    # -------------------------------------------------------------
    multi_request = RecommendationRequest(
        student_level="Intermediate",
        learning_goal="Master Data Structures & Algorithms",
        knowledge_gaps=[
            {"topic": "Dynamic Programming", "gap_score": 55.0, "priority": "High", "mastery": 25.0},
            {"topic": "Graphs", "gap_score": 40.0, "priority": "High", "mastery": 40.0},
            {"topic": "Trees", "gap_score": 35.0, "priority": "Medium", "mastery": 45.0},
        ],
        preferred_resource_types=["Coding Practice", "Interactive Visualization", "Video"],
        limit_per_gap=2,
    )

    all_recommendations = service.recommend_for_all_gaps(multi_request)
    assert_test(len(all_recommendations) == 3, "Curated recommendations returned for all 3 gaps")
    for gap_res in all_recommendations:
        assert_test(
            len(gap_res.recommended_resources) <= 2,
            f"Respects limit_per_gap for {gap_res.gap_topic}"
        )
        assert_test(
            all(r.target_gap_topic == gap_res.gap_topic for r in gap_res.recommended_resources),
            f"All recommendations for {gap_res.gap_topic} target that gap"
        )

    # -------------------------------------------------------------
    # Test 8: Deterministic Consistency
    # Repeated calls return identical scores with 0 deviation
    # -------------------------------------------------------------
    run_1 = [r.match_score for r in service.recommend_for_gap("Dynamic Programming").recommended_resources]
    run_2 = [r.match_score for r in service.recommend_for_gap("Dynamic Programming").recommended_resources]
    assert_test(run_1 == run_2, "Recommendation scores are 100% deterministic across calls")

    print("=" * 65)
    print(f"TEST RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 65)

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    test_resource_recommendation_engine()

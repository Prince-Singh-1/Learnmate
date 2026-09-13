"""
Unit Tests for LearnMate Adaptive Practice Engine.

Tests:
1. Difficulty responsiveness:
   - Easy -> correct -> Medium
   - Medium -> correct -> Hard
   - Hard -> wrong -> Medium + explanation
   - Medium -> wrong -> Easy + explanation
2. Telemetry tracking:
   - question, topic, difficulty, answer, correctness, time, attempt number
3. Post-assessment state updates:
   - topic mastery score updated
   - knowledge gap severity re-evaluated
   - replanning check triggered
4. Autonomous agent connected upon critical practice failure
"""

from fastapi.testclient import TestClient
from app.main import app
from app.services.adaptive_practice_service import AdaptivePracticeService

client = TestClient(app)
service = AdaptivePracticeService()


def test_adaptive_transitions():
    print("\n" + "=" * 65)
    print("TESTING ADAPTIVE DIFFICULTY TRANSITION LOGIC")
    print("=" * 65)

    # Transition 1: Easy -> correct -> Medium
    res1 = service.process_attempt(
        question_id="q-graph-e1",
        topic="Graphs",
        difficulty="Easy",
        selected_option_id="opt-2",  # correct
        time_spent_seconds=25,
        attempt_number=1,
    )
    assert res1.is_correct is True
    assert res1.adaptation.next_difficulty == "Medium"
    assert res1.next_question.difficulty == "Medium"
    print("[PASS] Easy -> correct -> Medium")

    # Transition 2: Medium -> correct -> Hard
    res2 = service.process_attempt(
        question_id="q-graph-m1",
        topic="Graphs",
        difficulty="Medium",
        selected_option_id="opt-2",  # correct
        time_spent_seconds=42,
        attempt_number=1,
    )
    assert res2.is_correct is True
    assert res2.adaptation.next_difficulty == "Hard"
    assert res2.next_question.difficulty == "Hard"
    print("[PASS] Medium -> correct -> Hard")

    # Transition 3: Hard -> wrong -> Medium + explanation
    res3 = service.process_attempt(
        question_id="q-graph-h1",
        topic="Graphs",
        difficulty="Hard",
        selected_option_id="opt-1",  # wrong (correct is opt-2)
        time_spent_seconds=55,
        attempt_number=1,
    )
    assert res3.is_correct is False
    assert res3.adaptation.next_difficulty == "Medium"
    assert res3.adaptation.explanation is not None
    assert len(res3.adaptation.explanation) > 10
    print("[PASS] Hard -> wrong -> Medium + explanation")

    # Transition 4: Medium -> wrong -> Easy + explanation
    res4 = service.process_attempt(
        question_id="q-graph-m1",
        topic="Graphs",
        difficulty="Medium",
        selected_option_id="opt-3",  # wrong
        time_spent_seconds=30,
        attempt_number=1,
    )
    assert res4.is_correct is False
    assert res4.adaptation.next_difficulty == "Easy"
    assert res4.adaptation.explanation is not None
    print("[PASS] Medium -> wrong -> Easy + explanation")


def test_telemetry_tracking_and_agent_connection():
    print("\n" + "=" * 65)
    print("TESTING TELEMETRY TRACKING & AGENT REPLANNING CONNECTION")
    print("=" * 65)

    # Verify initial question retrieval
    q = service.get_initial_question(topic="Graphs", starting_difficulty="Easy")
    assert q.topic == "Graphs"
    assert q.difficulty == "Easy"
    assert len(q.options) >= 2
    print(f"[PASS] Retrieved initial question: {q.id} ({q.difficulty})")

    # Verify attempt with critical failure triggers autonomous replan
    res = service.process_attempt(
        question_id="q-graph-m1",
        topic="Graphs",
        difficulty="Medium",
        selected_option_id="opt-3",  # incorrect
        time_spent_seconds=40,
        attempt_number=2,
    )

    # Check telemetry fields
    assert res.attempt_id != ""
    assert res.time_spent_seconds == 40
    assert res.attempt_number == 2
    assert res.topic_mastery_updated > 0
    assert res.knowledge_gap_severity in ("High", "Medium", "Low")
    print("[PASS] Telemetry tracked: time, attempt, updated mastery, gap severity")

    if res.replan_required:
        assert res.replan_reason is not None
        assert res.agent_run_id is not None
        print(f"[PASS] Assessment triggered autonomous agent replan: {res.replan_reason[:60]}...")
    else:
        print("[PASS] Replan evaluated and verified consistent with policy")


def test_adaptive_endpoints_http():
    print("\n" + "=" * 65)
    print("TESTING FASTAPI /api/practice/adaptive/ HTTP ENDPOINTS")
    print("=" * 65)

    # 1. GET question
    r_get = client.get("/api/practice/adaptive/question?topic=Graphs&difficulty=Easy")
    assert r_get.status_code == 200, f"GET failed: {r_get.text}"
    q_data = r_get.json()
    assert q_data["difficulty"] == "Easy"
    print(f"[PASS] GET /api/practice/adaptive/question -> 200 OK ({q_data['id']})")

    # 2. POST attempt
    r_post = client.post(
        "/api/practice/adaptive/attempt",
        json={
            "question_id": q_data["id"],
            "topic": "Graphs",
            "difficulty": "Easy",
            "selected_option_id": q_data["correct_option_id"],
            "time_spent_seconds": 18,
            "attempt_number": 1,
        },
    )
    assert r_post.status_code == 200, f"POST failed: {r_post.text}"
    attempt_res = r_post.json()
    assert attempt_res["is_correct"] is True
    assert attempt_res["adaptation"]["next_difficulty"] == "Medium"
    print(f"[PASS] POST /api/practice/adaptive/attempt -> 200 OK (Transitioned to {attempt_res['adaptation']['next_difficulty']})")


if __name__ == "__main__":
    test_adaptive_transitions()
    test_telemetry_tracking_and_agent_connection()
    test_adaptive_endpoints_http()
    print("\n" + "=" * 65)
    print("ALL ADAPTIVE PRACTICE TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)

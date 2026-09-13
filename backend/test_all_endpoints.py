"""
Automated Test Suite for LearnMate FastAPI Backend.

Tests all 12 API groups and verified endpoints:
1.  GET /api/student
2.  GET /api/goals
3.  GET /api/performance
4.  GET /api/gaps
5.  GET /api/resources
6.  GET /api/calendar
7.  GET /api/activities & /api/activities/today
8.  GET /api/assessments
9.  GET /api/plan
10. POST /api/activities/complete
11. POST /api/activities/missed
12. POST /api/assessments/result
13. POST /api/agent/run
14. POST /api/replan
15. POST /api/verification
"""

import sys
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

tests_passed = 0
tests_failed = 0


def run_test(name: str, method: str, url: str, json_data: dict = None, expected_status: int = 200):
    global tests_passed, tests_failed
    print(f"\n[TEST] {method} {url} - {name}...")
    try:
        if method == "GET":
            response = client.get(url)
        elif method == "POST":
            response = client.post(url, json=json_data or {})
        else:
            raise ValueError(f"Unsupported method: {method}")

        if response.status_code == expected_status:
            data = response.json()
            print(f"  --> PASS (Status {response.status_code})")
            # Print sample key info
            if isinstance(data, dict):
                sample_keys = list(data.keys())[:5]
                print(f"      Keys: {sample_keys}")
            elif isinstance(data, list):
                print(f"      Items count: {len(data)}")
            tests_passed += 1
            return data
        else:
            print(f"  --> FAIL! Expected {expected_status}, got {response.status_code}")
            print(f"      Response: {response.text}")
            tests_failed += 1
            return None
    except Exception as e:
        print(f"  --> EXCEPTION: {e}")
        tests_failed += 1
        return None


def main():
    print("=" * 60)
    print("LEARNMATE FASTAPI BACKEND - ALL ENDPOINTS VERIFICATION")
    print("=" * 60)

    # 1. Health Check
    run_test("Health Check", "GET", "/api/health")

    # 2. Student
    run_test("Get Student Profile", "GET", "/api/student")
    run_test("Get Student By Query", "GET", "/api/student?student_id=stu-001")

    # 3. Current Goals
    run_test("Get Current Goals", "GET", "/api/goals")

    # 4. Performance
    run_test("Get Performance Overview", "GET", "/api/performance")

    # 5. Knowledge Gaps
    run_test("Get Knowledge Gaps", "GET", "/api/gaps")

    # 6. Recommended Resources
    run_test("Get Recommended Resources", "GET", "/api/resources")

    # 7. Calendar Availability
    run_test("Get Calendar Availability", "GET", "/api/calendar")

    # 8. Today's Activities
    run_test("Get Activities List", "GET", "/api/activities")
    run_test("Get Today's Activities", "GET", "/api/activities/today")

    # 9. Assessments
    run_test("Get Assessments List", "GET", "/api/assessments")

    # 10. Learning Plan
    run_test("Get Active Learning Plan", "GET", "/api/plan")

    # 11. Activity Completion
    run_test(
        "Post Activity Complete",
        "POST",
        "/api/activities/complete",
        {"activity_id": "act-2", "notes": "Completed Dijkstra implementation on LeetCode"},
    )

    # 12. Activity Missed
    run_test(
        "Post Activity Missed",
        "POST",
        "/api/activities/missed",
        {"activity_id": "act-3", "reason": "Conflict with college lab exam"},
    )

    # 13. Assessment Result
    run_test(
        "Post Assessment Result",
        "POST",
        "/api/assessments/result",
        {"topic": "Graphs", "score": 88.0, "max_score": 100.0},
    )

    # 14. Autonomous Agent Run
    run_test(
        "Post Agent Run (10-Step Autonomous Loop)",
        "POST",
        "/api/agent/run",
        {"student_id": "stu-001", "trigger": "user_dashboard_click"},
    )

    # 15. Dynamic Replanning
    run_test(
        "Post Autonomous Replan",
        "POST",
        "/api/replan",
        {"student_id": "stu-001", "reason": "Missed Binary Trees Video Session"},
    )

    # 16. Plan Verification
    run_test(
        "Post Plan Verification",
        "POST",
        "/api/verification",
        {"student_id": "stu-001", "target_deadline": "2025-11-30", "buffer_days_required": 7},
    )

    print("\n" + "=" * 60)
    print(f"RESULTS: {tests_passed} PASSED | {tests_failed} FAILED")
    print("=" * 60)

    if tests_failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

"""
Live HTTP Test Script for LearnMate Backend on port 8000 using standard library urllib.
"""

import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"

endpoints = [
    ("GET", "/api/health", None),
    ("GET", "/api/student", None),
    ("GET", "/api/goals", None),
    ("GET", "/api/performance", None),
    ("GET", "/api/gaps", None),
    ("GET", "/api/resources", None),
    ("GET", "/api/calendar", None),
    ("GET", "/api/activities", None),
    ("GET", "/api/activities/today", None),
    ("GET", "/api/assessments", None),
    ("GET", "/api/plan", None),
    ("POST", "/api/activities/complete", {"activity_id": "act-2", "notes": "Completed Dijkstra practice"}),
    ("POST", "/api/activities/missed", {"activity_id": "act-3", "reason": "Exam prep"}),
    ("POST", "/api/assessments/result", {"topic": "Trees", "score": 90.0, "max_score": 100.0}),
    ("POST", "/api/agent/run", {"student_id": "stu-001"}),
    ("POST", "/api/replan", {"student_id": "stu-001", "reason": "Autonomous schedule update"}),
    ("POST", "/api/verification", {"student_id": "stu-001"}),
]

print("=" * 60)
print("TESTING LIVE HTTP ENDPOINTS AGAINST", BASE_URL)
print("=" * 60)

all_pass = True
passed_count = 0

for method, path, body in endpoints:
    url = BASE_URL + path
    try:
        data = json.dumps(body).encode("utf-8") if body else None
        headers = {"Content-Type": "application/json"} if body else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body_resp = json.loads(response.read().decode("utf-8"))
            if status == 200:
                print(f"[OK] {method:4} {path:26} -> 200 OK")
                passed_count += 1
            else:
                print(f"[FAIL] {method:4} {path:26} -> {status}")
                all_pass = False
    except urllib.error.HTTPError as e:
        print(f"[FAIL] {method:4} {path:26} -> HTTP {e.code}: {e.read().decode('utf-8')}")
        all_pass = False
    except Exception as e:
        print(f"[ERROR] {method:4} {path:26} -> {e}")
        all_pass = False

print("\n" + "=" * 60)
print(f"LIVE HTTP RESULTS: {passed_count}/{len(endpoints)} PASSED")
print("=" * 60)

if not all_pass:
    exit(1)

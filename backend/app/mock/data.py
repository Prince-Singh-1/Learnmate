"""
LearnMate Mock / Synthetic Data Store & State Management.

Provides realistic, deterministic in-memory data for:
- Student profile (Prince Singh - B.Tech CSE)
- Learning goals & milestones (Data Structures & Algorithms)
- Performance metrics & historical scores
- Knowledge gaps
- Learning resources & recommendations
- Calendar availability slots
- Scheduled daily activities
- Assessments & quiz results
- Autonomous replanning logs
"""

from datetime import datetime, timedelta
import copy


# ─── Mock Student Profile ──────────────────────────────────────────

_STUDENT = {
    "id": "stu-001",
    "name": "Prince Singh",
    "email": "prince.singh@university.edu",
    "degree": "B.Tech (CSE)",
    "institution": "Institute of Technology",
    "avatar_url": "/prince-avatar.jpg",
    "current_goal": "Master Data Structures & Algorithms",
    "target_deadline": "2025-11-30T00:00:00",
    "overall_progress": 68.0,
    "day_streak": 12,
    "time_spent_hours": 24.5,
    "topics_completed": 8,
    "created_at": "2025-08-01T09:00:00",
}


# ─── Goals & Milestones ────────────────────────────────────────────

_GOALS = [
    {
        "id": "goal-001",
        "student_id": "stu-001",
        "title": "Master Data Structures & Algorithms",
        "description": "Become interview ready with strong algorithmic problem solving skills.",
        "target_date": "2025-11-30",
        "remaining_days": 79,
        "priority": "High",
        "status": "in_progress",
        "progress_percentage": 68.0,
        "topics": ["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming", "Sorting"],
        "milestones": [
            {"id": "ms-1", "title": "Linear Data Structures", "target_date": "2025-08-25", "completed": True, "progress": 100},
            {"id": "ms-2", "title": "Tree & Graph Traversals", "target_date": "2025-09-20", "completed": False, "progress": 55},
            {"id": "ms-3", "title": "Dynamic Programming & Greedy", "target_date": "2025-10-15", "completed": False, "progress": 25},
            {"id": "ms-4", "title": "Mock Interviews & Speed Runs", "target_date": "2025-11-15", "completed": False, "progress": 0},
        ],
    }
]


# ─── Performance Data ──────────────────────────────────────────────

_PERFORMANCE_POINTS = [
    {"week": "Week 1", "score": 45.0, "target": 60.0},
    {"week": "Week 2", "score": 55.0, "target": 65.0},
    {"week": "Week 3", "score": 62.0, "target": 70.0},
    {"week": "Week 4", "score": 68.0, "target": 75.0},
]

_TOPIC_MASTERY = [
    {"id": "tm-1", "topic": "Arrays", "mastery": 85.0, "color": "#6366f1", "icon": "📊"},
    {"id": "tm-2", "topic": "Linked Lists", "mastery": 70.0, "color": "#8b5cf6", "icon": "🔗"},
    {"id": "tm-3", "topic": "Trees", "mastery": 45.0, "color": "#a78bfa", "icon": "🌳"},
    {"id": "tm-4", "topic": "Graphs", "mastery": 30.0, "color": "#c084fc", "icon": "📈"},
    {"id": "tm-5", "topic": "Dynamic Programming", "mastery": 25.0, "color": "#e879f9", "icon": "🧩"},
    {"id": "tm-6", "topic": "Sorting", "mastery": 80.0, "color": "#22d3ee", "icon": "📶"},
]


# ─── Knowledge Gaps ────────────────────────────────────────────────

_KNOWLEDGE_GAPS = [
    {
        "id": "gap-1",
        "topic": "Dynamic Programming",
        "severity": "High",
        "mastery": 25.0,
        "description": "Subproblem overlapping & optimal substructure formulation",
        "reason": "Subproblem overlapping & optimal substructure formulation",
        "estimated_hours": 6.0,
        "detected_at": "2025-09-10T14:30:00",
        "recommended_action": "Complete DP Memoization vs Tabulation guide and 10 medium exercises",
    },
    {
        "id": "gap-2",
        "topic": "Graphs",
        "severity": "High",
        "mastery": 30.0,
        "description": "Shortest Path (Dijkstra) and Minimum Spanning Trees (Kruskal/Prim)",
        "reason": "Shortest Path (Dijkstra) and Minimum Spanning Trees (Kruskal/Prim)",
        "estimated_hours": 5.5,
        "detected_at": "2025-09-11T10:00:00",
        "recommended_action": "Watch visual walkthrough and solve 5 graph traversal challenges",
    },
    {
        "id": "gap-3",
        "topic": "Trees",
        "severity": "Medium",
        "mastery": 45.0,
        "description": "Binary Search Tree balancing & Lowest Common Ancestor logic",
        "reason": "Binary Search Tree balancing & Lowest Common Ancestor logic",
        "estimated_hours": 4.0,
        "detected_at": "2025-09-08T18:00:00",
        "recommended_action": "Review BST rotation slides and practice recursive LCA problems",
    },
    {
        "id": "gap-4",
        "topic": "Linked Lists",
        "severity": "Low",
        "mastery": 70.0,
        "description": "Fast & Slow pointer cycle detection edge cases",
        "reason": "Fast & Slow pointer cycle detection edge cases",
        "estimated_hours": 2.0,
        "detected_at": "2025-09-05T12:00:00",
        "recommended_action": "Self-quiz on two-pointer technique",
    },
    {
        "id": "gap-5",
        "topic": "Sorting",
        "severity": "Low",
        "mastery": 80.0,
        "description": "Quick review of advanced in-place QuickSort partitioning",
        "reason": "Quick review of advanced in-place QuickSort partitioning",
        "estimated_hours": 1.5,
        "detected_at": "2025-09-01T15:00:00",
        "recommended_action": "Review Lomuto vs Hoare partition schemes",
    },
]


# ─── Recommended Learning Resources ────────────────────────────────

_RESOURCES = [
    {
        "id": "res-1",
        "title": "Graph Algorithms: BFS, DFS & Dijkstra Explained",
        "type": "Video",
        "source": "Video • MIT OpenCourseWare",
        "detail": "45 mins",
        "duration_minutes": 45,
        "difficulty": "Intermediate",
        "quality_score": 96,
        "match_score": 95,
        "match_label": "Top Match",
        "color": "#6366f1",
        "url": "https://ocw.mit.edu/graphs",
        "topic": "Graphs",
    },
    {
        "id": "res-2",
        "title": "DP Cheat Sheet & Recurrence Relations",
        "type": "PDF",
        "source": "PDF • Stanford CS",
        "detail": "15 pages",
        "duration_minutes": 30,
        "difficulty": "Beginner",
        "quality_score": 94,
        "match_score": 90,
        "match_label": "High Match",
        "color": "#ef4444",
        "url": "https://stanford.edu/dp-notes.pdf",
        "topic": "Dynamic Programming",
    },
    {
        "id": "res-3",
        "title": "Interactive Graph & Tree Visualizer",
        "type": "Interactive Visualization",
        "source": "Web Tool • VisuAlgo",
        "detail": "Interactive Sandbox",
        "duration_minutes": 30,
        "difficulty": "Beginner",
        "quality_score": 98,
        "match_score": 94,
        "match_label": "Highly Recommended",
        "color": "#3b82f6",
        "url": "https://visualgo.net/en/dfsbfs",
        "topic": "Graphs",
    },
    {
        "id": "res-4",
        "title": "LeetCode Curated 50: Dynamic Programming Patterns",
        "type": "Coding Practice",
        "source": "Coding Practice • NeetCode",
        "detail": "Hands-on Drills",
        "duration_minutes": 60,
        "difficulty": "Intermediate",
        "quality_score": 95,
        "match_score": 92,
        "match_label": "Recommended",
        "color": "#10b981",
        "url": "https://neetcode.io/practice/dp",
        "topic": "Dynamic Programming",
    },
    {
        "id": "res-5",
        "title": "Demystifying 0/1 Knapsack & Memoization",
        "type": "Article",
        "source": "Deep-Dive Article • GeeksforGeeks",
        "detail": "20 mins read",
        "duration_minutes": 20,
        "difficulty": "Beginner",
        "quality_score": 88,
        "match_score": 86,
        "match_label": "Good Match",
        "color": "#f59e0b",
        "url": "https://geeksforgeeks.org/knapsack",
        "topic": "Dynamic Programming",
    },
    {
        "id": "res-6",
        "title": "Diagnostic Quiz: Shortest Paths & Graph Cycles",
        "type": "Quiz",
        "source": "Interactive Quiz • LearnMate Diagnostic",
        "detail": "15 Questions",
        "duration_minutes": 25,
        "difficulty": "Intermediate",
        "quality_score": 92,
        "match_score": 89,
        "match_label": "Diagnostic Match",
        "color": "#8b5cf6",
        "url": "https://learnmate.ai/quiz/graphs-shortest-path",
        "topic": "Graphs",
    },
    {
        "id": "res-7",
        "title": "Binary Search Tree Balancing & AVL Rotations",
        "type": "Video",
        "source": "Video • Abdul Bari",
        "detail": "35 mins",
        "duration_minutes": 35,
        "difficulty": "Intermediate",
        "quality_score": 97,
        "match_score": 91,
        "match_label": "Top Match",
        "color": "#a855f7",
        "url": "https://youtube.com/abdulbari-trees",
        "topic": "Trees",
    },
    {
        "id": "res-8",
        "title": "BST & LCA Coding Challenges",
        "type": "Coding Practice",
        "source": "Coding Practice • LeetCode",
        "detail": "10 Medium Problems",
        "duration_minutes": 75,
        "difficulty": "Intermediate",
        "quality_score": 93,
        "match_score": 88,
        "match_label": "Practice Match",
        "color": "#06b6d4",
        "url": "https://leetcode.com/tag/tree",
        "topic": "Trees",
    },
    {
        "id": "res-9",
        "title": "Fast & Slow Pointers in Linked Lists Guide",
        "type": "Article",
        "source": "Article • Educative.io",
        "detail": "15 mins read",
        "duration_minutes": 15,
        "difficulty": "Beginner",
        "quality_score": 90,
        "match_score": 85,
        "match_label": "Reference",
        "color": "#ec4899",
        "url": "https://educative.io/linked-lists-pointers",
        "topic": "Linked Lists",
    },
    {
        "id": "res-10",
        "title": "Interactive Sorting Visualizer (QuickSort vs MergeSort)",
        "type": "Interactive Visualization",
        "source": "Visualizer • Algorithm Visualizer",
        "detail": "Real-time Step Visualizer",
        "duration_minutes": 20,
        "difficulty": "Beginner",
        "quality_score": 94,
        "match_score": 82,
        "match_label": "Visual Guide",
        "color": "#14b8a6",
        "url": "https://algorithm-visualizer.org/sorting",
        "topic": "Sorting",
    },
    {
        "id": "res-11",
        "title": "Comprehensive Dynamic Programming Reference Manual",
        "type": "PDF",
        "source": "PDF • MIT CSAIL",
        "detail": "45 pages",
        "duration_minutes": 90,
        "difficulty": "Advanced",
        "quality_score": 97,
        "match_score": 85,
        "match_label": "Advanced Reference",
        "color": "#e11d48",
        "url": "https://csail.mit.edu/dp-manual.pdf",
        "topic": "Dynamic Programming",
    },
    {
        "id": "res-12",
        "title": "Quick Knowledge Check: Dynamic Programming",
        "type": "Quiz",
        "source": "Checkpoint Quiz • LearnMate",
        "detail": "10 Questions",
        "duration_minutes": 15,
        "difficulty": "Beginner",
        "quality_score": 89,
        "match_score": 87,
        "match_label": "Quick Check",
        "color": "#f43f5e",
        "url": "https://learnmate.ai/quiz/dp-fundamentals",
        "topic": "Dynamic Programming",
    },
]


# ─── Calendar Availability Slots ───────────────────────────────────

_CALENDAR_SLOTS = [
    {
        "id": f"slot-{i}",
        "day": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
        "weekday": (datetime.now() + timedelta(days=i)).strftime("%A"),
        "start_time": "09:00",
        "end_time": "11:30",
        "duration_minutes": 150,
        "is_available": True,
        "label": "Morning Study Block",
    }
    for i in range(7)
] + [
    {
        "id": f"slot-eve-{i}",
        "day": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
        "weekday": (datetime.now() + timedelta(days=i)).strftime("%A"),
        "start_time": "14:00",
        "end_time": "16:30",
        "duration_minutes": 150,
        "is_available": (i % 2 == 0),
        "label": "Afternoon Practice Block",
    }
    for i in range(7)
]


# ─── Today's Scheduled Activities ──────────────────────────────────

_ACTIVITIES = [
    {
        "id": "act-1",
        "time": "9:00",
        "end_time": "10:00 AM",
        "title": "Graph Algorithms (Video)",
        "type": "video",
        "topic": "Graphs",
        "duration_minutes": 60,
        "completed": True,
        "missed": False,
        "scheduled_date": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "id": "act-2",
        "time": "10:30",
        "end_time": "11:30 AM",
        "title": "Practice: Dijkstra's Algorithm",
        "type": "practice",
        "topic": "Graphs",
        "duration_minutes": 60,
        "completed": False,
        "missed": False,
        "scheduled_date": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "id": "act-3",
        "time": "2:00",
        "end_time": "3:00 PM",
        "title": "Read: DP Notes",
        "type": "reading",
        "topic": "Dynamic Programming",
        "duration_minutes": 60,
        "completed": False,
        "missed": False,
        "scheduled_date": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "id": "act-4",
        "time": "6:00",
        "end_time": "6:30 PM",
        "title": "Quiz: Graphs (20 Questions)",
        "type": "quiz",
        "topic": "Graphs",
        "duration_minutes": 30,
        "completed": False,
        "missed": False,
        "scheduled_date": datetime.now().strftime("%Y-%m-%d"),
    },
]


# ─── Recent Activity Feed ──────────────────────────────────────────

_RECENT_ACTIVITIES = [
    {
        "id": "rec-1",
        "type": "activity",
        "title": "Completed: Arrays Practice Set",
        "description": "Completed: Arrays Practice Set",
        "status": "completed",
        "timestamp": "Today, 10:15 AM",
        "details": "10/10 questions solved",
    },
    {
        "id": "rec-2",
        "type": "activity",
        "title": "Missed: Binary Trees Video",
        "description": "Missed: Binary Trees Video",
        "status": "missed",
        "timestamp": "Yesterday, 6:00 PM",
        "details": "Flagged for Autonomous Replan",
    },
    {
        "id": "rec-3",
        "type": "quiz",
        "title": "Scored 80% in Sorting Quiz",
        "description": "Scored 80% in Sorting Quiz",
        "status": "scored",
        "timestamp": "10 Sep 2025",
        "details": "16/20 correct",
    },
    {
        "id": "rec-4",
        "type": "activity",
        "title": "Completed: Hashing Notes",
        "description": "Completed: Hashing Notes",
        "status": "completed",
        "timestamp": "9 Sep 2025",
        "details": "Read all 8 pages",
    },
    {
        "id": "rec-5",
        "type": "schedule",
        "title": "Rescheduled: DP Practice",
        "description": "Rescheduled: DP Practice",
        "status": "rescheduled",
        "timestamp": "9 Sep 2025",
        "details": "Shifted to Friday Morning window",
    },
]


# ─── Assessments History ───────────────────────────────────────────

_ASSESSMENTS = [
    {
        "id": "asmt-001",
        "student_id": "stu-001",
        "title": "Sorting Algorithms Assessment",
        "topic": "Sorting",
        "score": 80.0,
        "max_score": 100.0,
        "percentage": 80.0,
        "status": "passed",
        "completed_at": "2025-09-10T11:00:00",
    },
    {
        "id": "asmt-002",
        "student_id": "stu-001",
        "title": "Arrays & Strings Diagnostic",
        "topic": "Arrays",
        "score": 85.0,
        "max_score": 100.0,
        "percentage": 85.0,
        "status": "passed",
        "completed_at": "2025-09-08T15:00:00",
    },
    {
        "id": "asmt-003",
        "student_id": "stu-001",
        "title": "Trees & Binary Search Trees Quiz",
        "topic": "Trees",
        "score": 45.0,
        "max_score": 100.0,
        "percentage": 45.0,
        "status": "needs_review",
        "completed_at": "2025-09-04T16:00:00",
    },
]


# ─── Learning Plan Structure ───────────────────────────────────────

_PLAN = {
    "id": "plan-stu-001-v3",
    "student_id": "stu-001",
    "version": 3,
    "status": "active",
    "goal": "Master Data Structures & Algorithms",
    "target_deadline": "2025-11-30",
    "remaining_days": 79,
    "required_study_hours": 96.0,
    "scheduled_study_hours": 102.0,
    "feasibility_ratio": 1.06,
    "deadline_guaranteed": True,
    "created_at": "2025-09-11T09:00:00",
    "activities": [
        {
            "id": "plan-act-1",
            "topic": "Graphs",
            "title": "Graph Algorithms Deep Dive (Video)",
            "type": "video",
            "duration_minutes": 60,
            "scheduled_start": "2025-09-12T09:00:00",
            "status": "completed",
        },
        {
            "id": "plan-act-2",
            "topic": "Graphs",
            "title": "Dijkstra's Algorithm Implementation",
            "type": "practice",
            "duration_minutes": 60,
            "scheduled_start": "2025-09-12T10:30:00",
            "status": "pending",
        },
        {
            "id": "plan-act-3",
            "topic": "Dynamic Programming",
            "title": "DP Memoization Patterns",
            "type": "reading",
            "duration_minutes": 60,
            "scheduled_start": "2025-09-12T14:00:00",
            "status": "pending",
        },
        {
            "id": "plan-act-4",
            "topic": "Trees",
            "title": "BST Traversals & Balancing (Rescheduled)",
            "type": "video",
            "duration_minutes": 45,
            "scheduled_start": "2025-09-13T09:30:00",
            "status": "pending",
        },
    ],
}


# ─── State Accessors & Mutators ────────────────────────────────────

def get_student_profile() -> dict:
    return copy.deepcopy(_STUDENT)


def get_current_goals() -> list[dict]:
    return copy.deepcopy(_GOALS)


def get_performance_overview() -> dict:
    return {
        "points": copy.deepcopy(_PERFORMANCE_POINTS),
        "topic_mastery": copy.deepcopy(_TOPIC_MASTERY),
        "overall_mastery": _STUDENT["overall_progress"],
        "strongest_topic": "Arrays (85%)",
        "weakest_topic": "Dynamic Programming (25%)",
    }


def get_knowledge_gaps() -> list[dict]:
    return copy.deepcopy(_KNOWLEDGE_GAPS)


def get_recommended_resources() -> list[dict]:
    return copy.deepcopy(_RESOURCES)


def get_calendar_slots() -> list[dict]:
    return copy.deepcopy(_CALENDAR_SLOTS)


def get_today_activities() -> list[dict]:
    return copy.deepcopy(_ACTIVITIES)


def get_recent_activities() -> list[dict]:
    return copy.deepcopy(_RECENT_ACTIVITIES)


def get_assessments() -> list[dict]:
    return copy.deepcopy(_ASSESSMENTS)


def get_learning_plan() -> dict:
    return copy.deepcopy(_PLAN)


def mark_activity_completed(activity_id: str) -> dict:
    for act in _ACTIVITIES:
        if act["id"] == activity_id:
            act["completed"] = True
            act["missed"] = False
            _STUDENT["time_spent_hours"] += round(act.get("duration_minutes", 60) / 60, 1)
            _STUDENT["overall_progress"] = min(100.0, _STUDENT["overall_progress"] + 0.5)

            # Prepend to recent activities
            _RECENT_ACTIVITIES.insert(
                0,
                {
                    "id": f"rec-{int(datetime.now().timestamp())}",
                    "type": "activity",
                    "title": f"Completed: {act['title']}",
                    "description": f"Completed: {act['title']}",
                    "status": "completed",
                    "timestamp": "Just now",
                    "details": "Session marked as completed",
                },
            )
            return {"success": True, "activity": act, "message": "Activity marked as completed"}
    return {"success": False, "message": f"Activity {activity_id} not found"}


def mark_activity_missed(activity_id: str) -> dict:
    for act in _ACTIVITIES:
        if act["id"] == activity_id:
            act["completed"] = False
            act["missed"] = True

            # Prepend to recent activities
            _RECENT_ACTIVITIES.insert(
                0,
                {
                    "id": f"rec-{int(datetime.now().timestamp())}",
                    "type": "activity",
                    "title": f"Missed: {act['title']}",
                    "description": f"Missed: {act['title']}",
                    "status": "missed",
                    "timestamp": "Just now",
                    "details": "Flagged for autonomous replan",
                },
            )
            return {
                "success": True,
                "activity": act,
                "message": "Activity marked as missed. Autonomous replan recommended.",
                "replan_recommended": True,
            }
    return {"success": False, "message": f"Activity {activity_id} not found"}


def record_assessment_result(topic: str, score: float, max_score: float = 100.0) -> dict:
    percentage = round((score / max_score) * 100.0, 1)
    new_asmt = {
        "id": f"asmt-{int(datetime.now().timestamp())}",
        "student_id": "stu-001",
        "title": f"{topic} Quiz",
        "topic": topic,
        "score": score,
        "max_score": max_score,
        "percentage": percentage,
        "status": "passed" if percentage >= 60.0 else "needs_review",
        "completed_at": datetime.now().isoformat(),
    }
    _ASSESSMENTS.insert(0, new_asmt)

    # Update topic mastery
    for tm in _TOPIC_MASTERY:
        if tm["topic"].lower() == topic.lower():
            # Rolling average
            tm["mastery"] = round((tm["mastery"] + percentage) / 2, 1)
            break

    # Recalculate knowledge gaps
    for gap in _KNOWLEDGE_GAPS:
        if gap["topic"].lower() == topic.lower():
            gap["mastery"] = percentage
            if percentage >= 75.0:
                gap["severity"] = "Low"
            elif percentage >= 50.0:
                gap["severity"] = "Medium"
            else:
                gap["severity"] = "High"

    # Prepend to recent activities
    _RECENT_ACTIVITIES.insert(
        0,
        {
            "id": f"rec-{int(datetime.now().timestamp())}",
            "type": "quiz",
            "title": f"Scored {percentage}% in {topic} Quiz",
            "description": f"Scored {percentage}% in {topic} Quiz",
            "status": "scored",
            "timestamp": "Just now",
            "details": f"{score}/{max_score} correct",
        },
    )

    return {"success": True, "assessment": new_asmt}


def execute_replan(reason: str) -> dict:
    _PLAN["version"] += 1
    new_version = _PLAN["version"]

    # Rebalance pending items
    rescheduled_count = 0
    for act in _PLAN["activities"]:
        if act["status"] == "pending":
            rescheduled_count += 1

    _RECENT_ACTIVITIES.insert(
        0,
        {
            "id": f"rec-{int(datetime.now().timestamp())}",
            "type": "schedule",
            "title": f"Autonomous Replan (v{new_version})",
            "description": f"Rebalanced schedule: {reason}",
            "status": "rescheduled",
            "timestamp": "Just now",
            "details": f"Version {new_version} verified. Deadline guaranteed.",
        },
    )

    return {
        "success": True,
        "plan_version": new_version,
        "reason": reason,
        "rescheduled_activities_count": rescheduled_count,
        "deadline_guaranteed": True,
        "feasibility_score": 98.4,
        "message": f"Autonomous Replan completed for reason: {reason}. Learning plan updated to v{new_version}.",
    }


def verify_current_plan(plan_id: str | None = None) -> dict:
    """Verify active plan constraints, coverage, and deadline."""
    plan = get_learning_plan()
    gaps = get_knowledge_gaps()
    high_gaps = [g["topic"] for g in gaps if g.get("severity") == "High"]
    covered_topics = {a["topic"] for a in plan.get("activities", [])}

    issues = []
    uncovered = [topic for topic in high_gaps if topic not in covered_topics]
    if uncovered:
        for topic in uncovered:
            issues.append(
                {
                    "code": "HIGH_SEVERITY_GAP_UNCOVERED",
                    "severity": "warning",
                    "message": f"High priority gap in '{topic}' needs more practice blocks scheduled.",
                    "topic": topic,
                }
            )

    feasibility_score = 98.4 if plan.get("scheduled_study_hours", 0) >= plan.get("required_study_hours", 0) else 85.0

    return {
        "valid": True,
        "plan_id": plan_id or plan.get("id", "plan-stu-001"),
        "plan_version": plan.get("version", 1),
        "goal_coverage_percentage": 94.5,
        "deadline_satisfied": True,
        "feasibility_score": feasibility_score,
        "issues": issues,
        "message": "Plan successfully verified. All hard constraints and target deadlines satisfied.",
    }


# ─── Legacy / Compatibility Helpers ──────────────────────────────

def get_mock_students() -> list[dict]:
    return [get_student_profile()]


def get_mock_plan(student_id: str = "stu-001") -> dict:
    return get_learning_plan()


def get_mock_performance(student_id: str = "stu-001") -> dict:
    return get_performance_overview()


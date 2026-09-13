"""
LearnMate Database Initialization & Seed Script.

Creates all database tables defined in app.models and seeds initial
realistic domain records for Prince Singh.
"""

from datetime import datetime, timedelta
from app.db.base import Base, engine
from app.db.session import SessionLocal
import app.models  # Ensures all models are registered on Base.metadata
from app.models import (
    Student,
    StudentEvent,
    LearningGoal,
    Topic,
    TopicMastery,
    KnowledgeGap,
    LearningResource,
    Recommendation,
    LearningActivity,
    StudySession,
    CalendarEvent,
    Assessment,
    AssessmentResult,
    LearningPlan,
    PlanVersion,
    PlanChange,
    AgentRun,
)


def init_db(seed_data: bool = True):
    """
    Initialize database schema and seed initial sample data.
    """
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print(f"Created {len(Base.metadata.tables)} tables: {list(Base.metadata.tables.keys())}")

    if not seed_data:
        return

    session = SessionLocal()
    try:
        # Check if already seeded
        existing_student = session.query(Student).filter(Student.id == "stu-001").first()
        if existing_student:
            print("Database already contains initial student (stu-001). Skipping duplicate seed.")
            return

        print("Seeding initial domain data...")

        # 1. Student
        student = Student(
            id="stu-001",
            name="Prince Singh",
            email="prince.singh@university.edu",
            preferred_study_times=["morning", "late_afternoon"],
            weekly_available_hours=15.0,
            degree="B.Tech (CSE)",
            institution="Institute of Technology",
            avatar_url="/prince-avatar.jpg",
            current_goal="Master Data Structures & Algorithms",
            target_deadline=datetime.utcnow() + timedelta(days=79),
            overall_progress=68.0,
            day_streak=12,
        )
        session.add(student)

        # 2. Learning Goal
        goal = LearningGoal(
            id="goal-001",
            student_id="stu-001",
            title="Master Data Structures & Algorithms",
            description="Become interview ready with strong problem solving skills.",
            target_date=datetime.utcnow() + timedelta(days=79),
            target_proficiency=85.0,
            status="in_progress",
            priority="High",
            topics=["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming", "Sorting"],
            milestones=[
                {"title": "Linear Structures", "completed": True, "progress": 100},
                {"title": "Tree & Graph Traversals", "completed": False, "progress": 55},
                {"title": "Dynamic Programming", "completed": False, "progress": 25},
            ],
        )
        session.add(goal)

        # 3. Topics
        topics_data = [
            ("Arrays", "arrays", "Linear arrays and sliding window", 85.0, 0.9, "stable", "#6366f1", "📊"),
            ("Linked Lists", "linked-lists", "Pointers, slow-fast cycle detection", 70.0, 0.8, "improving", "#8b5cf6", "🔗"),
            ("Trees", "trees", "BST, traversals, LCA algorithms", 45.0, 0.6, "declining", "#a78bfa", "🌳"),
            ("Graphs", "graphs", "BFS, DFS, Dijkstra, MST algorithms", 30.0, 0.5, "needs_remediation", "#c084fc", "📈"),
            ("Dynamic Programming", "dynamic-programming", "Memoization, tabulation, optimal substructure", 25.0, 0.4, "critical_gap", "#e879f9", "🧩"),
            ("Sorting", "sorting", "QuickSort, MergeSort, partitioning", 80.0, 0.9, "improving", "#22d3ee", "📶"),
        ]

        for name, slug, desc, score, conf, trend, color, icon in topics_data:
            t = Topic(
                id=f"top-{slug}",
                name=name,
                slug=slug,
                description=desc,
                category="Data Structures",
                color=color,
                icon=icon,
            )
            session.add(t)

            # TopicMastery
            tm = TopicMastery(
                id=f"tm-{slug}",
                student_id="stu-001",
                topic=name,
                topic_id=f"top-{slug}",
                mastery_score=score,
                confidence=conf,
                target_mastery=80.0,
                trend=trend,
            )
            session.add(tm)

        # 4. Knowledge Gaps
        gaps_data = [
            ("Dynamic Programming", "top-dynamic-programming", 55.0, "High", 12.0, "Weak in memoization and tabulation patterns"),
            ("Graphs", "top-graphs", 50.0, "High", 10.0, "Need practice with shortest path and traversals"),
            ("Trees", "top-trees", 35.0, "Medium", 6.0, "Balanced trees and segment trees need work"),
        ]
        for topic_name, top_id, gap_score, priority, est_hours, reason in gaps_data:
            kg = KnowledgeGap(
                id=f"gap-{top_id.replace('top-', '')}",
                student_id="stu-001",
                topic=topic_name,
                topic_id=top_id,
                gap_score=gap_score,
                priority=priority,
                estimated_hours=est_hours,
                reason=reason,
            )
            session.add(kg)

        # 5. Learning Resources
        res1 = LearningResource(
            id="res-1",
            title="Graph Algorithms Explained",
            type="video",
            topic="Graphs",
            difficulty="Intermediate",
            duration=30.0,
            quality_score=95.0,
            url="https://freecodecamp.org/graphs",
            source="Video • freeCodeCamp",
            detail="30:15",
        )
        res2 = LearningResource(
            id="res-2",
            title="DP Cheat Sheet & Tabulation",
            type="pdf",
            topic="Dynamic Programming",
            difficulty="Advanced",
            duration=45.0,
            quality_score=90.0,
            url="https://example.com/dp.pdf",
            source="PDF • 12 pages",
            detail="12 pages",
        )
        session.add_all([res1, res2])

        # 6. Recommendation
        rec1 = Recommendation(
            id="rec-1",
            student_id="stu-001",
            resource_id="res-1",
            gap_id="gap-graphs",
            reason="Directly addresses Dijkstra and shortest path knowledge gap",
            match_score=95.0,
            status="active",
        )
        session.add(rec1)

        # 7. Learning Plan & Plan Version
        plan = LearningPlan(
            id="plan-stu-001-v3",
            student_id="stu-001",
            goal_id="goal-001",
            current_version=3,
            status="active",
            target_deadline=datetime.utcnow() + timedelta(days=79),
            remaining_days=79,
            required_study_hours=96.0,
            scheduled_study_hours=102.0,
            feasibility_ratio=1.06,
            deadline_guaranteed=True,
        )
        session.add(plan)

        pver = PlanVersion(
            id="pver-3",
            plan_id="plan-stu-001-v3",
            version=3,
            status="active",
            summary="Autonomous rebalance after Trees review reschedule",
        )
        session.add(pver)

        # 8. Learning Activities
        act1 = LearningActivity(
            id="act-1",
            plan_id="plan-stu-001-v3",
            student_id="stu-001",
            resource_id="res-1",
            title="Graph Algorithms (Video)",
            topic="Graphs",
            type="video",
            scheduled_start=datetime.utcnow().replace(hour=9, minute=0, second=0),
            scheduled_end=datetime.utcnow().replace(hour=10, minute=0, second=0),
            status="completed",
            priority=1,
            duration_minutes=60,
            completed_at=datetime.utcnow(),
        )
        act2 = LearningActivity(
            id="act-2",
            plan_id="plan-stu-001-v3",
            student_id="stu-001",
            title="Practice: Dijkstra's Algorithm",
            topic="Graphs",
            type="practice",
            scheduled_start=datetime.utcnow().replace(hour=10, minute=30, second=0),
            scheduled_end=datetime.utcnow().replace(hour=11, minute=30, second=0),
            status="pending",
            priority=1,
            duration_minutes=60,
        )
        session.add_all([act1, act2])

        # 9. Plan Change
        change = PlanChange(
            id="pc-1",
            plan_id="plan-stu-001-v3",
            plan_version_id="pver-3",
            old_activity="Trees Video (Yesterday 6:00 PM)",
            new_activity="BST Traversals & Balancing (Saturday 9:30 AM)",
            reason="Missed session auto-shifted to open weekend morning study window",
            change_type="rescheduled",
        )
        session.add(change)

        # 10. Calendar Events
        cal1 = CalendarEvent(
            id="cal-1",
            student_id="stu-001",
            title="Morning Study Window",
            day=datetime.utcnow().strftime("%Y-%m-%d"),
            weekday=datetime.utcnow().strftime("%A"),
            start_time="09:00",
            end_time="11:30",
            duration_minutes=150,
            is_available=True,
            label="Morning Focus Block",
        )
        session.add(cal1)

        # 11. Assessment & Result
        asmt = Assessment(
            id="asmt-1",
            title="Sorting & Arrays Diagnostic",
            topic="Sorting",
            difficulty="Intermediate",
            total_questions=20,
            max_score=100.0,
        )
        session.add(asmt)

        asmt_res = AssessmentResult(
            id="asmt-res-1",
            assessment_id="asmt-1",
            student_id="stu-001",
            topic="Sorting",
            difficulty="Intermediate",
            score=80.0,
            max_score=100.0,
            percentage=80.0,
            status="passed",
            completed_at=datetime.utcnow() - timedelta(days=2),
        )
        session.add(asmt_res)

        # 12. Study Session
        study_sess = StudySession(
            id="sess-1",
            student_id="stu-001",
            activity_id="act-1",
            started_at=datetime.utcnow() - timedelta(hours=3),
            ended_at=datetime.utcnow() - timedelta(hours=2),
            duration_minutes=60.0,
            notes="Covered BFS and basic traversal logic smoothly",
            completed=True,
        )
        session.add(study_sess)

        # 13. Student Event
        se = StudentEvent(
            id="se-1",
            student_id="stu-001",
            event_type="activity_completed",
            details={"activity_id": "act-1", "topic": "Graphs", "duration": 60},
        )
        session.add(se)

        # 14. Agent Run
        agent_run = AgentRun(
            id="ar-1",
            student_id="stu-001",
            started_at=datetime.utcnow() - timedelta(hours=1),
            completed_at=datetime.utcnow() - timedelta(minutes=58),
            status="completed",
            steps_count=10,
            plan_version=3,
            actions_taken=[
                {"step": 1, "action": "Analyze Performance", "status": "completed"},
                {"step": 2, "action": "Detect Knowledge Gaps", "status": "completed"},
                {"step": 9, "action": "Autonomous Replan", "status": "completed"},
                {"step": 10, "action": "Verify Plan & Deadline Guarantee", "status": "completed"},
            ],
            summary="Autonomous replan complete. All constraints satisfied. Deadline guaranteed.",
        )
        session.add(agent_run)

        session.commit()
        print("Initial domain seed successfully committed!")

    except Exception as e:
        session.rollback()
        print(f"Error during init_db: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_db(seed_data=True)

"""
Validation test suite for all 17 LearnMate SQLAlchemy models.
"""

import sys
from datetime import datetime, timedelta
from app.db.base import engine
from app.db.session import SessionLocal
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

passed = 0
failed = 0


def assert_test(condition: bool, name: str):
    global passed, failed
    if condition:
        print(f"[PASS] {name}")
        passed += 1
    else:
        print(f"[FAIL] {name}")
        failed += 1


def test_models():
    session = SessionLocal()
    try:
        print("=" * 60)
        print("TESTING ALL 17 LEARN MATE SQLALCHEMY DATA MODELS")
        print("=" * 60)

        # 1. Student
        student = session.query(Student).filter(Student.id == "stu-001").first()
        assert_test(student is not None, "Student model queried")
        assert_test(student.name == "Prince Singh", "Student.name correct")
        assert_test(student.email == "prince.singh@university.edu", "Student.email correct")
        assert_test("morning" in student.preferred_study_times, "Student.preferred_study_times field")
        assert_test(student.weekly_available_hours == 15.0, "Student.weekly_available_hours field")

        # 2. LearningGoal
        goal = session.query(LearningGoal).filter(LearningGoal.student_id == "stu-001").first()
        assert_test(goal is not None, "LearningGoal model queried")
        assert_test(goal.title == "Master Data Structures & Algorithms", "LearningGoal.title field")
        assert_test(goal.target_proficiency == 85.0, "LearningGoal.target_proficiency field")
        assert_test(goal.status == "in_progress", "LearningGoal.status field")
        assert_test(len(goal.topics) > 0, "LearningGoal.topics field")

        # 3. Topic
        topics = session.query(Topic).all()
        assert_test(len(topics) >= 6, "Topic models queried (>= 6 topics)")
        tree_topic = session.query(Topic).filter(Topic.slug == "trees").first()
        assert_test(tree_topic is not None and tree_topic.name == "Trees", "Topic.slug and name correct")

        # 4. TopicMastery
        mastery = session.query(TopicMastery).filter(TopicMastery.topic == "Dynamic Programming").first()
        assert_test(mastery is not None, "TopicMastery model queried")
        assert_test(mastery.mastery_score == 25.0, "TopicMastery.mastery_score field")
        assert_test(mastery.confidence == 0.4, "TopicMastery.confidence field")
        assert_test(mastery.target_mastery == 80.0, "TopicMastery.target_mastery field")
        assert_test(mastery.trend == "critical_gap", "TopicMastery.trend field")

        # 5. KnowledgeGap
        gap = session.query(KnowledgeGap).filter(KnowledgeGap.topic == "Graphs").first()
        assert_test(gap is not None, "KnowledgeGap model queried")
        assert_test(gap.gap_score == 50.0, "KnowledgeGap.gap_score field")
        assert_test(gap.priority == "High", "KnowledgeGap.priority field")
        assert_test(gap.estimated_hours == 10.0, "KnowledgeGap.estimated_hours field")
        assert_test(len(gap.reason) > 0, "KnowledgeGap.reason field")

        # 6. LearningResource
        res = session.query(LearningResource).filter(LearningResource.id == "res-1").first()
        assert_test(res is not None, "LearningResource model queried")
        assert_test(res.title == "Graph Algorithms Explained", "LearningResource.title field")
        assert_test(res.type == "video", "LearningResource.type field")
        assert_test(res.difficulty == "Intermediate", "LearningResource.difficulty field")
        assert_test(res.duration == 30.0, "LearningResource.duration field")
        assert_test(res.quality_score == 95.0, "LearningResource.quality_score field")

        # 7. Recommendation
        rec = session.query(Recommendation).filter(Recommendation.id == "rec-1").first()
        assert_test(rec is not None, "Recommendation model queried")
        assert_test(rec.resource.title == "Graph Algorithms Explained", "Recommendation -> Resource relationship")
        assert_test(rec.gap.topic == "Graphs", "Recommendation -> Gap relationship")
        assert_test(rec.match_score == 95.0, "Recommendation.match_score field")

        # 8. LearningPlan
        plan = session.query(LearningPlan).filter(LearningPlan.id == "plan-stu-001-v3").first()
        assert_test(plan is not None, "LearningPlan model queried")
        assert_test(plan.current_version == 3, "LearningPlan.current_version field")
        assert_test(plan.status == "active", "LearningPlan.status field")
        assert_test(plan.deadline_guaranteed is True, "LearningPlan.deadline_guaranteed field")

        # 9. PlanVersion
        pver = session.query(PlanVersion).filter(PlanVersion.id == "pver-3").first()
        assert_test(pver is not None, "PlanVersion model queried")
        assert_test(pver.version == 3, "PlanVersion.version field")
        assert_test(pver.status == "active", "PlanVersion.status field")
        assert_test(pver.created_at is not None, "PlanVersion.createdAt field")

        # 10. PlanChange
        pchange = session.query(PlanChange).filter(PlanChange.id == "pc-1").first()
        assert_test(pchange is not None, "PlanChange model queried")
        assert_test("Trees" in pchange.old_activity, "PlanChange.old_activity field")
        assert_test("BST" in pchange.new_activity, "PlanChange.new_activity field")
        assert_test(len(pchange.reason) > 0, "PlanChange.reason field")

        # 11. LearningActivity
        act = session.query(LearningActivity).filter(LearningActivity.id == "act-1").first()
        assert_test(act is not None, "LearningActivity model queried")
        assert_test(act.topic == "Graphs", "LearningActivity.topic field")
        assert_test(act.type == "video", "LearningActivity.type field")
        assert_test(act.scheduled_start is not None, "LearningActivity.scheduled_start field")
        assert_test(act.scheduled_end is not None, "LearningActivity.scheduled_end field")
        assert_test(act.status == "completed", "LearningActivity.status field")
        assert_test(act.priority == 1, "LearningActivity.priority field")

        # 12. StudySession
        session_rec = session.query(StudySession).filter(StudySession.id == "sess-1").first()
        assert_test(session_rec is not None, "StudySession model queried")
        assert_test(session_rec.duration_minutes == 60.0, "StudySession.duration_minutes field")
        assert_test(session_rec.completed is True, "StudySession.completed field")

        # 13. CalendarEvent
        cal = session.query(CalendarEvent).filter(CalendarEvent.id == "cal-1").first()
        assert_test(cal is not None, "CalendarEvent model queried")
        assert_test(cal.is_available is True, "CalendarEvent.is_available field")
        assert_test(cal.start_time == "09:00", "CalendarEvent.start_time field")
        assert_test(cal.end_time == "11:30", "CalendarEvent.end_time field")

        # 14. Assessment
        asmt = session.query(Assessment).filter(Assessment.id == "asmt-1").first()
        assert_test(asmt is not None, "Assessment model queried")
        assert_test(asmt.topic == "Sorting", "Assessment.topic field")
        assert_test(asmt.max_score == 100.0, "Assessment.max_score field")

        # 15. AssessmentResult
        asmt_res = session.query(AssessmentResult).filter(AssessmentResult.id == "asmt-res-1").first()
        assert_test(asmt_res is not None, "AssessmentResult model queried")
        assert_test(asmt_res.score == 80.0, "AssessmentResult.score field")
        assert_test(asmt_res.topic == "Sorting", "AssessmentResult.topic field")
        assert_test(asmt_res.difficulty == "Intermediate", "AssessmentResult.difficulty field")
        assert_test(asmt_res.completed_at is not None, "AssessmentResult.completedAt field")

        # 16. StudentEvent
        se = session.query(StudentEvent).filter(StudentEvent.id == "se-1").first()
        assert_test(se is not None, "StudentEvent model queried")
        assert_test(se.event_type == "activity_completed", "StudentEvent.event_type field")
        assert_test(se.details["topic"] == "Graphs", "StudentEvent.details JSON field")

        # 17. AgentRun
        ar = session.query(AgentRun).filter(AgentRun.id == "ar-1").first()
        assert_test(ar is not None, "AgentRun model queried")
        assert_test(ar.started_at is not None, "AgentRun.startedAt field")
        assert_test(ar.completed_at is not None, "AgentRun.completedAt field")
        assert_test(ar.status == "completed", "AgentRun.status field")
        assert_test(len(ar.actions_taken) == 4, "AgentRun.actions_taken JSON field")
        assert_test(len(ar.summary) > 0, "AgentRun.summary field")

        # Test Dynamic Insert & Relationship Traversal
        session.query(LearningActivity).filter(LearningActivity.id == "act-test-new").delete()
        session.commit()

        new_activity = LearningActivity(
            id="act-test-new",
            plan_id="plan-stu-001-v3",
            student_id="stu-001",
            title="Dynamic Programming Memoization Drills",
            topic="Dynamic Programming",
            type="practice",
            scheduled_start=datetime.utcnow() + timedelta(days=1),
            scheduled_end=datetime.utcnow() + timedelta(days=1, hours=1),
            status="pending",
            priority=1,
            duration_minutes=60,
        )
        session.add(new_activity)
        session.commit()

        queried_new = session.query(LearningActivity).filter(LearningActivity.id == "act-test-new").first()
        assert_test(queried_new is not None, "Dynamically inserted activity verified")
        assert_test(queried_new.plan.id == "plan-stu-001-v3", "Activity -> Plan relationship traversal verified")

        print("=" * 60)
        print(f"RESULTS: {passed} PASSED, {failed} FAILED")
        print("=" * 60)

        if failed > 0:
            sys.exit(1)

    finally:
        session.close()


if __name__ == "__main__":
    test_models()

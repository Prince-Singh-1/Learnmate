"""
Comprehensive Unit Tests for LearnMate PlanVerifier.

Tests all 10 validation rules:
Rule 1: High-priority knowledge gaps receive enough learning time
Rule 2: Required topics are covered
Rule 3: Practice is included
Rule 4: Assessment is included
Rule 5: Revision is included
Rule 6: Calendar conflicts do not exist
Rule 7: Daily limits are respected
Rule 8: Weekly available hours are respected
Rule 9: Target deadline can still be reached
Rule 10: Required learning hours fit available time

Also verifies:
- Return schema { valid, warnings, violations, estimatedCompletionDate,
  goalCoverage, requiredHours, availableHours, goalStillAchievable }
- Invalid plans are not approved/activated
- Plan correction generation
"""

import sys
import unittest
from datetime import datetime, timedelta

from app.services.plan_verifier import PlanVerifier


class TestPlanVerifier(unittest.TestCase):
    def setUp(self):
        self.verifier = PlanVerifier()
        self.base_time = datetime.utcnow() + timedelta(days=2)
        self.deadline = self.base_time + timedelta(days=20)

        # Baseline valid plan satisfying all 10 rules
        self.valid_plan = {
            "id": "plan-valid-001",
            "version": 1,
            "target_deadline": self.deadline.isoformat(),
            "required_study_hours": 6.0,
            "activities": [
                {
                    "id": "act-dp-learn",
                    "topic": "Dynamic Programming",
                    "title": "DP Foundations",
                    "type": "Learn",
                    "scheduled_start": self.base_time.replace(hour=9, minute=0).isoformat(),
                    "scheduled_end": self.base_time.replace(hour=10, minute=0).isoformat(),
                    "duration_minutes": 60,
                    "priority": 1,
                },
                {
                    "id": "act-dp-practice",
                    "topic": "Dynamic Programming",
                    "title": "DP Knapsack Practice",
                    "type": "Practice",
                    "scheduled_start": (self.base_time + timedelta(days=1)).replace(hour=9, minute=0).isoformat(),
                    "scheduled_end": (self.base_time + timedelta(days=1)).replace(hour=11, minute=0).isoformat(),
                    "duration_minutes": 120,
                    "priority": 1,
                },
                {
                    "id": "act-graph-practice",
                    "topic": "Graphs",
                    "title": "BFS & DFS Coding Practice",
                    "type": "Coding Practice",
                    "scheduled_start": (self.base_time + timedelta(days=2)).replace(hour=9, minute=0).isoformat(),
                    "scheduled_end": (self.base_time + timedelta(days=2)).replace(hour=11, minute=0).isoformat(),
                    "duration_minutes": 120,
                    "priority": 1,
                },
                {
                    "id": "act-dp-quiz",
                    "topic": "Dynamic Programming",
                    "title": "DP Milestone Assessment",
                    "type": "Assessment",
                    "scheduled_start": (self.base_time + timedelta(days=3)).replace(hour=9, minute=0).isoformat(),
                    "scheduled_end": (self.base_time + timedelta(days=3)).replace(hour=9, minute=30).isoformat(),
                    "duration_minutes": 30,
                    "priority": 1,
                },
                {
                    "id": "act-sort-revision",
                    "topic": "Sorting",
                    "title": "QuickSort Spaced Revision",
                    "type": "Revision",
                    "scheduled_start": (self.base_time + timedelta(days=4)).replace(hour=9, minute=0).isoformat(),
                    "scheduled_end": (self.base_time + timedelta(days=4)).replace(hour=9, minute=30).isoformat(),
                    "duration_minutes": 30,
                    "priority": 3,
                },
            ],
        }

        self.valid_gaps = [
            {"topic": "Dynamic Programming", "priority": "High", "estimated_hours": 3.0},
            {"topic": "Graphs", "priority": "High", "estimated_hours": 2.0},
        ]
        self.valid_goals = ["Dynamic Programming", "Graphs", "Sorting"]

    def test_baseline_valid_plan_passes_all_rules(self):
        """Baseline balanced plan must pass all 10 rules."""
        res = self.verifier.verify(
            plan=self.valid_plan,
            goals=self.valid_goals,
            deadline=self.deadline.isoformat(),
            knowledge_gaps=self.valid_gaps,
            daily_limit_hours=3.5,
            weekly_available_hours=15.0,
        )
        self.assertTrue(res["valid"])
        self.assertEqual(len(res["violations"]), 0)
        self.assertEqual(res["goalCoverage"], 100.0)
        self.assertTrue(res["goalStillAchievable"])
        self.assertIn("valid", res)
        self.assertIn("warnings", res)
        self.assertIn("violations", res)
        self.assertIn("estimatedCompletionDate", res)
        self.assertIn("goalCoverage", res)
        self.assertIn("requiredHours", res)
        self.assertIn("availableHours", res)
        self.assertIn("goalStillAchievable", res)

    # -------------------------------------------------------------
    # RULE 1: High-Priority Knowledge Gaps Learning Time
    # -------------------------------------------------------------
    def test_rule_1_high_priority_gap_insufficient_time(self):
        """Rule 1 violation when a high priority gap receives zero or insufficient study time."""
        # Dynamic Programming requires 10 hours, but only 3 hours scheduled
        large_gap = [
            {"topic": "Dynamic Programming", "priority": "High", "estimated_hours": 10.0},
        ]
        res = self.verifier.verify(
            plan=self.valid_plan,
            goals=self.valid_goals,
            deadline=self.deadline.isoformat(),
            knowledge_gaps=large_gap,
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 1 Violation" in v and "Dynamic Programming" in v for v in res["violations"]))

    # -------------------------------------------------------------
    # RULE 2: Required Topics Covered
    # -------------------------------------------------------------
    def test_rule_2_uncovered_required_topic(self):
        """Rule 2 violation when a required goal topic has no scheduled activities."""
        goals_with_uncovered = ["Dynamic Programming", "Graphs", "Sorting", "Heaps and Tries"]
        res = self.verifier.verify(
            plan=self.valid_plan,
            goals=goals_with_uncovered,
            deadline=self.deadline.isoformat(),
            knowledge_gaps=self.valid_gaps,
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 2 Violation" in v and "Heaps and Tries" in v for v in res["violations"]))
        self.assertLess(res["goalCoverage"], 100.0)

    # -------------------------------------------------------------
    # RULE 3: Practice Is Included
    # -------------------------------------------------------------
    def test_rule_3_missing_practice(self):
        """Rule 3 violation when plan contains 0 practice activities."""
        plan_no_practice = dict(self.valid_plan)
        plan_no_practice["activities"] = [
            a for a in self.valid_plan["activities"]
            if a.get("type") not in ["Practice", "Coding Practice"]
        ]
        res = self.verifier.verify(
            plan=plan_no_practice,
            goals=self.valid_goals,
            deadline=self.deadline.isoformat(),
            knowledge_gaps=[],
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 3 Violation" in v for v in res["violations"]))

    # -------------------------------------------------------------
    # RULE 4: Assessment Is Included
    # -------------------------------------------------------------
    def test_rule_4_missing_assessment(self):
        """Rule 4 violation when plan contains 0 assessment / quiz activities."""
        plan_no_assessment = dict(self.valid_plan)
        plan_no_assessment["activities"] = [
            a for a in self.valid_plan["activities"]
            if a.get("type") not in ["Assessment", "Quiz"]
        ]
        res = self.verifier.verify(
            plan=plan_no_assessment,
            goals=self.valid_goals,
            deadline=self.deadline.isoformat(),
            knowledge_gaps=[],
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 4 Violation" in v for v in res["violations"]))

    # -------------------------------------------------------------
    # RULE 5: Revision Is Included
    # -------------------------------------------------------------
    def test_rule_5_missing_revision(self):
        """Rule 5 violation when plan contains 0 revision activities."""
        plan_no_revision = dict(self.valid_plan)
        plan_no_revision["activities"] = [
            a for a in self.valid_plan["activities"]
            if a.get("type") not in ["Revision", "Review"]
        ]
        res = self.verifier.verify(
            plan=plan_no_revision,
            goals=self.valid_goals,
            deadline=self.deadline.isoformat(),
            knowledge_gaps=[],
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 5 Violation" in v for v in res["violations"]))

    # -------------------------------------------------------------
    # RULE 6: Calendar Conflicts Do Not Exist
    # -------------------------------------------------------------
    def test_rule_6_calendar_conflict_detected(self):
        """Rule 6 violation when an activity overlaps with a busy calendar block."""
        conflict_event = {
            "title": "Final Team Presentation",
            "start": self.base_time.replace(hour=9, minute=30).isoformat(),
            "end": self.base_time.replace(hour=10, minute=30).isoformat(),
        }
        res = self.verifier.verify(
            plan=self.valid_plan,
            goals=self.valid_goals,
            deadline=self.deadline.isoformat(),
            calendar_events=[conflict_event],
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 6 Violation" in v and "Final Team Presentation" in v for v in res["violations"]))

    # -------------------------------------------------------------
    # RULE 7: Daily Limits Respected
    # -------------------------------------------------------------
    def test_rule_7_daily_limit_exceeded(self):
        """Rule 7 violation when activities scheduled on a single day exceed daily limit."""
        overloaded_day = dict(self.valid_plan)
        # Put 5 hours on day 1 (limit is 3.5h)
        overloaded_day["activities"] = [
            {
                "id": "act-heavy-1",
                "topic": "Dynamic Programming",
                "title": "DP Deep Dive",
                "type": "Learn",
                "scheduled_start": self.base_time.replace(hour=8, minute=0).isoformat(),
                "scheduled_end": self.base_time.replace(hour=13, minute=0).isoformat(),
                "duration_minutes": 300,  # 5 hours!
            },
            {
                "id": "act-heavy-practice",
                "topic": "Dynamic Programming",
                "title": "Practice",
                "type": "Practice",
                "scheduled_start": (self.base_time + timedelta(days=1)).isoformat(),
                "duration_minutes": 60,
            },
            {
                "id": "act-heavy-quiz",
                "topic": "Dynamic Programming",
                "title": "Quiz",
                "type": "Quiz",
                "scheduled_start": (self.base_time + timedelta(days=2)).isoformat(),
                "duration_minutes": 30,
            },
            {
                "id": "act-heavy-rev",
                "topic": "Dynamic Programming",
                "title": "Revision",
                "type": "Revision",
                "scheduled_start": (self.base_time + timedelta(days=3)).isoformat(),
                "duration_minutes": 30,
            },
        ]
        res = self.verifier.verify(
            plan=overloaded_day,
            goals=["Dynamic Programming"],
            deadline=self.deadline.isoformat(),
            daily_limit_hours=3.5,
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 7 Violation" in v and "Daily study limit exceeded" in v for v in res["violations"]))

    # -------------------------------------------------------------
    # RULE 8: Weekly Available Hours Respected
    # -------------------------------------------------------------
    def test_rule_8_weekly_limit_exceeded(self):
        """Rule 8 violation when total hours in a week exceed weekly limit."""
        overloaded_week = dict(self.valid_plan)
        # Put 20 hours in the same week (limit is 15h)
        overloaded_week["activities"] = [
            {
                "id": f"act-day-{i}",
                "topic": "Dynamic Programming",
                "title": f"Study Block {i}",
                "type": "Practice" if i % 2 == 0 else "Learn",
                "scheduled_start": (self.base_time + timedelta(days=i)).replace(hour=9, minute=0).isoformat(),
                "scheduled_end": (self.base_time + timedelta(days=i)).replace(hour=12, minute=0).isoformat(),
                "duration_minutes": 180,  # 3 hours * 7 days = 21 hours
            }
            for i in range(7)
        ] + [
            {"id": "act-quiz", "topic": "Dynamic Programming", "type": "Quiz", "duration_minutes": 30, "scheduled_start": (self.base_time + timedelta(days=1, hours=4)).isoformat()},
            {"id": "act-rev", "topic": "Dynamic Programming", "type": "Revision", "duration_minutes": 30, "scheduled_start": (self.base_time + timedelta(days=2, hours=4)).isoformat()},
        ]
        res = self.verifier.verify(
            plan=overloaded_week,
            goals=["Dynamic Programming"],
            deadline=self.deadline.isoformat(),
            weekly_available_hours=15.0,
            daily_limit_hours=4.0,
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 8 Violation" in v and "Weekly hours exceeded" in v for v in res["violations"]))

    # -------------------------------------------------------------
    # RULE 9: Target Deadline Can Still Be Reached
    # -------------------------------------------------------------
    def test_rule_9_target_deadline_breached(self):
        """Rule 9 violation when scheduled activities end after target deadline."""
        past_deadline = self.base_time + timedelta(days=5)
        res = self.verifier.verify(
            plan=self.valid_plan,  # activities run up to day 4 (base_time + 4 days, but let's set deadline earlier)
            goals=self.valid_goals,
            deadline=(self.base_time + timedelta(days=1)).isoformat(),  # deadline is day 1, plan ends day 4!
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 9 Violation" in v and "breaches target deadline" in v for v in res["violations"]))

    # -------------------------------------------------------------
    # RULE 10: Required Learning Hours Fit Available Time
    # -------------------------------------------------------------
    def test_rule_10_required_hours_exceed_available_time(self):
        """Rule 10 violation when required hours exceed remaining available hours before deadline."""
        # 40 hours required, but only 2 days left at 7h/week = ~2.0 hours available!
        res = self.verifier.verify(
            plan={
                "id": "plan-huge",
                "required_study_hours": 40.0,
                "activities": self.valid_plan["activities"],
            },
            goals=self.valid_goals,
            deadline=(datetime.utcnow() + timedelta(days=2)).isoformat(),
            weekly_available_hours=7.0,
        )
        self.assertFalse(res["valid"])
        self.assertTrue(any("Rule 10 Violation" in v and "exceed available study capacity" in v for v in res["violations"]))
        self.assertFalse(res["goalStillAchievable"])

    # -------------------------------------------------------------
    # Auto-Correction & Invalidation Handling
    # -------------------------------------------------------------
    def test_generate_corrected_plan_resolves_violations(self):
        """Auto-correction must resolve missing practice/assessment/revision violations."""
        incomplete_plan = {
            "id": "plan-incomplete",
            "version": 1,
            "target_deadline": (self.base_time + timedelta(days=20)).isoformat(),
            "activities": [
                {
                    "id": "act-only-learn",
                    "topic": "Dynamic Programming",
                    "title": "DP Only Theory",
                    "type": "Learn",
                    "scheduled_start": self.base_time.replace(hour=9, minute=0).isoformat(),
                    "scheduled_end": self.base_time.replace(hour=10, minute=0).isoformat(),
                    "duration_minutes": 60,
                }
            ],
        }
        # Incomplete plan has no practice, assessment, or revision
        initial_verif = self.verifier.verify(
            plan=incomplete_plan,
            goals=["Dynamic Programming"],
        )
        self.assertFalse(initial_verif["valid"])
        self.assertTrue(len(initial_verif["violations"]) >= 3)

        # Generate corrected plan
        corrected = self.verifier.generate_corrected_plan(
            invalid_plan=incomplete_plan,
            verification_result=initial_verif,
            goals=["Dynamic Programming"],
        )
        corrected_types = [a.get("type") for a in corrected["activities"]]
        self.assertIn("Practice", corrected_types)
        self.assertIn("Quiz", corrected_types)
        self.assertIn("Revision", corrected_types)

        # Re-verify corrected plan
        post_verif = self.verifier.verify(
            plan=corrected,
            goals=["Dynamic Programming"],
            deadline=(self.base_time + timedelta(days=20)).isoformat(),
        )
        self.assertTrue(post_verif["valid"])
        self.assertEqual(len(post_verif["violations"]), 0)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlanVerifier)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

"""
Comprehensive Test Suite for LearnMate Autonomous Replanning Engine.

Tests ReplanningService:
- All 7 inputs (current plan, student state, new performance, new calendar availability,
  missed activities, remaining time, goal deadline)
- Comparison between OLD PLAN and NEW PLAN
- Detection of all 8 possible actions:
    1. move activity
    2. remove activity
    3. add activity
    4. shorten activity
    5. extend activity
    6. change resource
    7. change activity type
    8. change priority
- Preservation of high-priority learning objectives
- PlanChange record generation for every modification
- Explicit explanations for every change (no silent modifications)
- Return schema { oldPlan, newPlan, changes, reason, goalStillAchievable }
- goalStillAchievable evaluation under achievable and unachievable scenarios
"""

import sys
import unittest
from datetime import datetime, timedelta

from app.services.replanning_service import (
    ReplanningService,
    ReplanningAction,
    PlanChangeItem,
    ReplanResult,
)


class TestReplanningService(unittest.TestCase):
    def setUp(self):
        self.service = ReplanningService()
        self.base_time = datetime.utcnow() + timedelta(days=1)
        self.old_plan = {
            "version": 1,
            "title": "Technical Interview Preparation",
            "target_deadline": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "activities": [
                {
                    "id": "act-dp-1",
                    "topic": "Dynamic Programming",
                    "title": "Dynamic Programming Foundations",
                    "type": "Learn",
                    "scheduled_start": self.base_time.replace(hour=9, minute=0).isoformat(),
                    "scheduled_end": self.base_time.replace(hour=10, minute=0).isoformat(),
                    "duration_minutes": 60,
                    "priority": 1,
                    "resource": "video-dp-01",
                    "status": "pending",
                },
                {
                    "id": "act-graph-1",
                    "topic": "Graphs",
                    "title": "Graph Traversal BFS & DFS",
                    "type": "Practice",
                    "scheduled_start": self.base_time.replace(hour=11, minute=0).isoformat(),
                    "scheduled_end": self.base_time.replace(hour=12, minute=0).isoformat(),
                    "duration_minutes": 60,
                    "priority": 1,
                    "resource": "quiz-graph-01",
                    "status": "pending",
                },
                {
                    "id": "act-sort-1",
                    "topic": "Sorting",
                    "title": "QuickSort & MergeSort Review",
                    "type": "Revision",
                    "scheduled_start": self.base_time.replace(hour=14, minute=0).isoformat(),
                    "scheduled_end": self.base_time.replace(hour=15, minute=0).isoformat(),
                    "duration_minutes": 60,
                    "priority": 3,
                    "resource": "article-sort-01",
                    "status": "pending",
                },
            ],
        }

    def test_return_structure_schema(self):
        """Verify return dict matches exact required keys."""
        res = self.service.replan(
            current_plan=self.old_plan,
            remaining_time={"days": 25},
        )
        self.assertIn("oldPlan", res)
        self.assertIn("newPlan", res)
        self.assertIn("changes", res)
        self.assertIn("reason", res)
        self.assertIn("goalStillAchievable", res)
        self.assertIsInstance(res["oldPlan"], dict)
        self.assertIsInstance(res["newPlan"], dict)
        self.assertIsInstance(res["changes"], list)
        self.assertIsInstance(res["reason"], str)
        self.assertIsInstance(res["goalStillAchievable"], bool)

    def test_action_move_activity_on_missed_session(self):
        """Missed session triggers 'move activity' to reschedule catch-up time."""
        missed = [
            {
                "id": "act-missed-1",
                "topic": "Dynamic Programming",
                "title": "DP Knapsack Practice",
                "duration_minutes": 45,
                "type": "Practice",
            }
        ]
        res = self.service.replan(
            current_plan=self.old_plan,
            missed_activities=missed,
            remaining_time={"days": 20},
        )
        actions = [c["action"] for c in res["changes"]]
        self.assertIn(ReplanningAction.MOVE_ACTIVITY.value, actions)
        move_change = next(c for c in res["changes"] if c["action"] == ReplanningAction.MOVE_ACTIVITY.value)
        self.assertIn("Moved Dynamic Programming", move_change["explanation"])
        self.assertTrue(len(move_change["explanation"]) > 10)

    def test_preserves_high_priority_and_removes_low_priority(self):
        """When missed session stresses study cap, drop low-priority Sorting, preserve DP & Graphs."""
        missed = [
            {
                "id": "act-missed-dp",
                "topic": "Dynamic Programming",
                "title": "DP Memoization Drill",
                "duration_minutes": 60,
                "type": "Practice",
            }
        ]
        res = self.service.replan(
            current_plan=self.old_plan,
            missed_activities=missed,
            remaining_time={"days": 15},
        )
        actions = [c["action"] for c in res["changes"]]
        self.assertIn(ReplanningAction.REMOVE_ACTIVITY.value, actions)
        rem_change = next(c for c in res["changes"] if c["action"] == ReplanningAction.REMOVE_ACTIVITY.value)
        self.assertIn("preserve high-priority", rem_change["explanation"].lower())

        # Check new plan activities: DP and Graphs must still exist; Sorting revision was removed
        new_topics = [a["topic"] for a in res["newPlan"]["activities"]]
        self.assertIn("Dynamic Programming", new_topics)
        self.assertIn("Graphs", new_topics)
        self.assertNotIn("Sorting", new_topics)

    def test_action_extend_activity_on_poor_performance(self):
        """Poor performance on Dynamic Programming triggers 'extend activity' by 30m."""
        perf = {
            "score": 42.0,
            "topic": "Dynamic Programming",
            "weak_topics": ["Dynamic Programming"],
        }
        res = self.service.replan(
            current_plan=self.old_plan,
            new_performance=perf,
        )
        actions = [c["action"] for c in res["changes"]]
        self.assertIn(ReplanningAction.EXTEND_ACTIVITY.value, actions)
        ext_change = next(c for c in res["changes"] if c["action"] == ReplanningAction.EXTEND_ACTIVITY.value)
        self.assertIn("Extended Dynamic Programming", ext_change["explanation"])

        # Verify activity duration increased
        dp_act = next(a for a in res["newPlan"]["activities"] if a["topic"] == "Dynamic Programming")
        self.assertEqual(dp_act["duration_minutes"], 90)

    def test_action_add_activity_for_new_weak_topic(self):
        """Lagging topic without existing scheduled session triggers 'add activity'."""
        perf = {
            "weak_topics": ["Binary Trees"],
        }
        res = self.service.replan(
            current_plan=self.old_plan,
            new_performance=perf,
        )
        actions = [c["action"] for c in res["changes"]]
        self.assertIn(ReplanningAction.ADD_ACTIVITY.value, actions)
        add_change = next(c for c in res["changes"] if c["action"] == ReplanningAction.ADD_ACTIVITY.value)
        self.assertIn("Added 45m remedial practice", add_change["explanation"])

        tree_acts = [a for a in res["newPlan"]["activities"] if a["topic"] == "Binary Trees"]
        self.assertEqual(len(tree_acts), 1)

    def test_action_shorten_activity_and_change_priority_on_high_mastery(self):
        """Mastered topic triggers 'shorten activity' and 'change priority'."""
        perf = {
            "strong_topics": ["Graphs"],
        }
        res = self.service.replan(
            current_plan=self.old_plan,
            new_performance=perf,
        )
        actions = [c["action"] for c in res["changes"]]
        self.assertIn(ReplanningAction.SHORTEN_ACTIVITY.value, actions)
        self.assertIn(ReplanningAction.CHANGE_PRIORITY.value, actions)

        short_change = next(c for c in res["changes"] if c["action"] == ReplanningAction.SHORTEN_ACTIVITY.value)
        self.assertIn("Shortened Graphs", short_change["explanation"])

        graph_act = next(a for a in res["newPlan"]["activities"] if a["topic"] == "Graphs")
        self.assertEqual(graph_act["duration_minutes"], 20)
        self.assertEqual(graph_act["priority"], 2)

    def test_action_move_activity_on_calendar_conflict(self):
        """Calendar conflict shifts overlapping activity forward."""
        conflict_start = self.base_time.replace(hour=9, minute=15)
        conflict_end = self.base_time.replace(hour=10, minute=30)
        cal = {
            "conflicts": [
                {
                    "title": "Team Standup & Review",
                    "start": conflict_start.isoformat(),
                    "end": conflict_end.isoformat(),
                }
            ]
        }
        res = self.service.replan(
            current_plan=self.old_plan,
            new_calendar_availability=cal,
        )
        actions = [c["action"] for c in res["changes"]]
        self.assertIn(ReplanningAction.MOVE_ACTIVITY.value, actions)
        move_change = next(c for c in res["changes"] if c["action"] == ReplanningAction.MOVE_ACTIVITY.value)
        self.assertIn("Team Standup", move_change["explanation"])

    def test_action_change_activity_type(self):
        """Learner preference triggers 'change activity type' from Learn to Coding Practice."""
        perf = {
            "prefer_interactive_practice": True,
        }
        res = self.service.replan(
            current_plan=self.old_plan,
            new_performance=perf,
        )
        actions = [c["action"] for c in res["changes"]]
        self.assertIn(ReplanningAction.CHANGE_ACTIVITY_TYPE.value, actions)
        type_change = next(c for c in res["changes"] if c["action"] == ReplanningAction.CHANGE_ACTIVITY_TYPE.value)
        self.assertIn("Coding Practice", type_change["explanation"])

    def test_compare_plans_detects_all_8_actions(self):
        """Test explicit compare_plans detects all 8 possible actions."""
        new_plan = {
            "version": 2,
            "target_deadline": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "activities": [
                # 1. Moved + Extended + Changed Resource + Changed Type: act-dp-1
                {
                    "id": "act-dp-1",
                    "topic": "Dynamic Programming",
                    "title": "Dynamic Programming Advanced",
                    "type": "Coding Practice",  # changed type
                    "scheduled_start": (self.base_time + timedelta(hours=3)).isoformat(),  # moved
                    "scheduled_end": (self.base_time + timedelta(hours=4, minutes=30)).isoformat(),
                    "duration_minutes": 90,  # extended (60 -> 90)
                    "priority": 1,
                    "resource": "visualizer-dp-interactive",  # changed resource
                    "status": "pending",
                },
                # 2. Shortened + Changed Priority: act-graph-1
                {
                    "id": "act-graph-1",
                    "topic": "Graphs",
                    "title": "Graph Traversal Rapid Check",
                    "type": "Practice",
                    "scheduled_start": self.base_time.replace(hour=11, minute=0).isoformat(),
                    "scheduled_end": self.base_time.replace(hour=11, minute=30).isoformat(),
                    "duration_minutes": 30,  # shortened (60 -> 30)
                    "priority": 2,  # changed priority (1 -> 2)
                    "resource": "quiz-graph-01",
                    "status": "pending",
                },
                # 3. act-sort-1 is REMOVED
                # 4. act-greedy-new is ADDED
                {
                    "id": "act-greedy-new",
                    "topic": "Greedy Algorithms",
                    "title": "Greedy Interval Scheduling Drill",
                    "type": "Practice",
                    "duration_minutes": 45,
                    "priority": 1,
                    "status": "pending",
                },
            ],
        }

        diff = self.service.compare_plans(self.old_plan, new_plan)
        actions = [c["action"] for c in diff["changes"]]

        self.assertIn(ReplanningAction.MOVE_ACTIVITY.value, actions)
        self.assertIn(ReplanningAction.REMOVE_ACTIVITY.value, actions)
        self.assertIn(ReplanningAction.ADD_ACTIVITY.value, actions)
        self.assertIn(ReplanningAction.SHORTEN_ACTIVITY.value, actions)
        self.assertIn(ReplanningAction.EXTEND_ACTIVITY.value, actions)
        self.assertIn(ReplanningAction.CHANGE_RESOURCE.value, actions)
        self.assertIn(ReplanningAction.CHANGE_ACTIVITY_TYPE.value, actions)
        self.assertIn(ReplanningAction.CHANGE_PRIORITY.value, actions)

        # Confirm all 8 unique action types detected
        unique_actions = set(actions)
        self.assertEqual(len(unique_actions), 8)

    def test_goal_still_achievable_evaluation(self):
        """Verify goalStillAchievable is True when ample time remains, and False when impossible."""
        # Achievable: 30 days left, 15h/week = ~64 hours available; plan has only 3 hours
        res_achievable = self.service.replan(
            current_plan=self.old_plan,
            remaining_time={"days": 30},
            new_calendar_availability={"weekly_available_hours": 15.0},
        )
        self.assertTrue(res_achievable["goalStillAchievable"])

        # Impossible: 1 day left, 2 hours/week available = ~0.28 hours available; plan has 3 hours
        res_unachievable = self.service.replan(
            current_plan=self.old_plan,
            remaining_time={"days": 1},
            new_calendar_availability={"weekly_available_hours": 1.0},
        )
        self.assertFalse(res_unachievable["goalStillAchievable"])

    def test_no_silent_modifications(self):
        """Every modification must produce a PlanChange record with a non-empty explanation."""
        missed = [
            {"id": "m1", "topic": "Dynamic Programming", "duration_minutes": 45},
            {"id": "m2", "topic": "Graphs", "duration_minutes": 45},
        ]
        perf = {"weak_topics": ["Heaps"]}
        res = self.service.replan(
            current_plan=self.old_plan,
            missed_activities=missed,
            new_performance=perf,
        )
        self.assertTrue(len(res["changes"]) > 0)
        for chg in res["changes"]:
            self.assertTrue(bool(chg.get("explanation")), f"Change {chg.get('id')} has empty explanation!")
            self.assertTrue(bool(chg.get("reason")), f"Change {chg.get('id')} has empty reason!")
            self.assertTrue(bool(chg.get("action")), f"Change {chg.get('id')} has empty action!")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReplanningService)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

"""
Unit Tests for LearnMate Autonomous Learning Agent (AgentOrchestrator).

Validates:
1. Closed-loop 12-stage autonomous workflow execution:
   LOAD STUDENT STATE -> ANALYZE PERFORMANCE -> IDENTIFY KNOWLEDGE GAPS ->
   RETRIEVE RESOURCES -> SELECT RESOURCES -> CREATE/UPDATE PLAN ->
   VERIFY PLAN -> ACTIVATE PLAN -> TRACK ACTIVITIES ->
   REASSESS PERFORMANCE -> DETECT CHANGES -> REPLAN IF NECESSARY
2. Verification of all 9 change detection telemetry conditions:
   - 1. Missed sessions
   - 2. Poor assessment performance
   - 3. Better-than-expected performance
   - 4. Faster-than-expected progress
   - 5. Slower-than-expected progress
   - 6. Reduced study availability
   - 7. Increased study availability
   - 8. Changed deadline
   - 9. Changed learning goal
3. Creation of an AgentRun record for every run.
4. Creation of PlanChange records for every plan modification.
5. Human-readable explanation matching the exact specification:
   "Two sessions were missed, reducing available learning time by 90 minutes. The agent moved Dynamic Programming practice to Saturday and removed low-priority Sorting revision."
6. PlanVerifier approval gate:
   - Agent does NOT activate plan when verifier rejects it (e.g. insufficient time)
   - Agent activates plan only when verifier approves it
"""

import sys
import asyncio
from datetime import datetime, timedelta
from app.agent.agent_orchestrator import (
    AgentOrchestrator,
    ChangeCategory,
    DetectedChange,
    AgentRunRecord,
    PlanChangeRecord,
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


async def test_agent_orchestrator():
    print("=" * 65)
    print("RUNNING UNIT TESTS FOR AGENT ORCHESTRATOR")
    print("=" * 65)

    orchestrator = AgentOrchestrator()

    # -------------------------------------------------------------
    # Test 1: Full 12-Stage Autonomous Loop Execution
    # -------------------------------------------------------------
    res = await orchestrator.execute_cycle(student_id="stu-001")

    assert_test(res["success"] is True, "Autonomous cycle executes successfully")
    assert_test(res["plan_activated"] is True, "Plan activated upon PlanVerifier approval")
    assert_test("agent_run" in res, "AgentRun record returned in output")
    agent_run = res["agent_run"]

    # Verify all 12 stages are logged in actions_taken
    stages = [a["stage"] for a in agent_run["actions_taken"]]
    expected_stages = [
        "LOAD_STUDENT_STATE",
        "ANALYZE_PERFORMANCE",
        "IDENTIFY_KNOWLEDGE_GAPS",
        "RETRIEVE_RESOURCES",
        "SELECT_RESOURCES",
        "CREATE_OR_UPDATE_PLAN",
        "VERIFY_PLAN",
        "ACTIVATE_PLAN",
        "TRACK_ACTIVITIES",
        "REASSESS_PERFORMANCE",
        "DETECT_CHANGES",
        "REPLAN_IF_NECESSARY",
    ]
    for expected in expected_stages:
        assert_test(expected in stages, f"Workflow includes stage '{expected}'")

    # -------------------------------------------------------------
    # Test 2: AgentRun Record Created & Populated
    # -------------------------------------------------------------
    assert_test(agent_run["id"].startswith("run-"), "AgentRun has unique run id")
    assert_test(agent_run["student_id"] == "stu-001", "AgentRun contains student_id")
    assert_test("started_at" in agent_run and "completed_at" in agent_run, "AgentRun contains timestamps")
    assert_test(agent_run["status"] == "completed", "AgentRun status is completed")
    assert_test(len(agent_run["summary"]) > 20, "AgentRun contains summary")

    # -------------------------------------------------------------
    # Test 3: PlanVerifier Gate (Plan NOT Activated if Verifier Rejects)
    # -------------------------------------------------------------
    # Overrides with an impossible deadline (1 day for 30 hours of work)
    infeasible_overrides = {
        "target_deadline": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "max_daily_study_hours": 1.0,
        "weekly_available_hours": 5.0,
        "knowledge_gaps": [
            {"topic": "Dynamic Programming", "priority": "High", "estimated_hours": 15.0},
            {"topic": "Graphs", "priority": "High", "estimated_hours": 15.0},
        ],
    }
    blocked_res = await orchestrator.execute_cycle(
        student_id="stu-001",
        state_overrides=infeasible_overrides,
    )

    assert_test(
        blocked_res["plan_activated"] is False,
        "PlanVerifier Gate: Agent DOES NOT activate plan when constraints fail"
    )
    assert_test(
        blocked_res["agent_run"]["plan_activated"] is False,
        "AgentRun record reflects unactivated plan status"
    )

    # -------------------------------------------------------------
    # Test 4: Missed Sessions & User Prompt Exact Example
    # "Two sessions were missed, reducing available learning time by 90 minutes.
    # The agent moved Dynamic Programming practice to Saturday and removed low-priority Sorting revision."
    # -------------------------------------------------------------
    missed_sessions_overrides = {
        "missed_activities": [
            {"id": "missed-1", "topic": "Dynamic Programming", "title": "DP Tabulation Practice", "duration_minutes": 45},
            {"id": "missed-2", "topic": "Dynamic Programming", "title": "DP Memoization Drills", "duration_minutes": 45},
        ],
    }
    missed_res = await orchestrator.execute_cycle(
        student_id="stu-001",
        state_overrides=missed_sessions_overrides,
    )

    assert_test(
        ChangeCategory.MISSED_SESSIONS.value in missed_res["detected_changes"],
        "Condition 1: Missed sessions detected"
    )
    assert_test(
        len(missed_res["plan_changes"]) >= 2,
        "PlanChange records created for missed session rebalance"
    )

    # Validate the human-readable explanation matching the user's requirement
    explanation = missed_res["explanation"]
    assert_test(
        "Two sessions were missed, reducing available learning time by 90 minutes" in explanation or
        "2 session(s) missed, reducing available learning time by 90 minutes" in explanation,
        f"Explanation states missed sessions and 90 minutes impact: '{explanation}'"
    )
    assert_test(
        "The agent moved Dynamic Programming practice to Saturday and removed low-priority Sorting revision" in explanation,
        f"Explanation contains exact action sentence: '{explanation}'"
    )

    # -------------------------------------------------------------
    # Test 5: Detection of All 9 Conditions
    # -------------------------------------------------------------
    # Condition 2: Poor assessment performance
    poor_asmt_res = await orchestrator.execute_cycle(
        state_overrides={"recent_assessments": [{"topic": "Dynamic Programming", "score": 32.0}]}
    )
    assert_test(ChangeCategory.POOR_ASSESSMENT.value in poor_asmt_res["detected_changes"], "Condition 2: Poor assessment detected")

    # Condition 3: Better-than-expected performance
    better_perf_res = await orchestrator.execute_cycle(
        state_overrides={"recent_assessments": [{"topic": "Sorting", "score": 96.0}]}
    )
    assert_test(ChangeCategory.BETTER_THAN_EXPECTED.value in better_perf_res["detected_changes"], "Condition 3: Better-than-expected performance detected")

    # Condition 4: Faster-than-expected progress
    fast_res = await orchestrator.execute_cycle(state_overrides={"learning_velocity": 1.40})
    assert_test(ChangeCategory.FASTER_PROGRESS.value in fast_res["detected_changes"], "Condition 4: Faster progress detected (1.40x)")

    # Condition 5: Slower-than-expected progress
    slow_res = await orchestrator.execute_cycle(state_overrides={"learning_velocity": 0.65})
    assert_test(ChangeCategory.SLOWER_PROGRESS.value in slow_res["detected_changes"], "Condition 5: Slower progress detected (0.65x)")

    # Condition 6: Reduced study availability
    red_avail_res = await orchestrator.execute_cycle(
        state_overrides={
            "student_profile": {"previous_weekly_hours": 15.0},
            "weekly_available_hours": 8.0,
        }
    )
    assert_test(ChangeCategory.REDUCED_AVAILABILITY.value in red_avail_res["detected_changes"], "Condition 6: Reduced study availability detected")

    # Condition 7: Increased study availability
    inc_avail_res = await orchestrator.execute_cycle(
        state_overrides={
            "student_profile": {"previous_weekly_hours": 15.0},
            "weekly_available_hours": 24.0,
        }
    )
    assert_test(ChangeCategory.INCREASED_AVAILABILITY.value in inc_avail_res["detected_changes"], "Condition 7: Increased study availability detected")

    # Condition 8: Changed deadline
    chg_dl_res = await orchestrator.execute_cycle(state_overrides={"deadline_delta_days": -10})
    assert_test(ChangeCategory.CHANGED_DEADLINE.value in chg_dl_res["detected_changes"], "Condition 8: Changed deadline detected (-10 days)")

    # Condition 9: Changed learning goal
    chg_goal_res = await orchestrator.execute_cycle(
        state_overrides={"new_goal_title": "Full Stack Senior Engineer Certification"}
    )
    assert_test(ChangeCategory.CHANGED_GOAL.value in chg_goal_res["detected_changes"], "Condition 9: Changed learning goal detected")

    # -------------------------------------------------------------
    # Test 6: PlanChange Records Have Human-Readable Explanations
    # -------------------------------------------------------------
    for pc in missed_res["plan_changes"]:
        assert_test(len(pc["explanation"]) > 10, f"PlanChange {pc['id']} has readable explanation: '{pc['explanation']}'")
        assert_test(pc["change_type"] in ("rescheduled", "removed", "inserted", "rebalanced"), f"PlanChange has valid change_type: '{pc['change_type']}'")

    print("=" * 65)
    print(f"TEST RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 65)

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_agent_orchestrator())

"""
Adaptive Practice Service for LearnMate.

Rules:
1. Question difficulty responds to student performance:
   - Easy -> correct -> Medium
   - Medium -> correct -> Hard
   - Hard -> wrong -> Medium + explanation
   - Medium -> wrong -> Easy + explanation
2. Tracks:
   - question
   - topic
   - difficulty
   - answer
   - correctness
   - time
   - attempt number
3. After an assessment / attempt:
   - Updates topic mastery score
   - Updates knowledge gaps
   - Checks whether replanning is required (e.g. repeated failure on High priority gap)
   - Connects assessment results to the autonomous learning agent
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.schemas.adaptive_practice import (
    AdaptiveQuestion,
    QuestionOption,
    AdaptiveNextQuestionResult,
    AdaptiveAttemptResultResponse,
    AdaptivePracticeSessionResponse,
)
from app.mock.data import (
    _STUDENT,
    _TOPIC_MASTERY,
    _KNOWLEDGE_GAPS,
    _ASSESSMENTS,
    _RECENT_ACTIVITIES,
    execute_replan,
)

# ─── Bank of Questions across Easy, Medium, and Hard ───────────────

QUESTION_BANK: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "Graphs": {
        "Easy": [
            {
                "id": "q-graph-e1",
                "topic": "Graphs",
                "difficulty": "Easy",
                "question_text": "Which graph representation is most space-efficient for a sparse graph with V vertices and E edges where E << V^2?",
                "options": [
                    {"id": "opt-1", "text": "Adjacency Matrix O(V^2)"},
                    {"id": "opt-2", "text": "Adjacency List O(V + E)"},
                    {"id": "opt-3", "text": "Incidence Matrix O(V * E)"},
                    {"id": "opt-4", "text": "Edge Array O(V^2)"},
                ],
                "correct_option_id": "opt-2",
                "explanation": "Adjacency Lists store only existing edges, consuming O(V + E) memory compared to O(V^2) for an Adjacency Matrix.",
                "target_concept": "Graph Representations",
            },
            {
                "id": "q-graph-e2",
                "topic": "Graphs",
                "difficulty": "Easy",
                "question_text": "What is the standard time complexity of Breadth-First Search (BFS) on an adjacency list?",
                "options": [
                    {"id": "opt-1", "text": "O(V + E)"},
                    {"id": "opt-2", "text": "O(V * E)"},
                    {"id": "opt-3", "text": "O(V^2)"},
                    {"id": "opt-4", "text": "O(log V)"},
                ],
                "correct_option_id": "opt-1",
                "explanation": "BFS visits every vertex once and examines each directed edge once, resulting in O(V + E) total time.",
                "target_concept": "BFS Traversal",
            },
        ],
        "Medium": [
            {
                "id": "q-graph-m1",
                "topic": "Graphs",
                "difficulty": "Medium",
                "question_text": "Why does standard Dijkstra's algorithm fail on graphs containing edges with negative weights?",
                "options": [
                    {"id": "opt-1", "text": "It enters an infinite cycle for any tree graph"},
                    {"id": "opt-2", "text": "Once a vertex is marked visited, Dijkstra assumes its shortest path is permanently finalized"},
                    {"id": "opt-3", "text": "A binary heap cannot store negative numbers"},
                    {"id": "opt-4", "text": "Edge relaxation only works for undirected graphs"},
                ],
                "correct_option_id": "opt-2",
                "explanation": "Dijkstra is greedy: once a node is extracted from the min-heap, its distance is considered optimal. A negative edge encountered later could yield a shorter path, violating Dijkstra's greedy invariant.",
                "target_concept": "Dijkstra Invariant & Negative Weights",
            },
            {
                "id": "q-graph-m2",
                "topic": "Graphs",
                "difficulty": "Medium",
                "question_text": "In Kahn's Algorithm for Topological Sort, which condition indicates that the directed graph has a cycle?",
                "options": [
                    {"id": "opt-1", "text": "The queue becomes empty before all V vertices are processed"},
                    {"id": "opt-2", "text": "In-degrees of all nodes reach zero in the first step"},
                    {"id": "opt-3", "text": "The graph has more than V edges"},
                    {"id": "opt-4", "text": "The source vertex has outgoing degree 0"},
                ],
                "correct_option_id": "opt-1",
                "explanation": "If vertices remain in a cycle, their in-degrees never drop to 0, so they are never enqueued. When count < V, a cycle exists.",
                "target_concept": "Topological Sort Cycle Detection",
            },
        ],
        "Hard": [
            {
                "id": "q-graph-h1",
                "topic": "Graphs",
                "difficulty": "Hard",
                "question_text": "In Tarjan's strongly connected components algorithm, what does the condition low[u] == disc[u] signify?",
                "options": [
                    {"id": "opt-1", "text": "Node u is an articulation point that disconnects the graph"},
                    {"id": "opt-2", "text": "Node u is the root of a Strongly Connected Component (SCC)"},
                    {"id": "opt-3", "text": "Node u is part of a negative-weight cycle"},
                    {"id": "opt-4", "text": "The graph is a Directed Acyclic Graph (DAG)"},
                ],
                "correct_option_id": "opt-2",
                "explanation": "When low[u] equals discovery time disc[u], no node in u's subtree has a back-edge to an ancestor of u. Thus u is the root of an SCC, and all nodes on the stack above u form that component.",
                "target_concept": "Tarjan SCC & Low-link Values",
            },
        ],
    },
    "Dynamic Programming": {
        "Easy": [
            {
                "id": "q-dp-e1",
                "topic": "Dynamic Programming",
                "difficulty": "Easy",
                "question_text": "What are the two foundational properties required for a problem to be solved using Dynamic Programming?",
                "options": [
                    {"id": "opt-1", "text": "Greedy Choice & Divide-and-Conquer"},
                    {"id": "opt-2", "text": "Optimal Substructure & Overlapping Subproblems"},
                    {"id": "opt-3", "text": "Depth-First Search & Binary Partitioning"},
                    {"id": "opt-4", "text": "Breadth Search & Heuristic Pruning"},
                ],
                "correct_option_id": "opt-2",
                "explanation": "Dynamic Programming requires Optimal Substructure (solution built from optimal sub-solutions) and Overlapping Subproblems (identical subproblems evaluated repeatedly).",
                "target_concept": "DP Prerequisites",
            },
        ],
        "Medium": [
            {
                "id": "q-dp-m1",
                "topic": "Dynamic Programming",
                "difficulty": "Medium",
                "question_text": "In the 0/1 Knapsack 1D array space optimization dp[w], why MUST the capacity loop iterate backwards from W down to wt[i]?",
                "options": [
                    {"id": "opt-1", "text": "To prevent item i from being included multiple times in the same knapsack"},
                    {"id": "opt-2", "text": "To achieve O(log W) binary search complexity"},
                    {"id": "opt-3", "text": "To satisfy recursion call stack limits in Python"},
                    {"id": "opt-4", "text": "To handle negative weights correctly"},
                ],
                "correct_option_id": "opt-1",
                "explanation": "Iterating forwards would overwrite dp[w - wt[i]] with the current item's choice, causing item i to be reused (Unbounded Knapsack behavior). Backward iteration preserves values from the previous item.",
                "target_concept": "0/1 Knapsack Space Optimization",
            },
        ],
        "Hard": [
            {
                "id": "q-dp-h1",
                "topic": "Dynamic Programming",
                "difficulty": "Hard",
                "question_text": "In Matrix Chain Multiplication DP for dimensions p[0..n], what is the recurrence relation for m[i, j]?",
                "options": [
                    {"id": "opt-1", "text": "min_{i <= k < j} { m[i, k] + m[k+1, j] + p[i-1]*p[k]*p[j] }"},
                    {"id": "opt-2", "text": "max_{i <= k < j} { m[i, k] * m[k+1, j] }"},
                    {"id": "opt-3", "text": "m[i, j-1] + p[i]*p[j]"},
                    {"id": "opt-4", "text": "min(m[i+1, j], m[i, j-1]) + p[i]"},
                ],
                "correct_option_id": "opt-1",
                "explanation": "Multiplying subchains A[i..k] and A[k+1..j] adds scalar multiplications equal to rows(A[i]) * cols(A[k]) * cols(A[j]), which is p[i-1] * p[k] * p[j].",
                "target_concept": "Interval DP / Matrix Chain Recurrence",
            },
        ],
    },
}

# In-memory session tracking
_ACTIVE_ATTEMPTS: List[Dict[str, Any]] = []


class AdaptivePracticeService:
    """Manages adaptive question selection and closed-loop learner telemetry."""

    def get_initial_question(self, topic: str = "Graphs", starting_difficulty: Optional[str] = None) -> AdaptiveQuestion:
        """
        Select initial question based on current topic mastery or requested difficulty.
        """
        topic_key = topic if topic in QUESTION_BANK else "Graphs"

        if not starting_difficulty:
            # Check student mastery
            mastery = 30.0
            for tm in _TOPIC_MASTERY:
                if tm["topic"].lower() == topic.lower():
                    mastery = tm.get("mastery", 30.0)
                    break

            if mastery >= 75.0:
                difficulty = "Hard"
            elif mastery >= 45.0:
                difficulty = "Medium"
            else:
                difficulty = "Easy"
        else:
            difficulty = starting_difficulty

        bank = QUESTION_BANK[topic_key].get(difficulty, QUESTION_BANK[topic_key]["Easy"])
        q_data = bank[0]

        return AdaptiveQuestion(
            id=q_data["id"],
            topic=topic_key,
            difficulty=difficulty,
            question_text=q_data["question_text"],
            options=[QuestionOption(**opt) for opt in q_data["options"]],
            correct_option_id=q_data["correct_option_id"],
            explanation=q_data["explanation"],
            target_concept=q_data["target_concept"],
            time_limit_seconds=90,
        )

    def process_attempt(
        self,
        question_id: str,
        topic: str,
        difficulty: str,
        selected_option_id: str,
        time_spent_seconds: int,
        attempt_number: int = 1,
        student_id: str = "stu-001",
    ) -> AdaptiveAttemptResultResponse:
        """
        Process answer, compute difficulty progression, update mastery and gaps,
        and trigger autonomous replanning if critical threshold is breached.
        """
        topic_key = topic if topic in QUESTION_BANK else "Graphs"
        bank = QUESTION_BANK[topic_key].get(difficulty, QUESTION_BANK[topic_key]["Easy"])

        # Locate question in bank
        curr_q = next((q for q in bank if q["id"] == question_id), bank[0])
        is_correct = selected_option_id == curr_q["correct_option_id"]

        # ─── Adaptive Difficulty Transition Rules ───────────────────
        # Easy -> correct -> Medium
        # Medium -> correct -> Hard
        # Hard -> wrong -> Medium + explanation
        # Medium -> wrong -> Easy + explanation
        explanation = None

        if is_correct:
            if difficulty == "Easy":
                next_difficulty = "Medium"
                adaptation_reason = "Easy question answered correctly! Upgraded to Medium."
            elif difficulty == "Medium":
                next_difficulty = "Hard"
                adaptation_reason = "Medium question answered correctly! Upgraded to Hard."
            else:  # Hard
                next_difficulty = "Hard"
                adaptation_reason = "Hard question answered correctly! Retaining high mastery challenge."
        else:
            explanation = curr_q["explanation"]
            if difficulty == "Hard":
                next_difficulty = "Medium"
                adaptation_reason = "Hard question missed. Stepped down to Medium with conceptual reinforcement."
            elif difficulty == "Medium":
                next_difficulty = "Easy"
                adaptation_reason = "Medium question missed. Stepped down to Easy to reinforce core prerequisites."
            else:  # Easy
                next_difficulty = "Easy"
                adaptation_reason = "Easy question missed. Retaining Easy with targeted explanation."

        # Fetch candidate next question
        next_bank = QUESTION_BANK[topic_key].get(next_difficulty, QUESTION_BANK[topic_key]["Easy"])
        # Pick different question if available
        next_q_candidates = [q for q in next_bank if q["id"] != question_id]
        chosen_next = next_q_candidates[0] if next_q_candidates else next_bank[0]

        next_question = AdaptiveQuestion(
            id=chosen_next["id"],
            topic=topic_key,
            difficulty=next_difficulty,
            question_text=chosen_next["question_text"],
            options=[QuestionOption(**opt) for opt in chosen_next["options"]],
            correct_option_id=chosen_next["correct_option_id"],
            explanation=chosen_next["explanation"],
            target_concept=chosen_next["target_concept"],
            time_limit_seconds=90,
        )

        # ─── Update Topic Mastery & Knowledge Gaps ──────────────────
        delta = 6.5 if is_correct else -4.0
        updated_mastery = 30.0

        for tm in _TOPIC_MASTERY:
            if tm["topic"].lower() == topic_key.lower():
                tm["mastery"] = min(98.0, max(15.0, round(tm["mastery"] + delta, 1)))
                updated_mastery = tm["mastery"]
                break

        # Re-evaluate gap severity
        gap_severity = "High"
        for gap in _KNOWLEDGE_GAPS:
            if gap["topic"].lower() == topic_key.lower():
                gap["mastery"] = updated_mastery
                if updated_mastery >= 75.0:
                    gap["severity"] = "Low"
                elif updated_mastery >= 50.0:
                    gap["severity"] = "Medium"
                else:
                    gap["severity"] = "High"
                gap_severity = gap["severity"]
                break

        # ─── Record In-Memory Telemetry Attempt ─────────────────────
        attempt_id = f"att-{uuid.uuid4().hex[:8]}"
        attempt_record = {
            "attempt_id": attempt_id,
            "question_id": question_id,
            "topic": topic_key,
            "difficulty": difficulty,
            "selected_option_id": selected_option_id,
            "correct_option_id": curr_q["correct_option_id"],
            "is_correct": is_correct,
            "time_spent_seconds": time_spent_seconds,
            "attempt_number": attempt_number,
            "timestamp": datetime.now().isoformat(),
        }
        _ACTIVE_ATTEMPTS.insert(0, attempt_record)

        # Record in Assessment list
        _ASSESSMENTS.insert(0, {
            "id": f"asmt-adp-{int(datetime.now().timestamp())}",
            "student_id": student_id,
            "title": f"Adaptive {topic_key} Check ({difficulty})",
            "topic": topic_key,
            "score": 100.0 if is_correct else 0.0,
            "max_score": 100.0,
            "percentage": 100.0 if is_correct else 0.0,
            "status": "passed" if is_correct else "needs_review",
            "completed_at": datetime.now().isoformat(),
        })

        # ─── Check Whether Replanning Is Required ───────────────────
        replan_required = False
        replan_reason = None
        agent_run_id = None

        if not is_correct and difficulty in ("Medium", "Hard") and gap_severity == "High":
            replan_required = True
            replan_reason = (
                f"Adaptive practice failure on {topic_key} ({difficulty}). "
                f"Autonomous agent scheduled 45m remedial practice and adjusted study calendar."
            )
            replan_result = execute_replan(reason=replan_reason)
            agent_run_id = f"agent-run-v{replan_result['plan_version']}"

            # Log to recent activities
            _RECENT_ACTIVITIES.insert(0, {
                "id": f"rec-{int(datetime.now().timestamp())}",
                "type": "schedule",
                "title": f"Adaptive Trigger: {topic_key} Replan",
                "description": replan_reason,
                "status": "rescheduled",
                "timestamp": "Just now",
                "details": f"Schedule rebalanced to Plan v{replan_result['plan_version']}",
            })

        return AdaptiveAttemptResultResponse(
            attempt_id=attempt_id,
            question_id=question_id,
            topic=topic_key,
            difficulty=difficulty,
            selected_option_id=selected_option_id,
            correct_option_id=curr_q["correct_option_id"],
            is_correct=is_correct,
            time_spent_seconds=time_spent_seconds,
            attempt_number=attempt_number,
            adaptation=AdaptiveNextQuestionResult(
                previous_difficulty=difficulty,
                was_correct=is_correct,
                next_difficulty=next_difficulty,
                adaptation_reason=adaptation_reason,
                explanation=explanation,
            ),
            next_question=next_question,
            topic_mastery_updated=updated_mastery,
            knowledge_gap_severity=gap_severity,
            replan_required=replan_required,
            replan_reason=replan_reason,
            agent_run_id=agent_run_id,
            message=(
                "Correct! Upgrading difficulty." if is_correct
                else f"Incorrect. {curr_q['explanation']}"
            ),
        )

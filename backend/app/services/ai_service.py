"""
OpenAI AI Service for LearnMate.

IMPORTANT DESIGN RULES:
1. Use the AI ONLY for tasks where reasoning or natural language is useful.
2. The AI does NOT directly modify the database or mutate tables.
3. Uses structured outputs with Pydantic schema validation (via client.beta.chat.completions.parse or fallback).
4. The deterministic scheduler, time constraints, calendar conflict detection,
   and plan verification remain pure deterministic Python code.
5. Graceful handling for:
   - API failure
   - timeout
   - invalid response
   - missing context
   - rate limits
   - missing or invalid API keys
"""

import logging
from typing import Optional, Dict, Any, List
from pydantic import ValidationError

from app.config import settings
from app.schemas.ai import (
    KnowledgeGapExplanationResponse,
    GapConceptBreakdown,
    ResourceRecommendationExplanationResponse,
    PlanChangeExplanationResponse,
    PlanChangeActionItem,
    PersonalizedAdviceResponse,
    AlternativeStudyStrategiesResponse,
    StudyStrategyOption,
    AnswerQuestionResponse,
    ProblemHintsResponse,
    ProblemHintStep,
)

logger = logging.getLogger(__name__)


class AIService:
    """Backend AI reasoning service using OpenAI API with structured outputs."""

    def __init__(self):
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model or "gpt-4o-mini"
        self.timeout = settings.openai_timeout_seconds or 12.0
        self._client = None

    def _get_client(self):
        """Lazy initialization of OpenAI client."""
        if not self.api_key:
            return None
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key, timeout=self.timeout)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                return None
        return self._client

    # ─────────────────────────────────────────────────────────────
    # Task 1: Explain Knowledge Gaps
    # ─────────────────────────────────────────────────────────────
    def explain_knowledge_gap(
        self,
        topic: str,
        severity: str = "High",
        mastery: float = 25.0,
        context: Optional[str] = None,
    ) -> KnowledgeGapExplanationResponse:
        """
        Explain why a knowledge gap exists, root causes, and remedial steps.
        """
        client = self._get_client()
        if client:
            try:
                prompt = (
                    f"Student has a {severity} severity knowledge gap in '{topic}' with mastery score {mastery}%."
                    f"\nContext: {context or 'Diagnostic quizzes show repeated errors in formulating subproblems.'}"
                    "\nProvide a rigorous root-cause pedagogical explanation and a structured remedial plan."
                )
                completion = client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are the LearnMate Pedagogical AI Agent. Provide empathetic, structured "
                                "learning diagnostics for computer science and mathematics students."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format=KnowledgeGapExplanationResponse,
                    timeout=self.timeout,
                )
                parsed = completion.choices[0].message.parsed
                if parsed:
                    parsed.source = "openai"
                    return parsed
            except Exception as e:
                logger.warning(f"OpenAI error in explain_knowledge_gap ({e}), activating deterministic fallback.")

        # Graceful Deterministic Fallback
        return KnowledgeGapExplanationResponse(
            topic=topic,
            severity=severity,
            root_cause_analysis=(
                f"Diagnostic telemetry shows mastery at {mastery}%. The student frequently struggles to identify "
                f"optimal substructure and state representation in {topic}, leading to recurring compilation or logic errors."
            ),
            concept_breakdowns=[
                GapConceptBreakdown(
                    concept=f"{topic} State Definition",
                    misconception="Treating recursive steps without caching overlapping subproblems",
                    clarification="Express each subproblem state explicitly with indices and base conditions first",
                ),
                GapConceptBreakdown(
                    concept=f"{topic} Transition Formulation",
                    misconception="Guessing transition relations without writing the recurrence on paper",
                    clarification="Draft the recurrence relation $dp[i] = \\min/\\max$ before translating to code",
                ),
            ],
            remedial_action_plan=[
                f"1. Review fundamental visual breakdown of 0/1 {topic} paradigms (30 mins)",
                f"2. Solve 3 guided beginner practice problems with step-by-step state diagrams (45 mins)",
                f"3. Retake the {topic} diagnostic check to verify retention (15 mins)",
            ],
            estimated_catchup_hours=round(max(2.0, (80.0 - mastery) * 0.15), 1),
            source="deterministic_fallback",
        )

    # ─────────────────────────────────────────────────────────────
    # Task 2: Explain Why Resource Was Recommended
    # ─────────────────────────────────────────────────────────────
    def explain_resource_recommendation(
        self,
        resource_id: str,
        resource_title: str,
        topic: str,
        resource_type: str,
        student_mastery: float = 25.0,
    ) -> ResourceRecommendationExplanationResponse:
        """
        Explain the pedagogical match score and reason for recommending a learning resource.
        """
        client = self._get_client()
        if client:
            try:
                prompt = (
                    f"Explain why '{resource_title}' ({resource_type}) on topic '{topic}' was selected for a "
                    f"student with {student_mastery}% current mastery."
                )
                completion = client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are LearnMate's Resource Intelligence Engine. Explain resource suitability clearly.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format=ResourceRecommendationExplanationResponse,
                    timeout=self.timeout,
                )
                parsed = completion.choices[0].message.parsed
                if parsed:
                    parsed.source = "openai"
                    return parsed
            except Exception as e:
                logger.warning(f"OpenAI error in explain_resource_recommendation ({e}), activating fallback.")

        # Graceful Deterministic Fallback
        return ResourceRecommendationExplanationResponse(
            resource_id=resource_id,
            resource_title=resource_title,
            topic=topic,
            resource_type=resource_type,
            primary_reason=(
                f"Selected because its {resource_type.lower()} format has proven high conceptual transfer "
                f"for learners at {student_mastery}% mastery in {topic}."
            ),
            pedagogical_alignment="Combines visual intuition with immediate code implementation, bridging the gap from theory to execution.",
            targeted_gap_resolved=f"Directly addresses subproblem decomposition friction in {topic}.",
            expected_outcome=f"Expected to boost {topic} mastery from {student_mastery}% toward the 65% milestone.",
            study_tips=[
                "Watch or read at 1.0x speed without skipping",
                "Re-implement each code snippet manually without copy-pasting",
                "Complete the accompanying checkpoint quiz immediately after",
            ],
            source="deterministic_fallback",
        )

    # ─────────────────────────────────────────────────────────────
    # Task 3: Explain Why The Plan Changed
    # ─────────────────────────────────────────────────────────────
    def explain_plan_change(
        self,
        plan_version: int = 11,
        trigger_event: str = "Missed Study Session: Binary Trees Video",
        reason: Optional[str] = None,
        explanations: Optional[List[str]] = None,
    ) -> PlanChangeExplanationResponse:
        """
        Explain why the autonomous agent replanned activities and moved calendar blocks.
        """
        client = self._get_client()
        if client:
            try:
                prompt = (
                    f"The autonomous planner generated Plan v{plan_version} following trigger: '{trigger_event}'. "
                    f"Reason: {reason or 'Dynamic priority rebalance'}. "
                    f"Provide an articulate, encouraging breakdown of why activities shifted."
                )
                completion = client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are the LearnMate Autonomous Replanning Explainer. Highlight safety, deadlines, and deliberate trade-offs.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format=PlanChangeExplanationResponse,
                    timeout=self.timeout,
                )
                parsed = completion.choices[0].message.parsed
                if parsed:
                    parsed.source = "openai"
                    return parsed
            except Exception as e:
                logger.warning(f"OpenAI error in explain_plan_change ({e}), activating fallback.")

        # Graceful Deterministic Fallback
        return PlanChangeExplanationResponse(
            plan_version=plan_version,
            trigger_event=trigger_event,
            high_level_narrative=(
                f"When '{trigger_event}' occurred, available study capacity was reduced. "
                "Rather than overburdening your upcoming weekdays, the autonomous planner protected your "
                "highest-priority gap (Dynamic Programming) by moving practice to a protected weekend slot "
                "and trimming redundant low-priority sorting drills."
            ),
            tradeoffs_made=[
                "Protected: High-priority Dynamic Programming received uninterrupted 90-minute weekend focus",
                "Deferred: Low-priority Sorting revision was pruned because your mastery is already at 80%",
                "Preserved: Target interview deadline of 30 Nov 2025 remains 100% reachable",
            ],
            action_items=[
                PlanChangeActionItem(
                    activity_title="Dynamic Programming Deep Dive",
                    change_type="moved",
                    reason="Shifted to Saturday morning to guarantee dedicated 90-minute uninterrupted focus",
                ),
                PlanChangeActionItem(
                    activity_title="QuickSort vs MergeSort Review",
                    change_type="shortened",
                    reason="Reduced by 20 minutes because recent quiz score was 85%+",
                ),
            ],
            deadline_impact="Zero delay — all milestone learning hours fit within weekly verified availability.",
            is_goal_still_achievable=True,
            source="deterministic_fallback",
        )

    # ─────────────────────────────────────────────────────────────
    # Task 4: Personalized Learning Advice
    # ─────────────────────────────────────────────────────────────
    def get_personalized_advice(
        self,
        student_name: str = "Prince",
        current_goal: str = "Master Data Structures & Algorithms",
        progress: float = 68.0,
        streak: int = 12,
        weakest_topic: str = "Dynamic Programming",
        strongest_topic: str = "Arrays",
    ) -> PersonalizedAdviceResponse:
        """
        Synthesize customized learning trajectory guidance based on active student state.
        """
        client = self._get_client()
        if client:
            try:
                prompt = (
                    f"Student: {student_name}, Goal: {current_goal}, Progress: {progress}%, "
                    f"Streak: {streak} days, Weakest: {weakest_topic}, Strongest: {strongest_topic}. "
                    "Deliver empathetic, tactical learning advice."
                )
                completion = client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are LearnMate's Senior AI Learning Coach. Offer specific, evidence-based advice.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format=PersonalizedAdviceResponse,
                    timeout=self.timeout,
                )
                parsed = completion.choices[0].message.parsed
                if parsed:
                    parsed.source = "openai"
                    return parsed
            except Exception as e:
                logger.warning(f"OpenAI error in get_personalized_advice ({e}), activating fallback.")

        # Graceful Deterministic Fallback
        return PersonalizedAdviceResponse(
            student_name=student_name,
            current_velocity_assessment=(
                f"You are maintaining strong momentum with a {streak}-day study streak and {progress}% overall progress. "
                f"Your foundation in {strongest_topic} is rock-solid."
            ),
            key_strengths=[
                f"High retention in {strongest_topic} (85%+ mastery)",
                f"Excellent consistency with a {streak}-day daily active streak",
                "Reliable follow-through on morning study sessions",
            ],
            urgent_priorities=[
                f"Allocate your freshest mental energy to {weakest_topic} subproblems",
                "Practice writing recurrences on paper before typing any code",
            ],
            daily_habit_recommendation="Do 15 minutes of state-diagram sketching every morning before looking at solutions.",
            motivational_verdict=f"You are within 32% of mastering {current_goal}. Consistent daily practice will take you across the finish line!",
            source="deterministic_fallback",
        )

    # ─────────────────────────────────────────────────────────────
    # Task 5: Suggest Alternative Study Strategies
    # ─────────────────────────────────────────────────────────────
    def suggest_study_strategies(
        self,
        challenge: str = "Time squeeze and cognitive fatigue with advanced Dynamic Programming",
        available_hours: float = 2.0,
    ) -> AlternativeStudyStrategiesResponse:
        """
        Suggest 2-3 cognitive learning techniques tailored to student fatigue or constraints.
        """
        client = self._get_client()
        if client:
            try:
                prompt = (
                    f"Student challenge: '{challenge}'. Available study time: {available_hours} hours. "
                    "Recommend 3 distinct evidence-based study strategies."
                )
                completion = client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are LearnMate's Cognitive Strategy Advisor.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format=AlternativeStudyStrategiesResponse,
                    timeout=self.timeout,
                )
                parsed = completion.choices[0].message.parsed
                if parsed:
                    parsed.source = "openai"
                    return parsed
            except Exception as e:
                logger.warning(f"OpenAI error in suggest_study_strategies ({e}), activating fallback.")

        # Graceful Deterministic Fallback
        return AlternativeStudyStrategiesResponse(
            current_challenge=challenge,
            strategies=[
                StudyStrategyOption(
                    name="The 25/5 Spaced Pomodoro Drill",
                    description="25 minutes intense focus on 1 specific subproblem, followed by 5 minutes cognitive downtime.",
                    why_it_fits_current_state="Prevents cognitive fatigue when tackling dense algorithmic problems.",
                    pros=["Limits mental burnout", "Keeps focus razor sharp"],
                    cons=["Requires strict discipline with timers"],
                ),
                StudyStrategyOption(
                    name="Feynman Peer Explanation Technique",
                    description="Explain the recurrence relation out loud in simple terms as if teaching a 10-year-old.",
                    why_it_fits_current_state="Immediately exposes fuzzy logic and ungrounded assumptions.",
                    pros=["Deep conceptual grounding", "Reveals hidden gaps quickly"],
                    cons=["Takes slightly longer per problem"],
                ),
                StudyStrategyOption(
                    name="Worked-Example Inversion (Cognitive Load Theory)",
                    description="Study fully annotated optimal code for 10 minutes, close it, then reconstruct it from first principles.",
                    why_it_fits_current_state="Drastically lowers working memory load when learning new DP patterns.",
                    pros=["Fastest way to absorb syntax patterns", "High confidence booster"],
                    cons=["Must avoid passive reading"],
                ),
            ],
            recommended_selection="The 25/5 Spaced Pomodoro Drill",
            implementation_guide="Apply this during your scheduled 09:00 study window today for two complete cycles.",
            source="deterministic_fallback",
        )

    # ─────────────────────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────────
    # Task 6: Answer Student Questions (Adapted to Student Level & Context)
    # ─────────────────────────────────────────────────────────────
    def answer_student_question(
        self,
        question: str,
        topic: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        quick_action: Optional[str] = None,
        student_answer: Optional[str] = None,
    ) -> AnswerQuestionResponse:
        """
        Answer student doubts and conceptual queries adapted to student's level and learning goal.
        Includes full context:
        - student's goal
        - current topic
        - topic mastery
        - recent assessment results
        - knowledge gaps
        - recent learning activities
        Supports quick actions:
        - Explain Concept
        - Give Example
        - Give Practice Questions
        - Give Hint
        - Check My Answer
        - Suggest Resources
        - Adjust My Plan
        - Why Did My Plan Change?
        """
        q_lower = question.lower()
        if any(w in q_lower for w in ["sort", "bubble", "merge", "quick", "insertion", "selection"]):
            topic_str = "Sorting"
        elif any(w in q_lower for w in ["tree", "bst", "binary tree", "traversal", "inorder", "preorder"]):
            topic_str = "Trees"
        elif any(w in q_lower for w in ["dijkstra", "shortest path", "graph", "bfs", "dfs", "adjacency"]):
            topic_str = "Graphs"
        elif any(w in q_lower for w in ["dp", "knapsack", "subproblem", "dynamic", "memo", "tabulation", "coin change"]):
            topic_str = "Dynamic Programming"
        elif any(w in q_lower for w in ["array", "string", "two pointer", "sliding window"]):
            topic_str = "Arrays"
        elif any(w in q_lower for w in ["hash", "map", "set"]):
            topic_str = "Hashing"
        elif any(w in q_lower for w in ["plan", "schedule", "deadline", "date"]):
            topic_str = "Study Plan"
        else:
            topic_str = topic or "Algorithms"

        # Assemble student telemetry context
        ctx = context or {}
        student_goal = ctx.get("student_goal", "Master Data Structures & Algorithms")
        mastery = ctx.get("topic_mastery", 80.0 if topic_str in ["Sorting", "Trees"] else (30.0 if topic_str == "Graphs" else 25.0))
        recent_assessments = ctx.get("recent_assessment_results", "Scored 80% in Sorting quiz; 52% in Graphs traversal quiz; 35% in DP state quiz")
        knowledge_gaps = ctx.get("knowledge_gaps", ["Dynamic Programming (High)", "Graphs (High)"])
        recent_activities = ctx.get("recent_activities", ["Completed: Dijkstra Shortest Path Video", "Missed: Binary Trees Video"])

        client = self._get_client()
        if client:
            try:
                system_prompt = (
                    "You are the LearnMate Autonomous AI Tutor. Adapt your explanation to the student's exact learning goal, "
                    "current level, and knowledge gaps. Avoid overwhelming beginners; be concise, pedagogically clear, and motivating.\n"
                    f"Student Learning Goal: {student_goal}\n"
                    f"Current Topic: {topic_str} (Mastery: {mastery}%)\n"
                    f"Recent Assessment Results: {recent_assessments}\n"
                    f"Identified Knowledge Gaps: {knowledge_gaps}\n"
                    f"Recent Learning Activities: {recent_activities}\n"
                )

                user_prompt = f"Student Question/Request: '{question}'"
                if quick_action:
                    user_prompt += f"\nRequested Quick Action Mode: {quick_action}"
                if student_answer:
                    user_prompt += f"\nStudent Submitted Answer to Check: '{student_answer}'"

                completion = client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format=AnswerQuestionResponse,
                    timeout=self.timeout,
                )
                parsed = completion.choices[0].message.parsed
                if parsed:
                    parsed.source = "openai"
                    parsed.student_context = {
                        "goal": student_goal,
                        "topic": topic_str,
                        "mastery": mastery,
                        "gaps": knowledge_gaps,
                    }
                    parsed.quick_action_type = quick_action
                    return parsed
            except Exception as e:
                logger.warning(f"OpenAI error in answer_student_question ({e}), activating deterministic fallback.")

        # ─── Rich Topic-Specific Fallbacks ─────────────────────────
        # 1. Sorting (Bubble Sort, Merge Sort, etc.)
        if topic_str == "Sorting":
            code_bubble = (
                "def bubble_sort(arr):\n"
                "    n = len(arr)\n"
                "    for i in range(n):\n"
                "        swapped = False\n"
                "        for j in range(0, n - i - 1):\n"
                "            if arr[j] > arr[j + 1]:\n"
                "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
                "                swapped = True\n"
                "        if not swapped: break  # Optimized O(N) best case\n"
                "    return arr\n\n"
                "print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))\n"
                "# Output: [11, 12, 22, 25, 34, 64, 90]"
            )
            return AnswerQuestionResponse(
                question=question,
                direct_answer=(
                    "Bubble Sort repeatedly steps through the list, compares adjacent elements, and swaps them if out of order. "
                    "In each pass, the largest remaining element 'bubbles up' to its correct position at the end.\n\n"
                    "Complexity Analysis:\n"
                    "• Best Case: O(N) (using the swapped flag when already sorted)\n"
                    "• Average/Worst Case: O(N²)\n"
                    "• Space: O(1) in-place auxiliary memory"
                ),
                key_points=[
                    "Adjacent element comparison: if arr[j] > arr[j+1], swap.",
                    "Pass i locks the i-th largest element at the right end.",
                    "Stable sorting algorithm with O(1) extra space.",
                ],
                code_example_or_analogy=code_bubble,
                related_topics=["Sorting", "Insertion Sort", "Merge Sort", "Quick Sort"],
                follow_up_questions=[
                    "Why is Merge Sort preferred over Bubble Sort for large datasets?",
                    "How does the swapped boolean flag allow O(N) best-case performance?",
                ],
                student_context={
                    "goal": student_goal,
                    "topic": "Sorting",
                    "mastery": 80.0,
                    "gaps": knowledge_gaps,
                },
                quick_action_type=quick_action or "explain_concept",
                source="deterministic_fallback",
            )

        # 2. Trees / Binary Search Trees
        if topic_str == "Trees":
            code_bst = (
                "class TreeNode:\n"
                "    def __init__(self, val=0, left=None, right=None):\n"
                "        self.val = val\n"
                "        self.left = left\n"
                "        self.right = right\n\n"
                "def inorder(root):\n"
                "    # Inorder of a BST always prints values in sorted order!\n"
                "    return inorder(root.left) + [root.val] + inorder(root.right) if root else []"
            )
            return AnswerQuestionResponse(
                question=question,
                direct_answer=(
                    "In a Binary Search Tree (BST), every node follows the ordering invariant: "
                    "all values in the left subtree are strictly less than root, and all values in the right subtree are strictly greater.\n\n"
                    "Key Operations:\n"
                    "• Search / Insert: Average O(log N), Worst O(N) if skewed.\n"
                    "• Inorder Traversal yields a sorted sequence."
                ),
                key_points=[
                    "BST Property: left < root < right.",
                    "Inorder traversal always yields sorted output.",
                    "Self-balancing BSTs (AVL, Red-Black) prevent O(N) degeneration.",
                ],
                code_example_or_analogy=code_bst,
                related_topics=["Trees", "Binary Search Tree", "AVL Trees", "Tree Traversals"],
                follow_up_questions=[
                    "How do you check if a binary tree is a valid BST?",
                    "What is the difference between BFS level order and DFS inorder?",
                ],
                student_context={
                    "goal": student_goal,
                    "topic": "Trees",
                    "mastery": 80.0,
                    "gaps": knowledge_gaps,
                },
                quick_action_type=quick_action or "explain_concept",
                source="deterministic_fallback",
            )

        # 3. Graphs / Dijkstra
        if topic_str == "Graphs":
            code_dijkstra = (
                "import heapq\n\n"
                "def dijkstra(graph, start):\n"
                "    dist = {node: float('inf') for node in graph}\n"
                "    dist[start] = 0\n"
                "    pq = [(0, start)]  # (distance, node)\n"
                "    while pq:\n"
                "        curr_dist, u = heapq.heappop(pq)\n"
                "        if curr_dist > dist[u]: continue\n"
                "        for v, weight in graph[u]:\n"
                "            if dist[u] + weight < dist[v]:\n"
                "                dist[v] = dist[u] + weight\n"
                "                heapq.heappush(pq, (dist[v], v))\n"
                "    return dist"
            )
            return AnswerQuestionResponse(
                question=question,
                direct_answer=(
                    "Dijkstra's Algorithm calculates the shortest path from a single source node to all other vertices "
                    "in a weighted graph with non-negative edge weights using a greedy min-heap approach.\n\n"
                    "Complexity:\n"
                    "• Time: O((V + E) log V) with a binary min-heap.\n"
                    "• Space: O(V) for distances and heap elements."
                ),
                key_points=[
                    "Greedy approach: always expands the closest unvisited vertex.",
                    "Only valid for non-negative edge weights (use Bellman-Ford for negative weights).",
                    f"Aligned with your goal: '{student_goal}' — Graphs is currently your #2 gap.",
                ],
                code_example_or_analogy=code_dijkstra,
                related_topics=["Graphs", "Shortest Path", "Priority Queue", "Bellman-Ford", "Breadth-First Search"],
                follow_up_questions=[
                    "What happens if an edge has a negative weight in Dijkstra?",
                    "How does Dijkstra differ from standard Breadth-First Search (BFS)?",
                ],
                student_context={
                    "goal": student_goal,
                    "topic": "Graphs",
                    "mastery": 30.0,
                    "gaps": knowledge_gaps,
                },
                quick_action_type=quick_action or "explain_concept",
                source="deterministic_fallback",
            )

        # 4. Dynamic Programming (Default)
        code_dp = (
            "# Top-Down Memoization Template\n"
            "memo = {}\n"
            "def solve(i, remaining):\n"
            "    if remaining == 0: return 0\n"
            "    if i < 0 or remaining < 0: return float('inf')\n"
            "    state = (i, remaining)\n"
            "    if state in memo: return memo[state]\n"
            "    take = 1 + solve(i, remaining - coins[i])\n"
            "    skip = solve(i - 1, remaining)\n"
            "    memo[state] = min(take, skip)\n"
            "    return memo[state]"
        )
        return AnswerQuestionResponse(
            question=question,
            direct_answer=(
                f"For {topic_str} (current mastery: {mastery}%):\n"
                "Dynamic Programming solves optimization problems by breaking them down into overlapping subproblems. "
                "The 3-step formula:\n"
                "1. State Representation: Define what your parameters represent (e.g. dp[i][w]).\n"
                "2. Recurrence Relation: Express the current answer in terms of smaller subproblem answers.\n"
                "3. Base Cases & Direction: Choose Top-Down Memoization or Bottom-Up Tabulation."
            ),
            key_points=[
                "Overlapping subproblems allow memoization to avoid redundant recalculation.",
                "Optimal substructure guarantees that the global optimum is built from local sub-optima.",
                f"Directly targets your current knowledge gap: {knowledge_gaps[0] if knowledge_gaps else 'Dynamic Programming'}.",
            ],
            code_example_or_analogy=code_dp,
            related_topics=["Dynamic Programming", "Recursion", "Memoization", "Tabulation"],
            follow_up_questions=[
                "Can you identify what changes between recursive steps in your state?",
                "Would you like to walk through 0/1 Knapsack or Coin Change next?",
            ],
            student_context={
                "goal": student_goal,
                "topic": topic_str,
                "mastery": mastery,
                "gaps": knowledge_gaps,
            },
            quick_action_type=quick_action or "explain_concept",
            source="deterministic_fallback",
        )

    # ─────────────────────────────────────────────────────────────
    # Task 7: Provide Practice Problem Hints
    # ─────────────────────────────────────────────────────────────
    def get_problem_hints(
        self,
        problem_title: str,
        topic: str = "Dynamic Programming",
        difficulty: str = "Medium",
    ) -> ProblemHintsResponse:
        """
        Deliver progressive 3-level hints for coding challenges without giving away full code.
        """
        client = self._get_client()
        if client:
            try:
                prompt = (
                    f"Generate 3 progressive hints for: '{problem_title}' (Topic: {topic}, Difficulty: {difficulty}). "
                    "Hint 1 = subtle direction, Hint 2 = conceptual insight, Hint 3 = algorithmic structure."
                )
                completion = client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are LearnMate's Practice Coach. Give progressive hints that encourage student discovery "
                                "without spoiling the full solution."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format=ProblemHintsResponse,
                    timeout=self.timeout,
                )
                parsed = completion.choices[0].message.parsed
                if parsed:
                    parsed.source = "openai"
                    return parsed
            except Exception as e:
                logger.warning(f"OpenAI error in get_problem_hints ({e}), activating fallback.")

        # Graceful Deterministic Fallback
        return ProblemHintsResponse(
            problem_title=problem_title,
            topic=topic,
            difficulty=difficulty,
            understanding_check="What are the parameters that uniquely identify your current state?",
            hints=[
                ProblemHintStep(
                    level=1,
                    hint_text="Start by identifying what choices you have at step $i$: include the current element or exclude it.",
                ),
                ProblemHintStep(
                    level=2,
                    hint_text="If you include element $i$, the remaining capacity decreases by weight[i] and profit increases by value[i].",
                ),
                ProblemHintStep(
                    level=3,
                    hint_text="Define $dp[w]$ as maximum value for capacity $w$. Iterate backwards from max capacity to avoid re-using the same item.",
                ),
            ],
            pitfall_to_avoid="Iterating forward in 1D DP arrays can cause 0/1 knapsack items to be counted multiple times.",
            complexity_target="Time: O(N * W), Space: O(W)",
            source="deterministic_fallback",
        )

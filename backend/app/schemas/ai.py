"""
Pydantic Schemas for Backend AI Service Structured Outputs.

Enforces strict JSON schemas for:
1. Explain knowledge gaps
2. Explain why a resource was recommended
3. Explain why the plan changed
4. Give personalized learning advice
5. Suggest alternative study strategies
6. Answer student questions
7. Provide hints for practice problems
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ─── Task 1: Explain Knowledge Gaps ────────────────────────────────
class GapConceptBreakdown(BaseModel):
    concept: str = Field(description="Sub-concept that the student struggles with")
    misconception: str = Field(description="Common misconception or pattern error")
    clarification: str = Field(description="Targeted mental model or rule to correct it")


class KnowledgeGapExplanationResponse(BaseModel):
    topic: str = Field(description="Topic name, e.g. Dynamic Programming")
    severity: str = Field(description="High, Medium, or Low")
    root_cause_analysis: str = Field(description="Why this gap formed based on telemetry")
    concept_breakdowns: List[GapConceptBreakdown] = Field(description="Key conceptual friction points")
    remedial_action_plan: List[str] = Field(description="Step-by-step action items to bridge the gap")
    estimated_catchup_hours: float = Field(description="Hours required to reach target proficiency")
    source: str = Field(default="openai", description="Source: 'openai' or 'deterministic_fallback'")


# ─── Task 2: Explain Resource Recommendation ──────────────────────
class ResourceRecommendationExplanationResponse(BaseModel):
    resource_id: str
    resource_title: str
    topic: str
    resource_type: str
    primary_reason: str = Field(description="Core justification for recommending this specific item")
    pedagogical_alignment: str = Field(description="How format matches student learning style and gap level")
    targeted_gap_resolved: str = Field(description="Specific gap sub-concept this resource resolves")
    expected_outcome: str = Field(description="What mastery metric will improve after completing this")
    study_tips: List[str] = Field(description="How student should consume this specific resource")
    source: str = Field(default="openai")


# ─── Task 3: Explain Why Plan Changed ──────────────────────────────
class PlanChangeActionItem(BaseModel):
    activity_title: str
    change_type: str  # "moved" | "shortened" | "added" | "extended" | "removed"
    reason: str


class PlanChangeExplanationResponse(BaseModel):
    plan_version: int
    trigger_event: str = Field(description="Event that prompted change, e.g., missed session, score surge")
    high_level_narrative: str = Field(description="Human-readable explanation of the autonomous decision")
    tradeoffs_made: List[str] = Field(description="What was sacrificed vs what was prioritized")
    action_items: List[PlanChangeActionItem] = Field(description="Per-activity adjustments")
    deadline_impact: str = Field(description="Status of original deadline")
    is_goal_still_achievable: bool = Field(description="Whether learning goal is reachable")
    source: str = Field(default="openai")


# ─── Task 4: Personalized Learning Advice ──────────────────────────
class PersonalizedAdviceResponse(BaseModel):
    student_name: str
    current_velocity_assessment: str = Field(description="Evaluation of current study pace and momentum")
    key_strengths: List[str] = Field(description="Topics or behaviors student is excelling at")
    urgent_priorities: List[str] = Field(description="Top 1-2 things to focus on right now")
    daily_habit_recommendation: str = Field(description="Practical daily adjustment for maximum retention")
    motivational_verdict: str = Field(description="Encouraging, grounded verdict")
    source: str = Field(default="openai")


# ─── Task 5: Alternative Study Strategies ──────────────────────────
class StudyStrategyOption(BaseModel):
    name: str = Field(description="Strategy name, e.g. Pomodoro Drill, Feynman Technique, Spaced Retrieval")
    description: str = Field(description="How to execute this technique")
    why_it_fits_current_state: str = Field(description="Why this suits the student's current cognitive load")
    pros: List[str]
    cons: List[str]


class AlternativeStudyStrategiesResponse(BaseModel):
    current_challenge: str = Field(description="Fatigue, cognitive overload, time crunch, etc.")
    strategies: List[StudyStrategyOption] = Field(description="2-3 alternative pedagogical approaches")
    recommended_selection: str = Field(description="The single best strategy to adopt today")
    implementation_guide: str = Field(description="How to integrate with existing schedule")
    source: str = Field(default="openai")


# ─── Task 6: Answer Student Questions ──────────────────────────────
class AnswerQuestionResponse(BaseModel):
    question: str
    direct_answer: str = Field(description="Clear, concise conceptual answer tailored to student level")
    key_points: List[str] = Field(description="Core takeaways or formulas")
    code_example_or_analogy: Optional[str] = Field(default=None, description="Illustrative Python snippet or real-world analogy")
    related_topics: List[str] = Field(description="Related topics in student's curriculum")
    follow_up_questions: List[str] = Field(description="Suggested check-for-understanding questions")
    student_context: Optional[Dict[str, Any]] = Field(default=None, description="Student learning context used to personalize response")
    quick_action_type: Optional[str] = Field(default=None, description="Triggered quick action if any")
    source: str = Field(default="openai")


# ─── Task 7: Practice Problem Hints ────────────────────────────────
class ProblemHintStep(BaseModel):
    level: int = Field(description="Hint level 1 (subtle), 2 (conceptual), 3 (algorithmic)")
    hint_text: str = Field(description="Hint without giving away complete solution")


class ProblemHintsResponse(BaseModel):
    problem_title: str
    topic: str
    difficulty: str
    understanding_check: str = Field(description="Clarifying question to test problem comprehension")
    hints: List[ProblemHintStep] = Field(description="Progressive 3-level hints")
    pitfall_to_avoid: str = Field(description="Common edge case or bug")
    complexity_target: str = Field(description="Target Time & Space complexity (e.g. O(V + E))")
    source: str = Field(default="openai")


# ─── Generic AI Request Wrapper ────────────────────────────────────
class AIExplainGapRequest(BaseModel):
    topic: str
    severity: Optional[str] = "High"
    mastery: Optional[float] = 25.0
    student_id: Optional[str] = "stu-001"


class AIExplainResourceRequest(BaseModel):
    resource_id: str
    resource_title: str
    topic: str
    resource_type: str
    student_id: Optional[str] = "stu-001"


class AIExplainPlanChangeRequest(BaseModel):
    reason: Optional[str] = None
    old_version: Optional[int] = 10
    new_version: Optional[int] = 11
    student_id: Optional[str] = "stu-001"


class AIAdviceRequest(BaseModel):
    student_id: Optional[str] = "stu-001"
    context: Optional[str] = None


class AIStrategiesRequest(BaseModel):
    challenge: Optional[str] = "Time squeeze and cognitive fatigue with advanced Dynamic Programming"
    available_hours: Optional[float] = 2.0


class AIQuestionRequest(BaseModel):
    question: str
    topic: Optional[str] = None
    student_id: Optional[str] = "stu-001"
    quick_action: Optional[str] = None  # "explain_concept", "give_example", "give_practice", "give_hint", "check_answer", "suggest_resources", "adjust_plan", "why_plan_changed"
    student_answer: Optional[str] = None


class AIProblemHintsRequest(BaseModel):
    problem_title: str
    topic: Optional[str] = None
    difficulty: Optional[str] = "Medium"
    student_id: Optional[str] = "stu-001"

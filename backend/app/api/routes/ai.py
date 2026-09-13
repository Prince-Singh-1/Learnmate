"""
AI Service API Routes for LearnMate.

Exposes endpoints for the 7 specialized AI reasoning tasks:
1. POST /api/ai/explain-gap
2. POST /api/ai/explain-resource
3. POST /api/ai/explain-plan-change
4. POST /api/ai/personalized-advice
5. POST /api/ai/strategies
6. POST /api/ai/answer-question
7. POST /api/ai/problem-hints

All tasks use structured outputs validated by Pydantic models.
Gracefully handles timeouts, API key absence, and rate limits.
"""

from fastapi import APIRouter
from app.services.ai_service import AIService
from app.schemas.ai import (
    AIExplainGapRequest,
    KnowledgeGapExplanationResponse,
    AIExplainResourceRequest,
    ResourceRecommendationExplanationResponse,
    AIExplainPlanChangeRequest,
    PlanChangeExplanationResponse,
    AIAdviceRequest,
    PersonalizedAdviceResponse,
    AIStrategiesRequest,
    AlternativeStudyStrategiesResponse,
    AIQuestionRequest,
    AnswerQuestionResponse,
    AIProblemHintsRequest,
    ProblemHintsResponse,
)
from app.mock.data import get_student_profile

router = APIRouter()
ai_service = AIService()


@router.post("/explain-gap", response_model=KnowledgeGapExplanationResponse)
async def explain_knowledge_gap(payload: AIExplainGapRequest):
    """
    Task 1: Explain why a knowledge gap exists, root causes, and remedial steps.
    """
    return ai_service.explain_knowledge_gap(
        topic=payload.topic,
        severity=payload.severity or "High",
        mastery=payload.mastery or 25.0,
    )


@router.post("/explain-resource", response_model=ResourceRecommendationExplanationResponse)
async def explain_resource_recommendation(payload: AIExplainResourceRequest):
    """
    Task 2: Explain why a specific learning resource was recommended.
    """
    return ai_service.explain_resource_recommendation(
        resource_id=payload.resource_id,
        resource_title=payload.resource_title,
        topic=payload.topic,
        resource_type=payload.resource_type,
    )


@router.post("/explain-plan-change", response_model=PlanChangeExplanationResponse)
async def explain_plan_change(payload: AIExplainPlanChangeRequest):
    """
    Task 3: Explain why the autonomous learning plan changed.
    """
    return ai_service.explain_plan_change(
        plan_version=payload.new_version or 11,
        trigger_event=payload.reason or "Dynamic workload balancing",
        reason=payload.reason,
    )


@router.post("/personalized-advice", response_model=PersonalizedAdviceResponse)
async def get_personalized_advice(payload: AIAdviceRequest):
    """
    Task 4: Deliver personalized learning advice based on active telemetry.
    """
    student = get_student_profile()
    return ai_service.get_personalized_advice(
        student_name=student.get("name", "Prince"),
        current_goal=student.get("current_goal", "Master Data Structures & Algorithms"),
        progress=student.get("overall_progress", 68.0),
        streak=student.get("day_streak", 12),
        weakest_topic="Dynamic Programming",
        strongest_topic="Arrays",
    )


@router.post("/strategies", response_model=AlternativeStudyStrategiesResponse)
async def suggest_study_strategies(payload: AIStrategiesRequest):
    """
    Task 5: Suggest alternative study strategies (e.g. Pomodoro, Feynman).
    """
    return ai_service.suggest_study_strategies(
        challenge=payload.challenge or "Cognitive fatigue with complex algorithmic state transitions",
        available_hours=payload.available_hours or 2.0,
    )


@router.post("/answer-question", response_model=AnswerQuestionResponse)
async def answer_student_question(payload: AIQuestionRequest):
    """
    Task 6: Answer student conceptual questions with structured explanations adapted to student level.
    Feeds:
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
    from app.mock.data import (
        get_student_profile,
        get_performance_overview,
        get_knowledge_gaps,
        get_recent_activities,
        get_assessments,
    )
    student = get_student_profile()
    perf = get_performance_overview()
    mastery_list = perf.get("topic_mastery", [])
    gaps = get_knowledge_gaps()
    recents = get_recent_activities()
    asmts = get_assessments()

    # Determine topic and topic mastery
    topic = payload.topic
    if not topic:
        if "dijkstra" in payload.question.lower() or "shortest" in payload.question.lower():
            topic = "Graphs"
        elif "dp" in payload.question.lower() or "knapsack" in payload.question.lower():
            topic = "Dynamic Programming"
        else:
            topic = "Graphs"

    topic_mastery_val = 30.0
    for tm in mastery_list:
        if tm["topic"].lower() == topic.lower():
            topic_mastery_val = tm.get("mastery", 30.0)
            break

    context = {
        "student_goal": student.get("current_goal", "Master Data Structures & Algorithms"),
        "current_topic": topic,
        "topic_mastery": topic_mastery_val,
        "recent_assessment_results": f"Latest assessment score: {asmts[0]['percentage']}% in {asmts[0]['topic']}" if asmts else "Average 60%",
        "knowledge_gaps": [f"{g['topic']} ({g['severity']})" for g in gaps[:3]],
        "recent_activities": [a["title"] for a in recents[:3]],
    }

    return ai_service.answer_student_question(
        question=payload.question,
        topic=topic,
        context=context,
        quick_action=payload.quick_action,
        student_answer=payload.student_answer,
    )



@router.post("/problem-hints", response_model=ProblemHintsResponse)
async def get_problem_hints(payload: AIProblemHintsRequest):
    """
    Task 7: Provide progressive hints for coding challenges without spoiling code.
    """
    return ai_service.get_problem_hints(
        problem_title=payload.problem_title,
        topic=payload.topic or "Dynamic Programming",
        difficulty=payload.difficulty or "Medium",
    )

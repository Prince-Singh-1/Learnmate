"""
Adaptive Practice API Routes for LearnMate.

Endpoints:
- GET /api/practice/adaptive/question?topic=Graphs&difficulty=Easy
- POST /api/practice/adaptive/attempt
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.adaptive_practice import (
    AdaptiveQuestion,
    QuestionAttemptSubmission,
    AdaptiveAttemptResultResponse,
)
from app.services.adaptive_practice_service import AdaptivePracticeService

router = APIRouter()
service = AdaptivePracticeService()


@router.get("/question", response_model=AdaptiveQuestion)
async def get_adaptive_question(
    topic: str = Query(default="Graphs"),
    difficulty: Optional[str] = Query(default=None),
):
    """
    Get an initial question adapted to student's current mastery level or requested difficulty.
    """
    return service.get_initial_question(topic=topic, starting_difficulty=difficulty)


@router.post("/attempt", response_model=AdaptiveAttemptResultResponse)
async def submit_question_attempt(payload: QuestionAttemptSubmission):
    """
    Submit an answer attempt.
    - Evaluates correctness.
    - Transitions difficulty (Easy -> Medium -> Hard, Hard -> wrong -> Medium + explanation).
    - Updates topic mastery and knowledge gap severity.
    - Checks whether autonomous replanning is required and triggers agent if needed.
    """
    return service.process_attempt(
        question_id=payload.question_id,
        topic=payload.topic,
        difficulty=payload.difficulty,
        selected_option_id=payload.selected_option_id,
        time_spent_seconds=payload.time_spent_seconds,
        attempt_number=payload.attempt_number,
        student_id=payload.student_id or "stu-001",
    )

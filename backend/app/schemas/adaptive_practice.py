"""
Adaptive Practice Schemas for LearnMate API.

Supports:
- Dynamic question generation responding to student performance
- Transitions:
  Easy -> correct -> Medium
  Medium -> correct -> Hard
  Hard -> wrong -> Medium + explanation
- Tracking:
  question, topic, difficulty, answer, correctness, time, attempt number
- Post-assessment autonomous effects:
  update topic mastery, update knowledge gaps, check whether replanning is required,
  and connect to autonomous learning agent.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class QuestionOption(BaseModel):
    id: str
    text: str


class AdaptiveQuestion(BaseModel):
    id: str
    topic: str
    difficulty: str  # "Easy" | "Medium" | "Hard"
    question_text: str
    options: List[QuestionOption]
    correct_option_id: str
    explanation: str
    target_concept: str
    time_limit_seconds: int = 90


class QuestionAttemptSubmission(BaseModel):
    question_id: str
    topic: str
    difficulty: str  # "Easy" | "Medium" | "Hard"
    selected_option_id: str
    time_spent_seconds: int
    attempt_number: int = 1
    student_id: Optional[str] = "stu-001"


class AdaptiveNextQuestionResult(BaseModel):
    previous_difficulty: str
    was_correct: bool
    next_difficulty: str
    adaptation_reason: str
    explanation: Optional[str] = None


class AdaptiveAttemptResultResponse(BaseModel):
    attempt_id: str
    question_id: str
    topic: str
    difficulty: str
    selected_option_id: str
    correct_option_id: str
    is_correct: bool
    time_spent_seconds: int
    attempt_number: int
    adaptation: AdaptiveNextQuestionResult
    next_question: Optional[AdaptiveQuestion] = None
    topic_mastery_updated: float
    knowledge_gap_severity: str
    replan_required: bool
    replan_reason: Optional[str] = None
    agent_run_id: Optional[str] = None
    message: str


class AdaptivePracticeSessionResponse(BaseModel):
    session_id: str
    student_id: str
    topic: str
    current_difficulty: str
    streak: int
    total_answered: int
    total_correct: int
    current_question: AdaptiveQuestion
    recent_attempts: List[Dict[str, Any]]

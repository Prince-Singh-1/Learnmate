"""
LearnMate Pydantic Schemas Package.
"""

from app.schemas.student import StudentResponse, StudentUpdateRequest
from app.schemas.goals import GoalItem, MilestoneItem, GoalsResponse
from app.schemas.performance import PerformancePoint, TopicMastery, PerformanceResponse
from app.schemas.gaps import KnowledgeGapItem, KnowledgeGapsResponse
from app.schemas.resources import ResourceItem, ResourcesResponse
from app.schemas.calendar import CalendarSlot, CalendarResponse
from app.schemas.activities import (
    ActivityItem,
    ActivitiesResponse,
    ActivityCompleteRequest,
    ActivityMissedRequest,
    ActivityActionResponse,
)
from app.schemas.assessments import (
    AssessmentItem,
    AssessmentsResponse,
    AssessmentResultRequest,
    AssessmentResultResponse,
)
from app.schemas.plan import PlanActivity, LearningPlanResponse
from app.schemas.agent import AgentRunRequest, AgentStepDetail, AgentRunResponse
from app.schemas.replan import ReplanRequest, ReplanResponse
from app.schemas.verification import (
    VerificationRequest,
    VerificationResponse,
    VerificationCheckItem,
)

__all__ = [
    "StudentResponse",
    "StudentUpdateRequest",
    "GoalItem",
    "MilestoneItem",
    "GoalsResponse",
    "PerformancePoint",
    "TopicMastery",
    "PerformanceResponse",
    "KnowledgeGapItem",
    "KnowledgeGapsResponse",
    "ResourceItem",
    "ResourcesResponse",
    "CalendarSlot",
    "CalendarResponse",
    "ActivityItem",
    "ActivitiesResponse",
    "ActivityCompleteRequest",
    "ActivityMissedRequest",
    "ActivityActionResponse",
    "AssessmentItem",
    "AssessmentsResponse",
    "AssessmentResultRequest",
    "AssessmentResultResponse",
    "PlanActivity",
    "LearningPlanResponse",
    "AgentRunRequest",
    "AgentStepDetail",
    "AgentRunResponse",
    "ReplanRequest",
    "ReplanResponse",
    "VerificationRequest",
    "VerificationResponse",
    "VerificationCheckItem",
]

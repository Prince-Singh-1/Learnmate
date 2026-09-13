"""
API dependency injection.

Provides database sessions, current user, and shared service instances.
"""

from typing import Generator
from functools import lru_cache

from app.services.student_service import StudentService
from app.services.activity_service import ActivityService
from app.services.performance_analyzer import PerformanceAnalyzer
from app.services.gap_detector import GapDetector
from app.services.resource_recommender import ResourceRecommender
from app.services.schedule_engine import ScheduleEngine
from app.services.plan_generator import PlanGenerator
from app.services.replanner import Replanner
from app.services.plan_verifier import PlanVerifier
from app.agent.learning_agent import LearningAgent


def get_db() -> Generator:
    """Get database session (mock for in-memory mode)."""
    yield None


@lru_cache()
def get_student_service() -> StudentService:
    return StudentService()


@lru_cache()
def get_activity_service() -> ActivityService:
    return ActivityService()


@lru_cache()
def get_performance_analyzer() -> PerformanceAnalyzer:
    return PerformanceAnalyzer()


@lru_cache()
def get_gap_detector() -> GapDetector:
    return GapDetector()


@lru_cache()
def get_resource_recommender() -> ResourceRecommender:
    return ResourceRecommender()


@lru_cache()
def get_schedule_engine() -> ScheduleEngine:
    return ScheduleEngine()


@lru_cache()
def get_plan_generator() -> PlanGenerator:
    return PlanGenerator()


@lru_cache()
def get_replanner() -> Replanner:
    return Replanner()


@lru_cache()
def get_plan_verifier() -> PlanVerifier:
    return PlanVerifier()


@lru_cache()
def get_learning_agent() -> LearningAgent:
    return LearningAgent()

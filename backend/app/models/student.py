"""
Student and StudentEvent SQLAlchemy models.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Student(Base):
    """Represents a student learner."""

    __tablename__ = "students"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    preferred_study_times = Column(JSON, default=lambda: ["morning", "afternoon"])
    weekly_available_hours = Column(Float, default=15.0)
    degree = Column(String(255), default="B.Tech (CSE)")
    institution = Column(String(255), default="Institute of Technology")
    avatar_url = Column(String(500), default="/prince-avatar.jpg")
    current_goal = Column(String(255), default="Master Data Structures & Algorithms")
    target_deadline = Column(DateTime, nullable=True)
    overall_progress = Column(Float, default=0.0)
    day_streak = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    goals = relationship("LearningGoal", back_populates="student", cascade="all, delete-orphan")
    plans = relationship("LearningPlan", back_populates="student", cascade="all, delete-orphan")
    events = relationship("StudentEvent", back_populates="student", cascade="all, delete-orphan")
    masteries = relationship("TopicMastery", back_populates="student", cascade="all, delete-orphan")
    gaps = relationship("KnowledgeGap", back_populates="student", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="student", cascade="all, delete-orphan")
    calendar_events = relationship("CalendarEvent", back_populates="student", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="student", cascade="all, delete-orphan")
    agent_runs = relationship("AgentRun", back_populates="student", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="student", cascade="all, delete-orphan")


class StudentEvent(Base):
    """Tracks chronological telemetry and behavioral events for a student."""

    __tablename__ = "student_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)  # e.g. activity_completed, session_missed, replan_triggered
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    student = relationship("Student", back_populates="events")

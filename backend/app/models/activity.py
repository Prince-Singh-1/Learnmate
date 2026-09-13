"""
LearningActivity and StudySession SQLAlchemy models.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class LearningActivity(Base):
    """An individual study unit or scheduled session item."""

    __tablename__ = "learning_activities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), ForeignKey("learning_plans.id"), nullable=True, index=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=True, index=True)
    resource_id = Column(String(36), ForeignKey("learning_resources.id"), nullable=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False, index=True)
    type = Column(String(50), nullable=False)  # video, practice, reading, quiz
    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=False)
    status = Column(String(50), default="pending")  # pending, completed, missed, rescheduled, deferred
    priority = Column(Integer, default=1)  # 1 = highest, 2 = medium, etc.
    duration_minutes = Column(Integer, default=60)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    plan = relationship("LearningPlan", back_populates="activities")
    resource = relationship("LearningResource", back_populates="activities")
    study_sessions = relationship("StudySession", back_populates="activity", cascade="all, delete-orphan")


class StudySession(Base):
    """Tracks an actual student study execution event."""

    __tablename__ = "study_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    activity_id = Column(String(36), ForeignKey("learning_activities.id"), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Float, default=0.0)
    notes = Column(String(1000), default="")
    completed = Column(Boolean, default=True)

    # Relationships
    student = relationship("Student", back_populates="study_sessions")
    activity = relationship("LearningActivity", back_populates="study_sessions")

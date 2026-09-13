"""
LearningPlan, PlanVersion, and PlanChange SQLAlchemy models.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class LearningPlan(Base):
    """An active or archived learning roadmap for a student."""

    __tablename__ = "learning_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    goal_id = Column(String(36), ForeignKey("learning_goals.id"), nullable=True)
    current_version = Column(Integer, default=1)
    status = Column(String(50), default="active")  # active, superseded, completed
    target_deadline = Column(DateTime, nullable=False)
    remaining_days = Column(Integer, default=60)
    required_study_hours = Column(Float, default=90.0)
    scheduled_study_hours = Column(Float, default=96.0)
    feasibility_ratio = Column(Float, default=1.06)
    deadline_guaranteed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="plans")
    goal = relationship("LearningGoal", back_populates="plans")
    versions = relationship("PlanVersion", back_populates="plan", cascade="all, delete-orphan")
    activities = relationship("LearningActivity", back_populates="plan", cascade="all, delete-orphan")
    changes = relationship("PlanChange", back_populates="plan", cascade="all, delete-orphan")


class PlanVersion(Base):
    """Immutable snapshot record of a learning plan revision."""

    __tablename__ = "plan_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), ForeignKey("learning_plans.id"), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    status = Column(String(50), default="active")  # active, superseded
    summary = Column(String(1000), default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    plan = relationship("LearningPlan", back_populates="versions")
    changes = relationship("PlanChange", back_populates="plan_version", cascade="all, delete-orphan")


class PlanChange(Base):
    """Tracks discrete schedule modifications resulting from autonomous replanning."""

    __tablename__ = "plan_changes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), ForeignKey("learning_plans.id"), nullable=False, index=True)
    plan_version_id = Column(String(36), ForeignKey("plan_versions.id"), nullable=True)
    old_activity = Column(String(255), nullable=True)
    new_activity = Column(String(255), nullable=True)
    old_activity_id = Column(String(36), nullable=True)
    new_activity_id = Column(String(36), nullable=True)
    reason = Column(String(1000), nullable=False)
    change_type = Column(String(50), default="rescheduled")  # rescheduled, inserted, deleted, rebalanced
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    plan = relationship("LearningPlan", back_populates="changes")
    plan_version = relationship("PlanVersion", back_populates="changes")

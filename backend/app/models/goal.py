"""
LearningGoal SQLAlchemy model.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class LearningGoal(Base):
    """Represents a primary learning objective or curriculum goal."""

    __tablename__ = "learning_goals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), default="")
    target_date = Column(DateTime, nullable=False)
    target_proficiency = Column(Float, default=85.0)  # Percentage threshold
    status = Column(String(50), default="in_progress")  # in_progress, achieved, paused, revised
    priority = Column(String(50), default="High")
    topics = Column(JSON, default=list)
    milestones = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="goals")
    plans = relationship("LearningPlan", back_populates="goal")

"""
Assessment and AssessmentResult SQLAlchemy models.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Assessment(Base):
    """Represents a standardized quiz or diagnostic test definition."""

    __tablename__ = "assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False, index=True)
    difficulty = Column(String(50), default="Intermediate")
    total_questions = Column(Integer, default=10)
    max_score = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    results = relationship("AssessmentResult", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentResult(Base):
    """Represents an individual student's completed assessment outcome."""

    __tablename__ = "assessment_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String(36), ForeignKey("assessments.id"), nullable=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    topic = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="Intermediate")
    score = Column(Float, nullable=False)
    max_score = Column(Float, default=100.0)
    percentage = Column(Float, nullable=False)
    status = Column(String(50), default="passed")  # passed, needs_review
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assessment = relationship("Assessment", back_populates="results")
    student = relationship("Student", back_populates="assessment_results")

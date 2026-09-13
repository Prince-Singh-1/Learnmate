"""
LearningResource and Recommendation SQLAlchemy models.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class LearningResource(Base):
    """A learning resource (video, article, exercise, quiz, web tool)."""

    __tablename__ = "learning_resources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)  # video, pdf, practice, tool, reading
    topic = Column(String(255), nullable=False, index=True)
    difficulty = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced
    duration = Column(Float, default=30.0)  # In minutes
    quality_score = Column(Float, default=90.0)  # Benchmark / user rating (0-100)
    url = Column(String(1000), nullable=True)
    source = Column(String(255), default="Curated Web")
    detail = Column(String(255), default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    recommendations = relationship("Recommendation", back_populates="resource", cascade="all, delete-orphan")
    activities = relationship("LearningActivity", back_populates="resource")


class Recommendation(Base):
    """An AI recommendation matching a resource to a student's gap."""

    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    resource_id = Column(String(36), ForeignKey("learning_resources.id"), nullable=False)
    gap_id = Column(String(36), ForeignKey("knowledge_gaps.id"), nullable=True)
    reason = Column(String(1000), nullable=False)
    match_score = Column(Float, default=90.0)
    status = Column(String(50), default="active")  # active, accepted, dismissed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="recommendations")
    resource = relationship("LearningResource", back_populates="recommendations")
    gap = relationship("KnowledgeGap", back_populates="recommendations")

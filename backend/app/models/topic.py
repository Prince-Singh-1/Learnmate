"""
Topic, TopicMastery, and KnowledgeGap SQLAlchemy models.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Topic(Base):
    """Represents a curriculum domain or syllabus concept."""

    __tablename__ = "topics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False)
    category = Column(String(255), default="Computer Science")
    description = Column(String(1000), default="")
    difficulty_level = Column(String(50), default="Intermediate")
    color = Column(String(50), default="#6366f1")
    icon = Column(String(50), default="📊")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    mastery_records = relationship("TopicMastery", back_populates="topic_ref")
    gap_records = relationship("KnowledgeGap", back_populates="topic_ref")


class TopicMastery(Base):
    """Tracks a student's quantitative mastery and trajectory in a topic."""

    __tablename__ = "topic_masteries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    topic = Column(String(255), nullable=False)
    topic_id = Column(String(36), ForeignKey("topics.id"), nullable=True)
    mastery_score = Column(Float, nullable=False)  # 0 to 100
    confidence = Column(Float, default=0.85)  # 0 to 1.0
    target_mastery = Column(Float, default=80.0)  # 0 to 100
    trend = Column(String(50), default="improving")  # improving, stable, declining
    assessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="masteries")
    topic_ref = relationship("Topic", back_populates="mastery_records")


class KnowledgeGap(Base):
    """Defines an identified deficit below benchmark mastery."""

    __tablename__ = "knowledge_gaps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    topic = Column(String(255), nullable=False)
    topic_id = Column(String(36), ForeignKey("topics.id"), nullable=True)
    gap_score = Column(Float, nullable=False)  # Distance from target
    priority = Column(String(50), default="High")  # High, Medium, Low
    estimated_hours = Column(Float, default=4.0)
    reason = Column(String(1000), nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="gaps")
    topic_ref = relationship("Topic", back_populates="gap_records")
    recommendations = relationship("Recommendation", back_populates="gap", cascade="all, delete-orphan")

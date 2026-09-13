"""
Performance record SQLAlchemy model.
"""

import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class PerformanceRecord(Base):
    """A single performance measurement for a student on a topic."""

    __tablename__ = "performance_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    topic = Column(String(255), nullable=False)
    score = Column(Float, nullable=False)
    mastery_level = Column(Float, default=0.0)  # 0.0 to 1.0
    assessed_at = Column(DateTime, nullable=False)

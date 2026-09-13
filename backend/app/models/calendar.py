"""
CalendarEvent SQLAlchemy model.
"""

import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class CalendarEvent(Base):
    """Represents a calendar study slot or external commitment."""

    __tablename__ = "calendar_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    title = Column(String(255), default="Study Block")
    day = Column(String(50), nullable=False)  # YYYY-MM-DD
    weekday = Column(String(50), nullable=False)  # Monday, Tuesday, etc.
    start_time = Column(String(50), nullable=False)  # HH:MM format
    end_time = Column(String(50), nullable=False)  # HH:MM format
    duration_minutes = Column(Integer, default=120)
    is_available = Column(Boolean, default=True)  # True = study window, False = busy/class
    label = Column(String(255), default="Available Window")
    recurrence = Column(String(50), default="weekly")  # weekly, daily, once

    # Relationships
    student = relationship("Student", back_populates="calendar_events")

"""
AgentRun SQLAlchemy model.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class AgentRun(Base):
    """Tracks an execution cycle of the 10-step Autonomous Learning Agent loop."""

    __tablename__ = "agent_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="completed")  # running, completed, failed
    actions_taken = Column(JSON, default=list)  # Detailed log of steps and decisions
    summary = Column(String(1000), default="")
    steps_count = Column(Integer, default=10)
    plan_version = Column(Integer, default=1)

    # Relationships
    student = relationship("Student", back_populates="agent_runs")

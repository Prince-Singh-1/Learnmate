"""
Goal Service.

Provides learning goals, roadmap milestones, target deadlines, and progress stats.
"""

from typing import Dict, Any
from app.mock.data import get_current_goals


class GoalService:
    """Manages student learning goals and milestones."""

    def get_goals(self, student_id: str = "stu-001") -> Dict[str, Any]:
        """
        Get all goals and primary goal for student.
        """
        goals = get_current_goals()
        primary = goals[0] if goals else None
        return {
            "student_id": student_id,
            "goals": goals,
            "primary_goal": primary,
        }

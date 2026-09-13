"""
Student Service.

Provides student profile retrieval and profile settings management.
"""

from typing import Dict, Any
from app.mock.data import get_student_profile, _STUDENT


class StudentService:
    """Manages student profile and metadata."""

    def get_student(self, student_id: str = "stu-001") -> Dict[str, Any]:
        """
        Get the student profile for Prince Singh.
        """
        return get_student_profile()

    def update_student(self, student_id: str, updates: dict) -> Dict[str, Any]:
        """
        Update student fields in memory.
        """
        for k, v in updates.items():
            if v is not None and k in _STUDENT:
                _STUDENT[k] = v
        return get_student_profile()

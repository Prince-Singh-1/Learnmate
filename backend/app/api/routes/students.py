"""
Student API endpoints.

Provides CRUD operations for student management.
"""

from fastapi import APIRouter
from app.mock.data import get_mock_students

router = APIRouter()


@router.get("/")
async def list_students():
    """List all students."""
    return get_mock_students()


@router.get("/{student_id}")
async def get_student(student_id: str):
    """Get a specific student by ID."""
    students = get_mock_students()
    for student in students:
        if student["id"] == student_id:
            return student
    return {"error": "Student not found"}


@router.post("/")
async def create_student():
    """Create a new student (stub)."""
    return {"message": "Student creation not yet implemented", "status": "stub"}

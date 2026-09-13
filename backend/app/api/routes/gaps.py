"""
Knowledge Gaps API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.gaps import KnowledgeGapsResponse
from app.services.gap_detector import GapDetector

router = APIRouter()
service = GapDetector()


@router.get("", response_model=KnowledgeGapsResponse)
@router.get("/", response_model=KnowledgeGapsResponse)
async def get_knowledge_gaps(student_id: str = "stu-001"):
    """
    Get detected knowledge gaps and remedial interventions.
    """
    return service.detect_gaps(student_id)

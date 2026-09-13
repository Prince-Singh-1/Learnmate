"""
Recommended Resources API routes for LearnMate.
"""

from fastapi import APIRouter
from app.schemas.resources import ResourcesResponse
from app.services.resource_recommender import ResourceRecommender

router = APIRouter()
service = ResourceRecommender()


@router.get("", response_model=ResourcesResponse)
@router.get("/", response_model=ResourcesResponse)
async def get_recommended_resources(student_id: str = "stu-001"):
    """
    Get AI-curated learning resources based on student goals and gaps.
    """
    return service.get_recommendations(student_id)

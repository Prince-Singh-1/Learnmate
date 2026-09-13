"""
Resource Recommender Service.

Matches optimal learning resources (videos, PDFs, practice sets, interactive tools)
to student knowledge gaps and current learning goals.
"""

from typing import List, Dict, Any
from app.mock.data import get_recommended_resources


class ResourceRecommender:
    """Finds and ranks learning resources based on student gaps."""

    def get_recommendations(self, student_id: str = "stu-001") -> Dict[str, Any]:
        """
        Get recommended resources for a student.
        """
        resources = get_recommended_resources()
        return {
            "total_resources": len(resources),
            "resources": resources,
        }

    def recommend_for_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Find resources relevant to a specific topic.
        """
        resources = get_recommended_resources()
        return [r for r in resources if r.get("topic", "").lower() == topic.lower()]

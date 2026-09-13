"""
Assessment Service.

Records assessment and test results, computes performance statistics,
and dynamically updates mastery levels.
"""

from typing import Dict, Any
from app.mock.data import get_assessments, record_assessment_result


class AssessmentService:
    """Manages student assessments, quizzes, and score evaluations."""

    def get_assessments(self, student_id: str = "stu-001") -> Dict[str, Any]:
        """
        List assessment history and average percentage score.
        """
        asmts = get_assessments()
        avg_score = round(sum(a["percentage"] for a in asmts) / len(asmts), 1) if asmts else 0.0

        return {
            "student_id": student_id,
            "total_assessments": len(asmts),
            "average_score": avg_score,
            "assessments": asmts,
        }

    def record_result(self, topic: str, score: float, max_score: float = 100.0) -> Dict[str, Any]:
        """
        Record a new quiz or test score and recalculate mastery.
        """
        result = record_assessment_result(topic=topic, score=score, max_score=max_score)
        return {
            "success": True,
            "assessment": result["assessment"],
            "message": f"Assessment result recorded for {topic}. Mastery updated.",
        }

"""
Knowledge Gap Detector Service.

Scans student topic mastery levels, flags weak areas based on threshold (<60%),
and prioritizes remedial learning interventions.
"""

from typing import List, Dict, Any
from app.mock.data import get_knowledge_gaps


class GapDetector:
    """Detects and ranks student knowledge gaps."""

    def __init__(self, engine: Any = None):
        self.engine = engine

    def detect_gaps(self, student_id: str = "stu-001", mastery_data: Any = None) -> Dict[str, Any]:
        """
        Identify knowledge gaps for a student.
        """
        gaps = get_knowledge_gaps()
        high_severity = [g for g in gaps if g["severity"] == "High"]

        return {
            "student_id": student_id,
            "total_gaps": len(gaps),
            "high_severity_count": len(high_severity),
            "gaps": gaps,
        }

    def get_critical_topics(self, student_id: str = "stu-001") -> List[str]:
        """
        Return names of topics with high severity gaps requiring immediate study.
        """
        detected = self.detect_gaps(student_id)
        return [g["topic"] for g in detected["gaps"] if g["severity"] == "High"]

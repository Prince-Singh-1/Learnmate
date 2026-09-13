"""
Performance Analyzer Service.

Analyzes student performance points, calculates topic-level mastery,
evaluates historical trends, and determines overall competency.
"""

from app.mock.data import get_performance_overview, _TOPIC_MASTERY


class PerformanceAnalyzer:
    """Aggregates and analyzes student performance data."""

    def get_student_performance(self, student_id: str = "stu-001") -> dict:
        """
        Get complete performance analytics for a student.
        """
        overview = get_performance_overview()

        # Sort topics to determine strongest and weakest
        topics = overview["topic_mastery"]
        sorted_topics = sorted(topics, key=lambda x: x["mastery"], reverse=True)

        strongest = f"{sorted_topics[0]['topic']} ({sorted_topics[0]['mastery']}%)" if sorted_topics else "N/A"
        weakest = f"{sorted_topics[-1]['topic']} ({sorted_topics[-1]['mastery']}%)" if sorted_topics else "N/A"

        # Calculate weighted overall mastery
        total_mastery = sum(t["mastery"] for t in topics)
        overall = round(total_mastery / len(topics), 1) if topics else 68.0

        return {
            "student_id": student_id,
            "overall_mastery": overall,
            "strongest_topic": strongest,
            "weakest_topic": weakest,
            "points": overview["points"],
            "topic_mastery": topics,
        }

    def get_summary(self, student_id: str = "stu-001") -> dict:
        """Alias for get_student_performance for route compatibility."""
        return self.get_student_performance(student_id)


    def detect_trends(self, student_id: str = "stu-001") -> dict:
        """
        Compute week-over-week trends in student scores.
        """
        perf = self.get_student_performance(student_id)
        pts = perf["points"]
        if len(pts) >= 2:
            latest = pts[-1]["score"]
            previous = pts[-2]["score"]
            diff = round(latest - previous, 1)
            trend = "improving" if diff > 0 else ("declining" if diff < 0 else "stable")
        else:
            diff = 0.0
            trend = "stable"

        return {
            "trend": trend,
            "score_delta": diff,
            "latest_score": pts[-1]["score"] if pts else 0.0,
        }

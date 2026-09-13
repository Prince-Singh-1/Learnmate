"""
Activity Service.

Handles listing today's scheduled activities, marking activities complete,
recording missed activities, and triggering replanning recommendations.
"""

from datetime import datetime
from typing import Dict, Any
from app.mock.data import (
    get_today_activities,
    get_recent_activities,
    mark_activity_completed,
    mark_activity_missed,
)


class ActivityService:
    """Manages scheduled daily learning activities."""

    def get_today_activities(self) -> Dict[str, Any]:
        """
        Get all scheduled activities for today with counts.
        """
        acts = get_today_activities()
        completed = sum(1 for a in acts if a["completed"])
        pending = len(acts) - completed

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_activities": len(acts),
            "completed_count": completed,
            "pending_count": pending,
            "activities": acts,
        }

    def get_recent_activities(self) -> list:
        """
        Get recent activity history.
        """
        return get_recent_activities()

    def complete_activity(self, activity_id: str, notes: str = None) -> Dict[str, Any]:
        """
        Mark an activity as completed.
        """
        result = mark_activity_completed(activity_id)
        return result

    def miss_activity(self, activity_id: str, reason: str = None) -> Dict[str, Any]:
        """
        Mark an activity as missed. Flags system for autonomous replan.
        """
        result = mark_activity_missed(activity_id)
        return result

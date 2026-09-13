"""
LearnMate Deterministic Performance Analysis Engine.

Receives multi-source student learning telemetry:
- assessment results
- quiz scores
- practice results
- activity completion
- time spent
- previous mastery
- target mastery

Calculates per topic:
- mastery (0 - 100)
- confidence (0.0 - 1.0)
- trend (improving, stable, declining)
- target (benchmark threshold)
- gap (target - mastery, min 0)
- priority (HIGH, MEDIUM, LOW)
- estimated learning hours

Automatically detects and ranks knowledge gaps using deterministic multi-factor scoring:
- size of knowledge gap
- importance of topic
- deadline proximity
- recent performance drift
- prerequisite dependencies (graph topological blocking)
- estimated learning effort
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import math


class PriorityLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TrendDirection(str, Enum):
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"


@dataclass
class AssessmentScore:
    """Represents a scored assessment or exam."""
    score: float
    max_score: float = 100.0
    weight: float = 1.0

    @property
    def percentage(self) -> float:
        if self.max_score <= 0:
            return 0.0
        return max(0.0, min(100.0, (self.score / self.max_score) * 100.0))


@dataclass
class QuizScore:
    """Represents a diagnostic quiz result."""
    score: float
    max_score: float = 100.0

    @property
    def percentage(self) -> float:
        if self.max_score <= 0:
            return 0.0
        return max(0.0, min(100.0, (self.score / self.max_score) * 100.0))


@dataclass
class PracticeResult:
    """Represents a coding exercise or practice session."""
    problems_solved: int
    total_problems: int
    hints_used: int = 0
    accuracy: Optional[float] = None

    @property
    def effective_score(self) -> float:
        if self.accuracy is not None:
            return max(0.0, min(100.0, self.accuracy))
        if self.total_problems <= 0:
            return 0.0
        raw_pct = (self.problems_solved / self.total_problems) * 100.0
        hint_penalty = min(20.0, self.hints_used * 2.5)
        return max(0.0, min(100.0, raw_pct - hint_penalty))


@dataclass
class ActivityCompletion:
    """Activity attendance and study schedule execution."""
    completed_activities: int
    scheduled_activities: int

    @property
    def completion_rate(self) -> float:
        if self.scheduled_activities <= 0:
            return 100.0
        return max(0.0, min(100.0, (self.completed_activities / self.scheduled_activities) * 100.0))


@dataclass
class TopicPerformanceInput:
    """Input telemetry for a single topic."""
    topic: str
    target_mastery: float = 80.0
    previous_mastery: Optional[float] = None
    assessment_results: List[AssessmentScore] = field(default_factory=list)
    quiz_scores: List[QuizScore] = field(default_factory=list)
    practice_results: List[PracticeResult] = field(default_factory=list)
    activity_completion: Optional[ActivityCompletion] = None
    time_spent_hours: float = 0.0
    importance: float = 1.0  # 1.0 (standard) to 2.0 (critical core topic)
    difficulty: str = "Intermediate"  # Beginner, Intermediate, Advanced
    prerequisites: List[str] = field(default_factory=list)


@dataclass
class TopicPerformanceResult:
    """Calculated metrics for a single topic."""
    topic: str
    mastery: float
    confidence: float
    trend: TrendDirection
    target: float
    gap: float
    priority: PriorityLevel
    estimated_learning_hours: float
    is_knowledge_gap: bool
    reason: str


@dataclass
class KnowledgeGapResult:
    """Defines an identified knowledge gap ready for scheduling and recommendation."""
    id: str
    topic: str
    gap_score: float
    priority: PriorityLevel
    mastery: float
    target: float
    confidence: float
    trend: TrendDirection
    estimated_hours: float
    reason: str
    recommended_action: str


class PerformanceEngine:
    """
    Deterministic mathematical engine for calculating student mastery,
    evaluating confidence and trajectory, and prioritizing knowledge gaps.
    """

    # Topic prerequisite dependency map (topics that depend on other topics)
    DEFAULT_DEPENDENCIES: Dict[str, List[str]] = {
        "Dynamic Programming": ["Recursion", "Arrays"],
        "Graphs": ["Trees", "Stack & Queue", "Recursion"],
        "Trees": ["Recursion", "Linked Lists"],
        "Binary Search": ["Arrays", "Sorting"],
        "Bit Manipulation": ["Arrays"],
    }

    # Difficulty effort multipliers
    DIFFICULTY_FACTORS: Dict[str, float] = {
        "Beginner": 0.10,
        "Intermediate": 0.14,
        "Advanced": 0.18,
    }

    def __init__(
        self,
        default_target_mastery: float = 80.0,
        prerequisite_graph: Optional[Dict[str, List[str]]] = None,
    ):
        self.default_target_mastery = default_target_mastery
        self.prerequisite_graph = (
            prerequisite_graph if prerequisite_graph is not None else self.DEFAULT_DEPENDENCIES
        )

    def calculate_topic(
        self,
        data: TopicPerformanceInput,
        days_until_deadline: int = 45,
        dependent_topics_count: int = 0,
    ) -> TopicPerformanceResult:
        """
        Deterministically calculate mastery, confidence, trend, gap, priority,
        and estimated hours for a single topic.
        """
        # 1. Calculate Component Averages
        asmt_pcts = [a.percentage for a in data.assessment_results]
        quiz_pcts = [q.percentage for q in data.quiz_scores]
        practice_pcts = [p.effective_score for p in data.practice_results]
        completion_pct = (
            data.activity_completion.completion_rate
            if data.activity_completion is not None
            else None
        )

        has_asmt = len(asmt_pcts) > 0
        has_quiz = len(quiz_pcts) > 0
        has_practice = len(practice_pcts) > 0
        has_completion = completion_pct is not None
        has_previous = data.previous_mastery is not None

        # 2. Weighted Mastery Formulation
        # Nominal weights: Assessments (40%), Practice (25%), Quizzes (20%), Completion (10%), Previous (5%)
        active_weights: Dict[str, float] = {}
        active_values: Dict[str, float] = {}

        if has_asmt:
            active_weights["asmt"] = 0.40
            # Higher weight to more recent assessments if multiple exist
            active_values["asmt"] = self._weighted_recent_average(asmt_pcts)
        if has_practice:
            active_weights["practice"] = 0.25
            active_values["practice"] = sum(practice_pcts) / len(practice_pcts)
        if has_quiz:
            active_weights["quiz"] = 0.20
            active_values["quiz"] = sum(quiz_pcts) / len(quiz_pcts)
        if has_completion:
            active_weights["completion"] = 0.10
            active_values["completion"] = completion_pct
        if has_previous:
            active_weights["previous"] = 0.05 if (has_asmt or has_practice or has_quiz) else 1.0
            active_values["previous"] = data.previous_mastery

        if not active_weights:
            # Fallback if no data provided at all
            mastery = 0.0
        else:
            total_weight = sum(active_weights.values())
            mastery = sum(active_values[k] * (active_weights[k] / total_weight) for k in active_weights)

        mastery = round(max(0.0, min(100.0, mastery)), 1)

        # 3. Confidence Metric
        # Depends on number of observations (saturation curve) and variance
        sample_size = len(asmt_pcts) + len(quiz_pcts) + len(practice_pcts)
        if sample_size == 0:
            confidence = 0.50 if has_previous else 0.20
        else:
            # Saturation model: 1 - exp(-N / 4.0), scaled between 0.35 and 0.98
            size_factor = 1.0 - math.exp(-sample_size / 4.0)
            confidence = 0.40 + (0.55 * size_factor)
            # Adjust slightly for time spent
            if data.time_spent_hours >= 5.0:
                confidence = min(0.98, confidence + 0.05)

        confidence = round(confidence, 2)

        # 4. Trend Evaluation
        # Compares recent performance against older baseline
        all_recent_scores = asmt_pcts + quiz_pcts + practice_pcts
        if len(all_recent_scores) >= 2:
            mid = len(all_recent_scores) // 2
            early = sum(all_recent_scores[:mid]) / max(1, mid)
            late = sum(all_recent_scores[mid:]) / max(1, len(all_recent_scores) - mid)
            delta = late - early
        elif data.previous_mastery is not None:
            delta = mastery - data.previous_mastery
        else:
            delta = 0.0

        if delta >= 4.0:
            trend = TrendDirection.IMPROVING
        elif delta <= -4.0:
            trend = TrendDirection.DECLINING
        else:
            trend = TrendDirection.STABLE

        # 5. Gap Calculation
        target = data.target_mastery if data.target_mastery > 0 else self.default_target_mastery
        raw_gap = target - mastery
        gap = round(max(0.0, raw_gap), 1)
        is_knowledge_gap = gap > 0.0

        # 6. Estimated Learning Hours
        # Proportional to gap size, adjusted by difficulty and confidence
        diff_factor = self.DIFFICULTY_FACTORS.get(data.difficulty, 0.14)
        if gap == 0.0:
            est_hours = 0.0
        else:
            # Base hours = gap * difficulty factor
            # Lower confidence requires more reinforcement effort (1.3x), high confidence is faster (0.9x)
            confidence_multiplier = 1.3 - (0.4 * confidence)
            est_hours = round(max(1.0, gap * diff_factor * confidence_multiplier), 1)

        # 7. Deterministic Priority Calculation
        priority, reason = self._compute_priority(
            topic=data.topic,
            mastery=mastery,
            target=target,
            gap=gap,
            trend=trend,
            importance=data.importance,
            days_until_deadline=days_until_deadline,
            dependent_topics_count=dependent_topics_count,
            estimated_hours=est_hours,
        )

        return TopicPerformanceResult(
            topic=data.topic,
            mastery=mastery,
            confidence=confidence,
            trend=trend,
            target=target,
            gap=gap,
            priority=priority,
            estimated_learning_hours=est_hours,
            is_knowledge_gap=is_knowledge_gap,
            reason=reason,
        )

    def analyze_curriculum(
        self,
        topics_data: List[TopicPerformanceInput],
        days_until_deadline: int = 45,
    ) -> Dict[str, Any]:
        """
        Analyze an entire syllabus/curriculum, calculate metrics for every topic,
        and automatically extract prioritized knowledge gaps.
        """
        # Count downstream dependencies (how many topics list topic T as a prerequisite)
        dep_counts: Dict[str, int] = {t.topic: 0 for t in topics_data}
        for t in topics_data:
            prereqs = t.prerequisites or self.prerequisite_graph.get(t.topic, [])
            for prereq in prereqs:
                if prereq in dep_counts:
                    dep_counts[prereq] += 1

        topic_results: Dict[str, TopicPerformanceResult] = {}
        knowledge_gaps: List[KnowledgeGapResult] = []

        for data in topics_data:
            downstream = dep_counts.get(data.topic, 0)
            res = self.calculate_topic(
                data=data,
                days_until_deadline=days_until_deadline,
                dependent_topics_count=downstream,
            )
            topic_results[data.topic] = res

            if res.is_knowledge_gap:
                knowledge_gaps.append(
                    KnowledgeGapResult(
                        id=f"gap-{data.topic.lower().replace(' ', '-')}",
                        topic=data.topic,
                        gap_score=res.gap,
                        priority=res.priority,
                        mastery=res.mastery,
                        target=res.target,
                        confidence=res.confidence,
                        trend=res.trend,
                        estimated_hours=res.estimated_learning_hours,
                        reason=res.reason,
                        recommended_action=(
                            f"Allocate {res.estimated_learning_hours} hrs of structured practice "
                            f"and concept drills to close the {res.gap}% gap in {data.topic}."
                        ),
                    )
                )

        # Sort gaps by priority: HIGH -> MEDIUM -> LOW, then largest gap
        priority_rank = {PriorityLevel.HIGH: 0, PriorityLevel.MEDIUM: 1, PriorityLevel.LOW: 2}
        knowledge_gaps.sort(
            key=lambda g: (priority_rank.get(g.priority, 3), -g.gap_score)
        )

        overall_mastery = (
            round(sum(r.mastery for r in topic_results.values()) / len(topic_results), 1)
            if topic_results
            else 0.0
        )

        return {
            "overall_mastery": overall_mastery,
            "topics": topic_results,
            "knowledge_gaps": knowledge_gaps,
            "total_gap_count": len(knowledge_gaps),
            "high_priority_count": sum(1 for g in knowledge_gaps if g.priority == PriorityLevel.HIGH),
            "total_estimated_remediation_hours": round(
                sum(g.estimated_hours for g in knowledge_gaps), 1
            ),
        }

    def _compute_priority(
        self,
        topic: str,
        mastery: float,
        target: float,
        gap: float,
        trend: TrendDirection,
        importance: float,
        days_until_deadline: int,
        dependent_topics_count: int,
        estimated_hours: float,
    ) -> tuple[PriorityLevel, str]:
        """
        Multi-factor deterministic priority scoring function.

        Factors:
        1. Size of knowledge gap (gap / 100)
        2. Topic importance multiplier (1.0 to 2.0)
        3. Deadline proximity urgency (shorter deadline = higher urgency)
        4. Recent performance trend (declining gives penalty boost)
        5. Prerequisite dependency blocking (blocks downstream topics)
        6. Estimated effort feasibility
        """
        if gap == 0.0:
            return (
                PriorityLevel.LOW,
                f"Mastery ({mastery}%) meets or exceeds target ({target}%). Gap is 0.",
            )

        # 1. Gap size component (0.0 to 1.0)
        score_gap = min(1.0, gap / 80.0)

        # 2. Importance component (0.0 to 1.0)
        score_importance = min(1.0, (importance - 1.0) / 1.0) if importance > 1.0 else 0.5

        # 3. Deadline urgency (0.0 to 1.0)
        if days_until_deadline <= 14:
            score_deadline = 1.0
        elif days_until_deadline <= 30:
            score_deadline = 0.8
        elif days_until_deadline <= 60:
            score_deadline = 0.6
        else:
            score_deadline = 0.3

        # 4. Trend urgency
        if trend == TrendDirection.DECLINING:
            score_trend = 1.0
        elif trend == TrendDirection.STABLE:
            score_trend = 0.5
        else:
            score_trend = 0.2

        # 5. Prerequisite dependency blocking
        # If this topic blocks 2 or more downstream topics, it is high urgency
        score_dep = min(1.0, dependent_topics_count * 0.4)

        # Composite Deterministic Index
        # Weights: Gap (0.40), Importance (0.20), Dependency Blocking (0.15), Deadline (0.15), Trend (0.10)
        composite = (
            (0.40 * score_gap)
            + (0.20 * score_importance)
            + (0.15 * score_dep)
            + (0.15 * score_deadline)
            + (0.10 * score_trend)
        )

        # Deterministic Rules:
        # 1. Large knowledge gap (gap >= 35.0) -> HIGH
        # 2. Critical prerequisite bottleneck (blocks >= 2 topics with gap >= 20) -> HIGH
        # 3. Imminent deadline (<= 14 days with gap >= 20) -> HIGH
        # 4. Composite urgency >= 0.50 with gap >= 25 -> HIGH
        # 5. Moderate gap (gap >= 12.0 or composite >= 0.30) -> MEDIUM
        # 6. Minor gap -> LOW
        is_large_gap = gap >= 35.0
        is_dependency_bottleneck = (dependent_topics_count >= 2 and gap >= 20.0)
        is_imminent_deadline = (days_until_deadline <= 14 and gap >= 20.0)
        is_high_composite = (composite >= 0.50 and gap >= 25.0)

        if is_large_gap or is_dependency_bottleneck or is_imminent_deadline or is_high_composite:
            priority = PriorityLevel.HIGH
            reason_parts = [f"Significant knowledge gap ({gap}%) below target {target}%"]
            if dependent_topics_count > 0:
                reason_parts.append(f"blocks {dependent_topics_count} dependent topic(s)")
            if days_until_deadline <= 14:
                reason_parts.append(f"deadline is imminent ({days_until_deadline} days remaining)")
            if trend == TrendDirection.DECLINING:
                reason_parts.append("scores show declining trend")
            reason = f"{'; '.join(reason_parts)}. Estimated remediation: {estimated_hours}h."
        elif gap >= 12.0 or composite >= 0.30:
            priority = PriorityLevel.MEDIUM
            reason = (
                f"Moderate knowledge gap ({gap}%). Mastery is {mastery}%, "
                f"requiring approximately {estimated_hours}h to reach target {target}%."
            )
        else:
            priority = PriorityLevel.LOW
            reason = (
                f"Minor gap ({gap}%). Topic is near target threshold ({target}%). "
                f"Requires {estimated_hours}h reinforcement."
            )

        return priority, reason

    def _weighted_recent_average(self, values: List[float]) -> float:
        """Weight later elements exponentially higher to reflect recent performance."""
        if not values:
            return 0.0
        n = len(values)
        if n == 1:
            return values[0]
        # Linear ramp weights: 1, 2, ..., n
        weights = [i + 1 for i in range(n)]
        return sum(v * w for v, w in zip(values, weights)) / sum(weights)

"""
LearnMate Learning Resource Recommendation Engine.

Receives:
- student level (Beginner, Intermediate, Advanced)
- learning goal (e.g. Master Data Structures & Algorithms)
- knowledge gaps (detected deficits per topic)
- topic mastery (quantitative score per topic)
- preferred resource types (Video, Article, PDF, Quiz, Coding Practice, Interactive Visualization)
- previous resource effectiveness (historical efficacy metrics)

Retrieves candidate resources from the mock resource database and scores each resource deterministically on:
1. Topic relevance (0.30)
2. Difficulty fit relative to student level & mastery (0.20)
3. Duration appropriateness for cognitive retention (0.10)
4. Quality score & benchmark rating (0.15)
5. Student resource type preference (0.15)
6. Previous historical effectiveness (0.10)

Returns top-ranked recommendations per knowledge gap without placing business logic in React.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set
from enum import Enum
from app.mock.data import get_recommended_resources


class SupportedResourceType(str, Enum):
    VIDEO = "Video"
    ARTICLE = "Article"
    PDF = "PDF"
    QUIZ = "Quiz"
    CODING_PRACTICE = "Coding Practice"
    INTERACTIVE_VISUALIZATION = "Interactive Visualization"

    @classmethod
    def normalize(cls, val: str) -> str:
        """Normalize varied casing and shorthand names."""
        v = val.strip().lower()
        mapping = {
            "video": cls.VIDEO.value,
            "article": cls.ARTICLE.value,
            "pdf": cls.PDF.value,
            "quiz": cls.QUIZ.value,
            "practice": cls.CODING_PRACTICE.value,
            "coding practice": cls.CODING_PRACTICE.value,
            "coding_practice": cls.CODING_PRACTICE.value,
            "tool": cls.INTERACTIVE_VISUALIZATION.value,
            "interactive visualization": cls.INTERACTIVE_VISUALIZATION.value,
            "interactive_visualization": cls.INTERACTIVE_VISUALIZATION.value,
            "visualization": cls.INTERACTIVE_VISUALIZATION.value,
        }
        return mapping.get(v, val)


@dataclass
class RecommendationRequest:
    """Input telemetry for resource recommendation."""
    student_level: str = "Intermediate"  # Beginner, Intermediate, Advanced
    learning_goal: str = "Master Data Structures & Algorithms"
    knowledge_gaps: List[Dict[str, Any]] = field(default_factory=list)
    topic_mastery: Dict[str, float] = field(default_factory=dict)
    preferred_resource_types: List[str] = field(
        default_factory=lambda: ["Video", "Coding Practice", "Interactive Visualization"]
    )
    previous_resource_effectiveness: Dict[str, float] = field(default_factory=dict)
    limit_per_gap: int = 3


@dataclass
class ScoreBreakdown:
    """Quantitative scoring component breakdown."""
    topic_relevance: float
    difficulty_fit: float
    duration_appropriateness: float
    quality: float
    student_preference: float
    previous_effectiveness: float
    final_score: float


@dataclass
class ScoredResource:
    """A scored and ranked candidate learning resource."""
    id: str
    title: str
    type: str
    topic: str
    difficulty: str
    duration_minutes: int
    quality_score: float
    url: Optional[str]
    source: str
    match_score: float
    match_label: str
    score_breakdown: ScoreBreakdown
    why_recommended: str
    target_gap_topic: str


@dataclass
class GapRecommendationResult:
    """Curated recommendations grouped by knowledge gap."""
    gap_topic: str
    gap_score: float
    priority: str
    student_mastery: float
    recommended_resources: List[ScoredResource]


class ResourceRecommendationService:
    """
    Deterministic recommendation service matching candidate study materials
    to detected knowledge gaps based on multidimensional ranking criteria.
    """

    # Weights sum strictly to 1.00
    WEIGHT_TOPIC_RELEVANCE = 0.30
    WEIGHT_DIFFICULTY_FIT = 0.20
    WEIGHT_QUALITY = 0.15
    WEIGHT_STUDENT_PREFERENCE = 0.15
    WEIGHT_PREVIOUS_EFFECTIVENESS = 0.10
    WEIGHT_DURATION = 0.10

    def __init__(self, resource_pool: Optional[List[Dict[str, Any]]] = None):
        self._resource_pool = (
            resource_pool if resource_pool is not None else get_recommended_resources()
        )

    def get_candidate_resources(self) -> List[Dict[str, Any]]:
        """Return the raw pool of candidate learning resources."""
        return self._resource_pool

    def score_resource(
        self,
        resource: Dict[str, Any],
        gap_topic: str,
        student_mastery: float,
        student_level: str,
        preferred_types: List[str],
        previous_effectiveness: Dict[str, float],
    ) -> tuple[float, ScoreBreakdown, str]:
        """
        Score a single candidate resource against a specific knowledge gap.

        Returns:
            tuple of (final_score, ScoreBreakdown, why_recommended)
        """
        res_topic = resource.get("topic", "")
        res_type = SupportedResourceType.normalize(resource.get("type", "Video"))
        res_diff = resource.get("difficulty", "Intermediate").capitalize()
        res_dur = resource.get("duration_minutes", 30)
        res_qual = float(resource.get("quality_score", 90.0))
        res_id = resource.get("id", "")

        # 1. Topic Relevance (0 - 100)
        if res_topic.lower() == gap_topic.lower():
            score_topic = 100.0
        elif res_topic.lower() in gap_topic.lower() or gap_topic.lower() in res_topic.lower():
            score_topic = 80.0
        else:
            # Not relevant to this gap
            score_topic = 0.0

        # 2. Difficulty Fit (0 - 100)
        # Low mastery (<40) benefits most from Beginner concepts
        # Mid mastery (40-70) benefits most from Intermediate
        # High mastery (>70) benefits from Advanced
        if student_mastery < 40.0:
            if res_diff == "Beginner":
                score_diff = 100.0
            elif res_diff == "Intermediate":
                score_diff = 75.0
            else:
                score_diff = 40.0
        elif student_mastery <= 70.0:
            if res_diff == "Intermediate":
                score_diff = 100.0
            elif res_diff == "Beginner":
                score_diff = 80.0
            else:
                score_diff = 70.0
        else:
            if res_diff == "Advanced":
                score_diff = 100.0
            elif res_diff == "Intermediate":
                score_diff = 85.0
            else:
                score_diff = 45.0

        # 3. Duration Appropriateness (0 - 100)
        # Optimal study chunks are 20 to 60 minutes
        if 20 <= res_dur <= 60:
            score_dur = 100.0
        elif 10 <= res_dur < 20:
            score_dur = 85.0
        elif 60 < res_dur <= 90:
            score_dur = 75.0
        else:
            score_dur = 60.0

        # 4. Quality Benchmark (0 - 100)
        score_qual = max(0.0, min(100.0, res_qual))

        # 5. Student Preference (0 - 100)
        norm_preferred = [SupportedResourceType.normalize(p).lower() for p in preferred_types]
        if norm_preferred and res_type.lower() == norm_preferred[0]:
            score_pref = 100.0  # #1 choice
        elif res_type.lower() in norm_preferred:
            score_pref = 90.0   # in preferred list
        else:
            score_pref = 50.0   # fallback format

        # 6. Previous Effectiveness (0 - 100)
        # Check specific resource ID first, then resource type
        eff_val = previous_effectiveness.get(res_id)
        if eff_val is None:
            eff_val = previous_effectiveness.get(res_type)
        if eff_val is None:
            eff_val = previous_effectiveness.get(res_type.lower())

        if eff_val is not None:
            # Scale 0.0-1.0 to 0-100
            score_eff = max(0.0, min(100.0, eff_val * 100.0 if eff_val <= 1.0 else eff_val))
        else:
            score_eff = 75.0  # Neutral baseline if unobserved

        # Weighted Sum
        final_score = (
            (self.WEIGHT_TOPIC_RELEVANCE * score_topic)
            + (self.WEIGHT_DIFFICULTY_FIT * score_diff)
            + (self.WEIGHT_QUALITY * score_qual)
            + (self.WEIGHT_STUDENT_PREFERENCE * score_pref)
            + (self.WEIGHT_PREVIOUS_EFFECTIVENESS * score_eff)
            + (self.WEIGHT_DURATION * score_dur)
        )
        final_score = round(final_score, 1)

        breakdown = ScoreBreakdown(
            topic_relevance=score_topic,
            difficulty_fit=score_diff,
            duration_appropriateness=score_dur,
            quality=score_qual,
            student_preference=score_pref,
            previous_effectiveness=score_eff,
            final_score=final_score,
        )

        # Generate deterministic justification
        reasons = []
        if score_topic == 100.0:
            reasons.append(f"Direct coverage of {gap_topic}")
        if score_pref >= 90.0:
            reasons.append(f"matches preferred format ({res_type})")
        if score_diff >= 90.0:
            reasons.append(f"{res_diff} difficulty matches your {student_mastery}% mastery level")
        if score_qual >= 92.0:
            reasons.append(f"high quality rating ({int(res_qual)}/100)")
        if score_eff >= 85.0:
            reasons.append("high historical effectiveness for your learning style")

        why_recommended = (
            f"Recommended because it provides {'; '.join(reasons)}."
            if reasons
            else f"Relevant study material for {gap_topic}."
        )

        return final_score, breakdown, why_recommended

    def recommend_for_gap(
        self,
        gap_topic: str,
        student_mastery: float = 30.0,
        gap_score: float = 50.0,
        priority: str = "High",
        student_level: str = "Intermediate",
        preferred_types: Optional[List[str]] = None,
        previous_effectiveness: Optional[Dict[str, float]] = None,
        limit: int = 3,
    ) -> GapRecommendationResult:
        """
        Retrieve and rank the best candidate resources for a specific knowledge gap.
        """
        pref = preferred_types or ["Video", "Coding Practice", "Interactive Visualization"]
        eff = previous_effectiveness or {}

        scored_list: List[ScoredResource] = []

        for candidate in self._resource_pool:
            score, breakdown, why = self.score_resource(
                resource=candidate,
                gap_topic=gap_topic,
                student_mastery=student_mastery,
                student_level=student_level,
                preferred_types=pref,
                previous_effectiveness=eff,
            )

            # Filter out completely irrelevant materials
            if breakdown.topic_relevance > 0:
                if score >= 90.0:
                    label = "Top Match"
                elif score >= 80.0:
                    label = "Highly Recommended"
                elif score >= 70.0:
                    label = "Recommended"
                else:
                    label = "Supplementary"

                scored_list.append(
                    ScoredResource(
                        id=candidate.get("id", ""),
                        title=candidate.get("title", ""),
                        type=SupportedResourceType.normalize(candidate.get("type", "Video")),
                        topic=candidate.get("topic", gap_topic),
                        difficulty=candidate.get("difficulty", "Intermediate"),
                        duration_minutes=candidate.get("duration_minutes", 30),
                        quality_score=float(candidate.get("quality_score", 90)),
                        url=candidate.get("url"),
                        source=candidate.get("source", ""),
                        match_score=score,
                        match_label=label,
                        score_breakdown=breakdown,
                        why_recommended=why,
                        target_gap_topic=gap_topic,
                    )
                )

        # Sort descending by match_score
        scored_list.sort(key=lambda r: -r.match_score)
        best_resources = scored_list[:limit]

        return GapRecommendationResult(
            gap_topic=gap_topic,
            gap_score=gap_score,
            priority=priority,
            student_mastery=student_mastery,
            recommended_resources=best_resources,
        )

    def recommend_for_all_gaps(
        self,
        request: RecommendationRequest,
    ) -> List[GapRecommendationResult]:
        """
        Given student context and a collection of knowledge gaps, return
        the highest-scoring recommendations for each gap.
        """
        results: List[GapRecommendationResult] = []

        gaps = request.knowledge_gaps
        if not gaps:
            # Fallback to topics in topic_mastery with gap below 80
            for topic, mastery in request.topic_mastery.items():
                if mastery < 80.0:
                    gaps.append({
                        "topic": topic,
                        "gap_score": round(80.0 - mastery, 1),
                        "priority": "High" if (80.0 - mastery) >= 35.0 else "Medium",
                        "mastery": mastery,
                    })

        for gap in gaps:
            gap_topic = gap.get("topic", "")
            if not gap_topic:
                continue

            mastery = float(
                gap.get("mastery", request.topic_mastery.get(gap_topic, 30.0))
            )
            gap_score = float(gap.get("gap_score", max(0.0, 80.0 - mastery)))
            priority = gap.get("priority", "High")

            gap_res = self.recommend_for_gap(
                gap_topic=gap_topic,
                student_mastery=mastery,
                gap_score=gap_score,
                priority=priority,
                student_level=request.student_level,
                preferred_types=request.preferred_resource_types,
                previous_effectiveness=request.previous_resource_effectiveness,
                limit=request.limit_per_gap,
            )
            results.append(gap_res)

        return results

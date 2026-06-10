"""Generated innovation report models."""

from dataclasses import dataclass, field
from datetime import datetime

from backend.models.evidence import Evidence
from backend.models.problem import Problem, ProblemAnalysis


@dataclass(frozen=True)
class Recommendation:
    """A prioritized, evidence-backed government action."""

    title: str
    category: str
    rationale: str
    action_steps: tuple[str, ...]
    confidence: float
    impact_score: int
    innovation_score: int
    estimated_cost: str
    timeframe: str
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class InnovationReport:
    """Structured result returned to the user interface."""

    report_id: str
    created_at: str
    problem: Problem
    title: str
    summary: str
    analysis: ProblemAnalysis
    recommendations: tuple[Recommendation, ...] = field(default_factory=tuple)
    evidence: tuple[Evidence, ...] = field(default_factory=tuple)
    policy_recommendations: tuple[str, ...] = field(default_factory=tuple)
    dataset_version: str = "hackathon-v1"

    @classmethod
    def timestamp(cls) -> str:
        """Return a portable UTC timestamp."""
        return datetime.now().astimezone().isoformat(timespec="seconds")

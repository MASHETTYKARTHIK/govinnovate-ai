"""Generated innovation report models."""

from dataclasses import dataclass, field

from backend.models.evidence import Evidence
from backend.models.problem import ProblemAnalysis


@dataclass(frozen=True)
class Recommendation:
    """A prioritized action backed by available evidence."""

    title: str
    rationale: str
    confidence: float


@dataclass(frozen=True)
class InnovationReport:
    """Structured result returned to the user interface."""

    title: str
    summary: str
    analysis: ProblemAnalysis
    recommendations: tuple[Recommendation, ...] = field(default_factory=tuple)
    evidence: tuple[Evidence, ...] = field(default_factory=tuple)
    dataset_version: str = "poc-v0"

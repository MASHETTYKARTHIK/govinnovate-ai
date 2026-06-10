"""Problem input and analysis models."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Problem:
    """A public-sector challenge submitted for analysis."""

    text: str
    location: str = ""
    sector: str = "Other"
    budget: str = "Not specified"
    timeframe: str = "6-12 months"
    target_population: str = ""


@dataclass(frozen=True)
class ProblemAnalysis:
    """Normalized representation produced by the problem analyzer."""

    title: str
    summary: str
    keywords: tuple[str, ...] = field(default_factory=tuple)
    challenges: tuple[str, ...] = field(default_factory=tuple)
    objectives: tuple[str, ...] = field(default_factory=tuple)
    readiness_score: int = 0
    urgency_score: int = 0

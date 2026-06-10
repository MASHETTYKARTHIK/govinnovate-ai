"""Problem input and analysis models."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Problem:
    """A public-sector challenge submitted for analysis."""

    text: str
    location: str = ""
    sector: str = "Other"


@dataclass(frozen=True)
class ProblemAnalysis:
    """Normalized representation produced by the problem analyzer."""

    title: str
    summary: str
    keywords: tuple[str, ...] = field(default_factory=tuple)

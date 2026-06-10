"""Evidence model used by retrieval and reporting."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    """A retrieved evidence item with provenance."""

    title: str
    summary: str
    source: str
    relevance: float

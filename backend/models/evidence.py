"""Evidence models used by retrieval and reporting."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Evidence:
    """A retrieved local dataset record with provenance and metadata."""

    id: str
    category: str
    title: str
    summary: str
    source: str
    relevance: float
    location: str = "Global"
    tags: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str | int | float] = field(default_factory=dict)

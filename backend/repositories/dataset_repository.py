"""Local JSON dataset repository for the POC."""

import json
from pathlib import Path

from backend.config import settings
from backend.models.evidence import Evidence


class DatasetRepository:
    """Read and search curated evidence records from local JSON files."""

    def __init__(self, dataset_path: Path | None = None) -> None:
        self.dataset_path = dataset_path or settings.dataset_path

    def search(self, keywords: tuple[str, ...], limit: int = 5) -> tuple[Evidence, ...]:
        """Rank records by simple keyword overlap."""
        ranked: list[Evidence] = []
        for path in self.dataset_path.glob("*.json"):
            records = json.loads(path.read_text(encoding="utf-8"))
            for record in records:
                searchable = f"{record['title']} {record['summary']}".lower()
                matches = sum(keyword in searchable for keyword in keywords)
                if matches:
                    ranked.append(
                        Evidence(
                            title=record["title"],
                            summary=record["summary"],
                            source=record["source"],
                            relevance=min(0.5 + matches * 0.1, 0.95),
                        )
                    )
        return tuple(sorted(ranked, key=lambda item: item.relevance, reverse=True)[:limit])

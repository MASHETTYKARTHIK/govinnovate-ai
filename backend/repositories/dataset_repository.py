"""Local JSON dataset repository with FAISS-style mock retrieval."""

import json

from backend.config import settings
from backend.models.evidence import Evidence
from backend.repositories.vector_index import MockFaissIndex


class DatasetRepository:
    """Load and search all curated local JSON datasets."""

    def __init__(self, dataset_path=None) -> None:
        # Cast for Python 3.9 compatibility; the caller can omit this argument.
        dataset_path = dataset_path

        # NOTE: Python 3.9 doesn't support the `Path | None` (PEP604) syntax.
        self.dataset_path = dataset_path or settings.dataset_path
        self._records = self._load_records()
        documents = [
            " ".join(
                [
                    str(record.get("title", "")),
                    str(record.get("summary", "")),
                    " ".join(record.get("tags", [])),
                    str(record.get("sector", "")),
                ]
            )
            for record in self._records
        ]
        self.index = MockFaissIndex(documents)

    def _load_records(self) -> list[dict]:
        records: list[dict] = []
        paths = sorted(self.dataset_path.glob("*.json"))
        paths += sorted((self.dataset_path / "curated").glob("*.json"))
        for path in paths:
            payload = json.loads(path.read_text(encoding="utf-8"))
            category = path.stem.replace("_", " ").title()
            for item in payload:
                item.setdefault("category", category)
                records.append(item)
        return records

    def search(self, query: str, limit: int = 12) -> tuple[Evidence, ...]:
        """Rank local records using semantic-style cosine similarity."""
        matches = self.index.search(query, limit=limit)
        results: list[Evidence] = []
        for index, score in matches:
            if score <= 0:
                continue
            record = self._records[index]
            metadata = {
                key: value
                for key, value in record.items()
                if key
                not in {
                    "id",
                    "category",
                    "title",
                    "summary",
                    "source",
                    "location",
                    "tags",
                }
            }
            results.append(
                Evidence(
                    id=str(record["id"]),
                    category=str(record["category"]),
                    title=str(record["title"]),
                    summary=str(record["summary"]),
                    source=str(record["source"]),
                    relevance=min(round(0.55 + score * 0.45, 3), 0.99),
                    location=str(record.get("location", "Global")),
                    tags=tuple(record.get("tags", [])),
                    metadata=metadata,
                )
            )
        return tuple(results)

    def counts(self) -> dict[str, int]:
        """Return record counts grouped by category."""
        counts: dict[str, int] = {}
        for record in self._records:
            category = str(record["category"])
            counts[category] = counts.get(category, 0) + 1
        return counts


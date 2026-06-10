"""Evidence retrieval coordinator."""

from backend.models.evidence import Evidence
from backend.models.problem import Problem, ProblemAnalysis
from backend.repositories.dataset_repository import DatasetRepository


class RetrievalCoordinator:
    """Coordinate mock-vector retrieval against local datasets."""

    def __init__(self, repository: DatasetRepository | None = None) -> None:
        self.repository = repository or DatasetRepository()

    def retrieve(
        self, problem: Problem, analysis: ProblemAnalysis, limit: int = 16
    ) -> tuple[Evidence, ...]:
        """Return evidence matching problem text and structured context."""
        query = " ".join(
            [
                problem.text,
                problem.sector,
                problem.location,
                " ".join(analysis.keywords),
            ]
        )
        return self.repository.search(query, limit=limit)

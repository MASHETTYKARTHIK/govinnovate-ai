"""Evidence retrieval coordinator placeholder."""

from backend.models.evidence import Evidence
from backend.models.problem import ProblemAnalysis
from backend.repositories.dataset_repository import DatasetRepository


class RetrievalCoordinator:
    """Coordinate retrieval and ranking against the local POC dataset."""

    def __init__(self, repository: DatasetRepository | None = None) -> None:
        self.repository = repository or DatasetRepository()

    def retrieve(self, analysis: ProblemAnalysis, limit: int = 5) -> tuple[Evidence, ...]:
        """Return the most relevant local evidence records."""
        return self.repository.search(analysis.keywords, limit=limit)

"""Integration tests for the complete local workflow."""

from pathlib import Path

from backend.agents.retrieval_coordinator import RetrievalCoordinator
from backend.models.problem import Problem
from backend.repositories.dataset_repository import DatasetRepository
from backend.repositories.report_repository import ReportRepository
from backend.services.orchestrator import AnalysisOrchestrator
from backend.services.report_service import generate_markdown


def test_orchestrator_generates_persists_and_exports_report(tmp_path: Path) -> None:
    dataset_repository = DatasetRepository(Path("datasets"))
    report_repository = ReportRepository(tmp_path / "reports.db")
    orchestrator = AnalysisOrchestrator(
        RetrievalCoordinator(dataset_repository),
        report_repository,
    )

    report = orchestrator.run(
        Problem(
            "Reduce traffic congestion with better bus reliability and traffic signals.",
            "Hyderabad",
            "Transport",
            "INR 50 lakh-2 crore",
            "6-12 months",
        )
    )
    markdown = generate_markdown(report)

    assert report.recommendations
    assert any(item.category == "Startups" for item in report.evidence)
    assert report_repository.history()[0]["report_id"] == report.report_id
    assert report.title in markdown
    assert "## Evidence Register" in markdown

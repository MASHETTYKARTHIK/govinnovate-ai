"""Smoke test for the POC workflow."""

from pathlib import Path

from backend.agents.retrieval_coordinator import RetrievalCoordinator
from backend.models.problem import Problem
from backend.repositories.dataset_repository import DatasetRepository
from backend.services.orchestrator import AnalysisOrchestrator


def test_orchestrator_generates_grounded_report() -> None:
    orchestrator = AnalysisOrchestrator()
    orchestrator.retrieval_coordinator = RetrievalCoordinator(
        DatasetRepository(Path("datasets/curated"))
    )

    report = orchestrator.run(Problem("Reduce traffic congestion.", "Hyderabad", "Transport"))

    assert report.recommendations
    assert report.evidence

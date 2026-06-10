"""Sequential analysis workflow for the local MVP."""

from backend.agents.problem_analyzer import ProblemAnalyzer
from backend.agents.report_generator import ReportGenerator
from backend.agents.retrieval_coordinator import RetrievalCoordinator
from backend.models.problem import Problem
from backend.models.report import InnovationReport
from backend.repositories.report_repository import ReportRepository


class AnalysisOrchestrator:
    """Run the three mock AI agents and persist the resulting report."""

    def __init__(
        self,
        retrieval_coordinator: RetrievalCoordinator | None = None,
        report_repository: ReportRepository | None = None,
    ) -> None:
        self.problem_analyzer = ProblemAnalyzer()
        self.retrieval_coordinator = retrieval_coordinator or RetrievalCoordinator()
        self.report_generator = ReportGenerator()
        self.report_repository = report_repository or ReportRepository()

    def run(self, problem: Problem) -> InnovationReport:
        """Analyze, retrieve evidence, generate, and persist a report."""
        analysis = self.problem_analyzer.analyze(problem)
        evidence = self.retrieval_coordinator.retrieve(problem, analysis)
        report = self.report_generator.generate(problem, analysis, evidence)
        self.report_repository.save(report)
        return report

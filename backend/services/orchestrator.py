"""Sequential analysis workflow for the POC."""

from backend.agents.problem_analyzer import ProblemAnalyzer
from backend.agents.report_generator import ReportGenerator
from backend.agents.retrieval_coordinator import RetrievalCoordinator
from backend.models.problem import Problem
from backend.models.report import InnovationReport


class AnalysisOrchestrator:
    """Run the POC agents in a clear sequential workflow."""

    def __init__(self) -> None:
        self.problem_analyzer = ProblemAnalyzer()
        self.retrieval_coordinator = RetrievalCoordinator()
        self.report_generator = ReportGenerator()

    def run(self, problem: Problem) -> InnovationReport:
        """Analyze, retrieve evidence, and generate a report."""
        analysis = self.problem_analyzer.analyze(problem)
        evidence = self.retrieval_coordinator.retrieve(analysis)
        return self.report_generator.generate(analysis, evidence)

"""Tests for deterministic problem analysis."""

from backend.agents.problem_analyzer import ProblemAnalyzer
from backend.models.problem import Problem


def test_problem_analyzer_extracts_context() -> None:
    problem = Problem("Reduce traffic congestion during peak hours.", "Hyderabad", "Transport")

    analysis = ProblemAnalyzer().analyze(problem)

    assert analysis.title == "Transport innovation challenge in Hyderabad"
    assert "traffic" in analysis.keywords

"""Tests for mock AI problem analysis."""

from backend.agents.problem_analyzer import ProblemAnalyzer
from backend.models.problem import Problem


def test_problem_analyzer_extracts_context_and_scores() -> None:
    problem = Problem(
        "Reduce traffic congestion and improve bus reliability during peak hours.",
        "Hyderabad",
        "Transport",
        "INR 10-50 lakh",
        "6-12 months",
    )

    analysis = ProblemAnalyzer().analyze(problem)

    assert analysis.title == "Transport innovation strategy for Hyderabad"
    assert "traffic" in analysis.keywords
    assert analysis.readiness_score > 50
    assert len(analysis.objectives) == 3

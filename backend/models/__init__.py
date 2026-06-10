"""Domain models shared across the backend."""

from backend.models.evidence import Evidence
from backend.models.problem import Problem, ProblemAnalysis
from backend.models.report import InnovationReport, Recommendation

__all__ = [
    "Evidence",
    "InnovationReport",
    "Problem",
    "ProblemAnalysis",
    "Recommendation",
]

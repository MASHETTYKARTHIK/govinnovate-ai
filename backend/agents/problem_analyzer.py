"""Problem analysis agent placeholder."""

import re

from backend.models.problem import Problem, ProblemAnalysis


class ProblemAnalyzer:
    """Normalize a submitted problem into a retrieval-ready representation."""

    def analyze(self, problem: Problem) -> ProblemAnalysis:
        """Create a deterministic placeholder analysis."""
        words = re.findall(r"[A-Za-z]{4,}", problem.text.lower())
        keywords = tuple(dict.fromkeys(words))[:8]
        title = f"{problem.sector} innovation challenge"
        if problem.location:
            title += f" in {problem.location}"
        return ProblemAnalysis(title=title, summary=problem.text, keywords=keywords)

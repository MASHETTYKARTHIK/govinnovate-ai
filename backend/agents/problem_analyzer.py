"""Deterministic mock AI problem analysis agent."""

import re

from backend.models.problem import Problem, ProblemAnalysis


class ProblemAnalyzer:
    """Normalize user input and simulate transparent AI reasoning."""

    STOP_WORDS = {
        "about", "after", "again", "also", "because", "could", "from", "have",
        "into", "more", "need", "problem", "public", "should", "that", "their",
        "there", "these", "this", "through", "using", "want", "with", "would",
    }

    def analyze(self, problem: Problem) -> ProblemAnalysis:
        """Create a dynamic analysis from the submitted context."""
        words = re.findall(r"[A-Za-z]{4,}", problem.text.lower())
        keywords = tuple(dict.fromkeys(word for word in words if word not in self.STOP_WORDS))[:10]
        location = problem.location or "the target region"
        title = f"{problem.sector} innovation strategy for {location}"
        challenges = (
            f"Fragmented delivery and evidence around {keywords[0] if keywords else problem.sector.lower()}",
            f"Need to demonstrate measurable outcomes within {problem.timeframe}",
            f"Stakeholder coordination and adoption risk in {location}",
        )
        objectives = (
            "Launch a measurable pilot using proven implementation patterns",
            "Build an evidence-backed procurement and policy pathway",
            "Track citizen outcomes, delivery cost, and operational learning",
        )
        detail_score = min(len(problem.text) // 8, 35)
        readiness = min(45 + detail_score + (10 if problem.budget != "Not specified" else 0), 92)
        urgency = min(55 + sum(word in problem.text.lower() for word in ("urgent", "critical", "crisis")) * 10, 90)
        return ProblemAnalysis(
            title=title,
            summary=(
                f"{location} can address this {problem.sector.lower()} challenge through a focused "
                "pilot that combines proven technology, policy support, and measurable outcomes."
            ),
            keywords=keywords,
            challenges=challenges,
            objectives=objectives,
            readiness_score=readiness,
            urgency_score=urgency,
        )

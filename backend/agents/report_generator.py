"""Evidence-grounded report generator placeholder."""

from backend.config import settings
from backend.models.evidence import Evidence
from backend.models.problem import ProblemAnalysis
from backend.models.report import InnovationReport, Recommendation


class ReportGenerator:
    """Generate a concise, deterministic report until an LLM adapter is added."""

    def generate(
        self,
        analysis: ProblemAnalysis,
        evidence: tuple[Evidence, ...],
    ) -> InnovationReport:
        """Build a structured report using only retrieved evidence."""
        recommendations = tuple(
            Recommendation(
                title=f"Evaluate: {item.title}",
                rationale=item.summary,
                confidence=item.relevance,
            )
            for item in evidence[:3]
        )
        if not recommendations:
            recommendations = (
                Recommendation(
                    title="Curate local evidence",
                    rationale="Add relevant case studies before selecting an intervention.",
                    confidence=0.25,
                ),
            )
        return InnovationReport(
            title=analysis.title,
            summary="A preliminary innovation brief generated from the available POC dataset.",
            analysis=analysis,
            recommendations=recommendations,
            evidence=evidence,
            dataset_version=settings.dataset_version,
        )

"""Evidence-grounded mock AI report generator."""

import hashlib

from backend.config import settings
from backend.models.evidence import Evidence
from backend.models.problem import Problem, ProblemAnalysis
from backend.models.report import InnovationReport, Recommendation


class ReportGenerator:
    """Generate dynamic, explainable recommendations from retrieved records."""

    def generate(
        self,
        problem: Problem,
        analysis: ProblemAnalysis,
        evidence: tuple[Evidence, ...],
    ) -> InnovationReport:
        """Build a structured report using only local evidence."""
        candidates = evidence[:5] or self._fallback_evidence(problem)
        recommendations = tuple(
            self._recommendation(item, index, problem) for index, item in enumerate(candidates[:4])
        )
        policies = self._policy_recommendations(problem, evidence)
        report_hash = hashlib.sha1(
            f"{problem.text}{InnovationReport.timestamp()}".encode("utf-8")
        ).hexdigest()[:8]
        return InnovationReport(
            report_id=f"GIA-{report_hash.upper()}",
            created_at=InnovationReport.timestamp(),
            problem=problem,
            title=analysis.title,
            summary=analysis.summary,
            analysis=analysis,
            recommendations=recommendations,
            evidence=evidence,
            policy_recommendations=policies,
            dataset_version=settings.dataset_version,
        )

    @staticmethod
    def _recommendation(item: Evidence, index: int, problem: Problem) -> Recommendation:
        score = min(round(item.relevance * 100), 96)
        impact = min(score + 5 - index * 2, 96)
        innovation = min(72 + len(item.tags) * 3 + index, 95)
        cost = str(item.metadata.get("estimated_cost", problem.budget))
        timeframe = str(item.metadata.get("timeframe", problem.timeframe))
        return Recommendation(
            title=item.title,
            category=item.category,
            rationale=(
                f"{item.summary} This option aligns with the stated {problem.sector.lower()} "
                f"challenge and has a {score}% local evidence match."
            ),
            action_steps=(
                "Validate the intervention with departments and affected communities.",
                f"Run a bounded {timeframe} pilot with baseline and outcome metrics.",
                "Review evidence after the pilot and prepare a scale-up decision.",
            ),
            confidence=item.relevance,
            impact_score=impact,
            innovation_score=innovation,
            estimated_cost=cost,
            timeframe=timeframe,
            evidence_ids=(item.id,),
        )

    @staticmethod
    def _policy_recommendations(
        problem: Problem, evidence: tuple[Evidence, ...]
    ) -> tuple[str, ...]:
        program_titles = [item.title for item in evidence if "Program" in item.category][:2]
        policies = [
            f"Create a cross-department {problem.sector.lower()} innovation working group.",
            "Use outcome-based pilot procurement with transparent success metrics.",
            "Publish a privacy, inclusion, and data-governance checklist before launch.",
        ]
        if program_titles:
            policies.append(f"Explore alignment with {' and '.join(program_titles)}.")
        return tuple(policies)

    @staticmethod
    def _fallback_evidence(problem: Problem) -> tuple[Evidence, ...]:
        return (
            Evidence(
                id="fallback-1",
                category="Local Discovery",
                title=f"Rapid {problem.sector} innovation pilot",
                summary="Start with a small, measurable pilot while curating stronger local evidence.",
                source="GovInnovate AI fallback framework",
                relevance=0.58,
                tags=("pilot", "measurement"),
                metadata={"estimated_cost": problem.budget, "timeframe": problem.timeframe},
            ),
        )

"""Complete Streamlit MVP entry point for GovInnovate AI."""

import sys
from html import escape
from pathlib import Path

# Streamlit can execute this file with only streamlit_app/ on sys.path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Optional Streamlit: smoke tests must be able to import the module even if
# streamlit isn't installed in the test environment.
try:
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover
    st = None



# Optional heavy dependencies: keep import-time lightweight so unit/integration
# tests can import this module even in minimal environments.

try:
    import pandas as pd

except ModuleNotFoundError:  # pragma: no cover
    pd = None


try:
    import plotly.express as px
except ModuleNotFoundError:  # pragma: no cover
    px = None



from backend.models.report import InnovationReport
from backend.repositories.dataset_repository import DatasetRepository
from backend.repositories.report_repository import ReportRepository
from backend.services.orchestrator import AnalysisOrchestrator
from backend.services.report_service import generate_markdown
from streamlit_app.components.problem_form import render_problem_form
from streamlit_app.components.report_view import evidence_frame, score_chart
from streamlit_app.styles import THEME_CSS

PAGES = (
    "Dashboard",
    "Upload Problem",
    "AI Analysis",
    "Recommendations",
    "Download Report",
)


def initialize() -> None:
    """Configure the application and shared state."""
    st.set_page_config(page_title="GovInnovate AI", page_icon="G", layout="wide")
    st.markdown(THEME_CSS, unsafe_allow_html=True)
    st.session_state.setdefault("page", "Dashboard")
    st.session_state.setdefault("report", None)


def navigate(page: str) -> None:
    """Switch pages and refresh the Streamlit script."""
    st.session_state.page = page
    st.rerun()


def sidebar() -> None:
    """Render professional sidebar navigation."""
    with st.sidebar:
        st.markdown("## GOVINNOVATE AI")
        st.caption("PUBLIC INNOVATION INTELLIGENCE")
        st.markdown("---")
        selected = st.radio(
            "Navigation",
            PAGES,
            index=PAGES.index(st.session_state.page),
            label_visibility="collapsed",
        )
        st.session_state.page = selected
        st.markdown("---")
        report = current_report()
        if report:
            st.success(f"Active brief: {report.report_id}")
            st.caption(report.title)
        else:
            st.info("Create an analysis to unlock the full workspace.")
        st.caption("Local datasets | Mock AI | SQLite")










def current_report() -> 'InnovationReport | None':
    """Return the active report from session state."""

    report = st.session_state.get("report")
    if isinstance(report, InnovationReport) or report is None:
        return report
    # Streamlit session state can contain stale values from earlier runs.
    return None



def hero(eyebrow: str, title: str, description: str) -> None:
    """Render a shared page heading."""
    st.markdown(
        f'<div class="eyebrow">{escape(eyebrow)}</div>'
        f'<div class="hero-title">{escape(title)}</div>'
        f'<p class="muted">{escape(description)}</p>',
        unsafe_allow_html=True,
    )


def render_dashboard() -> None:
    """Render portfolio analytics and recent activity."""
    hero(
        "MISSION CONTROL",
        "Turn public challenges into pilot-ready action.",
        "Explore local evidence, run transparent mock AI analysis, and produce decision-ready briefs.",
    )
    counts = DatasetRepository().counts()
    history = ReportRepository().history()
    cols = st.columns(4)
    cols[0].metric("Evidence records", sum(counts.values()), "Local JSON")
    cols[1].metric("Datasets online", len(counts), "100% local")
    cols[2].metric("Reports generated", len(history), "SQLite tracked")
    average = (
        round(sum(row["impact_score"] for row in history) / len(history))
        if history
        else 0
    )
    cols[3].metric("Average impact", f"{average}/100", "Across reports")

    left, right = st.columns([1.35, 1])
    with left:
        st.markdown("### Evidence landscape")
        frame = pd.DataFrame(
            {"Dataset": list(counts), "Records": list(counts.values())}
        )
        chart = px.bar(frame, x="Dataset", y="Records", color="Dataset")
        chart.update_layout(
            showlegend=False,
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#dbe8f7",
        )
        st.plotly_chart(chart, width="stretch")
    with right:
        st.markdown("### Workflow")
        st.markdown(
            """
            <div class="glass-card">
              <b>01. Define</b><p class="muted">Capture local needs, constraints, budget, and timing.</p>
              <b>02. Discover</b><p class="muted">Rank research, cases, startups, and programs.</p>
              <b>03. Decide</b><p class="muted">Compare impact, innovation, cost, and policy actions.</p>
              <b>04. Deliver</b><p class="muted">Download an auditable Markdown brief.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start a new analysis", type="primary", width="stretch"):
            navigate("Upload Problem")

    st.markdown("### Recent analyses")
    if history:
        st.dataframe(pd.DataFrame(history), width="stretch", hide_index=True)
    else:
        st.caption("No reports yet. Your first analysis will appear here.")


def render_upload() -> None:
    """Render problem intake and execute the workflow."""
    hero(
        "CHALLENGE INTAKE",
        "Describe the public problem.",
        "The stronger the context, the sharper the evidence matching and recommendations.",
    )
    problem = render_problem_form()
    if problem:
        with st.status(
            "GovInnovate AI is building the innovation brief...", expanded=True
        ) as status:
            st.write("Structuring the challenge and extracting decision signals")
            st.write("Searching the local FAISS-style evidence index")
            report = AnalysisOrchestrator().run(problem)
            st.write("Scoring interventions and assembling the report")
            status.update(label="Analysis complete", state="complete")
        st.session_state.report = report
        st.success(f"Created {report.report_id}")
        if st.button("Open AI analysis", type="primary"):
            navigate("AI Analysis")


def require_report() -> 'InnovationReport | None':



    """Prompt for an analysis when a downstream page has no report."""
    report = current_report()
    if not report:
        st.warning("Run an innovation analysis first to unlock this view.")
        if st.button("Go to problem upload", type="primary"):
            navigate("Upload Problem")
    return report


def render_analysis() -> None:
    """Render transparent AI reasoning and evidence."""
    hero(
        "AI REASONING",
        "Understand the challenge signals.",
        "Every output is derived from local data.",
    )
    report = require_report()
    if not report:
        return
    cols = st.columns(3)
    cols[0].metric("Readiness", f"{report.analysis.readiness_score}/100")
    cols[1].metric("Urgency", f"{report.analysis.urgency_score}/100")
    cols[2].metric("Evidence matched", len(report.evidence))
    st.markdown(
        f'<div class="glass-card">{escape(report.summary)}</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns(2)
    with left:
        st.markdown("### Core challenges")
        for challenge in report.analysis.challenges:
            st.markdown(f"- {challenge}")
    with right:
        st.markdown("### Strategic objectives")
        for objective in report.analysis.objectives:
            st.markdown(f"- {objective}")
    st.markdown("### Extracted signals")
    st.markdown(
        " ".join(
            f'<span class="badge">{escape(tag)}</span>'
            for tag in report.analysis.keywords
        ),
        unsafe_allow_html=True,
    )
    st.markdown("### Evidence map")
    categories = sorted({evidence.category for evidence in report.evidence})
    tabs = st.tabs(categories) if categories else []
    for tab, category in zip(tabs, categories, strict=False):
        with tab:
            rows = [
                evidence
                for evidence in report.evidence
                if evidence.category == category
            ]
            for evidence in rows:
                st.markdown(f"**{evidence.title}** - {evidence.relevance:.0%} match")
                st.caption(f"{evidence.summary} | {evidence.source}")


def render_recommendations() -> None:
    """Render scored actions, policy recommendations, and comparisons."""
    hero(
        "DECISION WORKSPACE",
        "Compare pilot-ready interventions.",
        "Prioritized by local evidence match.",
    )
    report = require_report()
    if not report:
        return
    st.plotly_chart(score_chart(report), width="stretch")
    for index, item in enumerate(report.recommendations, 1):
        with st.expander(
            f"{index}. {item.title} | Impact {item.impact_score} | Innovation {item.innovation_score}",
            expanded=index == 1,
        ):
            a, b, c = st.columns(3)
            a.metric("Confidence", f"{item.confidence:.0%}")
            b.metric("Estimated cost", item.estimated_cost)
            c.metric("Timeframe", item.timeframe)
            st.write(item.rationale)
            st.markdown("**Pilot actions**")
            for step in item.action_steps:
                st.markdown(f"- {step}")
    st.markdown("### Policy recommendations")
    for policy in report.policy_recommendations:
        st.markdown(
            f'<div class="glass-card">{escape(policy)}</div>', unsafe_allow_html=True
        )


def render_download() -> None:
    """Render final report preview and Markdown download."""
    hero(
        "REPORT CENTER",
        "Export the decision brief.",
        "A portable, auditable artifact for stakeholders.",
    )
    report = require_report()
    if not report:
        return
    markdown = generate_markdown(report)
    cols = st.columns(4)
    cols[0].metric("Report ID", report.report_id)
    cols[1].metric("Recommendations", len(report.recommendations))
    cols[2].metric("Evidence records", len(report.evidence))
    cols[3].metric("Dataset", report.dataset_version)
    st.download_button(
        "Download Markdown report",
        markdown,
        file_name=f"{report.report_id.lower()}-innovation-brief.md",
        mime="text/markdown",
        type="primary",
        width="stretch",
    )
    with st.expander("Preview evidence register"):
        st.dataframe(evidence_frame(report), width="stretch", hide_index=True)
    with st.expander("Preview full Markdown report"):
        st.markdown(markdown)


def main() -> None:
    """Run the selected page."""
    initialize()
    sidebar()
    pages = {
        "Dashboard": render_dashboard,
        "Upload Problem": render_upload,
        "AI Analysis": render_analysis,
        "Recommendations": render_recommendations,
        "Download Report": render_download,
    }
    pages[st.session_state.page]()


if __name__ == "__main__":
    main()

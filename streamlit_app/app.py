"""Complete Streamlit MVP entry point for GovInnovate AI."""

import sys
from html import escape
from pathlib import Path

# Streamlit can execute this file with only streamlit_app/ on sys.path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import plotly.express as px
import streamlit as st

from backend.models.report import InnovationReport
from backend.repositories.dataset_repository import DatasetRepository
from backend.repositories.report_repository import ReportRepository
from backend.services.orchestrator import AnalysisOrchestrator
from backend.services.report_service import generate_markdown
from streamlit_app.components.problem_form import render_problem_form
from streamlit_app.components.report_view import (
    evidence_frame,
    evidence_map,
    score_chart,
)
from streamlit_app.styles import THEME_CSS
from streamlit_app.translations import (
    DEFAULT_LANGUAGE,
    LANGUAGE_OPTIONS,
)
from streamlit_app.translations import (
    t as translate,
)

PAGES = (
    "Dashboard",
    "Upload Problem",
    "AI Analysis",
    "Recommendations",
    "Download Report",
)

PAGE_KEYS = {
    "Dashboard": "page_dashboard",
    "Upload Problem": "page_upload",
    "AI Analysis": "page_analysis",
    "Recommendations": "page_recommendations",
    "Download Report": "page_download",
}


def initialize() -> None:
    """Configure the application and shared state."""
    st.set_page_config(page_title="GovInnovate AI", page_icon="G", layout="wide")
    st.markdown(THEME_CSS, unsafe_allow_html=True)
    st.session_state.setdefault("page", "Dashboard")
    st.session_state.setdefault("report", None)
    st.session_state.setdefault("language", DEFAULT_LANGUAGE)


def navigate(page: str) -> None:
    """Switch pages and refresh the Streamlit script."""
    st.session_state.page = page
    st.rerun()


def sidebar() -> None:
    """Render professional sidebar navigation."""
    with st.sidebar:
        st.markdown(f"## {t('app_title').upper()}")
        st.caption(t("public_innovation"))
        st.markdown("---")
        language = st.selectbox(
            t("language"),
            tuple(LANGUAGE_OPTIONS),
            index=tuple(LANGUAGE_OPTIONS).index(selected_language()),
            format_func=lambda code: LANGUAGE_OPTIONS[code],
        )
        st.session_state.language = language
        st.markdown("---")
        selected = st.radio(
            "Navigation",
            PAGES,
            index=PAGES.index(st.session_state.page),
            label_visibility="collapsed",
            format_func=lambda page: t(PAGE_KEYS[page]),
        )
        st.session_state.page = selected
        st.markdown("---")
        report = current_report()
        if report:
            st.success(f"{t('active_brief')}: {report.report_id}")
            st.caption(report.title)
        else:
            st.info(t("unlock_message"))
        st.caption(t("local_stack"))


def current_report() -> InnovationReport | None:
    """Return the active report from session state."""
    report = st.session_state.get("report")
    return report if isinstance(report, InnovationReport) else None


def selected_language() -> str:
    """Return the active UI language code."""
    language = st.session_state.get("language", DEFAULT_LANGUAGE)
    return language if isinstance(language, str) else DEFAULT_LANGUAGE


def t(key: str, **values: object) -> str:
    """Translate a UI string for the active Streamlit session."""
    text = translate(key, selected_language())
    return text.format(**values) if values else text


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
        t("dashboard_eyebrow"),
        t("dashboard_title"),
        t("dashboard_description"),
    )
    counts = DatasetRepository().counts()
    history = ReportRepository().history()
    cols = st.columns(4)
    cols[0].metric(t("evidence_records"), sum(counts.values()), "Local JSON")
    cols[1].metric(t("datasets_online"), len(counts), "100% local")
    cols[2].metric(t("reports_generated"), len(history), "SQLite tracked")
    average = (
        round(sum(row["impact_score"] for row in history) / len(history))
        if history
        else 0
    )
    cols[3].metric(t("average_impact"), f"{average}/100", "Across reports")

    left, right = st.columns([1.35, 1])
    with left:
        st.markdown(f"### {t('evidence_landscape')}")
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
        st.markdown(f"### {t('workflow')}")
        st.markdown(t("workflow_html"), unsafe_allow_html=True)
        if st.button(t("new_analysis"), type="primary", width="stretch"):
            navigate("Upload Problem")

    st.markdown(f"### {t('recent_analyses')}")
    if history:
        st.dataframe(pd.DataFrame(history), width="stretch", hide_index=True)
    else:
        st.caption(t("no_reports"))


def render_upload() -> None:
    """Render problem intake and execute the workflow."""
    hero(
        t("challenge_intake"),
        t("upload_title"),
        t("upload_description"),
    )
    problem = render_problem_form(t)
    if problem:
        with st.status(t("processing_title"), expanded=True) as status:
            st.write(t("processing_structure"))
            st.write(t("processing_search"))
            report = AnalysisOrchestrator().run(problem)
            st.write(t("processing_score"))
            status.update(label=t("analysis_complete"), state="complete")
        st.session_state.report = report
        st.success(t("created_report", report_id=report.report_id))
        if st.button(t("open_analysis"), type="primary"):
            navigate("AI Analysis")


def require_report() -> InnovationReport | None:
    """Prompt for an analysis when a downstream page has no report."""
    report = current_report()
    if not report:
        st.warning(t("require_report"))
        if st.button(t("go_upload"), type="primary"):
            navigate("Upload Problem")
    return report


def render_analysis() -> None:
    """Render transparent AI reasoning and evidence."""
    hero(
        t("reasoning_eyebrow"),
        t("reasoning_title"),
        t("reasoning_description"),
    )
    report = require_report()
    if not report:
        return
    cols = st.columns(3)
    cols[0].metric(t("readiness"), f"{report.analysis.readiness_score}/100")
    cols[1].metric(t("urgency"), f"{report.analysis.urgency_score}/100")
    cols[2].metric(t("evidence_matched"), len(report.evidence))
    st.markdown(
        f'<div class="glass-card">{escape(report.summary)}</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns(2)
    with left:
        st.markdown(f"### {t('core_challenges')}")
        for challenge in report.analysis.challenges:
            st.markdown(f"- {challenge}")
    with right:
        st.markdown(f"### {t('strategic_objectives')}")
        for objective in report.analysis.objectives:
            st.markdown(f"- {objective}")
    st.markdown(f"### {t('extracted_signals')}")
    st.markdown(
        " ".join(
            f'<span class="badge">{escape(tag)}</span>'
            for tag in report.analysis.keywords
        ),
        unsafe_allow_html=True,
    )
    st.markdown(f"### {t('evidence_map')}")
    with st.spinner(t("map_loading")):
        map_figure = evidence_map(report)
    if map_figure.data:
        st.plotly_chart(map_figure, width="stretch")
    elif report.evidence:
        st.info(t("map_unavailable"))
    else:
        st.info(t("map_empty"))

    st.markdown(f"### {t('matched_evidence')}")
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
        t("workspace_eyebrow"),
        t("workspace_title"),
        t("workspace_description"),
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
            a.metric(t("confidence"), f"{item.confidence:.0%}")
            b.metric(t("estimated_cost"), item.estimated_cost)
            c.metric(t("timeframe"), item.timeframe)
            st.write(item.rationale)
            st.markdown(f"**{t('pilot_actions')}**")
            for step in item.action_steps:
                st.markdown(f"- {step}")
    st.markdown(f"### {t('policy_recommendations')}")
    for policy in report.policy_recommendations:
        st.markdown(
            f'<div class="glass-card">{escape(policy)}</div>', unsafe_allow_html=True
        )


def render_download() -> None:
    """Render final report preview and Markdown download."""
    hero(
        t("report_center"),
        t("report_title"),
        t("report_description"),
    )
    report = require_report()
    if not report:
        return
    markdown = generate_markdown(report)
    cols = st.columns(4)
    cols[0].metric(t("report_id"), report.report_id)
    cols[1].metric(t("recommendations"), len(report.recommendations))
    cols[2].metric(t("evidence_records"), len(report.evidence))
    cols[3].metric(t("dataset"), report.dataset_version)
    st.download_button(
        t("download_markdown"),
        markdown,
        file_name=f"{report.report_id.lower()}-innovation-brief.md",
        mime="text/markdown",
        type="primary",
        width="stretch",
    )
    with st.expander(t("evidence_register")):
        st.dataframe(evidence_frame(report), width="stretch", hide_index=True)
    with st.expander(t("full_report")):
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

"""Report display component."""

from backend.models.report import InnovationReport


def render_report(report: InnovationReport) -> None:
    """Render an innovation report as dashboard cards and evidence tabs."""
    import streamlit as st

    st.subheader(report.title)
    st.write(report.summary)

    columns = st.columns(len(report.recommendations))
    for column, recommendation in zip(columns, report.recommendations):
        with column:
            st.metric(recommendation.title, f"{recommendation.confidence:.0%} confidence")
            st.write(recommendation.rationale)

    with st.expander("Evidence and provenance", expanded=True):
        for evidence in report.evidence:
            st.markdown(f"**{evidence.title}**  \n{evidence.summary}")
            st.caption(f"Source: {evidence.source} | Relevance: {evidence.relevance:.0%}")

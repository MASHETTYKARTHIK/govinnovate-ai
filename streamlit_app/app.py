"""Streamlit entry point for the GovInnovate AI hackathon application."""

import streamlit as st

from backend.services.orchestrator import AnalysisOrchestrator
from streamlit_app.components.problem_form import render_problem_form
from streamlit_app.components.report_view import render_report


def main() -> None:
    """Render the single-page problem analysis workflow."""
    st.set_page_config(page_title="GovInnovate AI", layout="wide")
    st.title("GovInnovate AI")
    st.caption("Evidence-backed innovation recommendations for public-sector challenges.")

    problem = render_problem_form()
    if problem is not None:
        with st.spinner("Analyzing evidence and preparing recommendations..."):
            report = AnalysisOrchestrator().run(problem)
        render_report(report)


if __name__ == "__main__":
    main()

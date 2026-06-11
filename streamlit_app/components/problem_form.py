"""Guided problem intake form."""

from collections.abc import Callable

from backend.models.problem import Problem


def render_problem_form(t: Callable[[str], str] | None = None) -> Problem | None:
    """Render a complete government challenge intake form."""
    import streamlit as st

    translate = t or (lambda key: key)
    with st.form("problem-form"):
        st.markdown(f"### {translate('challenge_define')}")
        problem_text = st.text_area(
            translate("problem_statement"),
            placeholder=translate("problem_help"),
            height=200,
        )
        left, right = st.columns(2)
        with left:
            location = st.text_input(
                translate("location"), placeholder="Hyderabad, Telangana"
            )
            sector = st.selectbox(
                translate("sector"),
                (
                    "Transport",
                    "Waste",
                    "Water",
                    "Health",
                    "Education",
                    "Energy",
                    "Other",
                ),
            )
            target_population = st.text_input(
                translate("target_population"),
                placeholder="Commuters in high-congestion corridors",
            )
        with right:
            budget = st.selectbox(
                translate("indicative_budget"),
                (
                    "Not specified",
                    "Under INR 10 lakh",
                    "INR 10-50 lakh",
                    "INR 50 lakh-2 crore",
                    "Above INR 2 crore",
                ),
            )
            timeframe = st.selectbox(
                translate("target_timeframe"),
                ("0-3 months", "3-6 months", "6-12 months", "12-24 months"),
            )
            st.info(
                "GovInnovate AI uses only local sample datasets and transparent mock reasoning."
            )
        submitted = st.form_submit_button(
            translate("run_analysis"), type="primary", width="stretch"
        )

    if not submitted:
        return None
    if len(problem_text.strip()) < 30:
        st.error(translate("problem_short"))
        return None
    return Problem(
        text=problem_text.strip(),
        location=location.strip(),
        sector=sector,
        budget=budget,
        timeframe=timeframe,
        target_population=target_population.strip(),
    )

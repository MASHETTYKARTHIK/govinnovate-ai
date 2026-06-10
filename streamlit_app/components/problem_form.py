"""Guided problem intake form."""







from backend.models.problem import Problem


def render_problem_form() -> 'Problem | None':

    return None


    """Render a complete government challenge intake form."""
    import streamlit as st

    with st.form("problem-form"):
        st.markdown("### Define the challenge")
        problem_text = st.text_area(
            "Problem statement",
            placeholder=(
                "Describe the challenge, affected communities, current constraints, "
                "and the outcome the government wants to achieve."
            ),
            height=200,
        )
        left, right = st.columns(2)
        with left:
            location = st.text_input("Location", placeholder="Hyderabad, Telangana")
            sector = st.selectbox(
                "Sector",
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
                "Target population",
                placeholder="Commuters in high-congestion corridors",
            )
        with right:
            budget = st.selectbox(
                "Indicative budget",
                (
                    "Not specified",
                    "Under INR 10 lakh",
                    "INR 10-50 lakh",
                    "INR 50 lakh-2 crore",
                    "Above INR 2 crore",
                ),
            )
            timeframe = st.selectbox(
                "Target timeframe",
                ("0-3 months", "3-6 months", "6-12 months", "12-24 months"),
            )
            st.info(
                "GovInnovate AI uses only local sample datasets and transparent mock reasoning."
            )
        submitted = st.form_submit_button(
            "Run innovation analysis", type="primary", width="stretch"
        )

    if not submitted:
        return None
    if len(problem_text.strip()) < 30:
        st.error(
            "Please provide at least 30 characters so the analysis has enough context."
        )
        return None
    return Problem(
        text=problem_text.strip(),
        location=location.strip(),
        sector=sector,
        budget=budget,
        timeframe=timeframe,
        target_population=target_population.strip(),
    )





    """Render a complete government challenge intake form."""

    import streamlit as st

    with st.form("problem-form"):
        st.markdown("### Define the challenge")
        problem_text = st.text_area(
            "Problem statement",
            placeholder=(
                "Describe the challenge, affected communities, current constraints, "
                "and the outcome the government wants to achieve."
            ),
            height=200,
        )
        left, right = st.columns(2)
        with left:
            location = st.text_input("Location", placeholder="Hyderabad, Telangana")
            sector = st.selectbox(
                "Sector",
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
                "Target population",
                placeholder="Commuters in high-congestion corridors",
            )
        with right:
            budget = st.selectbox(
                "Indicative budget",
                (
                    "Not specified",
                    "Under INR 10 lakh",
                    "INR 10-50 lakh",
                    "INR 50 lakh-2 crore",
                    "Above INR 2 crore",
                ),
            )
            timeframe = st.selectbox(
                "Target timeframe",
                ("0-3 months", "3-6 months", "6-12 months", "12-24 months"),
            )
            st.info(
                "GovInnovate AI uses only local sample datasets and transparent mock reasoning."
            )
        submitted = st.form_submit_button(
            "Run innovation analysis", type="primary", width="stretch"
        )

    if not submitted:
        return None
    if len(problem_text.strip()) < 30:
        st.error(
            "Please provide at least 30 characters so the analysis has enough context."
        )
        return None
    return Problem(
        text=problem_text.strip(),
        location=location.strip(),
        sector=sector,
        budget=budget,
        timeframe=timeframe,
        target_population=target_population.strip(),
    )

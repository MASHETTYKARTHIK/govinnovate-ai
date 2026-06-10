"""Problem input form component."""

from backend.models.problem import Problem


def render_problem_form() -> Problem | None:
    """Render the problem form and return submitted input."""
    import streamlit as st

    with st.form("problem-form"):
        problem_text = st.text_area(
            "Describe the public-sector challenge",
            placeholder="Example: Reduce peak-hour traffic congestion in Hyderabad...",
            height=180,
        )
        location = st.text_input("Location", placeholder="Hyderabad, India")
        sector = st.selectbox(
            "Sector",
            ("Transport", "Waste", "Water", "Health", "Education", "Other"),
        )
        submitted = st.form_submit_button("Generate innovation brief", type="primary")

    if not submitted:
        return None
    if not problem_text.strip():
        st.error("Please describe the challenge before continuing.")
        return None
    return Problem(text=problem_text.strip(), location=location.strip(), sector=sector)

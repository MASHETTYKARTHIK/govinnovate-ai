"""Reusable report presentation components."""

import pandas as pd
import plotly.graph_objects as go

from backend.models.report import InnovationReport


def score_chart(report: InnovationReport) -> go.Figure:
    """Create a grouped score chart for recommendations."""
    figure = go.Figure()
    titles = [item.title for item in report.recommendations]
    figure.add_bar(
        name="Impact",
        x=titles,
        y=[item.impact_score for item in report.recommendations],
    )
    figure.add_bar(
        name="Innovation",
        x=titles,
        y=[item.innovation_score for item in report.recommendations],
    )
    figure.update_layout(
        barmode="group",
        height=380,
        margin=dict(l=10, r=10, t=35, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#dbe8f7",
        legend_orientation="h",
        yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,.08)"),
        xaxis=dict(tickangle=-15),
    )
    return figure


def evidence_frame(report: InnovationReport) -> pd.DataFrame:
    """Create a display-ready evidence table."""
    return pd.DataFrame(
        [
            {
                "Type": item.category,
                "Evidence": item.title,
                "Location": item.location,
                "Match": f"{item.relevance:.0%}",
                "Source": item.source,
            }
            for item in report.evidence
        ]
    )

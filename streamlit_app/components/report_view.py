"""Reusable report presentation components."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from backend.models.evidence import Evidence
from backend.models.report import InnovationReport

LOCATION_COORDINATES = {
    "global": (20.0, 0.0),
    "hyderabad": (17.385, 78.4867),
    "india": (22.9734, 78.6569),
    "south asia": (23.685, 90.3563),
}


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


def evidence_map_frame(report: InnovationReport) -> pd.DataFrame:
    """Create geocoded evidence rows for map rendering."""
    return pd.DataFrame(
        row for item in report.evidence if (row := _evidence_map_row(item)) is not None
    )


def evidence_map(report: InnovationReport) -> go.Figure:
    """Create an interactive evidence map with provenance-rich hover details."""
    frame = evidence_map_frame(report)
    if frame.empty:
        return go.Figure()

    center = {
        "lat": float(frame["lat"].mean()),
        "lon": float(frame["lon"].mean()),
    }
    figure = px.scatter_geo(
        frame,
        lat="lat",
        lon="lon",
        color="category",
        size="score",
        hover_name="title",
        hover_data={
            "category": True,
            "score": ":.0%",
            "location": True,
            "source": True,
            "lat": False,
            "lon": False,
        },
        projection="natural earth",
        scope="world",
    )
    figure.update_geos(
        center=center,
        lataxis_range=[center["lat"] - 35, center["lat"] + 35],
        lonaxis_range=[center["lon"] - 55, center["lon"] + 55],
        showcountries=True,
        countrycolor="rgba(255,255,255,.22)",
        showcoastlines=True,
        coastlinecolor="rgba(255,255,255,.16)",
        showland=True,
        landcolor="rgba(50,70,86,.58)",
        showocean=True,
        oceancolor="rgba(12,22,34,.95)",
    )
    figure.update_layout(
        height=430,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#dbe8f7",
        legend_orientation="h",
        legend_title_text="",
    )
    return figure


def _evidence_map_row(item: Evidence) -> dict[str, object] | None:
    coordinates = _coordinates_for(item)
    if coordinates is None:
        return None
    latitude, longitude = coordinates
    return {
        "title": item.title,
        "category": item.category,
        "score": item.relevance,
        "location": item.location or "Global",
        "source": item.source,
        "lat": latitude,
        "lon": longitude,
    }


def _coordinates_for(item: Evidence) -> tuple[float, float] | None:
    latitude = item.metadata.get("latitude") or item.metadata.get("lat")
    longitude = item.metadata.get("longitude") or item.metadata.get("lon")
    if isinstance(latitude, int | float) and isinstance(longitude, int | float):
        return float(latitude), float(longitude)

    location = item.location.strip().lower() if item.location else "global"
    if location in LOCATION_COORDINATES:
        return LOCATION_COORDINATES[location]
    for known_location, coordinates in LOCATION_COORDINATES.items():
        if known_location in location:
            return coordinates
    return None

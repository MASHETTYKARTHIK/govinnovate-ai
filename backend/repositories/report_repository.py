"""SQLite persistence for generated report history."""

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

from backend.config import settings
from backend.models.report import InnovationReport


class ReportRepository:
    """Persist lightweight report metadata and serialized report payloads."""

    def __init__(self, database_path: Path | None = None) -> None:
        self.database_path = database_path or settings.database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    report_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    title TEXT NOT NULL,
                    sector TEXT NOT NULL,
                    location TEXT NOT NULL,
                    impact_score INTEGER NOT NULL,
                    payload TEXT NOT NULL
                )
                """)

    def save(self, report: InnovationReport) -> None:
        """Insert or replace a report."""
        impact = round(
            sum(item.impact_score for item in report.recommendations)
            / max(len(report.recommendations), 1)
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO reports
                (report_id, created_at, title, sector, location, impact_score, payload)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    report.report_id,
                    report.created_at,
                    report.title,
                    report.problem.sector,
                    report.problem.location,
                    impact,
                    json.dumps(asdict(report)),
                ),
            )

    def history(self, limit: int = 25) -> list[dict]:
        """Return newest report summaries for the dashboard."""
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT report_id, created_at, title, sector, location, impact_score
                FROM reports ORDER BY created_at DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

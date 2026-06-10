"""Runtime configuration loaded from environment variables."""

from dataclasses import dataclass
from os import getenv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    """Application settings with hackathon-friendly local defaults."""

    dataset_path: Path = Path(
        getenv("GOVINNOVATE_DATASET_PATH", PROJECT_ROOT / "datasets")
    )
    report_path: Path = Path(
        getenv("GOVINNOVATE_REPORT_PATH", PROJECT_ROOT / "reports/generated")
    )
    database_path: Path = Path(
        getenv(
            "GOVINNOVATE_DATABASE_PATH",
            PROJECT_ROOT / "reports/generated/govinnovate.db",
        )
    )
    dataset_version: str = getenv("GOVINNOVATE_DATASET_VERSION", "hackathon-v1")


settings = Settings()

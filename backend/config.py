"""Runtime configuration loaded from environment variables."""

from dataclasses import dataclass
from os import getenv
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Application settings with hackathon-friendly local defaults."""

    dataset_path: Path = Path(getenv("GOVINNOVATE_DATASET_PATH", "datasets/curated"))
    report_path: Path = Path(getenv("GOVINNOVATE_REPORT_PATH", "reports/generated"))
    dataset_version: str = getenv("GOVINNOVATE_DATASET_VERSION", "poc-v0")


settings = Settings()

"""Smoke test the Streamlit application module."""

import importlib
import subprocess
import sys
from pathlib import Path


def test_streamlit_app_imports() -> None:
    module = importlib.import_module("streamlit_app.app")

    assert callable(module.main)


def test_streamlit_entrypoint_bootstraps_project_root() -> None:
    project_root = Path(__file__).resolve().parents[2]
    script = (
        "import runpy, sys; "
        f"root=r'{project_root}'; "
        f"sys.path=[r'{project_root / 'streamlit_app'}'] + "
        "[path for path in sys.path if path and root.lower() not in path.lower()]; "
        f"runpy.run_path(r'{project_root / 'streamlit_app' / 'app.py'}', run_name='import_probe')"
    )

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

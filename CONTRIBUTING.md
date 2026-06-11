# Contributing to GovInnovate AI

Thank you for helping build GovInnovate AI. Contributions should remain focused,
reviewable, and useful for a hackathon-ready public-sector innovation platform.

## Project Setup

Requirements:

- Python 3.10+
- Git

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install the current MVP dependencies:

```bash
pip install streamlit pandas plotly pytest
```

## Launch Streamlit

From the repository root:

```bash
streamlit run streamlit_app/app.py
```

The application uses local JSON datasets and creates runtime SQLite artifacts
under `reports/generated/`.

## Branch Naming

Create branches from the latest default branch using:

```text
feature/short-description
fix/short-description
docs/short-description
test/short-description
chore/short-description
```

Examples: `feature/report-filters`, `fix/streamlit-imports`.

## Commit Messages

Use concise, imperative commit messages:

```text
feat: add recommendation score chart
fix: handle empty evidence results
test: cover report markdown export
docs: clarify local setup
```

Keep each commit focused on one logical change.

## Merge Request Workflow

1. Create a focused branch and implement the smallest complete change.
2. Add or update tests for behavior changes.
3. Run the full test suite locally.
4. Open a merge request with a clear summary, verification steps, and screenshots
   for visible Streamlit changes.
5. Address review feedback and keep the branch free of generated artifacts.

Avoid unrelated refactors in the same merge request.

## Testing

Run all tests from the repository root:

```bash
python -m pytest -q
```

For Streamlit changes, also launch the application and verify the affected
workflow manually.

## Coding Standards

- Follow PEP 8 and use type hints for public functions.
- Keep modules small, focused, and compatible with the existing architecture.
- Prefer clear domain models and deterministic logic over hidden behavior.
- Add concise docstrings for modules, classes, and public functions.
- Keep data local and do not commit secrets, personal data, caches, or databases.
- Preserve citation and provenance information in generated recommendations.

## Before Submitting

- Tests pass.
- Streamlit launches without errors.
- No `__pycache__`, `.pyc`, `.env`, virtual environment, or SQLite artifacts are included.
- The merge request explains what changed and why.

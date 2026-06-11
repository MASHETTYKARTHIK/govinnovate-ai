# GovInnovate AI User Manual

GovInnovate AI is a local Streamlit application that converts public-sector
problem statements into evidence-backed innovation recommendations and
downloadable decision briefs.

The hackathon MVP uses local JSON datasets, transparent mock AI reasoning, and
SQLite report history. It does not require an external AI API.

## System Requirements

- Python 3.10 or newer
- Git
- A modern web browser
- Windows, macOS, or Linux

Required Python packages:

- Streamlit
- Pandas
- Plotly
- pytest, for running the test suite

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd govinnovate-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the MVP dependencies:

```bash
pip install streamlit pandas plotly pytest
```

## Run the Application

From the repository root, run:

```bash
streamlit run streamlit_app/app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open the URL in a browser. Stop the application by pressing `Ctrl+C` in the
terminal.

## Application Workflow

Use the sidebar to move through five stages:

1. **Dashboard** presents dataset coverage, generated-report statistics, and
   recent analysis history.
2. **Upload Problem** captures the challenge and starts the analysis.
3. **AI Analysis** explains the identified challenges, objectives, keywords,
   readiness, urgency, and matched evidence.
4. **Recommendations** compares prioritized interventions, scores, costs,
   timeframes, actions, and policy recommendations.
5. **Download Report** previews and downloads the complete Markdown brief.

## Upload a Problem

Open **Upload Problem** from the sidebar and complete the challenge form.

Provide:

- **Problem statement:** Describe the challenge, affected communities,
  constraints, and desired outcome. At least 30 characters are required.
- **Location:** Enter the city, district, state, or region.
- **Sector:** Select the most relevant public-service area.
- **Target population:** Identify the people or communities affected.
- **Indicative budget:** Select the closest available budget range.
- **Target timeframe:** Select the expected implementation period.

Select **Run innovation analysis**. The application will structure the
challenge, search local evidence, score interventions, and create a report.

For stronger results, include measurable goals and specific local constraints
instead of entering only a broad topic.

## How AI Analysis Works

The MVP uses deterministic mock AI reasoning designed for transparent
demonstrations:

1. The problem analyzer extracts keywords and creates a structured summary,
   challenges, objectives, readiness score, and urgency score.
2. A local FAISS-style mock vector index compares the problem with JSON records
   in `datasets/`.
3. The retrieval layer ranks relevant research papers, startups, case studies,
   and government programs.
4. The report generator creates evidence-linked recommendations and assigns
   confidence, impact, innovation, cost, and timeframe values.

The analysis is generated locally. Treat recommendations as decision support,
not as final policy or procurement advice. Validate them with officials,
communities, subject-matter experts, and authoritative sources.

## Recommendations and Evidence

The **Recommendations** page displays:

- Prioritized interventions
- Impact and innovation score comparison
- Evidence-match confidence
- Estimated cost and timeframe
- Suggested pilot actions
- Policy recommendations

The **AI Analysis** page groups matched evidence by category and displays source
information. Use these records to understand why an intervention was suggested.

## Report Generation

Every completed analysis creates a structured report containing:

- Executive summary
- Problem context
- AI analysis and scores
- Recommendations and action steps
- Policy recommendations
- Evidence register and provenance

Open **Download Report** and select **Download Markdown report** to save the
brief. Markdown files can be opened in text editors, documentation tools, or
converted into presentation-ready formats.

Report history is stored locally in:

```text
reports/generated/govinnovate.db
```

The database is a runtime artifact and is excluded from version control.

## Troubleshooting

### `streamlit` is not recognized

Confirm the virtual environment is active, then run:

```bash
pip install streamlit
python -m streamlit run streamlit_app/app.py
```

### `ModuleNotFoundError: No module named 'backend'`

Run the application from the repository root:

```bash
streamlit run streamlit_app/app.py
```

Do not launch `app.py` from inside the `streamlit_app/` directory.

### Port 8501 is already in use

Choose another port:

```bash
streamlit run streamlit_app/app.py --server.port 8502
```

### No recommendations or limited evidence appear

- Add more detail to the problem statement.
- Use terms related to the selected sector.
- Confirm the JSON files exist under `datasets/`.
- Restart Streamlit after changing dataset files.

### Report history is missing

The SQLite database is created when an analysis completes. Confirm that the
application can write to `reports/generated/`.

### Verify the installation

Run the automated tests:

```bash
python -m pytest -q
```

All tests should pass before reporting an application issue.

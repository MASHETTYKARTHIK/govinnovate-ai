# GovInnovate AI Agent Architecture

GovInnovate AI uses a sequential, evidence-grounded agent workflow to transform
a public-sector problem statement into a structured innovation report.

The current hackathon MVP is deterministic and local-first. It simulates AI
reasoning without external model APIs, retrieves evidence from local JSON
datasets, and preserves provenance throughout the workflow.

## Architecture Overview

```text
Streamlit problem form
        |
        v
     Problem
        |
        v
Analysis Orchestrator
        |
        +--> Problem Analyzer Agent --> ProblemAnalysis
        |
        +--> Retrieval Coordinator Agent
        |         |
        |         +--> Dataset Repository
        |                    |
        |                    +--> Mock FAISS Vector Index
        |         |
        |         +--> Evidence records
        |
        +--> Report Generator Agent --> InnovationReport
        |
        +--> Report Repository --> SQLite history
```

## Core Data Contracts

The workflow exchanges immutable dataclass models defined under
`backend/models/`.

| Model | Purpose |
|---|---|
| `Problem` | Captures the submitted challenge, location, sector, budget, timeframe, and target population. |
| `ProblemAnalysis` | Stores the normalized title, summary, keywords, challenges, objectives, readiness score, and urgency score. |
| `Evidence` | Represents a retrieved dataset record with category, source, relevance, tags, location, and metadata. |
| `Recommendation` | Contains a prioritized action, rationale, action steps, confidence, scores, cost, timeframe, and evidence references. |
| `InnovationReport` | Combines the original problem, analysis, recommendations, evidence, policy actions, and dataset version. |

## Problem Analyzer Agent

**Implementation:** `backend/agents/problem_analyzer.py`

### Responsibility

The Problem Analyzer converts free-text user input into a structured problem
representation suitable for evidence retrieval and reporting.

### Inputs

- A `Problem` object submitted through Streamlit

### Processing

- Extracts meaningful keywords while filtering common stop words
- Builds a location- and sector-aware strategy title
- Identifies core implementation challenges
- Defines practical strategic objectives
- Calculates deterministic readiness and urgency scores

The readiness score considers the amount of submitted detail and whether a
budget is specified. The urgency score responds to explicit urgency terms in
the problem statement.

### Output

- A `ProblemAnalysis` object

The agent does not access datasets or generate final recommendations.

## Retrieval Coordinator Agent

**Implementation:** `backend/agents/retrieval_coordinator.py`

### Responsibility

The Retrieval Coordinator converts the submitted problem and structured
analysis into a retrieval query and requests ranked evidence from the Dataset
Repository.

### Inputs

- Original `Problem`
- Structured `ProblemAnalysis`
- Optional result limit, defaulting to 16 records

### Processing

The coordinator combines:

- Full problem text
- Sector
- Location
- Extracted analysis keywords

This combined query gives the retrieval layer both natural-language context and
structured decision signals.

### Output

- An ordered tuple of `Evidence` records

The coordinator does not interpret evidence or create recommendations. Its role
is to keep query construction separate from data access and ranking.

## Dataset Repository

**Implementation:** `backend/repositories/dataset_repository.py`

### Responsibility

The Dataset Repository is the data-access boundary for the local evidence base.
It loads JSON records, builds the in-memory search index, executes searches,
and converts raw records into typed `Evidence` objects.

### Dataset Sources

The repository loads JSON files from `datasets/` and `datasets/curated/`.
Current evidence categories include:

- Research papers
- Startups
- Case studies
- Government programs

### Index Preparation

For every record, the repository constructs a searchable document from:

- Title
- Summary
- Tags
- Sector

These documents are passed to the local `MockFaissIndex` when the repository is
initialized.

### Search Output

The repository:

1. Requests ranked document indexes and similarity scores.
2. Excludes records with no similarity.
3. Maps similarity into a user-facing relevance score.
4. Preserves source, location, tags, and remaining dataset fields as metadata.
5. Returns typed `Evidence` records in descending relevance order.

The `counts()` operation supports dashboard dataset statistics.

## Vector Search Workflow

**Implementation:** `backend/repositories/vector_index.py`

The MVP uses `MockFaissIndex`, a deterministic FAISS-style local search
component. It provides the role of a vector index without requiring the native
FAISS dependency or an external embedding service.

### Indexing

1. Normalize each document to lowercase.
2. Extract alphanumeric tokens with at least three characters.
3. Represent each document as a token-frequency vector.
4. Store all vectors in memory.

### Querying

1. Apply the same tokenization to the retrieval query.
2. Calculate cosine similarity between the query vector and each document
   vector.
3. Sort records by descending similarity.
4. Return document indexes and similarity scores up to the requested limit.

### Relevance Mapping

The Dataset Repository maps positive cosine similarity scores into a relevance
range beginning at `0.55` and capped at `0.99`. This relevance value becomes
the recommendation confidence signal and contributes to impact scoring.

### Production Extension

The repository boundary allows `MockFaissIndex` to be replaced with native
FAISS, a hosted vector database, or embedding-based retrieval without changing
the agent contracts.

## Report Generator Agent

**Implementation:** `backend/agents/report_generator.py`

### Responsibility

The Report Generator transforms analysis and retrieved evidence into an
explainable, decision-ready `InnovationReport`.

### Inputs

- Original `Problem`
- Structured `ProblemAnalysis`
- Ranked `Evidence` records

### Processing

- Selects the highest-ranked evidence candidates
- Generates up to four recommendations
- Links each recommendation to its source evidence identifier
- Calculates confidence, impact, and innovation scores
- Carries cost and timeframe metadata into recommendations
- Generates practical pilot action steps
- Produces cross-department, procurement, governance, and program-alignment
  policy recommendations
- Assigns a report identifier, timestamp, and dataset version

If retrieval returns no evidence, the agent creates a clearly identified local
discovery fallback recommendation.

### Output

- A complete `InnovationReport`

All recommendations retain evidence references to support auditability.

## Analysis Orchestrator

**Implementation:** `backend/services/orchestrator.py`

### Responsibility

The Analysis Orchestrator owns the end-to-end execution sequence and is the
primary service called by the Streamlit application.

### Execution Sequence

```text
Problem
  -> ProblemAnalyzer.analyze()
  -> RetrievalCoordinator.retrieve()
  -> ReportGenerator.generate()
  -> ReportRepository.save()
  -> InnovationReport
```

### Design Role

The orchestrator:

- Keeps Streamlit independent from individual agents
- Enforces the current sequential workflow
- Supports dependency injection for retrieval and persistence during testing
- Persists completed reports before returning them to the user interface

It does not contain analysis, retrieval, ranking, or report-generation logic.

## Persistence and Reporting

The `ReportRepository` stores completed report summaries and serialized payloads
in a local SQLite database under `reports/generated/`. The dashboard uses this
history for report counts and recent-analysis views.

The Markdown report service converts an `InnovationReport` into a downloadable
brief containing problem context, scores, recommendations, policy actions, and
the evidence register.

## End-to-End Data Flow

1. A user submits a challenge through the Streamlit problem form.
2. Streamlit creates a typed `Problem` and sends it to the Analysis
   Orchestrator.
3. The Problem Analyzer produces a structured `ProblemAnalysis`.
4. The Retrieval Coordinator combines the problem and analysis into a search
   query.
5. The Dataset Repository searches the local vector index and returns ranked,
   provenance-rich `Evidence`.
6. The Report Generator creates evidence-linked recommendations and policy
   actions.
7. The Analysis Orchestrator saves the report to SQLite.
8. Streamlit displays the analysis, evidence, recommendation scores, and
   downloadable Markdown report.

## Architecture Principles

- **Evidence grounded:** Recommendations reference retrieved evidence records.
- **Transparent:** Scoring and retrieval are deterministic and inspectable.
- **Local first:** The MVP runs without external model or vector database APIs.
- **Modular:** Agents, repositories, models, orchestration, and presentation
  have separate responsibilities.
- **Testable:** Dependencies can be injected and each workflow stage can be
  verified independently.
- **Extensible:** Mock reasoning and vector search can be replaced without
  changing the overall data flow.


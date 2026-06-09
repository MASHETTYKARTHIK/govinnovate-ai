# GovInnovate AI — Task Breakdown & Implementation Roadmap (001-govinnovate-ai)

## Overview

This document breaks the POC into ordered, parallelizable tasks ready for Phase 2 implementation. Tasks are organized by workstream and estimated story points.

---

## Workstream 1: Backend Foundation (4 Weeks, 40 SP)

### T1.1: FastAPI Backend Scaffold (3 SP)
**Owner:** Backend Lead  
**Depends On:** None  
**Description:**
- Create FastAPI project skeleton (app.py, requirements.txt, .env template).
- Setup project structure: `src/api`, `src/agents`, `src/rag`, `src/models`.
- Configure logging (structlog, JSON format).
- Add health check endpoint (`GET /health`).
- Add request/response logging middleware.

**Acceptance Criteria:**
- [x] FastAPI server runs on `localhost:8000`.
- [x] Health check endpoint returns 200.
- [x] Logs structured JSON format.
- [x] README with setup instructions.

**Estimated Effort:** 8 hours

---

### T1.2: Environment & Secrets Management (2 SP)
**Owner:** DevOps / Backend  
**Depends On:** T1.1  
**Description:**
- Create `.env.template` with required variables (LLM_API_KEY, VECTOR_DB_PATH, etc.).
- Setup `python-dotenv` for local development.
- Document environment setup in README.
- Add config class (Pydantic Settings) for type-safe config.

**Acceptance Criteria:**
- [x] `.env.template` covers all services (LLM, DB, storage).
- [x] Config validates on startup; fails fast if required vars missing.
- [x] CI/CD can inject secrets via GitHub Actions.

**Estimated Effort:** 4 hours

---

### T1.3: Database Models & Migrations (5 SP)
**Owner:** Backend / Database  
**Depends On:** T1.1  
**Description:**
- Define SQLAlchemy ORM models (Problems, Reports, Documents, Chunks, Embeddings, Scores, AgentLogs).
- Create Alembic migrations.
- Setup PostgreSQL connection (or SQLite for POC).
- Seed initial test data.

**Acceptance Criteria:**
- [x] All tables created and queryable.
- [x] Migrations run successfully.
- [x] Test data inserted.
- [x] Schema documented in `data-model.md`.

**Estimated Effort:** 12 hours

---

### T1.4: LLM Integration Layer (5 SP)
**Owner:** ML / Backend  
**Depends On:** T1.1, T1.2  
**Description:**
- Wrap OpenAI API (GPT-4 + Embeddings).
- Create `llm_client.py`: methods for completion, embedding, token counting.
- Implement retry logic (exponential backoff, 3 retries).
- Add token usage logging.
- Create mock LLM for testing (deterministic responses).

**Acceptance Criteria:**
- [x] `llm_client.completion()` works; logs tokens + cost.
- [x] `llm_client.embed()` returns vector + logs.
- [x] Retry logic tested (simulate timeout).
- [x] Mock LLM deterministic; suitable for tests.

**Estimated Effort:** 12 hours

---

### T1.5: Vector DB Integration (FAISS) (4 SP)
**Owner:** Backend / ML  
**Depends On:** T1.1, T1.3, T1.4  
**Description:**
- Setup FAISS (pip install faiss-cpu).
- Create `vector_store.py`: methods for add_vector, search, load, save.
- Implement IndexFactory: create index, add embeddings, serialize.
- Create mock vector store for testing.
- Test persistence (save/load index).

**Acceptance Criteria:**
- [x] `vector_store.search(query_vector, k=5)` returns top-5.
- [x] Index serializable to disk.
- [x] Performance: <500 ms for 100k embeddings search.
- [x] Mock vector store for testing.

**Estimated Effort:** 10 hours

---

### T1.6: RAG Ingestion Pipeline (6 SP)
**Owner:** Data / Backend  
**Depends On:** T1.3, T1.4, T1.5  
**Description:**
- Create `ingestion.py`: document parsing (PDF, CSV, TXT).
- Implement chunking: semantic chunking (500–800 tokens, 50–100 overlap).
- Embed chunks via LLM.
- Store chunks + embeddings in DB + FAISS.
- Create admin API endpoint: `POST /admin/ingest` (upload dataset CSV).

**Acceptance Criteria:**
- [x] Parse PDF/CSV/TXT files.
- [x] Chunks created with metadata (doc_id, chunk_index, token_count).
- [x] Embeddings stored; searchable.
- [x] Admin endpoint accepts file upload; returns status.
- [x] Ingestion logged; traceable.

**Estimated Effort:** 14 hours

---

### T1.7: Testing Framework & Unit Tests (5 SP)
**Owner:** QA / Backend  
**Depends On:** All T1.x  
**Description:**
- Setup pytest + fixtures.
- Write unit tests for LLM client (mock), vector store (in-memory), ingestion.
- Add conftest.py with shared fixtures (test DB, test vector store).
- Setup pytest.ini; coverage targets (80% core modules).
- Add GitHub Actions workflow: run tests on PR.

**Acceptance Criteria:**
- [x] Test suite runs in <30 seconds.
- [x] Coverage ≥80% for core modules.
- [x] GitHub Actions enforces passing tests on PR.
- [x] README includes `pytest` command.

**Estimated Effort:** 12 hours

---

## Workstream 2: Agents & Orchestration (3 Weeks, 35 SP)

### T2.1: Problem Analyzer Agent (5 SP)
**Owner:** ML / Agent Dev  
**Depends On:** T1.4  
**Description:**
- Create `agents/problem_analyzer.py`.
- Design prompt template: extract title, tags, KPIs, constraints from free-text input.
- Implement function: `analyze_problem(problem_text, taxonomy_ref) -> AnalyzedProblem`.
- Add validation: ensure tags exist in taxonomy; KPIs are measurable.
- Create few-shot examples (transportation, water, waste examples).

**Acceptance Criteria:**
- [x] Agent produces structured output (Pydantic model).
- [x] Prompt tested on 10 diverse problem statements.
- [x] Output validation enforced; graceful error on invalid tags.
- [x] Few-shot examples in prompt.
- [x] Latency <10 sec per call.

**Estimated Effort:** 12 hours

---

### T2.2: Retrieval Coordinator Agent (6 SP)
**Owner:** Backend / ML  
**Depends On:** T1.4, T1.5, T2.1  
**Description:**
- Create `agents/retrieval_coordinator.py`.
- Implement retrieval pipeline: query embed → hybrid search (vector + keyword) → rank → deduplicate.
- Ranking: combine similarity + recency + authority (tunable weights).
- Return: top-K docs per type (research, case_study, startup).
- Add filtering: by geo, year, type.

**Acceptance Criteria:**
- [x] Hybrid search returns ≥3 relevant docs per type.
- [x] Ranking tunable; documented.
- [x] Deduplication removes duplicate docs.
- [x] Latency <1 sec for 100k embeddings.
- [x] Filtering works (geo, year, type).

**Estimated Effort:** 14 hours

---

### T2.3: Report Generator Agent (7 SP)
**Owner:** ML / Backend  
**Depends On:** T1.4, T2.1, T2.2  
**Description:**
- Create `agents/report_generator.py`.
- Design prompt template for synthesis: input retrieved context + analyzed problem → generate 8 sections (Analysis, Cases, Research, Startups, Policy, Roadmap, Cost, Impact).
- Parse LLM output into structured JSON (section objects).
- Compute scores (feasibility, cost, impact, risk, sustainability) from retrieved data + synthesis.
- Implement scoring methodology (formula, weights, explanation).

**Acceptance Criteria:**
- [x] All 8 sections generated with content + sources.
- [x] Scores computed and range 0–100.
- [x] Scores include "why" (3–5 contributing factors).
- [x] Output validated (all fields present).
- [x] Latency <30 sec.

**Estimated Effort:** 16 hours

---

### T2.4: Orchestrator (Sequential) (5 SP)
**Owner:** Backend  
**Depends On:** T2.1, T2.2, T2.3  
**Description:**
- Create `orchestrator.py`: Main coordinator.
- Sequential execution: Problem Analyzer → Retrieval → Report Generator.
- Error handling: retry, fallback, graceful degradation.
- Logging: each agent call logged (input, output, latency, tokens).
- Implement timeout (max 5 min).

**Acceptance Criteria:**
- [x] E2E orchestration works; produces report JSON.
- [x] Errors logged; don't crash.
- [x] Timeouts enforced.
- [x] Agent logs stored in DB.
- [x] Latency <5 min for small dataset.

**Estimated Effort:** 12 hours

---

### T2.5: Agent Tests & Integration (2 SP)
**Owner:** QA / Backend  
**Depends On:** T2.1, T2.2, T2.3, T2.4  
**Description:**
- Write integration tests: mock vector DB, test E2E flow.
- Create test dataset (5–10 example problems + expected outputs).
- Test orchestration: error cases, timeouts.
- Measure latency; ensure <5 min.

**Acceptance Criteria:**
- [x] Integration tests pass.
- [x] Latency benchmarked.
- [x] Error cases tested.
- [x] Coverage ≥60% for agents.

**Estimated Effort:** 8 hours

---

## Workstream 3: API & Data Layer (2 Weeks, 25 SP)

### T3.1: Problem API Endpoints (4 SP)
**Owner:** Backend  
**Depends On:** T1.1, T1.3, T2.4  
**Description:**
- Implement `POST /api/v1/problems` (create problem).
- Implement `GET /api/v1/problems/{id}` (fetch problem details).
- Add request validation (Pydantic).
- Add error responses (400, 404, 500).
- Document endpoints in OpenAPI/Swagger.

**Acceptance Criteria:**
- [x] Problem created in DB; returns problem_id.
- [x] Endpoints queryable via Swagger UI.
- [x] Validation enforced; 400 on invalid input.
- [x] Error messages clear.

**Estimated Effort:** 10 hours

---

### T3.2: Analysis API Endpoint (4 SP)
**Owner:** Backend  
**Depends On:** T2.4, T3.1  
**Description:**
- Implement `POST /api/v1/problems/{id}/analyze` (trigger analysis).
- Call orchestrator; return job status + report_id.
- For POC: synchronous (wait for completion); return report JSON.
- Add timeout handling.

**Acceptance Criteria:**
- [x] Endpoint triggers orchestrator.
- [x] Returns report JSON with scores + sections.
- [x] Timeout enforced (<5 min returns error).
- [x] Errors handled gracefully.

**Estimated Effort:** 10 hours

---

### T3.3: Report API Endpoints (4 SP)
**Owner:** Backend  
**Depends On:** T3.2  
**Description:**
- Implement `GET /api/v1/reports/{id}` (fetch report).
- Implement `GET /api/v1/reports/{id}/export?format=pdf|md|json` (export).
- Validate report exists; return 404 if not.
- Format conversion: JSON → PDF/Markdown.

**Acceptance Criteria:**
- [x] Fetch report returns JSON with all sections.
- [x] Export formats all work (PDF valid, Markdown parsable).
- [x] 404 if report not found.

**Estimated Effort:** 10 hours

---

### T3.4: Search API Endpoint (3 SP)
**Owner:** Backend  
**Depends On:** T2.2, T3.1  
**Description:**
- Implement `POST /api/v1/search` (full-text + semantic search).
- Query parameters: query text, filters (type, year, geo), k.
- Returns ranked docs with metadata + relevance score.

**Acceptance Criteria:**
- [x] Hybrid search returns top-K results.
- [x] Relevance scores shown.
- [x] Filters applied correctly.

**Estimated Effort:** 8 hours

---

### T3.5: Admin API (Ingestion) (3 SP)
**Owner:** Backend  
**Depends On:** T1.6, T3.1  
**Description:**
- Implement `POST /admin/ingest` (upload dataset).
- Accept CSV/PDF upload; trigger ingestion pipeline.
- Return status + counts (docs ingested, chunks created, vectors stored).

**Acceptance Criteria:**
- [x] File upload works.
- [x] Ingestion triggered; status returned.
- [x] Counts accurate.

**Estimated Effort:** 8 hours

---

### T3.6: API Documentation & OpenAPI (2 SP)
**Owner:** Backend  
**Depends On:** T3.1, T3.2, T3.3, T3.4, T3.5  
**Description:**
- Add docstrings + Pydantic models for all endpoints.
- Generate OpenAPI spec (FastAPI auto-generates).
- Create README: API overview + examples + curl commands.

**Acceptance Criteria:**
- [x] Swagger UI shows all endpoints.
- [x] Endpoint documentation clear.
- [x] Examples include request/response.

**Estimated Effort:** 6 hours

---

## Workstream 4: Frontend (2 Weeks, 28 SP)

### T4.1: React Scaffold + Setup (3 SP)
**Owner:** Frontend  
**Depends On:** None  
**Description:**
- Create React app (CRA or Vite).
- Setup TypeScript, ESLint, Prettier.
- Create basic routing (React Router).
- Configure API client (Axios).
- Create environment config (.env for API URL).

**Acceptance Criteria:**
- [x] React app starts on `localhost:3000`.
- [x] TypeScript strict mode enabled.
- [x] API client configured; can make requests.

**Estimated Effort:** 8 hours

---

### T4.2: Upload Page Component (5 SP)
**Owner:** Frontend  
**Depends On:** T4.1, T3.1  
**Description:**
- Create form component: text input (problem), optional fields (location, budget, sector).
- Add validation: text required, length 50–1000 chars.
- Add autocomplete: location dropdown, sector tags.
- Submit handler: call `POST /api/v1/problems` + navigate to analysis page.
- Loading spinner on submit.

**Acceptance Criteria:**
- [x] Form renders; all fields functional.
- [x] Validation shows error messages.
- [x] Submit calls API; shows loading.
- [x] Navigation to analysis page on success.

**Estimated Effort:** 12 hours

---

### T4.3: Analysis/Results Page Component (8 SP)
**Owner:** Frontend  
**Depends On:** T4.1, T3.2, T3.3  
**Description:**
- Fetch report via `GET /api/v1/reports/{id}`.
- Display problem summary card (title, tags, status).
- Create evidence tabs: Research, Cases, Startups (each showing top 5 with snippets + links).
- Display scoring dashboard: 5 scores (feasibility, cost, impact, risk, sustainability) as color-coded cards.
- Show composite score prominently.

**Acceptance Criteria:**
- [x] Page renders with report data.
- [x] Tabs switch between evidence types.
- [x] Scores displayed with color coding.
- [x] Links are clickable.
- [x] Responsive layout.

**Estimated Effort:** 18 hours

---

### T4.4: Report Page Component (5 SP)
**Owner:** Frontend  
**Depends On:** T4.1, T3.3  
**Description:**
- Display full report: sections (Analysis, Cases, Research, Startups, Policy, Roadmap, Cost, Impact).
- Each section: title, content, related sources (collapsible).
- Table of contents (TOC) on left; auto-scroll to sections.
- Download buttons: PDF, Markdown, JSON.
- Feedback buttons (useful/not useful).

**Acceptance Criteria:**
- [x] Sections render with formatting.
- [x] Sources visible; clickable.
- [x] TOC navigates to sections.
- [x] Download buttons work.
- [x] Responsive; readable on tablet/mobile (Phase 2).

**Estimated Effort:** 14 hours

---

### T4.5: Dashboard / Home Page (3 SP)
**Owner:** Frontend  
**Depends On:** T4.1  
**Description:**
- Landing page: "Get Started" button → Upload page.
- "How It Works" explainer (3 steps with icons/graphics).
- "Example Problem" button → pre-fill sample problem.
- (Phase 2) "My Reports" section (if user auth added).

**Acceptance Criteria:**
- [x] Landing page renders.
- [x] Get Started button navigates.
- [x] Example problem works.
- [x] Responsive design.

**Estimated Effort:** 8 hours

---

### T4.6: Frontend Styling & UX Polish (4 SP)
**Owner:** Frontend / Design  
**Depends On:** T4.2, T4.3, T4.4, T4.5  
**Description:**
- Apply consistent styling (Tailwind CSS or styled-components).
- Color scheme: government-friendly (blues, grays, high contrast).
- Typography: clear, readable (14px body, 20px headings).
- Spacing: consistent margins/padding.
- Dark mode support (optional Phase 2).
- Accessibility: WCAG AA compliant (alt text, keyboard nav).

**Acceptance Criteria:**
- [x] Design consistent across pages.
- [x] Responsive on mobile (Phase 2).
- [x] Color contrast ≥4.5:1.
- [x] Keyboard navigation works.

**Estimated Effort:** 12 hours

---

## Workstream 5: Reporting & Export (1.5 Weeks, 15 SP)

### T5.1: JSON Report Model (2 SP)
**Owner:** Backend  
**Depends On:** T2.3  
**Description:**
- Define Pydantic model: Report (sections, scores, metadata).
- Section model: title, content, sources (list of {title, url, confidence}).
- Score model: feasibility, cost, impact, risk, sustainability, composite.
- Validation: all fields required; numeric ranges enforced.

**Acceptance Criteria:**
- [x] Model validates reports correctly.
- [x] Serializes to JSON.
- [x] Deserializes from JSON.

**Estimated Effort:** 4 hours

---

### T5.2: PDF Export (5 SP)
**Owner:** Backend  
**Depends On:** T5.1  
**Description:**
- Create Jinja2 HTML template for report.
- Use wkhtmltopdf or Weasyprint to render HTML → PDF.
- Include header (logo, title), footer (date, page numbers), sections with styling.
- Embed source links as footnotes or bibliography.
- Test PDF generation; ensure pagination correct.

**Acceptance Criteria:**
- [x] PDF generated from JSON report.
- [x] Formatting correct; all content visible.
- [x] Links and citations preserved.
- [x] File size <5 MB.

**Estimated Effort:** 12 hours

---

### T5.3: Markdown Export (2 SP)
**Owner:** Backend  
**Depends On:** T5.1  
**Description:**
- Create Markdown formatter for report.
- Output: structured Markdown with headings, lists, tables, links.
- Include bibliography in APA format.
- Test: render in GitHub, verify formatting.

**Acceptance Criteria:**
- [x] Markdown valid; renders correctly on GitHub.
- [x] All content preserved.
- [x] Links functional.

**Estimated Effort:** 4 hours

---

### T5.4: Report Storage & Retrieval (2 SP)
**Owner:** Backend  
**Depends On:** T5.1, T5.2, T5.3, T3.3  
**Description:**
- Store generated reports in S3 (or local FS for POC).
- Index: report_id → S3 path.
- Implement cleanup: archive old reports after 30 days (Phase 2).

**Acceptance Criteria:**
- [x] Reports stored persistently.
- [x] Retrieval works via API.
- [x] S3 paths logged.

**Estimated Effort:** 4 hours

---

## Workstream 6: Data & Datasets (1 Week, 12 SP)

### T6.1: Dataset Curation & Preparation (5 SP)
**Owner:** Data  
**Depends On:** None  
**Description:**
- Identify 20–30 high-quality sources: research papers, case studies, startup info.
- Focus on 2–3 sectors (transport, waste, water).
- Create source CSV: title, authors, year, URL, type, abstract/summary, metadata (geo, sector).
- Validate data quality; ensure URLs valid.

**Acceptance Criteria:**
- [x] Dataset CSV with 20+ sources.
- [x] All URLs verified.
- [x] Metadata complete (type, sector, geo).
- [x] Document list in README.

**Estimated Effort:** 12 hours

---

### T6.2: Data Model Documentation (3 SP)
**Owner:** Backend / Data  
**Depends On:** T1.3, T6.1  
**Description:**
- Create `data-model.md`: describe all tables, fields, relationships.
- Include ER diagram (Mermaid or PlantUML).
- Document data types, constraints, indexes.
- Example queries for common operations.

**Acceptance Criteria:**
- [x] All entities documented.
- [x] ER diagram clear.
- [x] Example queries provided.

**Estimated Effort:** 6 hours

---

### T6.3: Schema Examples & Sample Data (2 SP)
**Owner:** Data  
**Depends On:** T6.1  
**Description:**
- Create example records for each entity (JSON + CSV).
- Include sample research papers, case studies, startup profiles.
- Use in documentation + tests.

**Acceptance Criteria:**
- [x] Example data realistic.
- [x] Covers all document types.
- [x] Available in `datasets/` folder.

**Estimated Effort:** 4 hours

---

## Workstream 7: Integration & Testing (1.5 Weeks, 20 SP)

### T7.1: End-to-End Integration Tests (5 SP)
**Owner:** QA  
**Depends On:** T3.1, T3.2, T3.3, T4.1, T5.1  
**Description:**
- Test full flow: upload problem → analyze → fetch report → export PDF/Markdown.
- Use test dataset (5 problems).
- Verify: report generated, scores computed, exports valid.
- Test error cases: invalid input, API timeouts, missing data.

**Acceptance Criteria:**
- [x] E2E tests pass.
- [x] All export formats valid.
- [x] Error cases handled.
- [x] Latency <5 min.

**Estimated Effort:** 12 hours

---

### T7.2: Performance Benchmarking (3 SP)
**Owner:** Backend / QA  
**Depends On:** T7.1  
**Description:**
- Benchmark latency: each agent, vector search, LLM call.
- Identify bottlenecks.
- Optimize: caching, indexing, batch operations.
- Document results in `PERFORMANCE.md`.

**Acceptance Criteria:**
- [x] Latency targets met (<5 min).
- [x] Bottlenecks identified + documented.
- [x] Optimization results logged.

**Estimated Effort:** 8 hours

---

### T7.3: Manual Testing & UAT (5 SP)
**Owner:** Product / QA  
**Depends On:** T7.1  
**Description:**
- Test with real use cases (5–10 problem scenarios).
- User walkthrough: can officer use UI without guidance?
- Verify outputs: are recommendations sensible? Are scores interpretable?
- Collect feedback; document issues.

**Acceptance Criteria:**
- [x] UAT passed with 3–5 users.
- [x] Issues logged (blockers vs. nice-to-haves).
- [x] Feedback incorporated into Phase 2 backlog.

**Estimated Effort:** 12 hours

---

### T7.4: Documentation & Runbooks (4 SP)
**Owner:** Tech Writer / DevOps  
**Depends On:** All prior tasks  
**Description:**
- Create README: project overview, setup, running locally.
- Create ARCHITECTURE.md: component overview, data flow diagrams.
- Create AGENTS.md: agent descriptions, prompts, outputs.
- Create CONTRIBUTING.md: dev workflow, code standards, PR process.
- Create OPERATIONS.md: deployment, monitoring, troubleshooting.

**Acceptance Criteria:**
- [x] All docs comprehensive + accurate.
- [x] Setup instructions tested (new dev can run locally in <1 hour).
- [x] Diagrams clear.

**Estimated Effort:** 10 hours

---

### T7.5: Demo Preparation (3 SP)
**Owner:** Product  
**Depends On:** T7.1, T7.4  
**Description:**
- Create demo script: 10–15 minute walkthrough of features.
- Prepare sample data + problems.
- Test demo flow; time it; ensure <5 min report generation.
- Record screen demo (optional; for async sharing).

**Acceptance Criteria:**
- [x] Demo script finalized.
- [x] Sample data tested.
- [x] Latency acceptable for live demo.
- [x] Demo video (optional) recorded.

**Estimated Effort:** 6 hours

---

## Summary: Task Dependencies & Parallelization

### Dependency Graph

```
T1.1 (FastAPI Scaffold)
  ├─> T1.2 (Env Setup)
  ├─> T1.3 (DB Models)
  │     ├─> T1.4 (LLM Integration)
  │     ├─> T1.5 (Vector DB)
  │     ├─> T1.6 (Ingestion Pipeline)
  │     │     ├─> T2.2 (Retrieval Agent)
  │     │     └─> T3.5 (Admin API)
  │     └─> T2.1 (Problem Analyzer)
  │           ├─> T2.2 (Retrieval Agent)
  │           └─> T2.4 (Orchestrator)
  └─> T1.7 (Testing)

Parallel Tracks (can start after T1.1 + T1.3):
  - Workstream 2: Agents (T2.1, T2.2, T2.3, T2.4)
  - Workstream 3: API (T3.1, T3.2, T3.3, T3.4)
  - Workstream 4: Frontend (T4.1, T4.2, T4.3, T4.4, T4.5, T4.6)
  - Workstream 6: Data (T6.1, T6.2, T6.3)
  
Final Integration:
  - Workstream 5: Reporting (T5.1, T5.2, T5.3, T5.4)
  - Workstream 7: Integration & Testing (T7.1, T7.2, T7.3, T7.4, T7.5)
```

### Recommended Parallelization

**Phase 1 (Week 1):** Backend foundation in series (T1.1 → T1.2 → T1.3 → T1.4 → T1.5).  
**Phase 2 (Week 2):** Parallel: Agents (T2.1-4), API (T3.1-5), Frontend (T4.1-6), Data (T6.1-3).  
**Phase 3 (Week 3):** Reporting (T5.1-4) + Integration tests (T7.1).  
**Phase 4 (Week 4):** Perf tuning (T7.2), UAT (T7.3), Docs (T7.4), Demo (T7.5).  

---

## Estimation Summary

| Workstream | Total SP | Story Points | Days (8h/day) | Team Size |
|---|---|---|---|---|
| **WS1: Backend** | 4w | 40 | 20 | 2 people |
| **WS2: Agents** | 3w | 35 | 17.5 | 2 people |
| **WS3: API** | 2w | 25 | 12.5 | 1 person |
| **WS4: Frontend** | 2w | 28 | 14 | 2 people |
| **WS5: Reporting** | 1.5w | 15 | 7.5 | 1 person |
| **WS6: Data** | 1w | 12 | 6 | 1 person |
| **WS7: Integration** | 1.5w | 20 | 10 | 2 people |
| **TOTAL** | **4 weeks** | **175 SP** | **87.5 days** | **6–8 people (parallel)** |

**Timeline:** 4 weeks with 6–8 engineers (parallel workstreams).

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| LLM API rate limits | Medium | High | Implement queue, batch requests, fallback. |
| Vector search slow | Low | Medium | Optimize FAISS index, profile, cache. |
| PDF export failures | Low | Medium | Test wkhtmltopdf; have Weasyprint fallback. |
| Scope creep | High | High | Enforce POC constraints; defer Phase 2 features. |
| Pilot delays | Medium | High | Secure pilot partners early; define success criteria upfront. |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-09 | Tech Team | Initial task breakdown; 175 SP, 4-week timeline. |

---

**Last Updated:** 2026-06-09  
**Target Completion:** 2026-07-07 (POC ready for pilot)

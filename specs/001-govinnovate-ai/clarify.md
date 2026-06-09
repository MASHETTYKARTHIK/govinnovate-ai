# GovInnovate AI — Clarification Q&A (001-govinnovate-ai)

## Purpose

This document captures structured Q&A to fill gaps in the specification and validate assumptions before technical planning begins. Questions are organized by domain.

---

## Product & Strategy

### Q1: What is the primary differentiator from existing solutions?
**Status:** Clarified  
**Answer:** 
- Most platforms (Ideascale, SurveySparrow) focus on crowdsourced ideas *from* citizens.
- GovInnovate AI focuses on *recommending* proven external solutions to government.
- Unique: AI-synthesis of global research + case studies + vendors into a *single unified report* with scores and roadmaps.
- Secondary: Transparency (all sources linked) + government-friendly (no jargon) + audit-able (all decisions logged).

### Q2: Are we positioning as B2B (government customers) or B2G (government as a service)?
**Status:** Clarified  
**Answer:**
- **POC/Pilot:** B2G freemium (free tier for pilot agencies; paid optional consulting).
- **Phase 2+:** SaaS subscription + professional services (implementation consulting, custom datasets, integrations).
- **Revenue model:** Per-report pricing OR agency subscription (to be tested with pilots).

### Q3: What is our go-to-market strategy?
**Status:** Clarified  
**Answer:**
- **Phase 1:** Direct outreach to 2–3 "champion" city/state governments.
- **Phase 2:** Partner with NGOs, think tanks, and development organizations (UNDP, World Bank) for distribution.
- **Phase 3:** Marketplace + third-party resellers (Zoom, government consultants).

### Q4: Should we build for global governments or focus on one country first?
**Status:** Clarified  
**Answer:**
- **POC/Pilot:** India-focused (language, case studies, regulatory context, pilot partners available).
- **Phase 2:** Expand to South Asia, SE Asia (adapt language, add local case studies).
- **Phase 3:** Global expansion (localization, regulatory adapts, multi-language).

---

## Technical Foundations

### Q5: Should we use open-source LLMs or proprietary APIs?
**Status:** Clarified  
**Answer:**
- **POC:** Proprietary APIs (OpenAI/Anthropic) — faster, more reliable, lower operational overhead.
- **Phase 2:** Multi-provider (OpenAI + Anthropic fallback + evaluate open-source options like Llama).
- **Phase 3:** On-premise option for governments concerned about data sovereignty.

### Q6: Vector DB: FAISS vs. Pinecone vs. Milvus?
**Status:** Clarified  
**Answer:**
- **POC:** FAISS (in-memory, local, no external dependency).
- **Phase 2:** Milvus (open-source, managed, scales well) or Pinecone (managed, less ops).
- **Decision:** Milvus preferred for cost & control; Pinecone if we need managed SaaS.

### Q7: How do we ensure reproducibility of embeddings?
**Status:** Clarified  
**Answer:**
- Lock embedding model version (e.g., `text-embedding-3-large` from OpenAI).
- Store model name + version in metadata for every chunk.
- If we update model, we re-embed entire corpus (triggered manually, logged).
- Use semantic versioning: major change = full re-embedding; minor = no re-embedding required.

### Q8: Should we cache LLM responses?
**Status:** Clarified  
**Answer:**
- **POC:** Simple caching: if same problem statement submitted, return cached report (24h TTL).
- **Phase 2:** Semantic caching (similar problems → reuse partial results) + Redis.
- **Implementation:** Cache key = hash(problem_text + dataset_version); invalidate on dataset update.

---

## Data & Datasets

### Q9: What data sources should we prioritize for ingestion?
**Status:** Clarified  
**Answer:**
- **POC:** Academic papers (Google Scholar, SSRN), government reports (National Bureau, World Bank), case study databases (Project Drawdown, Sustainable Development Solutions Network).
- **Phase 2:** Real-time feeds (ArXiv, World Bank API), news sources, startup databases (Crunchbase API).
- **Curation:** Human-curated priority dataset (50–100 docs) for POC; expand to 1000+ by Phase 2.

### Q10: How do we handle PII and sensitive data in documents?
**Status:** Clarified  
**Answer:**
- Scan all ingested documents for PII patterns (email, phone, SSN, ID numbers, names if flagged).
- Redact PII in extracted chunks; flag document as "contains sensitive data".
- User must acknowledge before viewing flagged documents.
- Log PII detection events (audit trail).

### Q11: How do we version datasets and maintain reproducibility?
**Status:** Clarified  
**Answer:**
- Every dataset has version (e.g., "transport_v1.0", "waste_v2.1").
- Immutable dataset snapshots: once frozen, cannot be modified (only new version created).
- Reports include: dataset version used, snapshot date, embedding model version.
- Enables re-running a report with different dataset versions to compare impact.

### Q12: Should we ingest real-time data (e.g., traffic sensors, weather)?
**Status:** Clarified  
**Answer:**
- **POC:** No real-time data; static datasets only.
- **Phase 2:** Optional integrations (GIS, traffic, water supply data) for impact predictions.
- **Phase 3:** Marketplace for third-party data sources (weather, economic, health data).

---

## Agents & AI/ML

### Q13: How many agents do we actually need for POC?
**Status:** Clarified  
**Answer:**
- **POC minimum (3 agents):**
  1. **Problem Analyzer:** Normalize problem; extract tags/KPIs.
  2. **Retrieval Coordinator:** Call vector search; rank results.
  3. **Report Generator:** Synthesize findings into sections; compute scores.
- **Phase 2 (add 5 more):** Research Finder, Case Study Finder, Startup Finder, Policy Advisor, Cost Estimator, Impact Estimator (specialized agents).

### Q14: Should agents be sequential or parallel?
**Status:** Clarified  
**Answer:**
- **POC:** Sequential (simpler orchestration; single-threaded).
- **Phase 2:** Parallel where independent (Research + Cases + Startups in parallel); sequential where dependent.
- **Implementation:** Async/await in Python; Celery + Redis for distributed task queue.

### Q15: How do we handle agent failures (e.g., LLM API timeout)?
**Status:** Clarified  
**Answer:**
- **POC:** Simple retry (3x with exponential backoff); fail-fast if all retries exhausted.
- **Phase 2:** Fallback LLM (if OpenAI down, try Anthropic); partial report generation (skip failed agent, continue others).
- **User experience:** Report status "partial" if some sections missing; allow user to retry or export what's available.

### Q16: How do we prevent LLM hallucinations in outputs?
**Status:** Clarified  
**Answer:**
- Grounding: all synthesis must reference retrieved context (citations required).
- Prompt design: few-shot examples showing correct citations.
- Post-processing: detect claims not in context; flag as "inferred" or filter.
- Monitoring: weekly audit of top 10 reports for hallucinations; adjust prompts if >5% detected.

### Q17: Should we use retrieval-augmented generation (RAG) or fine-tuning?
**Status:** Clarified  
**Answer:**
- **POC & Phase 2:** RAG (simpler, faster to iterate, no fine-tuning cost).
- **Phase 3:** Evaluate fine-tuning if RAG retrieval quality plateaus.
- **Rationale:** RAG allows quick dataset updates without retraining; better for government (transparency of sources).

---

## User Experience & Interfaces

### Q18: Should we build a web UI or CLI for POC?
**Status:** Clarified  
**Answer:**
- **POC:** Simple web UI (single-page, no complex navigation) + optional CLI (for demo/testing).
- **Implementation:** React for UI; Streamlit or FastAPI for CLI; both call same backend API.

### Q19: What's the minimum viable dashboard?
**Status:** Clarified  
**Answer:**
- **POC Dashboard:**
  - Upload page: text input + submit.
  - Results page: problem summary + evidence cards (research, cases, startups) + scoring + download.
  - No user accounts, no saved reports (for POC).
- **Phase 2:** Add saved reports, user accounts, export history, admin panel.

### Q20: How do we present uncertainty and confidence in recommendations?
**Status:** Clarified  
**Answer:**
- Every recommendation includes: confidence level (0–100%), evidence count (# sources), evidence strength (strong/moderate/exploratory).
- Visualized: confidence score as progress bar; color-coded (green >70%, yellow 40–70%, red <40%).
- Footnote: "Based on N research papers and M case studies from geographic regions X, Y, Z."
- User tooltip: "This recommendation has moderate confidence due to limited local data; validate with local experts."

### Q21: Should we support multiple languages in POC?
**Status:** Clarified  
**Answer:**
- **POC:** English only (both UI + content).
- **Phase 2:** Hindi + regional language support (India focus).
- **Phase 3:** Multi-language (French, Spanish, Bahasa, etc. for global expansion).

---

## Evaluation & Metrics

### Q22: How do we evaluate retrieval quality?
**Status:** Clarified  
**Answer:**
- **POC:** Human evaluation on 20 test problems; domain experts rate retrieved docs for relevance (binary: relevant/not relevant).
- **Metric:** Precision@5 (fraction of top 5 docs relevant) — target ≥60%.
- **Phase 2:** Build held-out evaluation set (100 test problems); continuous monitoring.

### Q23: How do we measure impact in pilots?
**Status:** Clarified  
**Answer:**
- **Pilot KPIs:**
  - Time saved per decision: (traditional research time) - (time using GovInnovate AI).
  - Decision quality: % of recommendations actually implemented / % of recommendations seriously considered.
  - Cost: cost of using platform vs. value of accelerated implementation.
  - Satisfaction: NPS from government users.
- **Measurement:** Pre/post surveys; usage logs; follow-up at 6-month post-implementation.

### Q24: How do we handle "wrong" or "bad" recommendations?
**Status:** Clarified  
**Answer:**
- Feedback loop: users can flag recommendations as "not applicable" or "already tried".
- Feedback logged and reviewed weekly (signal for dataset or scoring issues).
- If pattern detected (e.g., particular recommendation consistently rated poorly), investigate cause and adjust ranking/prompts.
- Transparency: publish feedback statistics (% of recommendations rated negatively) in quarterly reports.

---

## Operations & Deployment

### Q25: What's the minimal infrastructure for POC?
**Status:** Clarified  
**Answer:**
- Single cloud instance (AWS EC2, GCP Compute, Azure VM): t3.medium or equivalent.
- PostgreSQL (managed RDS) for metadata; local FAISS for vectors.
- S3 for document storage + logs.
- LLM API (OpenAI) — pay-as-you-go, no infrastructure needed.
- Total POC cost: ~$500–800/month.

### Q26: How do we monitor LLM token usage and cost?
**Status:** Clarified  
**Answer:**
- Log every LLM API call: model, tokens_input, tokens_output, cost.
- Aggregate daily: cost per report, cost per agent, token efficiency.
- Alert: if daily cost exceeds $50 (POC threshold) or if latency exceeds 5 min.
- Phase 2: implement token budgeting per agent (e.g., max 2000 tokens per agent call).

### Q27: How often should we re-index the vector database?
**Status:** Clarified  
**Answer:**
- **POC:** Manual re-indexing on dataset updates (not frequent; ~1/week if any).
- **Phase 2:** Automated incremental indexing (new docs added to index without full rebuild).
- **Versioning:** Each index snapshot tagged with dataset version (enables rollback if needed).

### Q28: What's the disaster recovery plan?
**Status:** Clarified  
**Answer:**
- **POC:** Daily backup of documents + metadata (S3 versioning); recoverable in <1 hour.
- **Phase 2 SLA:** RTO 1 hour, RPO 1 day; multi-region standby replica.
- **Automation:** Terraform for infra; can redeploy entire system in ~30 min.

---

## Regulatory & Compliance

### Q29: Do we need specific government approvals for POC?
**Status:** Clarified  
**Answer:**
- **POC:** No formal approval needed (pilot with willing agencies, internal tool).
- **Phase 2:** Depends on country:
  - **India:** Possible registration as "GovTech" service under e-Governance policy; data handling per India Data Protection Bill (draft).
  - **Others:** Regulatory review varies by country.
- **Action:** Consult with legal/compliance early in Phase 2.

### Q30: How do we handle data residency and privacy?
**Status:** Clarified  
**Answer:**
- **POC:** No formal requirement; data stored on cloud (AWS/GCP default region).
- **Phase 2:** Offer data residency options (India-only storage) for government contracts.
- **Privacy:** PII detection + redaction; compliance with GDPR (if EU users), India Data Protection Bill (if India users).
- **Audit:** Immutable logs of all data access; exportable for government audit.

---

## Roadmap & Priorities

### Q31: What's the priority sequence for Phase 2 features?
**Status:** Clarified  
**Answer:**
1. **High Priority:** Multi-agent architecture, advanced costing, expanded datasets (1000+ docs).
2. **Medium Priority:** RBAC, audit workflows, integrations (GIS, sensors), advanced reporting.
3. **Lower Priority:** Mobile app, marketplace, international languages.
- **Rationale:** Pilot feedback determines actual prioritization; adjust based on user needs.

### Q32: Should we plan for geographic expansion or vertical specialization first?
**Status:** Clarified  
**Answer:**
- **Phase 2:** Vertical specialization (master 3–4 sectors: transport, waste, health, education).
- **Phase 3:** Geographic expansion (replicate stack to other countries with localized data).
- **Rationale:** Depth over breadth; build credibility in core sectors before expanding.

---

## Assumptions to Validate in Pilot

### A1: Government officers find plain-text problem input intuitive.
**Validation Method:** Usability testing with 3–5 pilot users; iterate UI if <70% find it intuitive.

### A2: Time savings (60–80% reduction) justify adoption.
**Validation Method:** Track time-on-task in pilot; measure against baseline (traditional research).

### A3: Evidence-backed recommendations increase adoption likelihood.
**Validation Method:** Track % of POC recommendations that proceed to pilot/implementation.

### A4: LLM-generated reports can be trusted by government stakeholders.
**Validation Method:** NPS + open feedback; audit for hallucinations.

### A5: 50–100 documents are sufficient for 3 sectors (POC).
**Validation Method:** Coverage analysis; if retrieval precision drops below 60%, expand dataset.

### A6: Scoring framework (5 dimensions) is actionable for decision-makers.
**Validation Method:** User feedback; iterate scoring weights if not intuitive.

---

## Open Questions (TBD)

| Question | Owner | Target Resolution | Impact |
|----------|-------|---|---|
| Exact pilot partner identification? | Business Dev | 2026-06-15 | Blocks pilot start. |
| Preferred embedding model + version lock? | ML/Data | 2026-06-12 | Blocks vector DB setup. |
| Final dataset sources + curation process? | Data | 2026-06-20 | Blocks indexing. |
| LLM model selection (GPT-4 vs. Claude)? | ML | 2026-06-12 | Affects cost + quality; should evaluate both. |
| Minimum viable admin features (Phase 2)? | Product | 2026-06-23 | Low priority for POC; clarify for Phase 2. |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-09 | Product Team | Initial Q&A compiled from spec review. |

---

**Last Updated:** 2026-06-09  
**Next Review:** 2026-06-23 (after initial POC discussions with pilot partners)

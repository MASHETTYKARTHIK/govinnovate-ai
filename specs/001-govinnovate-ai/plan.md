# GovInnovate AI — Technical Blueprint & Architecture (001-govinnovate-ai)

## Overview

This document specifies the technology stack, system architecture, data flow, and deployment strategy for GovInnovate AI POC and Phase 2 production.

---

## Technology Stack

### POC Stack (2–4 weeks)

| Layer | Component | Rationale |
|-------|-----------|-----------|
| **Language** | Python 3.10+ | Fast iteration; strong ML/AI libraries; government IT comfort. |
| **Backend** | FastAPI | Async support; auto-documentation (OpenAPI); modern Python framework. |
| **Frontend** | React 18 + TypeScript | Modern UX; componentization; team familiarity. |
| **LLM** | OpenAI GPT-4 API | State-of-the-art; reliable; low operational overhead. |
| **Embeddings** | OpenAI `text-embedding-3-large` | Fixed model; high quality; reproducible. |
| **Vector DB** | FAISS (local) | In-memory, no external dep; sufficient for POC (<100k embeddings). |
| **Metadata DB** | PostgreSQL 14 | Structured data; ACID compliance; optional for POC (SQLite fallback). |
| **Storage** | Local filesystem (POC) / S3 (Phase 2) | Documents, PDFs, exports. |
| **Caching** | Python memory (POC) / Redis (Phase 2) | LLM response cache, retrieval cache. |
| **Reporting** | Jinja2 + wkhtmltopdf | PDF generation from templates. |
| **Testing** | pytest + Pytest-asyncio | Unit tests, integration tests. |
| **Linting** | Black + Flake8 + isort | Code quality enforcement. |
| **Logging** | Python logging + structlog | Structured JSON logs. |
| **Monitoring** | Print statements (POC) / Prometheus + Grafana (Phase 2) | Metrics and alerting. |
| **Deployment** | Docker (optional POC) + Docker Compose | Reproducible environments. |

### Phase 2 Stack (Production Hardening)

| Layer | Component | Change Rationale |
|-------|-----------|---|
| **Backend** | FastAPI + Uvicorn (async workers) | Horizontal scaling. |
| **Async Tasks** | Celery + Redis | Background jobs (ingestion, re-indexing). |
| **Vector DB** | Milvus (self-hosted) or Pinecone (managed) | Scalable; persistent; vector-only optimization. |
| **Metadata DB** | RDS PostgreSQL (AWS managed) | High availability; automated backups. |
| **Storage** | S3 (AWS) or GCS (Google) | Managed object storage; versioning. |
| **Frontend** | React 18 + Redux Toolkit + TypeScript | State management; scalable. |
| **Auth** | OAuth2 (Auth0) or AWS Cognito | Multi-tenant support; RBAC. |
| **Monitoring** | Prometheus + Grafana + ELK Stack | Full observability. |
| **Infrastructure** | Kubernetes (EKS/AKS) + Terraform | Cloud-native, infrastructure-as-code. |
| **CI/CD** | GitHub Actions or GitLab CI | Automated testing, deployment. |

### Phase 3 Stack (Ecosystem & Scale)

| Layer | Component | Change Rationale |
|-------|-----------|---|
| **API Gateway** | Kong or AWS API Gateway | Rate limiting, RBAC, multi-tenant. |
| **LLM** | Multi-provider (OpenAI + Anthropic + local LLaMA) | Redundancy; cost optimization; on-prem option. |
| **Data Pipeline** | Airflow or Prefect | Orchestrated ingestion; scheduled re-indexing. |
| **Analytics** | Segment + Mixpanel | User behavior tracking; product insights. |
| **Search** | Elasticsearch (for keyword search, combined with vector search) | Hybrid search; faceted navigation. |

---

## System Architecture

### High-Level Component Diagram (POC)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client Layer                                 │
│  ┌──────────────────┐            ┌──────────────────┐               │
│  │  React Frontend  │            │   CLI / Scripts  │               │
│  │  (Upload, View   │  ◄────────► (for testing)    │               │
│  │   Report)        │            │                  │               │
│  └──────────────────┘            └──────────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
            │ HTTP/JSON                    │ API calls
            ▼                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     API Layer (FastAPI)                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ POST /api/v1/problems                                        │  │
│  │ POST /api/v1/problems/{id}/analyze                           │  │
│  │ GET /api/v1/reports/{id}                                     │  │
│  │ POST /api/v1/search                                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
            │ Internal calls
            ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Orchestration Layer (Agent Coordinator)                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ 1. Problem Analyzer Agent (normalize + tag)                  │  │
│  │ 2. Retrieval Coordinator (vector search)                     │  │
│  │ 3. Report Generator Agent (synthesize + score)               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
            │ ▼ API calls
┌──────────────────────────────────────────────────────────────────────┐
│                    AI / LLM Layer                                    │
│  ┌──────────────────────┐      ┌──────────────────────┐              │
│  │  OpenAI GPT-4 API    │      │  Prompt Templates    │              │
│  │  (gpt-4-turbo)       │      │  (Jinja2, versioned) │              │
│  └──────────────────────┘      └──────────────────────┘              │
└──────────────────────────────────────────────────────────────────────┘
            │ Vector search / context retrieval
            ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    RAG Layer                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Ingestion Pipeline:  Extract → Chunk → Embed → Index         │ │
│  │ Retrieval Pipeline:  Query → Embed → Search → Rank           │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
      │                    │                   │                   │
      ▼                    ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Document Store   │ │ Vector Index     │ │ Metadata DB      │ │ Cache Layer      │
│ (local FS / S3)  │ │ (FAISS)          │ │ (PostgreSQL)     │ │ (Python memory)  │
│ - PDFs           │ │ - Embeddings     │ │ - Doc metadata   │ │ - LLM responses  │
│ - CSVs           │ │ - Chunk refs     │ │ - Chunk info     │ │ - Retrieval res. │
│ - HTML           │ │                  │ │ - Scores         │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                    Output Layer                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │ PDF Export       │  │ Markdown Export  │  │ JSON API         │   │
│  │ (wkhtmltopdf)    │  │ (plain text)     │  │ (structured)     │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram (POC Single Report Generation)

```
User Input:
"Traffic congestion in Hyderabad"
        │
        ▼
┌──────────────────────────────────┐
│ API: POST /problems              │
│ - Store problem text             │
│ - Assign problem_id              │
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│ Agent 1: Problem Analyzer        │
│ INPUT: {text, id}                │
│ OUTPUT: {title, tags, KPIs, ...} │
│ LLM: Extract structure           │
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│ Agent 2: Retrieval Coordinator   │
│ INPUT: {tags, KPIs}              │
│ - Build search query             │
│ - Embed query                    │
│ - Vector search FAISS            │
│ OUTPUT: top 5 research + cases + │
│         startups (ranked)        │
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│ Agent 3: Report Generator        │
│ INPUT: {retrieved context, tags} │
│ - Build LLM prompt (system +     │
│   few-shot + retrieved context)  │
│ - Call LLM (GPT-4)               │
│ - Parse output into sections     │
│ - Compute scores                 │
│ OUTPUT: report JSON              │
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│ Export Layer                     │
│ - JSON → PDF (Jinja2 template)   │
│ - JSON → Markdown                │
│ - Store report in S3 / local FS  │
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│ API Response: GET /reports/{id}  │
│ - Return JSON + download links   │
└──────────────────────────────────┘
```

### Phase 2 Architecture (Microservices)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Load Balancer (AWS ALB)                           │
└─────────────────────────────────────────────────────────────────────┘
        │
        ├─────────────────┬─────────────────┬─────────────────┐
        ▼                 ▼                 ▼                 ▼
┌──────────────┐   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ API Server 1 │   │ API Server 2  │  │ API Server 3 │  │ ... N        │
│ (FastAPI)    │   │ (FastAPI)     │  │ (FastAPI)    │  │              │
│ Async/Uvicorn│   │ Async/Uvicorn│  │ Async/Uvicorn│  │ (Kubernetes) │
└──────────────┘   └──────────────┘  └──────────────┘  └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   Redis      │  │   RDS        │  │   S3         │
    │   (cache +   │  │  PostgreSQL  │  │  (documents) │
    │    queue)    │  │  (metadata)  │  │              │
    └──────────────┘  └──────────────┘  └──────────────┘
        │
    ┌───┴────────────┐
    ▼                ▼
┌──────────────┐  ┌──────────────┐
│ Celery Task  │  │ Ingestion    │
│ Workers (N)  │  │ Pipeline     │
│              │  │ (ETL)        │
└──────────────┘  └──────────────┘
    │                   │
    └───────┬───────────┘
            ▼
        ┌──────────────┐
        │   Milvus     │
        │   (vector DB)│
        │   (managed   │
        │    cluster)  │
        └──────────────┘
```

---

## API Specification (POC)

### 1. Create Problem

**Endpoint:** `POST /api/v1/problems`

**Request:**
```json
{
  "title": "Traffic Congestion in Hyderabad",
  "text": "Peak-hour gridlock on arterial roads; high transit times; demand-supply mismatch.",
  "location": "Hyderabad, India",
  "budget_min": 1000000,
  "budget_max": 3000000,
  "sector_tags": ["transport", "urban-planning"],
  "timeframe_months": 12
}
```

**Response (201 Created):**
```json
{
  "problem_id": "prob_12345abc",
  "status": "created",
  "created_at": "2026-06-09T10:30:00Z",
  "next_step": "/api/v1/problems/prob_12345abc/analyze"
}
```

### 2. Analyze Problem

**Endpoint:** `POST /api/v1/problems/{problem_id}/analyze`

**Request:**
```json
{
  "priority": "normal",
  "agents": ["problem-analyzer", "retrieval-coordinator", "report-generator"],
  "max_latency_seconds": 300
}
```

**Response (202 Accepted):**
```json
{
  "analysis_job_id": "job_67890def",
  "status": "queued",
  "estimated_completion": "2026-06-09T10:40:00Z",
  "poll_url": "/api/v1/jobs/job_67890def"
}
```

### 3. Get Report

**Endpoint:** `GET /api/v1/reports/{report_id}`

**Response (200 OK):**
```json
{
  "report_id": "report_xyz789",
  "problem_id": "prob_12345abc",
  "status": "complete",
  "created_at": "2026-06-09T10:40:00Z",
  "sections": {
    "analysis": {
      "title": "Problem Analysis",
      "content": "...",
      "sources": [
        {"title": "Study X", "url": "...", "score": 0.92}
      ]
    },
    "cases": {...},
    "research": {...},
    "startups": {...},
    "policy": {...},
    "roadmap": {...},
    "cost": {...},
    "impact": {...}
  },
  "scores": {
    "feasibility": 75,
    "cost": 60,
    "impact": 80,
    "risk": 70,
    "sustainability": 65,
    "composite": 74
  },
  "export_urls": {
    "pdf": "/api/v1/reports/report_xyz789/export?format=pdf",
    "markdown": "/api/v1/reports/report_xyz789/export?format=md",
    "json": "/api/v1/reports/report_xyz789/export?format=json"
  }
}
```

### 4. Search Knowledge Base

**Endpoint:** `POST /api/v1/search`

**Request:**
```json
{
  "query": "adaptive traffic signal control",
  "filters": {
    "type": ["research", "case_study"],
    "year_min": 2015,
    "geo": ["India", "Asia"]
  },
  "k": 10,
  "search_type": "hybrid"
}
```

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": "doc_001",
      "title": "Adaptive Traffic Signal Control in Urban Settings",
      "authors": ["Smith, J.", "Doe, K."],
      "year": 2021,
      "type": "research",
      "snippet": "Adaptive signal control algorithms improved throughput by 12-18% in trial cities...",
      "relevance_score": 0.94,
      "url": "https://doi.org/10.1016/j.trc.2021.103210",
      "evidence_strength": "strong"
    }
  ],
  "total_results": 1,
  "query_time_ms": 245
}
```

### 5. Export Report

**Endpoint:** `GET /api/v1/reports/{report_id}/export`

**Query Parameters:** `format=pdf|md|json`

**Response:** File download (PDF/Markdown) or JSON payload.

---

## Database Schema (POC)

### Problems Table
```sql
CREATE TABLE problems (
  id UUID PRIMARY KEY,
  user_id VARCHAR (optional for POC),
  title VARCHAR(255),
  text TEXT,
  location VARCHAR(255),
  budget_min DECIMAL,
  budget_max DECIMAL,
  sector_tags JSONB,
  timeframe_months INT,
  normalized_problem JSONB,
  status VARCHAR(50), -- "created", "analyzing", "complete", "error"
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Reports Table
```sql
CREATE TABLE reports (
  id UUID PRIMARY KEY,
  problem_id UUID REFERENCES problems(id),
  status VARCHAR(50),
  sections_json JSONB,
  scores JSONB,
  dataset_version VARCHAR(50),
  embedding_model VARCHAR(100),
  llm_model VARCHAR(100),
  total_tokens INT,
  cost_usd DECIMAL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Documents Table
```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  title VARCHAR(255),
  source_type VARCHAR(50), -- "research", "case_study", "startup", "policy"
  year INT,
  authors JSONB,
  source_url TEXT,
  file_path VARCHAR(500),
  metadata JSONB,
  dataset_version VARCHAR(50),
  ingestion_timestamp TIMESTAMP,
  created_at TIMESTAMP
);
```

### Chunks Table
```sql
CREATE TABLE chunks (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id),
  text TEXT,
  token_count INT,
  embedding_id UUID,
  created_at TIMESTAMP
);
```

### Embeddings Table
```sql
CREATE TABLE embeddings (
  id UUID PRIMARY KEY,
  chunk_id UUID REFERENCES chunks(id),
  model VARCHAR(100),
  dimension INT,
  vector_ref VARCHAR(255), -- reference to FAISS/Milvus
  created_at TIMESTAMP
);
```

### Scores Table
```sql
CREATE TABLE scores (
  id UUID PRIMARY KEY,
  report_id UUID REFERENCES reports(id),
  recommendation_id VARCHAR(255),
  feasibility_score INT,
  cost_score INT,
  impact_score INT,
  risk_score INT,
  sustainability_score INT,
  composite_score INT,
  methodology_version VARCHAR(50),
  created_at TIMESTAMP
);
```

### Agent Logs Table
```sql
CREATE TABLE agent_logs (
  id UUID PRIMARY KEY,
  report_id UUID REFERENCES reports(id),
  agent_name VARCHAR(100),
  input_json JSONB,
  output_json JSONB,
  duration_ms INT,
  token_usage INT,
  error_message TEXT (nullable),
  created_at TIMESTAMP
);
```

---

## Deployment & Infrastructure

### POC Deployment (2–4 weeks)

**Environment:** Single EC2 instance (AWS) or equivalent.

**Setup Steps:**
1. Provision t3.medium EC2 (Ubuntu 22.04).
2. Install Docker & Docker Compose.
3. Clone repo; build backend + frontend images.
4. Launch services: FastAPI backend, React frontend, FAISS vector DB (in-process), SQLite metadata (optional).
5. Configure environment variables (LLM API keys, S3 credentials).
6. Run migrations; seed initial dataset.
7. Deploy via `docker-compose up -d`.

**Monitoring (POC):**
- Logs: stdout to file; basic tail monitoring.
- Health check: simple `/health` endpoint.
- Alerts: none (manual monitoring only).

### Phase 2 Deployment (Production)

**Environment:** AWS EKS or Azure AKS (Kubernetes).

**Infrastructure-as-Code:** Terraform.

**Services:**
- API servers (FastAPI, autoscaling replicas).
- Celery workers (background tasks, autoscaling).
- PostgreSQL RDS (managed, Multi-AZ).
- Redis (ElastiCache, managed).
- Milvus vector DB (self-managed cluster or managed service).
- S3 (managed object storage).

**CI/CD:**
- GitHub Actions: run tests, build images, push to ECR, deploy to EKS.
- Staging environment mirrors production.

**Monitoring:**
- Prometheus (metrics collection).
- Grafana (dashboards).
- CloudWatch (logs + alerts).

---

## Sequencing & Milestones

### Week 1–2 (POC Sprint 1)
- [ ] Backend setup (FastAPI skeleton).
- [ ] FAISS vector DB integration (local).
- [ ] Simple LLM prompt template for "Problem Analyzer" agent.
- [ ] Dataset ingestion pipeline (manual CSV import).

### Week 2–3 (POC Sprint 2)
- [ ] Retrieval pipeline (vector search, ranking).
- [ ] Report generation (JSON structure + export to Markdown).
- [ ] React frontend (upload form, results display).
- [ ] Basic integration tests.

### Week 3–4 (POC Sprint 3)
- [ ] Scoring framework (compute 5 scores).
- [ ] PDF export (Jinja2 templates).
- [ ] Dashboard (summary cards, source links).
- [ ] End-to-end test with real problem.

### Week 4+ (Pilot & Hardening)
- [ ] Feedback from pilot users.
- [ ] Dataset expansion (50+ docs per sector).
- [ ] Advanced prompts + few-shot examples.
- [ ] Performance optimization (latency <5 min).

---

## Performance Targets

### POC Targets
| Metric | Target | Acceptable | Stretch |
|--------|--------|-----------|---------|
| **End-to-End Latency** | ≤ 5 min | ≤ 10 min | ≤ 3 min |
| **Vector Search Latency** | ≤ 500 ms | ≤ 2 sec | ≤ 200 ms |
| **LLM Response Latency** | ≤ 30 sec | ≤ 60 sec | ≤ 15 sec |
| **Report Gen Time** | ≤ 10 sec | ≤ 30 sec | ≤ 5 sec |
| **Throughput** | 1 concurrent report | 2 concurrent | 5 concurrent |

### Phase 2 Production Targets
| Metric | SLA | Monitoring |
|--------|-----|-----------|
| **API Uptime** | 99.9% | CloudWatch + PagerDuty |
| **Latency (p95)** | ≤ 10 sec | Prometheus percentile |
| **Error Rate** | < 0.1% | CloudWatch alarms |
| **Cost per Report** | < $1 | Billing tracking |

---

## Disaster Recovery & Backup

### POC (Minimal)
- **Backup:** Daily S3 backup of documents + metadata (SQLite export if used).
- **Recovery:** Manual restore from S3; ~1 hour downtime acceptable.

### Phase 2 (Production)
- **RTO:** 1 hour (recovery time objective).
- **RPO:** 1 day (recovery point objective).
- **Backups:** Automated daily RDS snapshots + S3 versioning.
- **Failover:** Multi-region standby (warm standby); automated failover via DNS.
- **Testing:** Quarterly disaster recovery drills (restore to test environment).

---

## Cost Estimation

### POC Monthly Cost (Rough)

| Item | Unit Cost | Qty | Total |
|------|-----------|-----|-------|
| EC2 Instance (t3.medium) | $30/mo | 1 | $30 |
| PostgreSQL RDS (optional) | $20/mo | 1 | $20 |
| S3 Storage (documents) | $0.023/GB | 5 GB | $0.12 |
| OpenAI GPT-4 API | $0.03/1K tokens | 1M tokens/mo | $30 |
| Embeddings API | $0.02/1M tokens | 200K tokens/mo | $4 |
| **Total** | | | **~$85/mo** |

### Phase 2 Production Monthly Cost (Estimate)

| Item | Unit Cost | Qty | Total |
|------|-----------|-----|-------|
| EKS (Kubernetes) | $0.10/hour/node | 3 nodes × 730 hrs | $219 |
| RDS PostgreSQL (db.t3.medium) | $0.192/hour | 730 hrs | $140 |
| Milvus (self-managed, 3 nodes) | Similar to compute | 3 × $100 | $300 |
| Redis (ElastiCache) | $0.017/hour | 730 hrs | $12 |
| S3 Storage | $0.023/GB | 100 GB | $2.30 |
| Data Transfer | $0.09/GB | 50 GB | $4.50 |
| OpenAI API (scaled) | $0.03/1K tokens | 100M tokens/mo | $3000 |
| **Total** | | | **~$3,680/mo** |

*(Assumes 10 concurrent users; scales linearly)*

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-09 | Tech Team | Initial blueprint. |

---

**Last Updated:** 2026-06-09  
**Next Review:** 2026-06-23 (after POC Sprint 2)

# Project Chimera — Technical Specification

## 1. Scope
This document defines the technical contracts for Project Chimera:
- Agent-facing API contracts (JSON schemas by example)
- Data model and persistence schema for high-velocity video/content metadata
- Runtime skill interfaces (inputs/outputs only)
No implementation code is defined here.

---

## 2. Glossary
- **Agent**: A decision-making component that plans and triggers skill calls.
- **Skill**: A deterministic capability package invoked by agents at runtime.
- **Workflow**: A sequence of agent actions governed by approvals and policies.
- **HITL**: Human-in-the-loop approval gate for sensitive actions.
- **Contract**: Strict input/output structure for APIs and skills.

---

## 3. API Contracts (JSON)

### 3.1 `POST /v1/trends/fetch`
Fetches and normalizes trend topics for a platform and region.

**Request**
```json
{
  "platform": "youtube",
  "region": "ET",
  "time_window": "24h",
  "limit": 25
}
Response

{
  "request_id": "req_01HT...",
  "platform": "youtube",
  "region": "ET",
  "time_window": "24h",
  "collected_at": "2026-02-05T10:00:00Z",
  "topics": [
    {
      "topic_id": "tpc_001",
      "label": "AI tools for developers",
      "description": "Short summary of the topic",
      "score": 0.92,
      "source": "platform_native",
      "observations": {
        "signal_count": 120,
        "top_hashtags": ["#ai", "#coding"]
      }
    }
  ]
}
Rules

platform MUST be a non-empty string.

region MUST be an ISO country code string.

limit MUST be between 1 and 100.

topics[].score MUST be in range [0.0, 1.0].

3.2 POST /v1/content/drafts
Creates a content draft from an approved trend topic.

Request

{
  "topic_id": "tpc_001",
  "platform": "youtube",
  "content_type": "short_script",
  "tone": "informative",
  "constraints": {
    "max_chars": 1200,
    "avoid_claims_without_sources": true
  }
}
Response

{
  "draft_id": "drf_001",
  "topic_id": "tpc_001",
  "platform": "youtube",
  "content_type": "short_script",
  "created_at": "2026-02-05T10:05:00Z",
  "confidence": 0.78,
  "content": {
    "title": "AI Tools Developers Actually Use",
    "body": "Draft text here...",
    "cta": "Follow for more."
  },
  "status": "DRAFT_CREATED"
}
Rules

Draft creation MUST NOT publish content.

Drafts MUST be versioned if regenerated (see schema).

3.3 POST /v1/reviews/evaluate
Evaluates a content draft against safety/policy rules.

Request

{
  "draft_id": "drf_001",
  "policy_profile": "default",
  "min_confidence_to_autopass": 0.85
}
Response

{
  "review_id": "rev_001",
  "draft_id": "drf_001",
  "evaluated_at": "2026-02-05T10:10:00Z",
  "decision": "REQUIRES_HUMAN_REVIEW",
  "reason_codes": ["LOW_CONFIDENCE"],
  "confidence": 0.78,
  "notes": "Confidence below threshold; human approval required."
}
Decision Enum

APPROVED

REJECTED

REQUIRES_HUMAN_REVIEW

3.4 POST /v1/approvals/human
Records human approval decision for a draft.

Request

{
  "draft_id": "drf_001",
  "review_id": "rev_001",
  "reviewer_id": "usr_123",
  "decision": "APPROVED",
  "comment": "OK to publish."
}
Response

{
  "approval_id": "hap_001",
  "draft_id": "drf_001",
  "review_id": "rev_001",
  "reviewer_id": "usr_123",
  "decision": "APPROVED",
  "recorded_at": "2026-02-05T10:15:00Z"
}
Rules

Approval MUST be required before publishing when review decision is REQUIRES_HUMAN_REVIEW.

3.5 POST /v1/publish/execute
Publishes approved content (abstracted behind a skill).

Request

{
  "draft_id": "drf_001",
  "platform": "youtube",
  "approval_id": "hap_001",
  "schedule_at": "2026-02-05T12:00:00Z"
}
Response

{
  "publish_id": "pub_001",
  "draft_id": "drf_001",
  "platform": "youtube",
  "scheduled_at": "2026-02-05T12:00:00Z",
  "status": "SCHEDULED"
}
Rules

Publish MUST fail if required approval evidence is missing.

Platform integration details are out of scope; publishing is mediated by a skill contract.

4. Data Model (PostgreSQL)
4.1 Entities
trend_topics: normalized topics discovered from sources

trend_observations: supporting signals and metadata for a topic

content_drafts: draft content versions generated for a topic/platform

reviews: automated policy/safety review records

human_approvals: human decision records

publish_jobs: scheduled or executed publish events

agent_status: availability/health signaling for agent social network participation

skill_runs: audit log of skill executions (inputs/outputs references)

4.2 ERD (Mermaid)
Diagram
erDiagram
  trend_topics ||--o{ trend_observations : has
  trend_topics ||--o{ content_drafts : produces
  content_drafts ||--o{ reviews : evaluated_by
  reviews ||--o{ human_approvals : may_require
  content_drafts ||--o{ publish_jobs : published_as
  content_drafts ||--o{ skill_runs : created_via
  publish_jobs ||--o{ skill_runs : executed_via
  agent_status ||--o{ skill_runs : triggers

  trend_topics {
    string topic_id PK
    string platform
    string region
    string label
    string description
    float score
    string source
    datetime collected_at
  }

  trend_observations {
    string observation_id PK
    string topic_id FK
    string key
    string value
  }

  content_drafts {
    string draft_id PK
    string topic_id FK
    string platform
    string content_type
    int version
    float confidence
    string title
    text body
    string cta
    string status
    datetime created_at
  }

  reviews {
    string review_id PK
    string draft_id FK
    string policy_profile
    string decision
    float confidence
    string reason_codes
    text notes
    datetime evaluated_at
  }

  human_approvals {
    string approval_id PK
    string review_id FK
    string draft_id FK
    string reviewer_id
    string decision
    text comment
    datetime recorded_at
  }

  publish_jobs {
    string publish_id PK
    string draft_id FK
    string platform
    string status
    datetime schedule_at
    datetime created_at
  }

  agent_status {
    string agent_id PK
    string state
    datetime last_heartbeat_at
    string status_message
  }

  skill_runs {
    string run_id PK
    string skill_name
    string triggered_by_agent_id
    string input_ref
    string output_ref
    string status
    datetime started_at
    datetime finished_at
  }
4.3 Schema Notes / Constraints
content_drafts.version MUST increment when a draft is regenerated for the same topic/platform/type.

reviews.decision MUST be one of: APPROVED, REJECTED, REQUIRES_HUMAN_REVIEW.

human_approvals MUST reference a review_id and draft_id.

publish_jobs MUST NOT be created unless:

there exists a review record, AND

if required, there exists a human approval record.

skill_runs.input_ref and output_ref SHOULD store references (paths/ids) rather than raw payloads for auditability.

5. Runtime Skill Interfaces (Contracts)
5.1 skill_fetch_trends
Input

{
  "platform": "youtube",
  "region": "ET",
  "time_window": "24h",
  "limit": 25
}
Output

{
  "topics": [
    {
      "topic_id": "tpc_001",
      "label": "string",
      "description": "string",
      "score": 0.0,
      "collected_at": "ISO-8601 datetime"
    }
  ]
}
5.2 skill_generate_draft
Input

{
  "topic_id": "tpc_001",
  "platform": "youtube",
  "content_type": "short_script",
  "tone": "informative",
  "constraints": {
    "max_chars": 1200
  }
}
Output

{
  "draft": {
    "draft_id": "drf_001",
    "title": "string",
    "body": "string",
    "cta": "string",
    "confidence": 0.0
  }
}
5.3 skill_evaluate_policy
Input

{
  "draft_id": "drf_001",
  "policy_profile": "default",
  "min_confidence_to_autopass": 0.85
}
Output

{
  "review": {
    "review_id": "rev_001",
    "decision": "APPROVED|REJECTED|REQUIRES_HUMAN_REVIEW",
    "reason_codes": ["string"],
    "confidence": 0.0,
    "notes": "string"
  }
}
5.4 skill_publish_content (abstracted)
Input

{
  "draft_id": "drf_001",
  "platform": "youtube",
  "approval_id": "hap_001",
  "schedule_at": "ISO-8601 datetime"
}
Output

{
  "publish": {
    "publish_id": "pub_001",
    "status": "SCHEDULED|PUBLISHED|FAILED"
  }
}
Rules

MUST error if approval evidence is missing where required.

MUST not expose secrets or tokens in outputs.

6. OpenClaw / Agent Social Network Participation (Functional Contract)
Even if the exact OpenClaw protocol is implemented later, Chimera MUST be able to publish:

capabilities: list of skills and their I/O contracts

status: current availability and last heartbeat

Minimum fields for availability/status:

{
  "agent_id": "chimera_core",
  "state": "idle|busy|degraded",
  "last_heartbeat_at": "ISO-8601 datetime",
  "capabilities": [
    {
      "skill_name": "skill_fetch_trends",
      "inputs": ["platform", "region", "time_window", "limit"],
      "outputs": ["topics"]
    }
  ]
}
7. Out of Scope (Technical)
Platform-specific auth/token integration

UI/dashboard implementation

Real-time comment moderation and engagement automation

Model training / fine-tuning

## Cross-References
- Functional behaviors and acceptance criteria: `specs/functional.md`
- Runtime skill contracts: `skills/README.md`
- Master constraints and success criteria: `specs/_meta.md`

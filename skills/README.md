# Project Chimera — Skills (Runtime Contracts)

## Purpose
A **Skill** is a deterministic, reusable capability invoked by Chimera agents at runtime.
Skills are **not** MCP developer tools. Skills MUST have strict input/output contracts and MUST be testable.

## Skill Design Rules
- Skills MUST accept a single JSON-serializable input object.
- Skills MUST return a single JSON-serializable output object.
- Skills MUST NOT publish content unless an approval reference is provided (when required).
- Skills MUST NOT leak secrets (tokens, keys) in outputs or logs.
- Skills SHOULD be idempotent where possible (safe to retry).

---

## Skill 1: `skill_fetch_trends`

### Description
Fetch and normalize trend topics for a given platform and region.

### Input Contract
```json
{
  "platform": "youtube",
  "region": "ET",
  "time_window": "24h",
  "limit": 25
}
Output Contract
{
  "topics": [
    {
      "topic_id": "tpc_001",
      "label": "string",
      "description": "string",
      "score": 0.0,
      "source": "string",
      "collected_at": "ISO-8601 datetime"
    }
  ]
}
Errors
{ "error": { "code": "INVALID_INPUT|UPSTREAM_ERROR", "message": "string" } }
Skill 2: skill_generate_draft
Description
Generate a content draft from an approved trend topic.

Input Contract
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
Output Contract
{
  "draft": {
    "draft_id": "drf_001",
    "title": "string",
    "body": "string",
    "cta": "string",
    "confidence": 0.0,
    "version": 1
  }
}
Errors
{ "error": { "code": "TOPIC_NOT_FOUND|INVALID_INPUT|GENERATION_ERROR", "message": "string" } }
Skill 3: skill_evaluate_policy
Description
Evaluate a draft against policy/brand safety rules.

Input Contract
{
  "draft_id": "drf_001",
  "policy_profile": "default",
  "min_confidence_to_autopass": 0.85
}
Output Contract
{
  "review": {
    "review_id": "rev_001",
    "decision": "APPROVED|REJECTED|REQUIRES_HUMAN_REVIEW",
    "reason_codes": ["string"],
    "confidence": 0.0,
    "notes": "string",
    "evaluated_at": "ISO-8601 datetime"
  }
}
Errors
{ "error": { "code": "DRAFT_NOT_FOUND|INVALID_INPUT|POLICY_ENGINE_ERROR", "message": "string" } }
(Optional) Skill 4: skill_publish_content (Abstracted)
Description
Publish approved content (or schedule publish) to a platform. Platform integration details are out of scope for this phase.

Input Contract
{
  "draft_id": "drf_001",
  "platform": "youtube",
  "approval_id": "hap_001",
  "schedule_at": "ISO-8601 datetime"
}
Output Contract
{
  "publish": {
    "publish_id": "pub_001",
    "status": "SCHEDULED|PUBLISHED|FAILED"
  }
}
Rules
MUST fail if approval_id is missing when human approval is required.

MUST NOT expose secrets in outputs.

Errors
{ "error": { "code": "MISSING_APPROVAL|INVALID_INPUT|PUBLISH_ERROR", "message": "string" } }
```
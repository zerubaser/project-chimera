# Tooling Strategy — Developer MCP Tools vs Runtime Skills

## Goal
Separate:
1) **Developer Tools (MCP servers)** used during development for productivity and traceability  
2) **Runtime Skills** used by Chimera agents during execution

This prevents conflating “how we build” with “what the agent can do”.

---

## A) Developer Tools (MCP)
These tools assist the human developer during repo design and governance.

### Recommended MCP Developer Tools
- **Filesystem MCP**: navigate, read, and edit repository files safely
- **Git MCP**: inspect status, diffs, commit history, and ensure clean hygiene
- **(Optional) Database MCP**: inspect schemas and validate query assumptions during later phases

### Developer Tool Principles
- Developer MCP tools MUST NOT be treated as agent runtime capabilities.
- Developer tools are used to improve:
  - traceability
  - code review readiness
  - spec alignment checks

---

## B) Runtime Skills (Chimera Agent Capabilities)
Runtime skills are deterministic capabilities that agents invoke while executing workflows.

### Required Properties
- Strict I/O contracts (JSON)
- Clear error shapes
- No secret leakage
- Approval gating for publishing
- Audit-friendly logging via `skill_runs`

### Current Planned Skills (Phase 1 Contracts)
- `skill_fetch_trends`
- `skill_generate_draft`
- `skill_evaluate_policy`
- (optional) `skill_publish_content`

---

## Governance Boundary
- Agents MAY only call skills listed in `skills/` and referenced in `specs/technical.md`.
- Any new skill MUST be added via:
  1) spec update
  2) interface contract
  3) tests defining expected parameters and outputs (before implementation)

# Project Chimera

Spec-driven implementation challenge repo.

## Quickstart

- Run tests in Docker (CI runs this):
  - `make test`

## Structure

- `specs/` — specifications (source of truth)
- `tests/` — failing tests first, then implementation
- `skills/` — runtime capabilities

## Architecture Decisions
See `specs/_meta.md` for non-goals and trade-offs.

Key decisions:
- Spec-first development
- TDD before implementation
- Human-in-the-loop for safety
- Explicit agent containment

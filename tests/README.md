# Project Chimera — Test Suite Documentation

## Purpose

This test suite validates that implementations conform to the contracts defined in:
- `specs/functional.md` - Functional capabilities and acceptance criteria
- `specs/technical.md` - API contracts, data models, and validation rules
- `skills/README.md` - Runtime skill contracts

## Test Organization

### Test Files

1. **`test_trend_fetcher.py`** - Basic contract shape tests for `skill_fetch_trends`
   - Maps to: `specs/functional.md` F1, `specs/technical.md` Section 3.1, `skills/README.md` Skill 1

2. **`test_content_draft.py`** - Basic contract shape tests for `skill_generate_draft`
   - Maps to: `specs/functional.md` F2, `specs/technical.md` Section 3.2, `skills/README.md` Skill 2

3. **`test_skill_interfaces.py`** - Decision enum and approval requirement tests
   - Maps to: `specs/functional.md` F3, F5, `specs/technical.md` Sections 3.3, 3.5

4. **`test_input_validation.py`** - Comprehensive input validation tests
   - Maps to: `specs/technical.md` Section 3 - Validation Rules for all skills
   - Tests: platform, region, time_window, limit, content_type, constraints, thresholds

5. **`test_output_contracts.py`** - Comprehensive output contract shape tests
   - Maps to: `specs/technical.md` Section 3 - Response shapes, `skills/README.md` Output Contracts
   - Tests: All required fields, ID patterns, enum values, data types, field lengths

6. **`test_error_handling.py`** - Error response structure and error code tests
   - Maps to: `specs/functional.md` F8, `specs/technical.md` Section 4, `skills/README.md` Error Codes
   - Tests: Error structure, error codes, failure transparency

7. **`test_behavioral_guarantees.py`** - Behavioral guarantee tests
   - Maps to: `specs/functional.md` Non-Functional Behavioral Guarantees, F1-F5 boundaries
   - Tests: Determinism, side effects, approval gates, JSON serializability

### Test Helpers

- **`helpers/validators.py`** - Reusable validation functions
  - Maps to: `specs/technical.md` validation rules
  - Functions: ID patterns, ISO 8601 dates, enums, confidence scores, error structures

## Test Mapping to Specs

### Input Validation Tests

| Test | Spec Reference | Validation Rule |
|------|---------------|----------------|
| `test_fetch_trends_validates_platform` | `specs/technical.md` 3.1 | platform MUST be one of: youtube, tiktok, instagram |
| `test_fetch_trends_validates_region` | `specs/technical.md` 3.1 | region MUST be ISO 3166-1 alpha-2 |
| `test_fetch_trends_validates_time_window` | `specs/technical.md` 3.1 | time_window MUST match pattern ^\d+[hHdD]$ |
| `test_fetch_trends_validates_limit` | `specs/technical.md` 3.1 | limit MUST be integer between 1 and 100 |
| `test_generate_draft_validates_content_type` | `specs/technical.md` 3.2 | content_type MUST be one of: short_script, caption, post |
| `test_generate_draft_validates_constraints` | `specs/technical.md` 3.2 | constraints.max_chars MUST be positive integer, max 50000 |
| `test_evaluate_policy_validates_confidence_threshold` | `specs/technical.md` 3.3 | min_confidence_to_autopass MUST be in range [0.0, 1.0] |

### Output Contract Tests

| Test | Spec Reference | Contract Requirement |
|------|---------------|---------------------|
| `test_fetch_trends_output_contract_complete` | `specs/technical.md` 3.1, `skills/README.md` Skill 1 | topics[] with topic_id, label, description, score, source, collected_at |
| `test_generate_draft_output_contract_complete` | `specs/technical.md` 3.2, `skills/README.md` Skill 2 | draft{} with draft_id, title, body, cta, confidence, version |
| `test_evaluate_policy_output_contract_complete` | `specs/technical.md` 3.3, `skills/README.md` Skill 3 | review{} with review_id, decision, reason_codes[], confidence, evaluated_at |
| `test_publish_content_output_contract_complete` | `specs/technical.md` 3.5, `skills/README.md` Skill 4 | publish{} with publish_id, draft_id, platform, status, scheduled_at |

### Error Handling Tests

| Test | Spec Reference | Error Requirement |
|------|---------------|------------------|
| `test_error_response_structure` | `specs/technical.md` Section 4 | Error structure: { "error": { "code", "message", "timestamp" } } |
| `test_fetch_trends_error_codes` | `specs/technical.md` 3.1, `skills/README.md` Skill 1 | INVALID_PLATFORM, INVALID_REGION, INVALID_TIME_WINDOW, INVALID_LIMIT |
| `test_generate_draft_error_codes` | `specs/technical.md` 3.2, `skills/README.md` Skill 2 | TOPIC_NOT_FOUND, INVALID_CONTENT_TYPE, INVALID_CONSTRAINT |
| `test_evaluate_policy_error_codes` | `specs/technical.md` 3.3, `skills/README.md` Skill 3 | DRAFT_NOT_FOUND, INVALID_CONFIDENCE_THRESHOLD |
| `test_publish_content_error_codes` | `specs/technical.md` 3.5, `skills/README.md` Skill 4 | MISSING_APPROVAL, INVALID_SCHEDULE_TIME |
| `test_failures_must_not_silently_continue` | `specs/functional.md` F8 | Failures MUST return structured error information |

### Behavioral Guarantee Tests

| Test | Spec Reference | Behavioral Guarantee |
|------|---------------|---------------------|
| `test_fetch_trends_deterministic` | `specs/functional.md` F1, `specs/technical.md` 3.1 | Given identical inputs, MUST return identical topic_id and score values |
| `test_fetch_trends_no_content_generation` | `specs/functional.md` F1, `specs/technical.md` 3.1 | MUST NOT return content generation fields |
| `test_generate_draft_no_publishing` | `specs/functional.md` F2, `specs/technical.md` 3.2 | Draft creation MUST NOT trigger publishing |
| `test_evaluate_policy_decision_constraints` | `specs/functional.md` F3, `specs/technical.md` 3.3 | REJECTED blocks publishing, REQUIRES_HUMAN_REVIEW requires approval |
| `test_publish_content_requires_approval` | `specs/functional.md` F5, `specs/technical.md` 3.5 | Publishing MUST fail without required approvals |
| `test_skills_return_json_serializable` | `skills/README.md` Skill Design Rules | Skills MUST return JSON-serializable objects |

## Running Tests

```bash
# Run all tests
pytest

# Run tests by marker
pytest -m contract          # All contract tests
pytest -m input_validation  # Input validation tests
pytest -m output_contract   # Output contract tests
pytest -m error_handling    # Error handling tests
pytest -m behavioral        # Behavioral guarantee tests

# Run specific test file
pytest tests/test_trend_fetcher.py
```

## Expected Test Status

**Day 3 Status**: All tests are expected to **FAIL** because:
- No implementation exists yet
- Skills are not implemented (`chimera.skills.*` modules don't exist)
- Tests validate contracts before implementation (TDD approach)

## Test Principles

1. **Spec-Driven**: Every test maps to explicit requirements in specs
2. **Contract-Focused**: Tests validate input/output contracts, not implementation details
3. **Fail-First**: Tests should fail until implementation matches contracts
4. **Comprehensive**: Cover all validation rules, error codes, and behavioral guarantees
5. **Maintainable**: Use helpers/validators.py for reusable validation logic

## Cross-References

- Functional capabilities: `specs/functional.md`
- Technical contracts: `specs/technical.md`
- Skill contracts: `skills/README.md`
- Master constraints: `specs/_meta.md`

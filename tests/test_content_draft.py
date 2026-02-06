"""
Day 3 - Failing tests (Spec-Driven)

Asserts contract defined in:
- specs/technical.md : POST /v1/content/drafts response shape
- skills/README.md   : skill_generate_draft output contract

Expected status today: FAIL (no implementation yet).
"""

import pytest


@pytest.mark.contract
def test_generate_draft_returns_contract_shape():
    # Import SHOULD fail today (no implementation yet).
    from chimera.skills.generate_draft import generate_draft  # noqa: F401

    result = generate_draft(
        {
            "topic_id": "tpc_001",
            "platform": "youtube",
            "content_type": "short_script",
            "tone": "informative",
            "constraints": {"max_chars": 1200, "avoid_claims_without_sources": True},
        }
    )

    assert isinstance(result, dict), "Skill output must be a JSON-serializable object"
    assert "draft" in result, "Output must include 'draft'"
    draft = result["draft"]
    assert isinstance(draft, dict), "'draft' must be an object"

    # Required fields from skills/README.md and specs/technical.md
    for key in ["draft_id", "title", "body", "cta", "confidence", "version"]:
        assert key in draft, f"Draft must include '{key}'"

    assert isinstance(draft["draft_id"], str) and draft["draft_id"]
    assert isinstance(draft["title"], str) and draft["title"]
    assert isinstance(draft["body"], str) and draft["body"]
    assert isinstance(draft["cta"], str), "cta must be a string (can be empty but should exist)"
    assert isinstance(draft["confidence"], (int, float)), "confidence must be numeric"
    assert 0.0 <= float(draft["confidence"]) <= 1.0, "confidence must be within [0.0, 1.0]"
    assert isinstance(draft["version"], int) and draft["version"] >= 1, "version must be an integer >= 1"

"""
Day 3 - Failing tests (Spec-Driven)

Asserts:
- Review decision enum consistency across specs:
  APPROVED | REJECTED | REQUIRES_HUMAN_REVIEW
- Publishing contract requires approval evidence when needed.

Expected status today: FAIL (no implementation yet).
"""

import pytest


DECISIONS = {"APPROVED", "REJECTED", "REQUIRES_HUMAN_REVIEW"}


@pytest.mark.contract
def test_evaluate_policy_returns_valid_decision_enum():
    # Import SHOULD fail today (no implementation yet).
    from chimera.skills.evaluate_policy import evaluate_policy  # noqa: F401

    result = evaluate_policy(
        {
            "draft_id": "drf_001",
            "policy_profile": "default",
            "min_confidence_to_autopass": 0.85,
        }
    )

    assert isinstance(result, dict)
    assert "review" in result
    review = result["review"]
    assert isinstance(review, dict)

    assert "decision" in review
    assert review["decision"] in DECISIONS, f"decision must be one of {sorted(DECISIONS)}"

    assert "reason_codes" in review and isinstance(review["reason_codes"], list)
    assert "confidence" in review and isinstance(review["confidence"], (int, float))
    assert 0.0 <= float(review["confidence"]) <= 1.0


@pytest.mark.contract
def test_publish_requires_approval_id_when_provided_in_contract():
    # Import SHOULD fail today (no implementation yet).
    from chimera.skills.publish_content import publish_content  # noqa: F401

    # This call should fail (raise) if approval_id is missing, per specs/technical.md & skills/README.md
    with pytest.raises(Exception):
        publish_content(
            {
                "draft_id": "drf_001",
                "platform": "youtube",
                # "approval_id": "hap_001",  # intentionally missing
                "schedule_at": "2026-02-05T12:00:00Z",
            }
        )

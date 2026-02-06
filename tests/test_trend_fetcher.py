"""
Day 3 - Failing tests (Spec-Driven)

This test asserts the contract defined in:
- specs/technical.md : POST /v1/trends/fetch response shape
- skills/README.md   : skill_fetch_trends output contract

Expected status today: FAIL (no implementation yet).
"""

import re
import pytest


def _is_iso8601_datetime(value: str) -> bool:
    # Minimal ISO-8601 check (good enough for spec enforcement in tests)
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", value))


@pytest.mark.contract
def test_fetch_trends_returns_contract_shape():
    """
    Contract:
      Input:  platform, region, time_window, limit
      Output: topics[] with topic_id, label, description, score, source, collected_at
    """

    # Import SHOULD fail today because implementation does not exist yet.
    # On Day 3 completion, you will implement this to make the test pass.
    from chimera.skills.fetch_trends import fetch_trends  # noqa: F401

    result = fetch_trends(
        {
            "platform": "youtube",
            "region": "ET",
            "time_window": "24h",
            "limit": 25,
        }
    )

    assert isinstance(result, dict), "Skill output must be a JSON-serializable object"
    assert "topics" in result, "Output must include 'topics'"
    assert isinstance(result["topics"], list), "'topics' must be a list"

    # If topics exist, validate the shape of the first one
    if result["topics"]:
        topic = result["topics"][0]
        assert isinstance(topic, dict)

        # Required fields
        for key in ["topic_id", "label", "description", "score", "source", "collected_at"]:
            assert key in topic, f"Topic must include '{key}'"

        assert isinstance(topic["topic_id"], str) and topic["topic_id"], "topic_id must be a non-empty string"
        assert isinstance(topic["label"], str) and topic["label"], "label must be a non-empty string"
        assert isinstance(topic["description"], str), "description must be a string"
        assert isinstance(topic["score"], (int, float)), "score must be numeric"
        assert 0.0 <= float(topic["score"]) <= 1.0, "score must be within [0.0, 1.0]"
        assert isinstance(topic["source"], str) and topic["source"], "source must be a non-empty string"
        assert isinstance(topic["collected_at"], str) and _is_iso8601_datetime(topic["collected_at"]), \
            "collected_at must be an ISO-8601 UTC datetime like 2026-02-05T10:00:00Z"

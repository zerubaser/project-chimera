"""
Day 3 - Input Validation Tests (Spec-Driven)

These tests assert input validation rules defined in:
- specs/technical.md Section 3 (API Contracts) - Validation Rules
- skills/README.md - Input Validation Rules

Expected status: FAIL (no implementation yet).
Each test maps to specific validation rules in the specs.
"""

import pytest
from tests.helpers.validators import (
    is_valid_platform,
    is_valid_region,
    is_valid_time_window,
    is_valid_content_type,
    is_valid_confidence_score,
)


@pytest.mark.contract
@pytest.mark.input_validation
def test_fetch_trends_validates_platform():
    """
    Maps to: specs/technical.md Section 3.1
    - platform MUST be exactly one of: "youtube", "tiktok", "instagram" (case-sensitive)
    - Invalid values return error code INVALID_PLATFORM
    """
    from chimera.skills.fetch_trends import fetch_trends  # noqa: F401

    # Valid platforms should work
    for platform in ["youtube", "tiktok", "instagram"]:
        result = fetch_trends({"platform": platform, "region": "ET", "time_window": "24h"})
        assert "error" not in result or result.get("error", {}).get("code") != "INVALID_PLATFORM"

    # Invalid platform should return error
    result = fetch_trends({"platform": "invalid", "region": "ET", "time_window": "24h"})
    assert "error" in result
    assert result["error"]["code"] == "INVALID_PLATFORM"


@pytest.mark.contract
@pytest.mark.input_validation
def test_fetch_trends_validates_region():
    """
    Maps to: specs/technical.md Section 3.1
    - region MUST be ISO 3166-1 alpha-2 country code (exactly 2 uppercase letters)
    - Invalid codes return error code INVALID_REGION
    """
    from chimera.skills.fetch_trends import fetch_trends  # noqa: F401

    # Valid region (2 uppercase letters)
    result = fetch_trends({"platform": "youtube", "region": "ET", "time_window": "24h"})
    assert "error" not in result or result.get("error", {}).get("code") != "INVALID_REGION"

    # Invalid regions should return error
    for invalid_region in ["et", "ETH", "12", "E"]:
        result = fetch_trends({"platform": "youtube", "region": invalid_region, "time_window": "24h"})
        assert "error" in result
        assert result["error"]["code"] == "INVALID_REGION"


@pytest.mark.contract
@pytest.mark.input_validation
def test_fetch_trends_validates_time_window():
    """
    Maps to: specs/technical.md Section 3.1
    - time_window MUST match pattern ^\d+[hHdD]$ (e.g., "24h", "7d")
    - Invalid format returns error code INVALID_TIME_WINDOW
    """
    from chimera.skills.fetch_trends import fetch_trends  # noqa: F401

    # Valid time windows
    for time_window in ["24h", "7d", "1H", "30D"]:
        result = fetch_trends({"platform": "youtube", "region": "ET", "time_window": time_window})
        assert "error" not in result or result.get("error", {}).get("code") != "INVALID_TIME_WINDOW"

    # Invalid time windows
    for invalid_window in ["24", "h24", "24hours", "1w"]:
        result = fetch_trends({"platform": "youtube", "region": "ET", "time_window": invalid_window})
        assert "error" in result
        assert result["error"]["code"] == "INVALID_TIME_WINDOW"


@pytest.mark.contract
@pytest.mark.input_validation
def test_fetch_trends_validates_limit():
    """
    Maps to: specs/technical.md Section 3.1
    - limit MUST be integer between 1 and 100 inclusive
    - Values outside range return error code INVALID_LIMIT
    - If omitted, defaults to 25
    """
    from chimera.skills.fetch_trends import fetch_trends  # noqa: F401

    # Valid limits
    for limit in [1, 25, 100]:
        result = fetch_trends({"platform": "youtube", "region": "ET", "time_window": "24h", "limit": limit})
        assert "error" not in result or result.get("error", {}).get("code") != "INVALID_LIMIT"

    # Invalid limits
    for invalid_limit in [0, 101, -1, 1.5]:
        result = fetch_trends({"platform": "youtube", "region": "ET", "time_window": "24h", "limit": invalid_limit})
        assert "error" in result
        assert result["error"]["code"] == "INVALID_LIMIT"


@pytest.mark.contract
@pytest.mark.input_validation
def test_generate_draft_validates_content_type():
    """
    Maps to: specs/technical.md Section 3.2
    - content_type MUST be exactly one of: "short_script", "caption", "post" (case-sensitive)
    - Invalid type returns error code INVALID_CONTENT_TYPE
    """
    from chimera.skills.generate_draft import generate_draft  # noqa: F401

    # Valid content types
    for content_type in ["short_script", "caption", "post"]:
        result = generate_draft({
            "topic_id": "tpc_001",
            "platform": "youtube",
            "content_type": content_type,
        })
        assert "error" not in result or result.get("error", {}).get("code") != "INVALID_CONTENT_TYPE"

    # Invalid content types
    for invalid_type in ["script", "SHORT_SCRIPT", "video", ""]:
        result = generate_draft({
            "topic_id": "tpc_001",
            "platform": "youtube",
            "content_type": invalid_type,
        })
        assert "error" in result
        assert result["error"]["code"] == "INVALID_CONTENT_TYPE"


@pytest.mark.contract
@pytest.mark.input_validation
def test_generate_draft_validates_constraints():
    """
    Maps to: specs/technical.md Section 3.2
    - constraints.max_chars MUST be positive integer
    - Values > 50000 return error code INVALID_CONSTRAINT
    - If not provided, defaults to 5000
    """
    from chimera.skills.generate_draft import generate_draft  # noqa: F401

    # Valid constraints
    result = generate_draft({
        "topic_id": "tpc_001",
        "platform": "youtube",
        "content_type": "short_script",
        "constraints": {"max_chars": 1200},
    })
    assert "error" not in result or result.get("error", {}).get("code") != "INVALID_CONSTRAINT"

    # Invalid constraint (> 50000)
    result = generate_draft({
        "topic_id": "tpc_001",
        "platform": "youtube",
        "content_type": "short_script",
        "constraints": {"max_chars": 50001},
    })
    assert "error" in result
    assert result["error"]["code"] == "INVALID_CONSTRAINT"


@pytest.mark.contract
@pytest.mark.input_validation
def test_evaluate_policy_validates_confidence_threshold():
    """
    Maps to: specs/technical.md Section 3.3
    - min_confidence_to_autopass MUST be float in range [0.0, 1.0] inclusive
    - Invalid range returns error code INVALID_CONFIDENCE_THRESHOLD
    """
    from chimera.skills.evaluate_policy import evaluate_policy  # noqa: F401

    # Valid thresholds
    for threshold in [0.0, 0.5, 0.85, 1.0]:
        result = evaluate_policy({
            "draft_id": "drf_001",
            "policy_profile": "default",
            "min_confidence_to_autopass": threshold,
        })
        assert "error" not in result or result.get("error", {}).get("code") != "INVALID_CONFIDENCE_THRESHOLD"

    # Invalid thresholds
    for invalid_threshold in [-0.1, 1.1, 2.0]:
        result = evaluate_policy({
            "draft_id": "drf_001",
            "policy_profile": "default",
            "min_confidence_to_autopass": invalid_threshold,
        })
        assert "error" in result
        assert result["error"]["code"] == "INVALID_CONFIDENCE_THRESHOLD"

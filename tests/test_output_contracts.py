"""
Day 3 - Output Contract Tests (Spec-Driven)

These tests assert output contract shapes defined in:
- specs/technical.md Section 3 (API Contracts) - Response shapes
- skills/README.md - Output Contracts

Expected status: FAIL (no implementation yet).
Each test maps to specific output contract requirements.
"""

import pytest
from tests.helpers.validators import (
    is_iso8601_datetime,
    matches_id_pattern,
    is_valid_decision,
    is_valid_reason_code,
    is_valid_publish_status,
    is_valid_confidence_score,
)


@pytest.mark.contract
@pytest.mark.output_contract
def test_fetch_trends_output_contract_complete():
    """
    Maps to: specs/technical.md Section 3.1, skills/README.md Skill 1
    - Output MUST include: topics[] with topic_id, label, description, score, source, collected_at
    - topic_id MUST match pattern ^tpc_[a-zA-Z0-9]+$
    - score MUST be in range [0.0, 1.0]
    - collected_at MUST be ISO 8601 datetime in UTC
    - Response MUST NOT contain content generation fields
    """
    from chimera.skills.fetch_trends import fetch_trends  # noqa: F401

    result = fetch_trends({
        "platform": "youtube",
        "region": "ET",
        "time_window": "24h",
        "limit": 25,
    })

    assert isinstance(result, dict)
    assert "topics" in result
    assert isinstance(result["topics"], list)

    if result["topics"]:
        topic = result["topics"][0]
        
        # Required fields
        assert "topic_id" in topic
        assert matches_id_pattern(topic["topic_id"], "topic_id")
        
        assert "label" in topic
        assert isinstance(topic["label"], str) and len(topic["label"]) > 0
        assert len(topic["label"]) <= 200  # Max 200 chars per spec
        
        assert "description" in topic
        assert isinstance(topic["description"], str)
        assert len(topic["description"]) <= 500  # Max 500 chars per spec
        
        assert "score" in topic
        assert is_valid_confidence_score(topic["score"])
        
        assert "source" in topic
        assert isinstance(topic["source"], str) and len(topic["source"]) > 0
        
        assert "collected_at" in topic
        assert is_iso8601_datetime(topic["collected_at"])
        
        # MUST NOT contain content generation fields
        forbidden_fields = ["title", "body", "content", "draft_id"]
        for field in forbidden_fields:
            assert field not in topic, f"Topic output must not include '{field}'"


@pytest.mark.contract
@pytest.mark.output_contract
def test_generate_draft_output_contract_complete():
    """
    Maps to: specs/technical.md Section 3.2, skills/README.md Skill 2
    - Output MUST include: draft{} with draft_id, topic_id, platform, content_type, title, body, cta, confidence, version
    - draft_id MUST match pattern ^drf_[a-zA-Z0-9]+$
    - confidence MUST be in range [0.0, 1.0]
    - title max 200 chars, body max 50000 chars, cta max 100 chars
    """
    from chimera.skills.generate_draft import generate_draft  # noqa: F401

    result = generate_draft({
        "topic_id": "tpc_001",
        "platform": "youtube",
        "content_type": "short_script",
    })

    assert isinstance(result, dict)
    assert "draft" in result
    draft = result["draft"]
    assert isinstance(draft, dict)

    # Required fields
    assert "draft_id" in draft
    assert matches_id_pattern(draft["draft_id"], "draft_id")
    
    assert "topic_id" in draft
    assert "platform" in draft
    assert "content_type" in draft
    
    assert "title" in draft
    assert isinstance(draft["title"], str) and len(draft["title"]) > 0
    assert len(draft["title"]) <= 200
    
    assert "body" in draft
    assert isinstance(draft["body"], str) and len(draft["body"]) > 0
    assert len(draft["body"]) <= 50000
    
    assert "cta" in draft  # Optional but should exist
    assert isinstance(draft["cta"], str)
    assert len(draft["cta"]) <= 100
    
    assert "confidence" in draft
    assert is_valid_confidence_score(draft["confidence"])
    
    assert "version" in draft
    assert isinstance(draft["version"], int) and draft["version"] >= 1


@pytest.mark.contract
@pytest.mark.output_contract
def test_evaluate_policy_output_contract_complete():
    """
    Maps to: specs/technical.md Section 3.3, skills/README.md Skill 3
    - Output MUST include: review{} with review_id, draft_id, decision, reason_codes[], confidence, notes, evaluated_at
    - decision MUST be one of: APPROVED, REJECTED, REQUIRES_HUMAN_REVIEW
    - reason_codes MUST be non-empty array from allowed set
    - confidence MUST be in range [0.0, 1.0]
    """
    from chimera.skills.evaluate_policy import evaluate_policy  # noqa: F401

    result = evaluate_policy({
        "draft_id": "drf_001",
        "policy_profile": "default",
        "min_confidence_to_autopass": 0.85,
    })

    assert isinstance(result, dict)
    assert "review" in result
    review = result["review"]
    assert isinstance(review, dict)

    assert "review_id" in review
    assert matches_id_pattern(review["review_id"], "review_id")
    
    assert "draft_id" in review
    
    assert "decision" in review
    assert is_valid_decision(review["decision"])
    
    assert "reason_codes" in review
    assert isinstance(review["reason_codes"], list)
    assert len(review["reason_codes"]) > 0  # Must be non-empty
    for code in review["reason_codes"]:
        assert is_valid_reason_code(code)
    
    assert "confidence" in review
    assert is_valid_confidence_score(review["confidence"])
    
    assert "notes" in review  # Optional but should exist
    assert isinstance(review["notes"], str)
    assert len(review["notes"]) <= 1000  # Max 1000 chars
    
    assert "evaluated_at" in review
    assert is_iso8601_datetime(review["evaluated_at"])


@pytest.mark.contract
@pytest.mark.output_contract
def test_publish_content_output_contract_complete():
    """
    Maps to: specs/technical.md Section 3.5, skills/README.md Skill 4
    - Output MUST include: publish{} with publish_id, draft_id, platform, status, scheduled_at
    - publish_id MUST match pattern ^pub_[a-zA-Z0-9]+$
    - status MUST be one of: SCHEDULED, PUBLISHED, FAILED
    - scheduled_at MUST be ISO 8601 datetime
    """
    from chimera.skills.publish_content import publish_content  # noqa: F401

    result = publish_content({
        "draft_id": "drf_001",
        "platform": "youtube",
        "approval_id": "hap_001",
        "schedule_at": "2026-02-05T12:00:00Z",
    })

    assert isinstance(result, dict)
    assert "publish" in result
    publish = result["publish"]
    assert isinstance(publish, dict)

    assert "publish_id" in publish
    assert matches_id_pattern(publish["publish_id"], "publish_id")
    
    assert "draft_id" in publish
    assert "platform" in publish
    
    assert "status" in publish
    assert is_valid_publish_status(publish["status"])
    
    assert "scheduled_at" in publish
    assert is_iso8601_datetime(publish["scheduled_at"])

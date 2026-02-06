"""
Pytest configuration and shared fixtures.

This file provides shared test fixtures and configuration for the test suite.
"""

import pytest


@pytest.fixture
def valid_trend_input():
    """
    Valid input for skill_fetch_trends.
    Maps to: specs/technical.md Section 3.1 Request
    """
    return {
        "platform": "youtube",
        "region": "ET",
        "time_window": "24h",
        "limit": 25,
    }


@pytest.fixture
def valid_draft_input():
    """
    Valid input for skill_generate_draft.
    Maps to: specs/technical.md Section 3.2 Request
    """
    return {
        "topic_id": "tpc_001",
        "platform": "youtube",
        "content_type": "short_script",
        "tone": "informative",
        "constraints": {
            "max_chars": 1200,
            "avoid_claims_without_sources": True,
        },
    }


@pytest.fixture
def valid_review_input():
    """
    Valid input for skill_evaluate_policy.
    Maps to: specs/technical.md Section 3.3 Request
    """
    return {
        "draft_id": "drf_001",
        "policy_profile": "default",
        "min_confidence_to_autopass": 0.85,
    }


@pytest.fixture
def valid_publish_input():
    """
    Valid input for skill_publish_content.
    Maps to: specs/technical.md Section 3.5 Request
    """
    return {
        "draft_id": "drf_001",
        "platform": "youtube",
        "approval_id": "hap_001",
        "schedule_at": "2026-02-05T12:00:00Z",
    }

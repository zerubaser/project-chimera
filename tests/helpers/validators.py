"""
Test helpers for validating spec contracts.

These validators map directly to validation rules in specs/technical.md.
"""

import re
from typing import Any, Dict


def is_iso8601_datetime(value: str) -> bool:
    """
    Validates ISO 8601 datetime format in UTC.
    Maps to: specs/technical.md validation rules for timestamp fields.
    """
    pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
    return bool(re.match(pattern, value))


def matches_id_pattern(value: str, pattern_type: str) -> bool:
    """
    Validates ID patterns as defined in specs/technical.md.
    
    Maps to: specs/technical.md Section 5.3 Schema Constraints Summary
    - topic_id: ^tpc_[a-zA-Z0-9]+$
    - draft_id: ^drf_[a-zA-Z0-9]+$
    - review_id: ^rev_[a-zA-Z0-9]+$
    - approval_id: ^hap_[a-zA-Z0-9]+$
    - publish_id: ^pub_[a-zA-Z0-9]+$
    - run_id: ^run_[a-zA-Z0-9]+$
    - request_id: ^req_[a-zA-Z0-9]+$
    """
    patterns = {
        "topic_id": r"^tpc_[a-zA-Z0-9]+$",
        "draft_id": r"^drf_[a-zA-Z0-9]+$",
        "review_id": r"^rev_[a-zA-Z0-9]+$",
        "approval_id": r"^hap_[a-zA-Z0-9]+$",
        "publish_id": r"^pub_[a-zA-Z0-9]+$",
        "run_id": r"^run_[a-zA-Z0-9]+$",
        "request_id": r"^req_[a-zA-Z0-9]+$",
        "reviewer_id": r"^usr_[a-zA-Z0-9]+$",
    }
    pattern = patterns.get(pattern_type)
    if not pattern:
        raise ValueError(f"Unknown pattern type: {pattern_type}")
    return bool(re.match(pattern, value))


def is_valid_platform(value: str) -> bool:
    """
    Validates platform identifier.
    Maps to: specs/technical.md Section 3.1 - platform MUST be one of: youtube, tiktok, instagram
    """
    return value in {"youtube", "tiktok", "instagram"}


def is_valid_region(value: str) -> bool:
    """
    Validates ISO 3166-1 alpha-2 country code.
    Maps to: specs/technical.md Section 3.1 - region MUST be ISO 3166-1 alpha-2 (exactly 2 uppercase letters)
    """
    return bool(re.match(r"^[A-Z]{2}$", value))


def is_valid_time_window(value: str) -> bool:
    """
    Validates time_window format.
    Maps to: specs/technical.md Section 3.1 - time_window MUST match pattern ^\d+[hHdD]$
    """
    return bool(re.match(r"^\d+[hHdD]$", value))


def is_valid_content_type(value: str) -> bool:
    """
    Validates content_type enum.
    Maps to: specs/technical.md Section 3.2 - content_type MUST be one of: short_script, caption, post
    """
    return value in {"short_script", "caption", "post"}


def is_valid_decision(value: str) -> bool:
    """
    Validates review decision enum.
    Maps to: specs/functional.md F3 and specs/technical.md Section 3.3
    - Decision MUST be exactly one of: APPROVED, REJECTED, REQUIRES_HUMAN_REVIEW
    """
    return value in {"APPROVED", "REJECTED", "REQUIRES_HUMAN_REVIEW"}


def is_valid_reason_code(value: str) -> bool:
    """
    Validates reason code enum.
    Maps to: specs/technical.md Section 3.3
    - reason_codes MUST be from allowed set: LOW_CONFIDENCE, POLICY_VIOLATION, BRAND_SAFETY_VIOLATION, UNKNOWN
    """
    return value in {"LOW_CONFIDENCE", "POLICY_VIOLATION", "BRAND_SAFETY_VIOLATION", "UNKNOWN"}


def is_valid_publish_status(value: str) -> bool:
    """
    Validates publish_jobs status enum.
    Maps to: specs/technical.md Section 3.5 - status MUST be one of: SCHEDULED, PUBLISHED, FAILED
    """
    return value in {"SCHEDULED", "PUBLISHED", "FAILED"}


def is_valid_confidence_score(value: Any) -> bool:
    """
    Validates confidence score range.
    Maps to: specs/technical.md - confidence MUST be float in range [0.0, 1.0] inclusive
    """
    try:
        score = float(value)
        return 0.0 <= score <= 1.0
    except (ValueError, TypeError):
        return False


def has_error_structure(error: Dict[str, Any]) -> bool:
    """
    Validates error response structure.
    Maps to: specs/technical.md Section 4 - Error Response Structure
    """
    if not isinstance(error, dict):
        return False
    if "error" not in error:
        return False
    
    error_obj = error["error"]
    required_fields = {"code", "message", "timestamp"}
    return all(field in error_obj for field in required_fields)

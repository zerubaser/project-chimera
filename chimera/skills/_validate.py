from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple


TIME_WINDOW_RE = re.compile(r"^\d+[hHdD]$")


def _get(d: Dict[str, Any], key: str) -> Any:
    return d.get(key, None)


def validate_fetch_trends(params: Dict[str, Any]) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    platform = _get(params, "platform")
    region = _get(params, "region")
    time_window = _get(params, "time_window")
    limit = _get(params, "limit")

    allowed_platforms = {"youtube", "tiktok", "x", "twitter", "reddit"}
    if not isinstance(platform, str) or platform.lower() not in allowed_platforms:
        return ("INVALID_PLATFORM", "platform must be one of: youtube, tiktok, x, twitter, reddit", {"platform": platform})

    if not isinstance(region, str) or not re.fullmatch(r"^[A-Z]{2}$", region):
        return ("INVALID_REGION", "region must be ISO-3166-1 alpha-2 uppercase (e.g., 'ET')", {"region": region})

    if not isinstance(time_window, str) or not TIME_WINDOW_RE.fullmatch(time_window):
        return ("INVALID_TIME_WINDOW", "time_window must match ^\\d+[hHdD]$ (e.g., '24h', '7d')", {"time_window": time_window})

    if limit is None:
        limit = 10
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1 or limit > 50:
        return ("INVALID_LIMIT", "limit must be an integer between 1 and 50", {"limit": limit})

    return None


def validate_generate_draft(params: Dict[str, Any]) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    content_type = _get(params, "content_type")
    trend = _get(params, "trend")
    constraints = _get(params, "constraints")

    allowed_types = {"tweet", "thread", "linkedin", "blog", "script"}
    if not isinstance(content_type, str) or content_type.lower() not in allowed_types:
        return ("INVALID_CONTENT_TYPE", "content_type must be one of: tweet, thread, linkedin, blog, script", {"content_type": content_type})

    if not isinstance(trend, dict):
        return ("INVALID_TREND", "trend must be an object/dict", {"trend": trend})

    if constraints is None:
        constraints = {}
    if not isinstance(constraints, dict):
        return ("INVALID_CONSTRAINTS", "constraints must be an object/dict", {"constraints": constraints})

    # common constraints fields (keep permissive but sane)
    max_chars = constraints.get("max_chars")
    if max_chars is not None and (not isinstance(max_chars, int) or max_chars < 1):
        return ("INVALID_CONSTRAINTS", "constraints.max_chars must be a positive integer", {"max_chars": max_chars})

    return None


def validate_evaluate_policy(params: Dict[str, Any]) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    draft = _get(params, "draft")
    confidence_threshold = _get(params, "confidence_threshold")

    if not isinstance(draft, dict):
        return ("INVALID_DRAFT", "draft must be an object/dict", {"draft": draft})

    if confidence_threshold is None:
        confidence_threshold = 0.7
    if not isinstance(confidence_threshold, (int, float)) or not (0.0 <= float(confidence_threshold) <= 1.0):
        return ("INVALID_CONFIDENCE_THRESHOLD", "confidence_threshold must be between 0 and 1", {"confidence_threshold": confidence_threshold})

    return None


def validate_publish_content(params: Dict[str, Any]) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    draft = _get(params, "draft")
    approval_id = _get(params, "approval_id")
    scheduled_at = _get(params, "scheduled_at")

    if not isinstance(draft, dict):
        return ("INVALID_DRAFT", "draft must be an object/dict", {"draft": draft})

    # You MUST require approval_id (tests mention this strongly)
    if not isinstance(approval_id, str) or not approval_id.strip():
        return ("MISSING_APPROVAL", "approval_id is required to publish", {"approval_id": approval_id})

    # scheduled_at can be optional; keep as string if provided
    if scheduled_at is not None and not isinstance(scheduled_at, str):
        return ("INVALID_SCHEDULED_AT", "scheduled_at must be a string if provided", {"scheduled_at": scheduled_at})

    return None

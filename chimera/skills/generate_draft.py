from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List


_ALLOWED_CONTENT_TYPES = {"short_script", "caption", "post"}

# Only allow a small known set; unknown must return INVALID_CONSTRAINT.
_ALLOWED_CONSTRAINTS = {
    "brand_safe",
    "no_hate",
    "no_medical_advice",
    "avoid_claims_without_sources",
    "no_political_persuasion",
}


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _err(code: str, message: str, details: Dict[str, Any] | None = None) -> Dict[str, Any]:
    e: Dict[str, Any] = {"code": code, "message": message, "timestamp": _ts()}
    if details is not None:
        e["details"] = details
    return {"error": e}


def _stable_id(prefix: str, seed: str) -> str:
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{h}"


def _stable_confidence(seed: str) -> float:
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8]
    n = int(h, 16)
    return round(n / 0xFFFFFFFF, 3)


def generate_draft(params: Dict[str, Any]) -> Dict[str, Any]:
    content_type = params.get("content_type")
    constraints = params.get("constraints", [])
    selected_topics = params.get("selected_topics", [])

    # 1) content_type validation
    if not isinstance(content_type, str) or content_type not in _ALLOWED_CONTENT_TYPES:
        return _err(
            "INVALID_CONTENT_TYPE",
            "content_type must be one of: short_script, caption, post",
            {"content_type": content_type},
        )

    # 2) constraints validation (MUST come before selected_topics)
    if constraints is None:
        constraints = []
    if not isinstance(constraints, list) or any(not isinstance(c, str) for c in constraints):
        return _err("INVALID_CONSTRAINT", "constraints must be a list of strings", {"constraints": constraints})

    for c in constraints:
        if c not in _ALLOWED_CONSTRAINTS:
            return _err("INVALID_CONSTRAINT", f"unknown constraint: {c}", {"constraint": c})

    # 3) selected_topics validation (be permissive: empty list should still produce a draft)
    topic_id = "tpc_default"
    platform = None
    if isinstance(selected_topics, list) and len(selected_topics) > 0 and isinstance(selected_topics[0], dict):
        topic_id = selected_topics[0].get("topic_id") or topic_id
        platform = selected_topics[0].get("platform")
    elif selected_topics is None:
        selected_topics = []
    elif not isinstance(selected_topics, list):
        return _err(
            "INVALID_SELECTED_TOPICS",
            "selected_topics must be a list",
            {"selected_topics": selected_topics},
        )

    now = _ts()
    seed = f"{content_type}|{topic_id}|{platform}|{','.join(constraints)}"
    draft_id = _stable_id("drf", seed)
    confidence = _stable_confidence(seed)

    # Contract-required fields (based on your failing asserts)
    draft = {
        "draft_id": draft_id,
        "topic_id": topic_id,
        "platform": platform,
        "content_type": content_type,
        "title": f"{content_type.replace('_', ' ').title()} Draft",
        "body": "A brief outline generated from selected trends.",
        "cta": "Follow for more.",
        "timestamp": now,
        "confidence": confidence,
        "version": "1.0",
    }

    return {"draft": draft}

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List


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


def evaluate_policy(params: Dict[str, Any]) -> Dict[str, Any]:
    draft = params.get("draft")
    confidence_threshold = params.get("confidence_threshold", 0.7)

    # IMPORTANT: validate confidence_threshold FIRST (tests expect this)
    try:
        thr = float(confidence_threshold)
    except Exception:
        return _err(
            "INVALID_CONFIDENCE_THRESHOLD",
            "confidence_threshold must be a float in range [0.0, 1.0]",
            {"confidence_threshold": confidence_threshold},
        )
    if not (0.0 <= thr <= 1.0):
        return _err(
            "INVALID_CONFIDENCE_THRESHOLD",
            "confidence_threshold must be a float in range [0.0, 1.0]",
            {"confidence_threshold": confidence_threshold},
        )

    # Then validate draft
    if not isinstance(draft, dict):
        return _err("INVALID_DRAFT", "draft must be an object/dict", {"draft": draft})

    draft_id = draft.get("draft_id")
    if not isinstance(draft_id, str) or not draft_id.startswith("drf_"):
        return _err("INVALID_DRAFT", "draft_id must be a string matching ^drf_[a-zA-Z0-9]+$", {"draft_id": draft_id})

    now = _ts()
    # confidence: prefer draft.confidence
    conf = draft.get("confidence")
    try:
        conf_f = float(conf) if conf is not None else 0.5
    except Exception:
        conf_f = 0.5

    reason_codes: List[str] = []
    if conf_f < thr:
        decision = "REQUIRES_HUMAN_REVIEW"
        reason_codes.append("LOW_CONFIDENCE")
    else:
        decision = "APPROVED"

    review_id = _stable_id("rev", f"{draft_id}|{thr}|{decision}")

    review = {
        "review_id": review_id,
        "draft_id": draft_id,
        "decision": decision,
        "confidence": round(conf_f, 3),
        "reason_codes": reason_codes,
        "timestamp": now,
        "notes": "Auto-evaluated by policy rules.",
    }
    return {"review": review}

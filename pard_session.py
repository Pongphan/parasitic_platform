"""Input identity and validated calculation events for the ParD page."""

import hashlib
import json
import math


def view_for_viewport(view, viewport):
    """Keep the saved image framing consistent if a resized iframe remounts."""
    ratio = viewport / view.get("viewport", viewport)
    return {"zoom": view["zoom"], "panX": view["panX"] * ratio,
            "panY": view["panY"] * ratio, "viewport": viewport}


def context_fingerprint(image_id, model_specs, normalize_to_01, viewport, source_label):
    payload = {
        "image": image_id,
        "models": model_specs,
        "normalize_to_01": normalize_to_01,
        "viewport": viewport,
        "source": source_label,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def refresh_context(session, image_id, context_id):
    """Discard results when inputs change; reset framing only for a new image."""
    image_changed = session.get("pard_image_id") != image_id
    context_changed = session.get("pard_context_id") != context_id
    had_result = session.get("pard_result") is not None
    if image_changed:
        session["pard_view"] = {"zoom": 1.0, "panX": 0.0, "panY": 0.0}
    # Component values persist across image changes. Never replay a consumed
    # click when returning to its image without another Calculate press.
    session.setdefault("pard_last_token", "")
    if context_changed:
        session["pard_result"] = None
    session["pard_image_id"] = image_id
    session["pard_context_id"] = context_id
    return context_changed and had_result


def calculation_event(state, image_id, viewport, last_token):
    """Ignore stale events, and reject malformed current-image coordinates."""
    if not isinstance(state, dict) or state.get("action") != "calculate":
        return None
    if state.get("image_id") != image_id:
        return None
    token = state.get("calc_token")
    if not isinstance(token, str) or not token.strip() or len(token) > 128:
        raise ValueError("Invalid calculation event. Please press Calculate again.")
    if token == last_token:
        return None
    try:
        values = {name: float(state[name]) for name in ("zoom", "panX", "panY", "viewport")}
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Invalid viewer coordinates. Please reset the image view.") from exc
    if not all(math.isfinite(value) for value in values.values()):
        raise ValueError("Viewer coordinates must be finite.")
    if not 0.15 <= values["zoom"] <= 12.0:
        raise ValueError("Viewer zoom is outside the supported range.")
    if values["viewport"] != viewport:
        # A queued click from the previous canvas size must not crop a new view.
        return None
    return {**values, "viewport": int(viewport), "calc_token": token}

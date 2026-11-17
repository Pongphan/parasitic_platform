import hashlib
import os
import streamlit.components.v1 as components

_component = components.declare_component(
    "viewer_component",
    path=os.path.dirname(__file__),
)

def viewer_component(
    image_b64: str,
    viewport: int,
    init_zoom: float,
    init_panX: float,
    init_panY: float,
    *,
    image_id: str | None = None,
    key: str | None = None,
    reset_token: str | int | None = None,
):
    """
    Returns dict ONLY when user presses Calculate on canvas:
      {
        "action": "calculate",
        "calc_token": "<unique>",
        "image_id": "<image identity>",
        "zoom": float,
        "panX": float,
        "panY": float,
        "viewport": int
      }
    Returns None until the first calculation. Streamlit may return the latest
    value again on later reruns; callers must deduplicate calc_token and check
    image_id. A stable key preserves the iframe while controls change.
    """
    identity = image_id or hashlib.sha256(image_b64.encode("ascii")).hexdigest()
    return _component(
        image_b64=image_b64,
        viewport=viewport,
        init_zoom=init_zoom,
        init_panX=init_panX,
        init_panY=init_panY,
        image_id=identity,
        reset_token=reset_token,
        key=key or "pard_viewer",
        default=None,
    )

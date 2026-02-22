import io
import base64
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import streamlit as st
from PIL import Image, UnidentifiedImageError
import tensorflow as tf

from viewer_component import viewer_component

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Image Classification",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==================== THEME (same as app.py) ====================
st.markdown(
    """
<style>
:root{
  --bg0:#1E293B;
  --bg1:#1E293B;
  --txt:#FFFFFF;
  --muted:rgba(234,241,255,.72);
  --muted2:rgba(234,241,255,.55);
  --stroke:rgba(234,241,255,.10);
  --stroke2:rgba(234,241,255,.16);
}

.stApp {
  background:
    radial-gradient(1200px 600px at 20% 10%, rgba(110,231,255,.08), transparent 55%),
    radial-gradient(900px 500px at 85% 15%, rgba(57, 62, 155, 0.126), transparent 55%),
    radial-gradient(800px 600px at 30% 85%, rgba(173,110,255,.05), transparent 60%),
    linear-gradient(180deg, var(--bg0), var(--bg1));
  color: var(--txt);
}
.block-container { padding-top: 1.0rem !important; padding-bottom: 2.0rem !important; max-width: 1250px; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.hero {
  border: 1px solid var(--stroke);
  border-radius: 22px;
  padding: 18px 20px 14px 20px;
  background: linear-gradient(180deg, rgba(73, 190, 249, 0.02), rgba(73, 190, 249, 0.02));
  box-shadow: 0 10px 36px rgba(0,0,0,.35);
  position: relative;
  overflow: hidden;
}

.hero:before{
  content:"";
  position:absolute;
  inset:-2px;
  background:
    radial-gradient(700px 220px at 20% 0%, rgba(110,231,255,.20), transparent 55%),
    radial-gradient(600px 240px at 80% 0%, rgba(57, 62, 155, 0.126), transparent 55%);
  filter: blur(16px);
  opacity:.55;
  pointer-events:none;
}

.hero h1{
  font-size: 1.9rem;
  line-height: 1.12;
  margin: 0;
  font-weight: 820;
  letter-spacing: .2px;
}

.hero p{
  margin: .55rem 0 0 0;
  color: #F1F5F9 !important;
  font-size: 1.0rem;
}

.section-label{
  margin-top: 1.05rem;
  margin-bottom: .55rem;
  color: #58C4FF !important;
  font-size: .92rem;
  letter-spacing: .14em;
  text-transform: uppercase;
}

.panel {
  border: 1px solid var(--stroke);
  border-radius: 18px;
  padding: 14px 14px 10px 14px;
  background: rgba(255,255,255,.02);
  box-shadow: 0 10px 26px rgba(0,0,0,.25);
}
.panel h3{
  margin: 0 0 10px 0;
  font-size: 1.06rem;
  font-weight: 780;
}
.small-muted{ color: var(--muted2); font-size: .9rem; }

.kpi {
  border: 1px solid var(--stroke);
  border-radius: 18px;
  padding: 12px 14px;
  background: rgba(255,255,255,.02);
  box-shadow: 0 10px 26px rgba(0,0,0,.25);
}

.badge{
  display:inline-block;
  font-size:.78rem;
  color: rgba(234,241,255,.82);
  border: 1px solid var(--stroke);
  background: rgba(255,255,255,.03);
  padding: 6px 10px;
  border-radius: 999px;
  letter-spacing: .2px;
  margin-right: 6px;
  margin-bottom: 6px;
}

.hr { height:1px; background: rgba(234,241,255,.08); margin: 10px 0 12px 0; }

.note {
  border-left: 3px solid rgba(110,231,255,.45);
  padding: 10px 12px;
  background: rgba(255,255,255,.02);
  border-radius: 14px;
  color: rgba(234,241,255,.82);
}

.warn {
  border-left: 3px solid rgba(255,170,80,.55);
  padding: 10px 12px;
  background: rgba(255,255,255,.02);
  border-radius: 14px;
  color: rgba(234,241,255,.82);
}

.table-wrap {
  border: 1px solid rgba(234,241,255,.10);
  border-radius: 16px;
  padding: 10px 10px;
  background: rgba(255,255,255,.02);
}

/* Metric text */
[data-testid="stMetricLabel"] p {
    color: #CBD5E1 !important;
    font-size: 1rem !important;
}
[data-testid="stMetricValue"] div {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* Sidebar text */
[data-testid="stCheckbox"] label p {
    color: #94A3B8 !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
div[data-testid="stVerticalBlock"] > div > div > div > span {
    color: #1E293B !important;
    font-weight: 850 !important;
    font-size: 1.25rem !important;
    opacity: 1 !important;
}
[data-testid="stSidebarNav"] span {
    color: #0F172A !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] p {
    color: #0F172A !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] {
    background-color: #E2E8F0 !important;
}

span, p, small, .small-muted {
    color: #F8FAFC !important;
    opacity: 1 !important;
    font-weight: 500 !important;
}

.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
</style>
""",
    unsafe_allow_html=True,
)

# ==================== HERO ====================
st.markdown(
    """
<div class="hero">
  <h1>🧠 Parasitic Vision</h1>
  <p>
    AI detection in parasitic images helps make diagnosis faster, more accurate, and more consistent, especially where expert microscopists are limited. It supports early treatment and improves public health surveillance.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# =========================
# Constants / Config
# =========================
CLASS_LABELS: List[str] = [
    "artifact",
    "opisthorchis viverrini egg",
    "minute intestinal fluke egg",
]

DEFAULT_INPUT_SIZE: Tuple[int, int] = (128, 128)

# Prefer model next to project root: parasitic_platform/pages_components/...
# This file is parasitic_platform/pages/3_Parasitic_Vision.py
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parent.parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "pages_components" / "img_classified_dataset2_paca.keras"


# =========================
# Helpers
# =========================
def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def pil_to_b64(img: Image.Image, fmt: str = "PNG") -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def compute_center_cell_crop_box(
    img: Image.Image,
    viewport: int,
    zoom: float,
    pan_x: float,
    pan_y: float,
) -> Tuple[int, int, int, int]:
    """
    Convert viewer state (viewport + zoom + pan) to crop box on original image,
    using the center cell of a 3x3 grid in the viewer.
    """
    w0, h0 = img.size
    vp = float(max(1, viewport))
    z = float(max(1e-6, zoom))

    step = vp / 3.0
    cell_l, cell_t = step, step
    cell_r, cell_b = 2.0 * step, 2.0 * step

    base_scale = min(vp / float(w0), vp / float(h0))
    scale = max(1e-9, base_scale * z)

    cx = vp / 2.0
    cy = vp / 2.0

    def screen_to_image(sx: float, sy: float) -> Tuple[float, float]:
        ix = (sx - cx - float(pan_x)) / scale + (w0 / 2.0)
        iy = (sy - cy - float(pan_y)) / scale + (h0 / 2.0)
        return ix, iy

    l, t = screen_to_image(cell_l, cell_t)
    r, b = screen_to_image(cell_r, cell_b)

    left = clamp(min(l, r), 0.0, float(w0))
    right = clamp(max(l, r), 0.0, float(w0))
    top = clamp(min(t, b), 0.0, float(h0))
    bottom = clamp(max(t, b), 0.0, float(h0))

    # Ensure at least 1 pixel in each dimension
    if right - left < 1:
        right = clamp(left + 1, 0.0, float(w0))
    if bottom - top < 1:
        bottom = clamp(top + 1, 0.0, float(h0))

    # Final integer conversion (safe bounds)
    x1 = int(np.floor(left))
    y1 = int(np.floor(top))
    x2 = int(np.ceil(right))
    y2 = int(np.ceil(bottom))

    x1 = max(0, min(x1, w0 - 1))
    y1 = max(0, min(y1, h0 - 1))
    x2 = max(x1 + 1, min(x2, w0))
    y2 = max(y1 + 1, min(y2, h0))

    return (x1, y1, x2, y2)


def resolve_model_path() -> Path:
    """
    Resolve model path robustly (portable across machines).
    """
    candidate_paths = [
        DEFAULT_MODEL_PATH,
        PROJECT_ROOT / "pages_components" / "img_classified_dataset2_paca.keras",
        Path("pages_components") / "img_classified_dataset2_paca.keras",
    ]

    for p in candidate_paths:
        if p.exists():
            return p.resolve()

    raise FileNotFoundError(
        "Model file not found. Expected something like:\n"
        f"- {DEFAULT_MODEL_PATH}\n"
        "Please ensure 'img_classified_dataset2_paca.keras' is inside 'pages_components/'."
    )


@st.cache_resource(show_spinner=False)
def load_model_cached(model_path_str: str):
    return tf.keras.models.load_model(model_path_str)


def get_model_input_size(model: tf.keras.Model, fallback: Tuple[int, int] = DEFAULT_INPUT_SIZE) -> Tuple[int, int]:
    """
    Try to infer model input size from Keras model.input_shape.
    Returns (width, height).
    """
    try:
        shape = model.input_shape  # e.g. (None, 128, 128, 3)
        if isinstance(shape, list) and len(shape) > 0:
            shape = shape[0]
        if shape is None or len(shape) < 4:
            return fallback

        h = shape[1]
        w = shape[2]
        if isinstance(h, int) and isinstance(w, int) and h > 0 and w > 0:
            return (w, h)
    except Exception:
        pass
    return fallback


def prepare_input_tensor(
    crop_img: Image.Image,
    model: tf.keras.Model,
) -> np.ndarray:
    """
    Preprocess ROI for model inference.
    """
    input_w, input_h = get_model_input_size(model, fallback=DEFAULT_INPUT_SIZE)
    resized = crop_img.convert("RGB").resize((input_w, input_h))
    arr = np.asarray(resized, dtype=np.float32)

    x = np.expand_dims(arr, axis=0)  # (1, H, W, 3)
    return x


def postprocess_prediction(
    y_pred_raw: np.ndarray,
    labels: List[str],
) -> Dict[str, Any]:
    """
    Convert model output to a unified dict:
      {
        "pred_index": int,
        "pred_label": str,
        "scores": List[float],
        "display_pairs": List[(label, score)]
      }

    Handles:
    - multiclass softmax logits/probabilities shape (1, C)
    - binary sigmoid shape (1, 1)
    - scalar outputs
    """
    y = np.asarray(y_pred_raw)

    # Squeeze batch dimension safely
    if y.ndim == 0:
        y = y.reshape(1)
    elif y.ndim >= 2 and y.shape[0] == 1:
        y = y[0]

    # Case 1: scalar / binary sigmoid
    if y.ndim == 0 or (y.ndim == 1 and y.shape[0] == 1):
        score = float(np.ravel(y)[0])

        # Clamp if probability-like; if not, still show raw-ish as score.
        score_clamped = float(max(0.0, min(1.0, score)))
        if len(labels) >= 2:
            scores = [1.0 - score_clamped, score_clamped]
            pred_index = int(score_clamped >= 0.5)
            used_labels = labels[:2]
        else:
            scores = [score_clamped]
            pred_index = 0
            used_labels = labels[:1] if labels else ["class_0"]

        pred_label = used_labels[pred_index] if pred_index < len(used_labels) else f"class_{pred_index}"
        display_pairs = list(zip(used_labels, scores))
        return {
            "pred_index": pred_index,
            "pred_label": pred_label,
            "scores": scores,
            "display_pairs": display_pairs,
        }

    # Case 2: vector outputs (multiclass)
    if y.ndim == 1:
        scores = [float(v) for v in y.tolist()]
        pred_index = int(np.argmax(y))

        # Align labels length to output length
        if len(labels) < len(scores):
            used_labels = labels + [f"class_{i}" for i in range(len(labels), len(scores))]
        else:
            used_labels = labels[: len(scores)]

        pred_label = used_labels[pred_index]
        display_pairs = list(zip(used_labels, scores))
        return {
            "pred_index": pred_index,
            "pred_label": pred_label,
            "scores": scores,
            "display_pairs": display_pairs,
        }

    # Fallback weird shapes -> flatten
    flat = y.flatten()
    scores = [float(v) for v in flat.tolist()]
    pred_index = int(np.argmax(flat))
    if len(labels) < len(scores):
        used_labels = labels + [f"class_{i}" for i in range(len(labels), len(scores))]
    else:
        used_labels = labels[: len(scores)]
    pred_label = used_labels[pred_index]
    display_pairs = list(zip(used_labels, scores))
    return {
        "pred_index": pred_index,
        "pred_label": pred_label,
        "scores": scores,
        "display_pairs": display_pairs,
    }


# -------------------- Quick Links --------------------
st.markdown('<div class="section-label">Quick links</div>', unsafe_allow_html=True)
ql1, ql2, ql3, ql4 = st.columns(4, gap="small")
with ql1:
    st.page_link("app.py", label="Home", icon="🏠")
with ql2:
    st.page_link("pages/1_Human_Parasite.py", label="Human Parasite", icon="🧬")
with ql3:
    st.page_link("pages/2_Parasitology_Research.py", label="Parasitology Research", icon="📚")
with ql4:
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")

# =========================
# Controls
# =========================
st.markdown('<div class="section-label">Inference controls</div>', unsafe_allow_html=True)

ctrl1, ctrl2 = st.columns(2)
with ctrl1:
    viewport = st.slider("Viewport size (px)", 360, 900, 360, 20)
with ctrl2:
    st.caption("Tip: Zoom/pan to place the target object inside the center box, then click **Calculate**.")

# =========================
# Session state
# =========================
if "viewer" not in st.session_state:
    st.session_state.viewer = {
        "zoom": 1.0,
        "panX": 0.0,
        "panY": 0.0,
        "viewport": int(viewport),
    }

# sync viewport from slider
st.session_state.viewer["viewport"] = int(viewport)

# Token guard
if "last_processed_calc_token" not in st.session_state:
    st.session_state.last_processed_calc_token = ""

# Persist last inference result so it remains visible across reruns
if "pv_last_result" not in st.session_state:
    st.session_state.pv_last_result = None

# =========================
# Upload image
# =========================
img_file = st.file_uploader(
    "Upload original image",
    type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"],
)

if not img_file:
    st.info("Upload an image to start.")
    st.stop()

try:
    original_img = Image.open(img_file).convert("RGB")
except UnidentifiedImageError:
    st.error("Unable to read the uploaded image. Please upload a valid PNG/JPG/TIFF/BMP file.")
    st.stop()
except Exception as e:
    st.error("Unexpected error while opening image.")
    st.exception(e)
    st.stop()

img_b64 = pil_to_b64(original_img, fmt="PNG")

# =========================
# Render viewer component
# =========================
state = viewer_component(
    image_b64=img_b64,
    viewport=int(st.session_state.viewer["viewport"]),
    init_zoom=float(st.session_state.viewer["zoom"]),
    init_panX=float(st.session_state.viewer["panX"]),
    init_panY=float(st.session_state.viewer["panY"]),
)

# Persist viewer state if component returns one
if isinstance(state, dict):
    try:
        st.session_state.viewer["zoom"] = float(state.get("zoom", st.session_state.viewer["zoom"]))
        st.session_state.viewer["panX"] = float(state.get("panX", st.session_state.viewer["panX"]))
        st.session_state.viewer["panY"] = float(state.get("panY", st.session_state.viewer["panY"]))
        st.session_state.viewer["viewport"] = int(state.get("viewport", st.session_state.viewer["viewport"]))
    except Exception:
        # Fallback to previous values if malformed component payload appears
        pass

st.caption(
    f"zoom={st.session_state.viewer['zoom']:.3f}, "
    f"panX={st.session_state.viewer['panX']:.1f}, "
    f"panY={st.session_state.viewer['panY']:.1f}, "
    f"vp={st.session_state.viewer['viewport']}"
)

# =========================
# Heavy calculation: ONLY when canvas Calculate clicked with NEW calc_token
# =========================
do_calc = False
calc_token = ""

if isinstance(state, dict) and state.get("action") == "calculate":
    incoming_token = str(state.get("calc_token", "")).strip()

    # Process only if token is new and non-empty
    if incoming_token and incoming_token != st.session_state.last_processed_calc_token:
        do_calc = True
        calc_token = incoming_token
        # Mark as processed immediately to avoid accidental double-processing during rerun loops
        st.session_state.last_processed_calc_token = incoming_token

if do_calc:
    zoom = float(st.session_state.viewer["zoom"])
    pan_x = float(st.session_state.viewer["panX"])
    pan_y = float(st.session_state.viewer["panY"])
    vp_recv = int(st.session_state.viewer["viewport"])

    # Load model (cached)
    try:
        model_path = resolve_model_path()
        model = load_model_cached(str(model_path))
    except Exception as e:
        st.error("Failed to load the TensorFlow/Keras model.")
        st.exception(e)
        st.stop()

    # Crop ROI according to viewer state (center cell)
    box = compute_center_cell_crop_box(original_img, vp_recv, zoom, pan_x, pan_y)
    roi_crop = original_img.crop(box)

    # Inference
    try:
        x_input = prepare_input_tensor(
            crop_img=roi_crop,
            model=model,
        )
        y_raw = model.predict(x_input, verbose=0)
        pred_info = postprocess_prediction(y_raw, CLASS_LABELS)

        # Save latest result in session_state
        st.session_state.pv_last_result = {
            "calc_token": calc_token,
            "zoom": zoom,
            "pan_x": pan_x,
            "pan_y": pan_y,
            "viewport": vp_recv,
            "box": box,
            "crop": roi_crop.copy(),
            "pred_info": pred_info,
            "raw_output": np.asarray(y_raw).tolist(),
            "input_shape": tuple(x_input.shape),
            "model_path": str(model_path),
        }

    except Exception as e:
        st.error("Model inference error.")
        st.exception(e)
        st.stop()

# =========================
# Render latest inference result (if available)
# =========================
result = st.session_state.pv_last_result

if result is not None:
    st.markdown("---")
    c1, c2 = st.columns([1.1, 1.2], gap="large")

    with c1:
        st.subheader("Region of Interest")
        st.image(result["crop"], use_container_width=True)
        st.caption(
            f"token={result['calc_token']} | "
            f"zoom={result['zoom']:.3f}, pan_x={result['pan_x']:.1f}, pan_y={result['pan_y']:.1f}, "
            f"vp={result['viewport']} | box={result['box']}"
        )

    with c2:
        pred_info = result["pred_info"]
        pred_index = pred_info["pred_index"]
        pred_label = pred_info["pred_label"]

        st.markdown(f"### Prediction: **{pred_label}**")
        st.caption(f"Predicted class index: {pred_index}")

        # Display scores
        for lbl, score in pred_info["display_pairs"]:
            # If score looks like probability, show percent. Otherwise show raw.
            if 0.0 <= float(score) <= 1.0:
                st.write(f"**{lbl}**: {float(score):.4f} ({float(score) * 100:.2f}%)")
                # Progress bar only makes sense for [0,1]
                try:
                    st.progress(float(score))
                except Exception:
                    pass
            else:
                st.write(f"**{lbl}**: {float(score):.6f}")
                
# -------------------- Footer --------------------
st.markdown(
    "<div style='margin-top:16px; color:rgba(234,241,255,.45); font-size:.86rem;'>"
    "© Parasitic Platform • Intelligent Platform for Parasitic Diseases 2026 • Penchom Janwan"
    "</div>",
    unsafe_allow_html=True,
)
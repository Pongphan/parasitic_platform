import io
import base64
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

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

# ==================== THEME ====================
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
.block-container { padding-top: 1.0rem !important; padding-bottom: 2.0rem !important; max-width: 1280px; }

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

THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parent.parent
MODELS_DIR = PROJECT_ROOT / "pages_components"


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

    if right - left < 1:
        right = clamp(left + 1, 0.0, float(w0))
    if bottom - top < 1:
        bottom = clamp(top + 1, 0.0, float(h0))

    x1 = int(np.floor(left))
    y1 = int(np.floor(top))
    x2 = int(np.ceil(right))
    y2 = int(np.ceil(bottom))

    x1 = max(0, min(x1, w0 - 1))
    y1 = max(0, min(y1, h0 - 1))
    x2 = max(x1 + 1, min(x2, w0))
    y2 = max(y1 + 1, min(y2, h0))

    return (x1, y1, x2, y2)


def discover_models(models_dir: Path) -> List[Path]:
    """
    Discover loadable TensorFlow/Keras models in pages_components:
    - *.keras
    - *.h5 / *.hdf5
    - SavedModel directories (containing saved_model.pb)
    """
    if not models_dir.exists():
        return []

    found: List[Path] = []

    # File-based Keras models
    for ext in ("*.keras", "*.h5", "*.hdf5"):
        found.extend(sorted(models_dir.glob(ext)))

    # SavedModel folders
    for p in sorted(models_dir.iterdir()):
        if p.is_dir() and (p / "saved_model.pb").exists():
            found.append(p)

    # Deduplicate while preserving order
    dedup: List[Path] = []
    seen = set()
    for p in found:
        key = str(p.resolve())
        if key not in seen:
            dedup.append(p.resolve())
            seen.add(key)
    return dedup


def path_display_name(p: Path) -> str:
    """Friendly name for UI."""
    if p.is_dir():
        return f"{p.name}  [SavedModel]"
    return p.name


@st.cache_resource(show_spinner=False)
def load_model_cached(model_path_str: str):
    return tf.keras.models.load_model(model_path_str)


def get_model_input_size(
    model: tf.keras.Model,
    fallback: Tuple[int, int] = DEFAULT_INPUT_SIZE
) -> Tuple[int, int]:
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
    normalize_to_01: bool = False,
) -> np.ndarray:
    input_w, input_h = get_model_input_size(model, fallback=DEFAULT_INPUT_SIZE)
    resized = crop_img.convert("RGB").resize((input_w, input_h))
    arr = np.asarray(resized, dtype=np.float32)

    if normalize_to_01:
        arr = arr / 255.0

    x = np.expand_dims(arr, axis=0)  # (1, H, W, 3)
    return x


def postprocess_prediction(y_pred_raw: np.ndarray, labels: List[str]) -> Dict[str, Any]:
    """
    Convert model output to unified dict.
    Handles multiclass vector, binary sigmoid scalar, and odd shapes.
    """
    y = np.asarray(y_pred_raw)

    if y.ndim == 0:
        y = y.reshape(1)
    elif y.ndim >= 2 and y.shape[0] == 1:
        y = y[0]

    # Binary scalar
    if y.ndim == 0 or (y.ndim == 1 and y.shape[0] == 1):
        score = float(np.ravel(y)[0])
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
        return {
            "pred_index": pred_index,
            "pred_label": pred_label,
            "scores": scores,
            "display_pairs": list(zip(used_labels, scores)),
            "num_classes": len(scores),
        }

    # Multiclass vector
    if y.ndim == 1:
        scores = [float(v) for v in y.tolist()]
        pred_index = int(np.argmax(y))

        if len(labels) < len(scores):
            used_labels = labels + [f"class_{i}" for i in range(len(labels), len(scores))]
        else:
            used_labels = labels[:len(scores)]

        return {
            "pred_index": pred_index,
            "pred_label": used_labels[pred_index],
            "scores": scores,
            "display_pairs": list(zip(used_labels, scores)),
            "num_classes": len(scores),
        }

    # Fallback
    flat = y.flatten()
    scores = [float(v) for v in flat.tolist()]
    pred_index = int(np.argmax(flat))
    if len(labels) < len(scores):
        used_labels = labels + [f"class_{i}" for i in range(len(labels), len(scores))]
    else:
        used_labels = labels[:len(scores)]
    return {
        "pred_index": pred_index,
        "pred_label": used_labels[pred_index],
        "scores": scores,
        "display_pairs": list(zip(used_labels, scores)),
        "num_classes": len(scores),
    }


def softmax_numpy(logits: np.ndarray) -> np.ndarray:
    x = np.asarray(logits, dtype=np.float64)
    x = x - np.max(x)
    ex = np.exp(x)
    den = np.sum(ex)
    if den <= 0:
        return np.zeros_like(x, dtype=np.float64)
    return ex / den


def normalize_scores_for_ensemble(scores: List[float]) -> Optional[np.ndarray]:
    """
    Convert per-model scores to a comparable probability-like vector for ensemble averaging.
    - If all scores in [0,1] and sum ~ 1 => use as-is
    - If all scores in [0,1] but sum != 1 => normalize by sum (if sum>0)
    - Else => apply softmax (treat as logits)
    Returns None if invalid.
    """
    if scores is None or len(scores) == 0:
        return None
    x = np.asarray(scores, dtype=np.float64)
    if not np.all(np.isfinite(x)):
        return None

    in01 = np.all((x >= 0.0) & (x <= 1.0))
    s = float(np.sum(x))

    if in01 and np.isclose(s, 1.0, atol=1e-3):
        return x
    if in01 and s > 0:
        return x / s

    # logits-like
    return softmax_numpy(x)


def build_ensemble_summary(per_model_results: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Ensemble only if all selected models share same num_classes.
    Uses average normalized scores + majority vote.
    """
    if not per_model_results:
        return None

    n_classes_set = {int(r["pred_info"]["num_classes"]) for r in per_model_results if "pred_info" in r}
    if len(n_classes_set) != 1:
        return None

    n_classes = next(iter(n_classes_set))
    if n_classes <= 0:
        return None

    prob_vectors = []
    labels_ref = None
    votes = []

    for r in per_model_results:
        pred_info = r["pred_info"]
        vec = normalize_scores_for_ensemble(pred_info["scores"])
        if vec is None or len(vec) != n_classes:
            return None
        prob_vectors.append(vec)
        votes.append(int(pred_info["pred_index"]))
        if labels_ref is None:
            labels_ref = [lbl for lbl, _ in pred_info["display_pairs"]]

    if not prob_vectors or labels_ref is None:
        return None

    avg_scores = np.mean(np.vstack(prob_vectors), axis=0)
    pred_index = int(np.argmax(avg_scores))
    pred_label = labels_ref[pred_index] if pred_index < len(labels_ref) else f"class_{pred_index}"

    # majority vote
    vote_counts = {i: votes.count(i) for i in sorted(set(votes))}
    maj_index = max(vote_counts.items(), key=lambda kv: kv[1])[0]
    maj_label = labels_ref[maj_index] if maj_index < len(labels_ref) else f"class_{maj_index}"

    return {
        "avg_scores": avg_scores.tolist(),
        "avg_pred_index": pred_index,
        "avg_pred_label": pred_label,
        "majority_vote_index": int(maj_index),
        "majority_vote_label": maj_label,
        "vote_counts": vote_counts,
        "labels": labels_ref,
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

available_model_paths = discover_models(MODELS_DIR)
model_name_to_path: Dict[str, Path] = {path_display_name(p): p for p in available_model_paths}
model_names = list(model_name_to_path.keys())

default_selection = model_names[:1] if model_names else []

cA, cB = st.columns([1.4, 1.0], gap="medium")
with cA:
    viewport = st.slider("Viewport size (px)", 360, 900, 400, 20)
with cB:
    normalize_to_01 = st.checkbox("Normalize input (/255)", value=False)

if not available_model_paths:
    st.error(f"No model files found in: {MODELS_DIR}")
    st.info("Put your models in `pages_components/` (.keras, .h5, .hdf5, or SavedModel folder).")
    st.stop()

selected_model_names = st.multiselect(
    "Select model(s) from pages_components",
    options=model_names,
    default=default_selection,
    help="You can select multiple models and run inference simultaneously.",
)

if not selected_model_names:
    st.warning("Please select at least one model.")
    st.stop()

selected_model_paths = [model_name_to_path[name] for name in selected_model_names]

st.caption(
    "Tip: Zoom/pan to place the target object inside the center box, then click **Calculate**. "
    "The app will run all selected models on the same ROI."
)

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

st.session_state.viewer["viewport"] = int(viewport)

if "last_processed_calc_token" not in st.session_state:
    st.session_state.last_processed_calc_token = ""

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

if isinstance(state, dict):
    try:
        st.session_state.viewer["zoom"] = float(state.get("zoom", st.session_state.viewer["zoom"]))
        st.session_state.viewer["panX"] = float(state.get("panX", st.session_state.viewer["panX"]))
        st.session_state.viewer["panY"] = float(state.get("panY", st.session_state.viewer["panY"]))
        st.session_state.viewer["viewport"] = int(state.get("viewport", st.session_state.viewer["viewport"]))
    except Exception:
        pass

st.caption(
    f"zoom={st.session_state.viewer['zoom']:.3f}, "
    f"panX={st.session_state.viewer['panX']:.1f}, "
    f"panY={st.session_state.viewer['panY']:.1f}, "
    f"vp={st.session_state.viewer['viewport']}"
)

# =========================
# Heavy calculation trigger
# =========================
do_calc = False
calc_token = ""

if isinstance(state, dict) and state.get("action") == "calculate":
    incoming_token = str(state.get("calc_token", "")).strip()
    if incoming_token and incoming_token != st.session_state.last_processed_calc_token:
        do_calc = True
        calc_token = incoming_token
        st.session_state.last_processed_calc_token = incoming_token

# =========================
# Run inference on ALL selected models
# =========================
if do_calc:
    zoom = float(st.session_state.viewer["zoom"])
    pan_x = float(st.session_state.viewer["panX"])
    pan_y = float(st.session_state.viewer["panY"])
    vp_recv = int(st.session_state.viewer["viewport"])

    box = compute_center_cell_crop_box(original_img, vp_recv, zoom, pan_x, pan_y)
    roi_crop = original_img.crop(box)

    per_model_results: List[Dict[str, Any]] = []
    load_errors: List[str] = []
    infer_errors: List[str] = []

    for model_path in selected_model_paths:
        model_name = path_display_name(model_path)

        try:
            model = load_model_cached(str(model_path))
        except Exception as e:
            load_errors.append(f"{model_name}: {e}")
            continue

        try:
            x_input = prepare_input_tensor(
                crop_img=roi_crop,
                model=model,
                normalize_to_01=normalize_to_01,
            )
            y_raw = model.predict(x_input, verbose=0)
            pred_info = postprocess_prediction(y_raw, CLASS_LABELS)

            per_model_results.append(
                {
                    "model_name": model_name,
                    "model_path": str(model_path),
                    "input_shape": tuple(x_input.shape),
                    "raw_output": np.asarray(y_raw).tolist(),
                    "pred_info": pred_info,
                }
            )
        except Exception as e:
            infer_errors.append(f"{model_name}: {e}")
            continue

    ensemble_summary = build_ensemble_summary(per_model_results)

    st.session_state.pv_last_result = {
        "calc_token": calc_token,
        "zoom": zoom,
        "pan_x": pan_x,
        "pan_y": pan_y,
        "viewport": vp_recv,
        "box": box,
        "crop": roi_crop.copy(),
        "per_model_results": per_model_results,
        "ensemble_summary": ensemble_summary,
        "load_errors": load_errors,
        "infer_errors": infer_errors,
        "normalize_to_01": normalize_to_01,
    }

# =========================
# Render latest result
# =========================
result = st.session_state.pv_last_result

if result is not None:
    st.markdown("---")
    left_col, right_col = st.columns([1.05, 1.35], gap="large")

    with left_col:
        st.subheader("Region of Interest")
        st.image(result["crop"], use_container_width=True)
        st.caption(
            f"token={result['calc_token']} | "
            f"zoom={result['zoom']:.3f}, pan_x={result['pan_x']:.1f}, pan_y={result['pan_y']:.1f}, "
            f"vp={result['viewport']} | box={result['box']}"
        )

        if result.get("load_errors"):
            st.markdown('<div class="warn"><b>Model load errors</b></div>', unsafe_allow_html=True)
            for msg in result["load_errors"]:
                st.error(msg)

        if result.get("infer_errors"):
            st.markdown('<div class="warn"><b>Inference errors</b></div>', unsafe_allow_html=True)
            for msg in result["infer_errors"]:
                st.error(msg)

    with right_col:
        st.subheader("Multi-model Predictions")

        per_model_results = result.get("per_model_results", [])
        if not per_model_results:
            st.error("No model produced a valid prediction.")
        else:
            # ---- Ensemble summary (if compatible) ----
            ens = result.get("ensemble_summary")
            if ens is not None:
                st.markdown("### Ensemble Summary")
                st.write(f"**Average-score prediction:** `{ens['avg_pred_label']}` (class {ens['avg_pred_index']})")
                st.write(f"**Majority vote:** `{ens['majority_vote_label']}` (class {ens['majority_vote_index']})")

                vote_text = ", ".join([f"class_{k}: {v}" for k, v in ens["vote_counts"].items()])
                st.caption(f"Votes → {vote_text}")

                with st.expander("Average scores (ensemble)"):
                    for lbl, score in zip(ens["labels"], ens["avg_scores"]):
                        st.write(f"**{lbl}**: {float(score):.4f} ({float(score)*100:.2f}%)")
                        try:
                            st.progress(float(score))
                        except Exception:
                            pass
            else:
                st.info("Ensemble summary is unavailable (selected models have incompatible output dimensions).")

            st.markdown("### Per-model Details")

            # summary table-like metrics
            for i, mr in enumerate(per_model_results, start=1):
                pred_info = mr["pred_info"]
                with st.expander(f"{i}. {mr['model_name']} → {pred_info['pred_label']}", expanded=(i == 1)):
                    st.write(f"**Prediction:** {pred_info['pred_label']} (class {pred_info['pred_index']})")

                    for lbl, score in pred_info["display_pairs"]:
                        if 0.0 <= float(score) <= 1.0:
                            st.write(f"**{lbl}**: {float(score):.4f} ({float(score) * 100:.2f}%)")
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

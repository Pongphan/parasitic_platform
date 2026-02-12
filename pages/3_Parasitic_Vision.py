# pages/3_Parasitic_Vision.py
import io
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Parasitic Vision", page_icon="🧠", layout="wide")

# ==================== THEME (same look & feel as app.py) ====================
st.markdown(
    """
<style>
:root{
  --bg0:#070A12;
  --bg1:#0A1020;
  --txt:#EAF1FF;
  --muted:rgba(234,241,255,.72);
  --muted2:rgba(234,241,255,.55);
  --stroke:rgba(234,241,255,.10);
  --stroke2:rgba(234,241,255,.16);
}

.stApp {
  background:
    radial-gradient(1200px 600px at 20% 10%, rgba(110,231,255,.08), transparent 55%),
    radial-gradient(900px 500px at 85% 15%, rgba(166,255,203,.06), transparent 55%),
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
  background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
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
    radial-gradient(600px 240px at 80% 0%, rgba(166,255,203,.16), transparent 55%);
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
  color: var(--muted);
  font-size: 1.0rem;
}

.section-label{
  margin-top: 1.05rem;
  margin-bottom: .55rem;
  color: var(--muted2);
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
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
</style>
""",
    unsafe_allow_html=True,
)

# ==================== HEADER ====================
st.markdown(
    """
<div class="hero">
  <h1>🧠 Parasitic Vision</h1>
  <p>
    Microscopy AI workspace: upload images → select model → run inference → review detections, confidence,
    and QA metrics. (Includes a demo model; plug in your real YOLO/TensorFlow models later.)
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="warn">
<b>Note:</b> This page ships with a <i>demo</i> inference backend (rule-based “toy detector”) so the UI works immediately.
Replace the <span class="mono">run_inference()</span> function with your trained model (YOLO/TensorFlow).
</div>
""",
    unsafe_allow_html=True,
)

# ==================== MODEL REGISTRY (UI selection) ====================
@dataclass
class ModelSpec:
    key: str
    name: str
    family: str
    input_size: Tuple[int, int]
    classes: List[str]
    notes: List[str]


MODEL_REGISTRY: Dict[str, ModelSpec] = {
    "demo_egg_detector": ModelSpec(
        key="demo_egg_detector",
        name="Demo Egg Detector (rule-based)",
        family="Demo",
        input_size=(1024, 1024),
        classes=["egg_like_object"],
        notes=[
            "Uses simple image processing to find round/oval bright regions.",
            "For UI testing only—replace with real model inference.",
        ],
    ),
    "placeholder_yolov8": ModelSpec(
        key="placeholder_yolov8",
        name="YOLOv8 (placeholder)",
        family="YOLO",
        input_size=(640, 640),
        classes=["class0", "class1", "class2"],
        notes=[
            "Placeholder entry. Wire to Ultralytics YOLO inference locally.",
            "Good for multi-class egg detection with tiling for large images.",
        ],
    ),
    "placeholder_tf": ModelSpec(
        key="placeholder_tf",
        name="TensorFlow Detector (placeholder)",
        family="TensorFlow",
        input_size=(512, 512),
        classes=["egg", "artifact"],
        notes=[
            "Placeholder entry. Wire to your TensorFlow/Keras model.",
            "Recommended: export SavedModel and implement preprocessing consistently.",
        ],
    ),
}

# ==================== UTILITIES ====================
def pil_to_np(img: Image.Image) -> np.ndarray:
    return np.array(img.convert("RGB"))

def np_to_pil(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(arr.astype(np.uint8))

def resize_keep_aspect(img: Image.Image, max_side: int = 1600) -> Image.Image:
    w, h = img.size
    s = max(w, h)
    if s <= max_side:
        return img
    scale = max_side / s
    return img.resize((int(w * scale), int(h * scale)), Image.BILINEAR)

def draw_boxes(
    img: Image.Image,
    dets: List[Dict],
    show_labels: bool = True,
    show_scores: bool = True,
) -> Image.Image:
    out = img.copy().convert("RGB")
    draw = ImageDraw.Draw(out)

    # Default font; if missing, fallback to PIL default
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 14)
    except Exception:
        font = ImageFont.load_default()

    for d in dets:
        x1, y1, x2, y2 = d["bbox"]
        label = d.get("label", "object")
        score = d.get("score", None)

        # Simple visual styling (no external libs)
        draw.rectangle([x1, y1, x2, y2], outline=(110, 231, 255), width=3)

        if show_labels or show_scores:
            tag = label
            if show_scores and score is not None:
                tag += f"  {score:.2f}"
            tw, th = draw.textbbox((0, 0), tag, font=font)[2:]
            pad = 4
            draw.rectangle([x1, y1 - th - 2 * pad, x1 + tw + 2 * pad, y1], fill=(10, 16, 32))
            draw.text((x1 + pad, y1 - th - pad), tag, fill=(234, 241, 255), font=font)

    return out

def iou(boxA, boxB) -> float:
    ax1, ay1, ax2, ay2 = boxA
    bx1, by1, bx2, by2 = boxB
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
    inter = iw * ih
    areaA = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    areaB = max(0, bx2 - bx1) * max(0, by2 - by1)
    union = areaA + areaB - inter
    return (inter / union) if union > 0 else 0.0

def nms(dets: List[Dict], iou_thresh: float = 0.4) -> List[Dict]:
    dets = sorted(dets, key=lambda d: d.get("score", 0.0), reverse=True)
    kept: List[Dict] = []
    for d in dets:
        ok = True
        for k in kept:
            if iou(d["bbox"], k["bbox"]) >= iou_thresh:
                ok = False
                break
        if ok:
            kept.append(d)
    return kept

# ==================== DEMO INFERENCE BACKEND ====================
def run_inference_demo(img: Image.Image, conf_thresh: float = 0.35) -> List[Dict]:
    """
    A toy detector: finds bright oval-ish blobs using a crude threshold on grayscale.
    This is ONLY to make the UI functional without external ML dependencies.
    """
    arr = np.array(img.convert("L"), dtype=np.float32)
    # Normalize
    arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)

    # Adaptive-ish threshold based on percentile
    t = float(np.percentile(arr, 92))
    mask = (arr >= t).astype(np.uint8)

    # Find connected components (simple scan using OpenCV-free approach)
    # We'll approximate via bounding boxes of "on" pixels blocks by downsampling.
    # For microscopy, this is just a placeholder; replace with ML.
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return []

    # Create coarse grid clusters
    step = max(6, int(max(img.size) / 180))
    xsq = (xs // step) * step
    ysq = (ys // step) * step
    coords = np.stack([xsq, ysq], axis=1)

    # Group by unique coarse cell
    uniq, counts = np.unique(coords, axis=0, return_counts=True)

    dets: List[Dict] = []
    for (cx, cy), c in zip(uniq, counts):
        # heuristic: ignore tiny clusters
        if c < 10:
            continue
        # Create a box around the coarse cell cluster
        x1 = int(max(0, cx - 2 * step))
        y1 = int(max(0, cy - 2 * step))
        x2 = int(min(img.size[0], cx + 6 * step))
        y2 = int(min(img.size[1], cy + 6 * step))

        # score heuristic proportional to density and brightness
        local = arr[y1:y2, x1:x2]
        score = float(np.clip(local.mean() * 1.2, 0, 1))
        if score >= conf_thresh:
            dets.append({"bbox": (x1, y1, x2, y2), "label": "egg_like_object", "score": score})

    # NMS to reduce duplicates
    dets = nms(dets, iou_thresh=0.35)
    return dets


def run_inference(img: Image.Image, model_key: str, conf_thresh: float) -> List[Dict]:
    """
    Dispatch inference based on model_key.
    Replace placeholders with real inference functions.
    """
    if model_key == "demo_egg_detector":
        return run_inference_demo(img, conf_thresh=conf_thresh)

    # Placeholder: return empty detections until wired
    return []


# ==================== SIDEBAR: CONFIG ====================
with st.sidebar:
    st.title("Inference Settings")

    model_key = st.selectbox("Model", options=list(MODEL_REGISTRY.keys()), format_func=lambda k: MODEL_REGISTRY[k].name)
    ms = MODEL_REGISTRY[model_key]

    st.caption("Model summary")
    st.write(f"**Family:** {ms.family}")
    st.write(f"**Input:** {ms.input_size[0]}×{ms.input_size[1]}")
    st.write(f"**Classes:** {', '.join(ms.classes)}")
    with st.expander("Model notes"):
        for n in ms.notes:
            st.write(f"• {n}")

    st.divider()
    conf_thresh = st.slider("Confidence threshold", 0.05, 0.95, 0.35, 0.01)
    iou_thresh = st.slider("NMS IoU threshold", 0.10, 0.80, 0.35, 0.01)
    show_labels = st.toggle("Show labels", value=True)
    show_scores = st.toggle("Show confidence", value=True)

    st.divider()
    st.caption("Navigation")
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_Human_Parasite.py", label="Human Parasite", icon="🧬")
    st.page_link("pages/2_Parasitology_Research.py", label="Parasitology Research", icon="📚")
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")


# ==================== MAIN: UPLOAD + RUN ====================
st.markdown('<div class="section-label">Upload microscopy image</div>', unsafe_allow_html=True)

u1, u2 = st.columns([1.6, 1], gap="small")

with u1:
    uploaded = st.file_uploader(
        "Upload image (JPG/PNG/TIF)",
        type=["jpg", "jpeg", "png", "tif", "tiff"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )

with u2:
    st.markdown(
        """
<div class="panel">
  <h3>🎯 Workflow</h3>
  <div class="small-muted">
    1) Upload image → 2) Select model → 3) Run inference → 4) Review detections & export.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

if uploaded is None:
    st.markdown(
        """
<div class="note">
<b>Tip:</b> Use a representative microscopy image. If you plan to deploy, include multiple devices, stains,
and magnifications in training to reduce dataset shift.
</div>
""",
        unsafe_allow_html=True,
    )
    st.stop()

# Load image
raw_bytes = uploaded.getvalue()
img = Image.open(io.BytesIO(raw_bytes))
img = resize_keep_aspect(img, max_side=1800)

# ==================== PREVIEW + METADATA ====================
meta1, meta2, meta3, meta4 = st.columns(4, gap="small")
w, h = img.size
meta1.metric("Width", str(w))
meta2.metric("Height", str(h))
meta3.metric("Mode", img.mode)
meta4.metric("Model", MODEL_REGISTRY[model_key].family)

st.markdown('<div class="section-label">Preview</div>', unsafe_allow_html=True)
st.image(img, use_container_width=True)

# ==================== RUN INFERENCE ====================
run = st.button("Run inference", type="primary", use_container_width=True)

if "last_dets" not in st.session_state:
    st.session_state["last_dets"] = None
if "last_model" not in st.session_state:
    st.session_state["last_model"] = None
if "last_conf" not in st.session_state:
    st.session_state["last_conf"] = None

if run:
    with st.spinner("Running model inference..."):
        t0 = time.time()
        dets = run_inference(img, model_key=model_key, conf_thresh=conf_thresh)
        # Apply NMS with user threshold (demo already does; keep consistent)
        dets = nms(dets, iou_thresh=iou_thresh)
        dt = (time.time() - t0) * 1000.0

    st.session_state["last_dets"] = dets
    st.session_state["last_model"] = model_key
    st.session_state["last_conf"] = conf_thresh
    st.session_state["last_ms"] = dt

# ==================== DISPLAY OUTPUT ====================
dets = st.session_state.get("last_dets", None)
if dets is None:
    st.markdown(
        """
<div class="note">
Click <b>Run inference</b> to generate detections. The demo model will output toy boxes so you can validate UI.
</div>
""",
        unsafe_allow_html=True,
    )
    st.stop()

st.markdown('<div class="section-label">Inference output</div>', unsafe_allow_html=True)

out_img = draw_boxes(img, dets, show_labels=show_labels, show_scores=show_scores)
st.image(out_img, use_container_width=True)

# ==================== KPI / QA METRICS ====================
dt = float(st.session_state.get("last_ms", 0.0))
k1, k2, k3, k4 = st.columns(4, gap="small")
k1.metric("Detections", str(len(dets)))
k2.metric("Inference time (ms)", f"{dt:.0f}")
k3.metric("Confidence threshold", f"{conf_thresh:.2f}")
k4.metric("NMS IoU threshold", f"{iou_thresh:.2f}")

# Per-class counts
counts: Dict[str, int] = {}
for d in dets:
    counts[d["label"]] = counts.get(d["label"], 0) + 1

st.markdown('<div class="section-label">Detections table</div>', unsafe_allow_html=True)
rows = []
for i, d in enumerate(dets, start=1):
    x1, y1, x2, y2 = d["bbox"]
    rows.append(
        {
            "#": i,
            "Label": d.get("label", "object"),
            "Confidence": round(float(d.get("score", 0.0)), 3),
            "x1": int(x1),
            "y1": int(y1),
            "x2": int(x2),
            "y2": int(y2),
            "Width": int(x2 - x1),
            "Height": int(y2 - y1),
        }
    )
st.dataframe(rows, use_container_width=True, hide_index=True)

st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
st.markdown(
    f"""
<div class="table-wrap">
<b>Model:</b> {MODEL_REGISTRY[model_key].name}<br>
<b>Classes detected:</b> {", ".join([f"{k} ({v})" for k, v in counts.items()]) if counts else "None"}<br>
<b>Interpretation:</b> Detections represent candidate regions of interest (ROI). Confirm by microscopy review / clinical context.
</div>
""",
    unsafe_allow_html=True,
)

# ==================== EXPORTS ====================
st.markdown('<div class="section-label">Export</div>', unsafe_allow_html=True)
e1, e2, e3 = st.columns([1, 1, 1], gap="small")

# Export annotated image
buf = io.BytesIO()
out_img.save(buf, format="PNG")
png_bytes = buf.getvalue()

with e1:
    st.download_button(
        "Download annotated image (PNG)",
        data=png_bytes,
        file_name="parasitic_vision_output.png",
        mime="image/png",
        use_container_width=True,
    )

# Export detections as CSV (simple)
import csv
csv_buf = io.StringIO()
writer = csv.DictWriter(csv_buf, fieldnames=list(rows[0].keys()) if rows else ["#"])
writer.writeheader()
for r in rows:
    writer.writerow(r)
csv_bytes = csv_buf.getvalue().encode("utf-8")

with e2:
    st.download_button(
        "Download detections (CSV)",
        data=csv_bytes,
        file_name="parasitic_vision_detections.csv",
        mime="text/csv",
        use_container_width=True,
    )

# Export as YOLO txt (normalized xywh)
def to_yolo_line(bbox, img_w, img_h, cls_id=0) -> str:
    x1, y1, x2, y2 = bbox
    cx = ((x1 + x2) / 2.0) / img_w
    cy = ((y1 + y2) / 2.0) / img_h
    bw = (x2 - x1) / img_w
    bh = (y2 - y1) / img_h
    return f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}"

yolo_lines = []
class_to_id = {c: i for i, c in enumerate(MODEL_REGISTRY[model_key].classes)}
for d in dets:
    label = d.get("label", MODEL_REGISTRY[model_key].classes[0] if MODEL_REGISTRY[model_key].classes else "class0")
    cls_id = class_to_id.get(label, 0)
    yolo_lines.append(to_yolo_line(d["bbox"], w, h, cls_id=cls_id))
yolo_txt = ("\n".join(yolo_lines) + "\n").encode("utf-8")

with e3:
    st.download_button(
        "Download labels (YOLO .txt)",
        data=yolo_txt,
        file_name="parasitic_vision_labels.txt",
        mime="text/plain",
        use_container_width=True,
    )

# ==================== ADVANCED: HOW TO PLUG YOUR REAL MODEL ====================
st.markdown('<div class="section-label">Advanced integration</div>', unsafe_allow_html=True)
with st.expander("How to connect a real YOLOv8 model (Ultralytics)"):
    st.write(
        "Replace `run_inference()` with Ultralytics inference. Example logic (high-level):\n"
        "1) Load YOLO weights once (cache with st.cache_resource)\n"
        "2) Run model(img)\n"
        "3) Convert results to dets = [{'bbox':(x1,y1,x2,y2),'label':class,'score':conf}, ...]\n"
        "4) Apply NMS if needed (or use model's built-in)\n"
        "\n"
        "Tip: for large microscopy (e.g., 1920×1080 or bigger), use tiling with overlap and merge boxes."
    )

with st.expander("How to connect a TensorFlow/Keras detector"):
    st.write(
        "Replace `run_inference()` with TensorFlow SavedModel/Keras inference:\n"
        "- Ensure preprocessing (resize/normalize) matches training\n"
        "- Run model to get boxes/scores/classes\n"
        "- Map output to the `dets` format used here\n"
        "\n"
        "Tip: add calibration (temperature scaling) and threshold tuning per site/device."
    )

with st.expander("Recommended evaluation & QA (research-grade)"):
    st.write(
        "**Offline metrics**: mAP@0.5, mAP@0.5:0.95, F1 at operating point, calibration (ECE), robustness across stains/devices.\n"
        "\n"
        "**Operational QA**: failure mode taxonomy (blur, debris, low contrast), drift checks (image stats), human audit sampling.\n"
        "\n"
        "**Reader study**: compare human vs AI-assisted workflows (time-to-result, error rate, agreement)."
    )

# ==================== Footer ====================
st.markdown(
    "<div style='margin-top:16px; color:rgba(234,241,255,.45); font-size:.86rem;'>"
    "Parasitic Vision • Upload → Model → Inference → QA → Export • Demo backend included; wire to your trained model for real use"
    "</div>",
    unsafe_allow_html=True,
)

import io
import os
import uuid
import base64
import tempfile
import numpy as np
import streamlit as st
from PIL import Image
import tensorflow as tf

from viewer_component import viewer_component

# =========================
# Page config
# =========================
st.set_page_config(page_title="Image Classification", layout="wide")
st.title("Image Classification with Custom Model")

# =========================
# Helpers
# =========================
def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def pil_to_b64(img: Image.Image, fmt="PNG") -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def compute_center_cell_crop_box(img: Image.Image, viewport: int, zoom: float, pan_x: float, pan_y: float):
    w0, h0 = img.size
    vp = float(viewport)

    step = vp / 3.0
    cell_l, cell_t = step, step
    cell_r, cell_b = 2.0 * step, 2.0 * step

    base_scale = min(vp / w0, vp / h0)
    scale = base_scale * float(zoom)

    cx = vp / 2.0
    cy = vp / 2.0

    def screen_to_image(sx, sy):
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

    return (int(round(left)), int(round(top)), int(round(right)), int(round(bottom)))

def save_uploaded_keras(uploaded_file) -> str:
    suffix = ".keras"
    tmp_dir = tempfile.gettempdir()
    fname = f"upload_{uuid.uuid4().hex}{suffix}"
    path = os.path.join(tmp_dir, fname)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

@st.cache_resource(show_spinner=False)
def load_model_cached(model_path: str):
    return tf.keras.models.load_model(model_path)

# =========================
# Session state
# =========================

viewport = st.slider("Viewport size (px)", 360, 900, 600, 20)

if "viewer" not in st.session_state:
    st.session_state.viewer = {"zoom": 1.0, "panX": 0.0, "panY": 0.0, "viewport": int(viewport)}
st.session_state.viewer["viewport"] = int(viewport)

# Token guard (fix repeated/ignored clicks)
if "last_processed_calc_token" not in st.session_state:
    st.session_state.last_processed_calc_token = ""

# =========================
# Upload files
# =========================
img_file = st.file_uploader("Upload original image", type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"])

if not img_file:
    st.info("Upload an image to start.")
    st.stop()

img = Image.open(img_file).convert("RGB")
img_b64 = pil_to_b64(img, fmt="PNG")

# =========================
# Render viewer component
# - returns dict ONLY when Calculate clicked on canvas
# =========================
state = viewer_component(
    image_b64=img_b64,
    viewport=int(st.session_state.viewer["viewport"]),
    init_zoom=float(st.session_state.viewer["zoom"]),
    init_panX=float(st.session_state.viewer["panX"]),
    init_panY=float(st.session_state.viewer["panY"]),
)

# If got a state update (only on Calculate click), persist it
if isinstance(state, dict):
    st.session_state.viewer["zoom"] = float(state.get("zoom", st.session_state.viewer["zoom"]))
    st.session_state.viewer["panX"] = float(state.get("panX", st.session_state.viewer["panX"]))
    st.session_state.viewer["panY"] = float(state.get("panY", st.session_state.viewer["panY"]))
    st.session_state.viewer["viewport"] = int(state.get("viewport", st.session_state.viewer["viewport"]))

# Debug caption (optional)
st.caption(
    f"zoom={st.session_state.viewer['zoom']:.3f}, "
    f"panX={st.session_state.viewer['panX']:.1f}, panY={st.session_state.viewer['panY']:.1f}, "
    f"vp={st.session_state.viewer['viewport']}"
)

# =========================
# Heavy calculation: ONLY when canvas Calculate clicked with NEW calc_token
# =========================
do_calc = False
calc_token = None

if isinstance(state, dict) and state.get("action") == "calculate":
    calc_token = str(state.get("calc_token", ""))
    if calc_token and calc_token != st.session_state.last_processed_calc_token:
        do_calc = True

    # Mark as processed first to avoid accidental double-processing
    st.session_state.last_processed_calc_token = calc_token

    zoom = float(st.session_state.viewer["zoom"])
    pan_x = float(st.session_state.viewer["panX"])
    pan_y = float(st.session_state.viewer["panY"])
    vp_recv = int(st.session_state.viewer["viewport"])

    # Load model
    try:
        #model = load_model_cached("D:\P Works\Project Python\py\parasitic_platform\pages_components\img_classified_transf_paca.keras")
        model = load_model_cached("pages_components/img_classified_transf_paca.keras")

    except Exception as e:
        st.exception(e)
        st.stop()

    # Crop image according to viewer state (center cell)
    box = compute_center_cell_crop_box(img, vp_recv, zoom, pan_x, pan_y)
    crop = img.crop(box)

    try:
        size = (128,128)  # Model input size
        img = crop.convert("RGB")
        img = img.resize(size)
        img = np.array(img)
        img = img.astype(np.float32)
        img = np.expand_dims(img, axis=0)

        y_outp = model.predict(img, verbose=0)
        y_outp = np.array(y_outp)
        y_pred = np.argmax(y_outp, axis=1)

    except Exception as e:
        st.error("Model ERROR")
        st.exception(e)
        st.stop()

    st.markdown("---")
    c1, c2 = st.columns(2)
    labels_text = ["artifact","opisthorchis viverrini egg","minute intestinal fluke egg"]

    with c1:
        st.subheader("Region of Interest")
        st.image(crop, use_container_width=True)
        st.caption(
            f"token={calc_token} | zoom={zoom:.3f}, pan_x={pan_x:.1f}, pan_y={pan_y:.1f}, "
            f"vp={vp_recv} | box={box}"
        )

    with c2:
        st.markdown(f"### Prediction: **{y_pred}**")
        for i in range(len(y_outp)):
            st.write(f"Confidence: **{y_outp[i]}**")    

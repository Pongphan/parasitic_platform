"""ParD: explicit image selection, validated ROI inference, and traceable results."""

import base64
import csv
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

from pard_core import (
    build_ensemble_summary,
    compute_center_cell_crop_box,
    discover_dataset_images,
    discover_models,
    load_inference_model,
    load_model_spec,
    path_display_name,
    postprocess_prediction,
    prepare_input_tensor,
)
from pard_session import calculation_event, context_fingerprint, refresh_context, view_for_viewport
from viewer_component import viewer_component

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "pages_components"
DATASET_DIR = PROJECT_ROOT / "pages_dataset"
MANIFEST = MODELS_DIR / "model_manifest.json"

st.set_page_config(
    page_title="ParD - Parasite Detection",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(f"<style>{(PROJECT_ROOT / 'ui' / 'pard.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
st.markdown(
    '<div class="pard-hero"><h1>🔬 ParD - Parasite Detection</h1>'
    '<p>Choose a microscopy image, frame an object, and compare parasite classification '
    'scores across your selected models.</p></div>',
    unsafe_allow_html=True,
)


def file_stamp(path):
    files = sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else [path]
    return tuple((str(p), p.stat().st_size, p.stat().st_mtime_ns) for p in files)


@st.cache_data(max_entries=32, show_spinner=False)
def model_spec_cached(path, stamp, manifest_stamp):
    return load_model_spec(path, MANIFEST)


@st.cache_resource(max_entries=12, show_spinner=False)
def model_cached(path, fingerprint):
    return load_inference_model(path, fingerprint)


@st.cache_data(max_entries=24, show_spinner=False)
def image_bytes_cached(path, stamp):
    return Path(path).read_bytes()


@st.cache_data(max_entries=24, show_spinner=False)
def thumbnail_cached(path, stamp):
    with Image.open(io.BytesIO(image_bytes_cached(path, stamp))) as image:
        preview = image.convert("RGB")
        preview.thumbnail((400, 300))
        out = io.BytesIO()
        preview.save(out, format="PNG")
        return out.getvalue()


def select_dataset(path):
    st.session_state.pard_dataset_path = path
    st.session_state.pard_gallery_selection = path
    st.session_state.pard_source_mode = "Dataset gallery"


def uploaded_image_changed():
    if st.session_state.get("pard_upload") is not None:
        st.session_state.pard_source_mode = "Upload"


links = st.columns(4)
for column, path, label, icon in zip(
    links,
    ["app.py", "pages/1_Human_Parasite.py", "pages/2_Parasitology_Research.py", "pages/4_About_Project.py"],
    ["Home", "Human Parasite", "Parasitology Research", "About Project"],
    ["🏠", "🧬", "📚", "ℹ️"],
):
    with column:
        st.page_link(path, label=label, icon=icon)

st.subheader("Inference controls")
controls = st.columns([1.4, 1])
with controls[0]:
    viewport = st.slider("Viewport size (px)", 360, 900, 900, 20, key="pard_viewport")
with controls[1]:
    normalize_to_01 = st.checkbox(
        "Normalize input (/255)", value=False, key="pard_normalize",
        help="Manual override of each model's manifest preprocessing. Enable only when required by the training pipeline.",
    )

available_paths = discover_models(MODELS_DIR)
model_paths = {path_display_name(path): path for path in available_paths}
selected_names = st.multiselect(
    "Select model(s)", options=list(model_paths), default=list(model_paths), key="pard_models",
)
if not model_paths:
    st.error("No supported models were found in pages_components/.")
elif not selected_names:
    st.info("Select at least one model before calculating.")

specs = {}
configuration_errors = []
for name in selected_names:
    try:
        path = model_paths[name]
        specs[name] = model_spec_cached(str(path), file_stamp(path), file_stamp(MANIFEST))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        configuration_errors.append(f"{name}: {exc}")
for error in configuration_errors:
    st.error(error)
if any(spec.get("verification") != "verified" for spec in specs.values()):
    st.caption(
        "The bundled models use legacy class labels and preprocessing that still need verification "
        "against the training data. Scores are model outputs, not validated diagnostic confidence."
    )

st.subheader("Image source")
st.session_state.setdefault("pard_source_mode", "Upload")
source_mode = st.radio("Use image from", ["Upload", "Dataset gallery"], horizontal=True, key="pard_source_mode")
uploaded = st.file_uploader(
    "Upload original image", type=["png", "jpg", "jpeg", "tif", "tiff", "bmp", "webp"],
    key="pard_upload", on_change=uploaded_image_changed,
)
dataset_images = discover_dataset_images(DATASET_DIR)
dataset_by_path = {str(path): path for path in dataset_images}
with st.expander("Dataset gallery", expanded=source_mode == "Dataset gallery"):
    if dataset_images:
        choices = list(dataset_by_path)
        current_path = st.session_state.get("pard_dataset_path")
        selected_path = st.selectbox(
            "Sample image", choices,
            index=choices.index(current_path) if current_path in choices else 0,
            format_func=lambda path: str(dataset_by_path[path].relative_to(DATASET_DIR)),
            key="pard_gallery_selection",
        )
        st.button("Use this image", on_click=select_dataset, args=(selected_path,), key="pard_use_dataset")
        if st.checkbox("Show sample previews", key="pard_show_previews"):
            for offset in range(0, len(dataset_images), 4):
                for column, path in zip(st.columns(4), dataset_images[offset:offset + 4]):
                    with column:
                        try:
                            st.image(thumbnail_cached(str(path), file_stamp(path)), caption=path.name, width="stretch")
                        except (OSError, ValueError) as exc:
                            st.warning(f"Preview unavailable: {exc}")
                        st.button("Use this image", key=f"pard_sample_{path.name}_{offset}", on_click=select_dataset, args=(str(path),))
    else:
        st.info("No sample images are available in pages_dataset/.")

image_bytes = None
source_label = ""
if source_mode == "Upload" and uploaded is not None:
    image_bytes = uploaded.getvalue()
    source_label = f"Upload: {uploaded.name}"
elif source_mode == "Dataset gallery":
    path = dataset_by_path.get(st.session_state.get("pard_dataset_path"))
    if path is not None:
        try:
            image_bytes = image_bytes_cached(str(path), file_stamp(path))
            source_label = f"Dataset: {path.name}"
        except OSError as exc:
            st.error(f"The selected sample cannot be opened: {exc}")

if image_bytes is None:
    st.session_state.pard_result = None
    st.info("Upload an image or choose a sample and press Use this image.")
    st.stop()

try:
    with Image.open(io.BytesIO(image_bytes)) as source_image:
        original_img = source_image.convert("RGB")
except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
    st.session_state.pard_result = None
    st.error(f"Unable to open this image: {exc}")
    st.stop()

image_id = hashlib.sha256(image_bytes).hexdigest()
context_id = context_fingerprint(image_id, specs, normalize_to_01, viewport, source_label)
if refresh_context(st.session_state, image_id, context_id):
    st.info("Inputs changed. Press Calculate to create a new result.")
view = view_for_viewport(st.session_state.pard_view, viewport)
st.session_state.pard_view = view
st.caption(f"Using {source_label} · {original_img.width} × {original_img.height} pixels")
st.write("Move the target object into the center box, then press **Calculate**.")
png = io.BytesIO()
original_img.save(png, format="PNG")
state = viewer_component(
    image_b64=base64.b64encode(png.getvalue()).decode("ascii"), viewport=viewport,
    init_zoom=view["zoom"], init_panX=view["panX"], init_panY=view["panY"],
    image_id=image_id, key="pard_viewer",
)

try:
    event = calculation_event(state, image_id, viewport, st.session_state.get("pard_last_token", ""))
except ValueError as exc:
    st.error(str(exc))
    event = None

if event is not None:
    st.session_state.pard_last_token = event["calc_token"]
    st.session_state.pard_view = {key: event[key] for key in ("zoom", "panX", "panY", "viewport")}
    st.session_state.pard_result = None
    if not selected_names or configuration_errors:
        st.error("Resolve the model selection or configuration errors before calculating.")
    else:
        try:
            box = compute_center_cell_crop_box(original_img, viewport, event["zoom"], event["panX"], event["panY"])
            roi_crop = original_img.crop(box)
        except ValueError as exc:
            st.warning(str(exc))
        else:
            per_model_results = []
            errors = []
            with st.spinner("Calculating selected models…"):
                for name in selected_names:
                    spec = specs[name]
                    try:
                        model = model_cached(str(model_paths[name]), spec["sha256"])
                        normalize = normalize_to_01 or spec["preprocessing"] == "rescale_0_1"
                        x_input = prepare_input_tensor(roi_crop, model, normalize_to_01=normalize)
                        raw = model.predict(x_input, verbose=0)
                        pred_info = postprocess_prediction(raw, spec["labels"])
                        per_model_results.append({
                            "model_name": name, "model_sha256": spec["sha256"],
                            "input_shape": list(x_input.shape), "pred_info": pred_info,
                            "preprocessing": "rescale_0_1" if normalize else "raw_0_255",
                            "verification": spec["verification"],
                        })
                    except Exception as exc:
                        errors.append(f"{name}: {exc}")
            st.session_state.pard_result = {
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "context_id": context_id, "image_sha256": image_id,
                "source": source_label, "viewer": event, "box": box, "crop": roi_crop,
                "per_model_results": per_model_results,
                "ensemble_summary": build_ensemble_summary(per_model_results), "errors": errors,
            }

result = st.session_state.get("pard_result")
if result is not None:
    st.divider()
    st.subheader("Last calculated result")
    st.caption(f"{result['source']} · Calculated {result['created_at_utc']} · ROI {result['box']}")
    crop_col, predictions_col = st.columns([1, 1.35], gap="large")
    with crop_col:
        st.subheader("Region of interest")
        st.image(result["crop"], width="stretch")
        for error in result["errors"]:
            st.error(error)
    with predictions_col:
        st.subheader("Multi-model predictions")
        predictions = result["per_model_results"]
        if not predictions:
            st.error("No model produced a valid prediction.")
        ensemble = result["ensemble_summary"]
        if ensemble is not None:
            st.markdown("### Ensemble summary")
            st.write(f"**Average-score prediction:** {ensemble['avg_pred_label']}")
            if ensemble["majority_vote_label"] is None:
                st.write("**Majority vote:** No strict majority")
            else:
                st.write(f"**Majority vote:** {ensemble['majority_vote_label']}")
            st.caption("Votes: " + ", ".join(f"{ensemble['labels'][int(index)]}: {count}" for index, count in ensemble["vote_counts"].items()))
            with st.expander("Average normalized scores", expanded=False):
                for label, score in zip(ensemble["labels"], ensemble["avg_scores"]):
                    st.write(f"{label}: {score:.4f}")
                    st.progress(float(score))
        elif predictions:
            st.info("These model outputs cannot be combined into a compatible ensemble.")
        st.markdown("### Per-model Details")
        for index, prediction in enumerate(predictions, 1):
            info = prediction["pred_info"]
            with st.expander(f"{index}. {prediction['model_name']} → {info['pred_label']}", expanded=False):
                st.write(f"**Prediction:** {info['pred_label']}")
                for label, score in info["display_pairs"]:
                    st.write(f"{label}: {score:.4f}")
                    if 0.0 <= score <= 1.0:
                        st.progress(float(score))
                st.caption(f"Preprocessing: {prediction['preprocessing']} · {prediction['verification']}")

    report = {key: value for key, value in result.items() if key != "crop"}
    rows = io.StringIO(newline="")
    writer = csv.writer(rows)
    writer.writerow(["model", "model_sha256", "label", "score", "prediction", "preprocessing", "image_sha256", "roi", "created_at_utc"])
    for prediction in result["per_model_results"]:
        for label, score in prediction["pred_info"]["display_pairs"]:
            writer.writerow([prediction["model_name"], prediction["model_sha256"], label, score,
                             prediction["pred_info"]["pred_label"], prediction["preprocessing"],
                             image_id, str(result["box"]), result["created_at_utc"]])
    crop_png = io.BytesIO()
    result["crop"].save(crop_png, format="PNG")
    downloads = st.columns(3)
    with downloads[0]:
        st.download_button("Download report (JSON)", json.dumps(report, ensure_ascii=False, indent=2), "pard_report.json", "application/json", on_click="ignore")
    with downloads[1]:
        st.download_button("Download scores (CSV)", rows.getvalue().encode("utf-8-sig"), "pard_scores.csv", "text/csv", on_click="ignore")
    with downloads[2]:
        st.download_button("Download ROI (PNG)", crop_png.getvalue(), "pard_roi.png", "image/png", on_click="ignore")

st.caption("ParD - Parasite Detection · Parasitic Platform · Penchom Janwan")

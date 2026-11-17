"""Image selection and classification contracts used by ParD.

This module has no Streamlit or eager TensorFlow dependency, so validation can
run before loading a model and can be tested independently of the interface.
"""

from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

DEFAULT_INPUT_SIZE = (128, 128)
ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
DEFAULT_MANIFEST = Path(__file__).resolve().parent / "pages_components" / "model_manifest.json"


def compute_center_cell_crop_box(
    img: Image.Image,
    viewport: int,
    zoom: float,
    pan_x: float,
    pan_y: float,
    *,
    minimum_side: int = 4,
) -> tuple[int, int, int, int]:
    """Map the center canvas cell onto the image, rejecting empty/sliver crops.

    The four-pixel minimum is an input-integrity guard, not a claim about the
    biological information needed for a reliable classification.
    """
    width, height = img.size
    values = np.asarray([viewport, zoom, pan_x, pan_y], dtype=np.float64)
    if not np.all(np.isfinite(values)) or viewport <= 0 or zoom <= 0:
        raise ValueError("Invalid viewer coordinates. Reset the image and try again.")
    if width <= 0 or height <= 0 or minimum_side < 1:
        raise ValueError("The image and minimum crop size must have positive dimensions.")
    vp = float(viewport)
    scale = min(vp / width, vp / height) * float(zoom)
    left = (vp / 3 - vp / 2 - pan_x) / scale + width / 2
    right = (2 * vp / 3 - vp / 2 - pan_x) / scale + width / 2
    top = (vp / 3 - vp / 2 - pan_y) / scale + height / 2
    bottom = (2 * vp / 3 - vp / 2 - pan_y) / scale + height / 2
    left, right = max(0.0, left), min(float(width), right)
    top, bottom = max(0.0, top), min(float(height), bottom)
    if right <= left or bottom <= top:
        raise ValueError("The center box does not overlap the image. Move the image into the box.")
    if right - left < minimum_side or bottom - top < minimum_side:
        raise ValueError("The selected image area is too small. Move the image or zoom out.")
    return int(np.floor(left)), int(np.floor(top)), int(np.ceil(right)), int(np.ceil(bottom))


def discover_models(models_dir: Path) -> list[Path]:
    root = Path(models_dir)
    if not root.is_dir():
        return []
    return sorted(
        p.resolve()
        for p in root.iterdir()
        if (p.is_file() and p.suffix.lower() in {".keras", ".h5", ".hdf5"})
        or (p.is_dir() and (p / "saved_model.pb").is_file())
    )


def discover_dataset_images(dataset_dir: Path) -> list[Path]:
    root = Path(dataset_dir)
    return sorted(p.resolve() for p in root.rglob("*") if p.is_file() and p.suffix.lower() in ALLOWED_IMAGE_EXTS)


def path_display_name(p: Path) -> str:
    p = Path(p)
    return f"{p.name}  [SavedModel]" if p.is_dir() else p.name


def relpath_or_name(p: Path, root: Path) -> str:
    try:
        return str(Path(p).relative_to(root))
    except ValueError:
        return Path(p).name


def model_fingerprint(model_path: str | Path) -> str:
    """Content digest used to bind manifests, caches and result provenance."""
    path = Path(model_path)
    digest = hashlib.sha256()
    if path.is_file():
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    elif path.is_dir() and (path / "saved_model.pb").is_file():
        for file in sorted(p for p in path.rglob("*") if p.is_file()):
            digest.update(file.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            with file.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
    else:
        raise FileNotFoundError(f"Model not found: {path.name}")
    return digest.hexdigest()


def load_model_spec(model_path: str | Path, manifest_path: str | Path | None = None) -> dict[str, Any]:
    """Read an explicit, content-bound class/preprocessing specification.

    Bundled entries preserve the previous application's assumptions, labelled
    as unverified. A new or replaced model needs its own reviewed specification.
    """
    path = Path(model_path)
    manifest = Path(manifest_path) if manifest_path is not None else DEFAULT_MANIFEST
    try:
        content = json.loads(manifest.read_text(encoding="utf-8"))
        spec = dict(content["models"][path.name])
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"No valid model specification for {path.name}. Add it to {manifest.name}.") from exc
    labels = spec.get("labels")
    if not isinstance(labels, list) or not labels or not all(isinstance(label, str) and label.strip() for label in labels):
        raise ValueError(f"{path.name}: the specification must list nonempty class labels in training order.")
    if len(labels) != len(set(labels)):
        raise ValueError(f"{path.name}: class labels must be unique.")
    if spec.get("preprocessing") not in {"raw_0_255", "rescale_0_1"}:
        raise ValueError(f"{path.name}: unsupported preprocessing specification.")
    fingerprint = model_fingerprint(path)
    if spec.get("sha256") != fingerprint:
        raise ValueError(f"{path.name}: the model has changed. Verify and update its specification before inference.")
    shape = spec.get("input_shape")
    if not isinstance(shape, list) or len(shape) != 4 or shape[-1] != 3:
        raise ValueError(f"{path.name}: the specification must describe one NHWC RGB image input.")
    spec.setdefault("verification", "unverified")
    spec["model_name"] = path.name
    spec["model_fingerprint"] = fingerprint
    return spec


def _single_image_shape(model: Any) -> tuple:
    shape = getattr(model, "input_shape", None)
    if isinstance(shape, list) and shape and isinstance(shape[0], (list, tuple)):
        if len(shape) != 1:
            raise ValueError("Only models with one image input are supported.")
        shape = shape[0]
    if hasattr(shape, "as_list"):
        shape = shape.as_list()
    if shape is None:
        raise ValueError("The model does not declare its image input shape.")
    shape = tuple(shape)
    if len(shape) != 4 or shape[-1] != 3 or shape[0] not in (None, 1):
        raise ValueError("Expected one RGB image with shape (1, height, width, 3).")
    return shape


def get_model_input_size(model: Any, fallback: tuple[int, int] = DEFAULT_INPUT_SIZE) -> tuple[int, int]:
    shape = _single_image_shape(model)
    height, width = shape[1:3]
    if height is None or width is None:
        return fallback
    if not isinstance(height, (int, np.integer)) or not isinstance(width, (int, np.integer)) or height <= 0 or width <= 0:
        raise ValueError("The model declares invalid image dimensions.")
    return int(width), int(height)


def prepare_input_tensor(crop_img: Image.Image, model: Any, normalize_to_01: bool = False) -> np.ndarray:
    width, height = get_model_input_size(model)
    dtype = getattr(model, "input_dtype", None)
    if normalize_to_01 and dtype is not None and np.issubdtype(np.dtype(dtype), np.integer):
        raise ValueError("An integer-input model cannot use /255 normalization.")
    resized = crop_img.convert("RGB").resize((width, height), Image.Resampling.BICUBIC)
    array = np.asarray(resized, dtype=np.float32)
    if normalize_to_01:
        array /= 255.0
    return np.expand_dims(array, axis=0)


def postprocess_prediction(y_pred_raw: Any, labels: list[str]) -> dict[str, Any]:
    if not labels or len(set(labels)) != len(labels):
        raise ValueError("Class labels must be nonempty and unique.")
    if isinstance(y_pred_raw, dict):
        if len(y_pred_raw) != 1:
            raise ValueError("Expected one classification output, not a detection or multi-output result.")
        y_pred_raw = next(iter(y_pred_raw.values()))
    try:
        values = np.asarray(y_pred_raw, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise ValueError("The model output is not a numeric classification vector.") from exc
    if values.ndim == 2 and values.shape[0] == 1:
        values = values[0]
    elif values.ndim == 0:
        values = values.reshape(1)
    if values.ndim != 1 or not values.size:
        raise ValueError("Expected one classification vector; batched, spatial or multi-output predictions are unsupported.")
    if not np.all(np.isfinite(values)):
        raise ValueError("The model returned NaN or infinity; no prediction was accepted.")
    if values.size > 1 and np.all(values == 0):
        raise ValueError("The model returned only zero scores. Verify its preprocessing before accepting a prediction.")
    if values.size == 1 and len(labels) == 2:
        score = float(values[0])
        if not 0 <= score <= 1:
            raise ValueError("A binary scalar output must be a score between 0 and 1.")
        values = np.asarray([1 - score, score])
    if values.size != len(labels):
        raise ValueError(f"The model returned {values.size} scores but its specification lists {len(labels)} classes.")
    index = int(np.argmax(values))
    scores = values.tolist()
    return {
        "pred_index": index,
        "pred_label": labels[index],
        "scores": scores,
        "display_pairs": list(zip(labels, scores)),
        "num_classes": len(scores),
        "score_kind": "model_score",
    }


def softmax_numpy(logits: np.ndarray) -> np.ndarray:
    values = np.asarray(logits, dtype=np.float64)
    if values.ndim != 1 or values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("Softmax requires a finite, nonempty score vector.")
    exponents = np.exp(values - np.max(values))
    return exponents / exponents.sum()


def normalize_scores_for_ensemble(scores: list[float]) -> np.ndarray | None:
    try:
        values = np.asarray(scores, dtype=np.float64)
    except (TypeError, ValueError):
        return None
    if values.ndim != 1 or values.size == 0 or not np.all(np.isfinite(values)):
        return None
    if np.all((values >= 0) & (values <= 1)):
        total = values.sum()
        return values / total if total > 0 else None
    return softmax_numpy(values)


def build_ensemble_summary(per_model_results: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not per_model_results:
        return None
    vectors, votes = [], []
    labels_ref = None
    for result in per_model_results:
        info = result.get("pred_info", {})
        labels = [label for label, _ in info.get("display_pairs", [])]
        if not labels or len(set(labels)) != len(labels):
            return None
        if labels_ref is None:
            labels_ref = labels
        if set(labels) != set(labels_ref):
            return None
        vector = normalize_scores_for_ensemble(info.get("scores"))
        if vector is None or len(vector) != len(labels):
            return None
        order = [labels.index(label) for label in labels_ref]
        vectors.append(vector[order])
        predicted_label = info.get("pred_label")
        if predicted_label not in labels_ref:
            return None
        votes.append(labels_ref.index(predicted_label))
    average = np.mean(np.vstack(vectors), axis=0)
    index = int(np.argmax(average))
    vote_counts = {i: votes.count(i) for i in sorted(set(votes))}
    highest = max(vote_counts.values())
    leaders = [i for i, count in vote_counts.items() if count == highest]
    majority = leaders[0] if len(leaders) == 1 and highest > len(votes) / 2 else None
    return {
        "avg_scores": average.tolist(),
        "avg_pred_index": index,
        "avg_pred_label": labels_ref[index],
        "majority_vote_index": majority,
        "majority_vote_label": labels_ref[majority] if majority is not None else None,
        "tied_indices": leaders if len(leaders) > 1 else [],
        "tied_labels": [labels_ref[i] for i in leaders] if len(leaders) > 1 else [],
        "vote_counts": vote_counts,
        "labels": labels_ref,
        "score_kind": "normalized_model_score",
    }


class SavedModelClassifier:
    """Adapt one exported classification signature to the Keras predict API."""

    def __init__(self, loaded: Any, tensorflow: Any):
        signatures = loaded.signatures
        names = [name for name in ("serving_default", "serve") if name in signatures]
        if not names:
            if len(signatures) != 1:
                raise ValueError("SavedModel must expose one classification signature or serving_default/serve.")
            names = list(signatures)
        self.endpoint_name = names[0]
        self._signature = signatures[self.endpoint_name]
        self._loaded = loaded  # Keep captured variables alive for the cached adapter.
        self._tensorflow = tensorflow
        positional, keyword = self._signature.structured_input_signature
        if len(positional) + len(keyword) != 1:
            raise ValueError("SavedModel must accept exactly one image tensor.")
        self._input_name = next(iter(keyword)) if keyword else None
        spec = keyword[self._input_name] if keyword else positional[0]
        self.input_shape = tuple(spec.shape)
        self._dtype = spec.dtype
        self.input_dtype = np.dtype(spec.dtype.as_numpy_dtype)
        _single_image_shape(self)
        outputs = self._signature.structured_outputs
        if isinstance(outputs, dict) and len(outputs) != 1:
            raise ValueError("SavedModel must return one classification tensor; detection outputs are unsupported.")
        if isinstance(outputs, (tuple, list)):
            raise ValueError("SavedModel must return one classification tensor.")

    def predict(self, inputs: np.ndarray, verbose: int = 0) -> np.ndarray:
        array = np.asarray(inputs, dtype=self.input_dtype)
        tensor = self._tensorflow.convert_to_tensor(array, dtype=self._dtype)
        output = self._signature(**{self._input_name: tensor}) if self._input_name else self._signature(tensor)
        if isinstance(output, dict):
            if len(output) != 1:
                raise ValueError("SavedModel returned more than one classification tensor.")
            output = next(iter(output.values()))
        return np.asarray(output.numpy() if hasattr(output, "numpy") else output)


def load_inference_model(model_path: str | Path, fingerprint: str | None = None) -> Any:
    path = Path(model_path)
    if fingerprint is not None and fingerprint != model_fingerprint(path):
        raise ValueError("The model changed while loading. Refresh its specification and retry.")
    try:
        tensorflow = importlib.import_module("tensorflow")
    except ImportError as exc:
        raise RuntimeError("TensorFlow is not installed. Install the project requirements to run inference.") from exc
    if path.is_dir() and (path / "saved_model.pb").is_file():
        return SavedModelClassifier(tensorflow.saved_model.load(str(path)), tensorflow)
    if path.is_file() and path.suffix.lower() in {".keras", ".h5", ".hdf5"}:
        model = tensorflow.keras.models.load_model(str(path), compile=False)
        _single_image_shape(model)
        return model
    raise ValueError("Select a .keras/.h5 model or a SavedModel folder containing saved_model.pb.")

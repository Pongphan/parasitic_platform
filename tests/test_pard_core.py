import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image
import pytest

from pard_core import (
    SavedModelClassifier,
    build_ensemble_summary,
    compute_center_cell_crop_box,
    discover_models,
    load_inference_model,
    load_model_spec,
    model_fingerprint,
    postprocess_prediction,
    prepare_input_tensor,
)


@pytest.mark.parametrize("pan", [500, -500])
def test_empty_center_roi_is_rejected_instead_of_classifying_edge_pixel(pan):
    image = Image.new("RGB", (1200, 1200))
    with pytest.raises(ValueError, match="does not overlap"):
        compute_center_cell_crop_box(image, 360, 1, pan, pan)


def test_crop_matches_canvas_geometry_and_rejects_sliver():
    image = Image.new("RGB", (1200, 1200))
    assert compute_center_cell_crop_box(image, 900, 1, 0, 0) == (400, 400, 800, 800)
    assert compute_center_cell_crop_box(image, 900, 2, 150, 0) == (400, 500, 600, 700)
    with pytest.raises(ValueError, match="too small"):
        compute_center_cell_crop_box(image, 900, 1, 599, 0)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -1, 0])
def test_invalid_zoom_is_rejected(value):
    with pytest.raises(ValueError, match="Invalid viewer"):
        compute_center_cell_crop_box(Image.new("RGB", (120, 120)), 900, value, 0, 0)


@pytest.mark.parametrize("scores", [[[np.nan, 0.2, 0.8]], [[np.inf, 0.2, 0.8]]])
def test_nonfinite_outputs_never_become_artifact_predictions(scores):
    with pytest.raises(ValueError, match="NaN or infinity"):
        postprocess_prediction(scores, ["artifact", "OV", "MIF"])


@pytest.mark.parametrize("scores", [[[0.2, 0.8]], np.ones((2, 3)), np.ones((1, 2, 3))])
def test_wrong_class_count_or_spatial_outputs_are_rejected(scores):
    with pytest.raises(ValueError):
        postprocess_prediction(scores, ["artifact", "OV", "MIF"])


def test_sigmoid_classification_keeps_scores_without_claiming_calibration():
    result = postprocess_prediction([[0.7, 0.9, 0.8]], ["artifact", "OV", "MIF"])
    assert result["pred_label"] == "OV"
    assert result["scores"] == [0.7, 0.9, 0.8]
    assert result["score_kind"] == "model_score"


def test_saturated_zero_scores_never_become_artifact_predictions():
    with pytest.raises(ValueError, match="only zero scores"):
        postprocess_prediction([[0, 0, 0]], ["artifact", "OV", "MIF"])


def test_ensemble_aligns_class_names_and_reports_tied_votes():
    results = [
        {"pred_info": postprocess_prediction([0.1, 0.8, 0.1], ["artifact", "OV", "MIF"])},
        {"pred_info": postprocess_prediction([0.8, 0.1, 0.1], ["MIF", "artifact", "OV"])},
    ]
    summary = build_ensemble_summary(results)
    assert summary["majority_vote_label"] is None
    assert summary["tied_labels"] == ["OV", "MIF"]
    assert summary["vote_counts"] == {1: 1, 2: 1}
    np.testing.assert_allclose(summary["avg_scores"], [0.1, 0.45, 0.45])


def test_ensemble_requires_same_class_set_and_does_not_call_plurality_majority():
    def prediction(label):
        return {"pred_info": postprocess_prediction(np.eye(3)[label], ["artifact", "OV", "MIF"])}
    summary = build_ensemble_summary([prediction(i) for i in [0, 0, 1, 2]])
    assert summary["majority_vote_index"] is None
    incompatible = {"pred_info": postprocess_prediction([0.1, 0.2, 0.7], ["other", "OV", "MIF"])}
    assert build_ensemble_summary([prediction(0), incompatible]) is None


def test_input_preprocessing_uses_model_shape_and_explicit_normalization():
    model = SimpleNamespace(input_shape=(None, 32, 48, 3))
    image = Image.new("RGB", (20, 20), color="white")
    raw = prepare_input_tensor(image, model)
    normalized = prepare_input_tensor(image, model, normalize_to_01=True)
    assert raw.shape == (1, 32, 48, 3)
    assert raw.dtype == np.float32
    assert np.all(raw == 255)
    assert np.all(normalized == 1)
    with pytest.raises(ValueError, match="one RGB image"):
        prepare_input_tensor(image, SimpleNamespace(input_shape=(None, 32, 32, 1)))


def test_manifest_is_bound_to_model_content(tmp_path):
    model = tmp_path / "classifier.keras"
    model.write_bytes(b"original-model")
    manifest = tmp_path / "model_manifest.json"
    manifest.write_text(json.dumps({"models": {model.name: {
        "labels": ["artifact", "OV", "MIF"],
        "preprocessing": "raw_0_255",
        "input_shape": [None, 128, 128, 3],
        "sha256": model_fingerprint(model),
        "verification": "legacy_unverified",
    }}}), encoding="utf-8")
    assert load_model_spec(model, manifest)["verification"] == "legacy_unverified"
    model.write_bytes(b"replacement-model")
    with pytest.raises(ValueError, match="model has changed"):
        load_model_spec(model, manifest)


def test_all_bundled_models_have_truthful_content_bound_specs():
    models_dir = Path(__file__).resolve().parents[1] / "pages_components"
    paths = discover_models(models_dir)
    assert len(paths) == 6
    for path in paths:
        spec = load_model_spec(path)
        assert spec["input_shape"] == [None, 128, 128, 3]
        assert spec["output_activation"] == "sigmoid"
        assert spec["verification"] == "legacy_unverified"
        assert spec["labels_verified"] is False
        assert spec["preprocessing_verified"] is False
        assert spec["validation_dataset"] is None


class FakeSignature:
    def __init__(self, outputs=None):
        dtype = SimpleNamespace(as_numpy_dtype=np.float32)
        self.structured_input_signature = ((), {"images": SimpleNamespace(shape=(None, 128, 128, 3), dtype=dtype)})
        self.structured_outputs = outputs or {"scores": object()}
        self.received = None

    def __call__(self, **kwargs):
        self.received = kwargs["images"]
        return {"scores": np.asarray([[0.1, 0.8, 0.1]])}


def test_savedmodel_uses_signature_instead_of_keras_loader():
    signature = FakeSignature()
    loaded = SimpleNamespace(signatures={"serving_default": signature})
    tensorflow = SimpleNamespace(convert_to_tensor=lambda array, dtype: array)
    model = SavedModelClassifier(loaded, tensorflow)
    output = model.predict(np.zeros((1, 128, 128, 3)))
    assert signature.received.shape == (1, 128, 128, 3)
    assert signature.received.dtype == np.float32
    assert postprocess_prediction(output, ["artifact", "OV", "MIF"])["pred_label"] == "OV"


def test_detection_savedmodel_does_not_masquerade_as_classifier():
    signature = FakeSignature({"detection_boxes": object(), "detection_scores": object()})
    loaded = SimpleNamespace(signatures={"serving_default": signature})
    with pytest.raises(ValueError, match="detection outputs are unsupported"):
        SavedModelClassifier(loaded, SimpleNamespace())


def test_real_savedmodel_signature_roundtrip_when_tensorflow_is_available(tmp_path):
    tensorflow = pytest.importorskip("tensorflow")

    class ExportedClassifier(tensorflow.Module):
        @tensorflow.function(input_signature=[tensorflow.TensorSpec([None, 8, 8, 3], tensorflow.float32, name="images")])
        def serve(self, images):
            return {"scores": tensorflow.reduce_mean(images, axis=(1, 2))}

    original = ExportedClassifier()
    saved_path = tmp_path / "classifier"
    tensorflow.saved_model.save(original, str(saved_path), signatures={"serving_default": original.serve})
    model = load_inference_model(saved_path, model_fingerprint(saved_path))
    image = Image.new("RGB", (16, 16), (30, 60, 90))
    output = model.predict(prepare_input_tensor(image, model))
    np.testing.assert_allclose(output, [[30, 60, 90]])

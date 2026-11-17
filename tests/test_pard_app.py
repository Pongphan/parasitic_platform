import hashlib
import io
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import streamlit as st
from PIL import Image
from streamlit.testing.v1 import AppTest

import pard_core
import viewer_component

ROOT = Path(__file__).resolve().parents[1]
PAGE = "pages/3_ParD_-_Parasite_Detection.py"


@pytest.fixture
def inference(monkeypatch):
    state = {"event": None, "calls": [], "viewer": None}

    def fake_viewer(**kwargs):
        state["viewer"] = kwargs
        return state["event"]

    class Model:
        input_shape = (None, 128, 128, 3)

        def predict(self, inputs, verbose=0):
            state["calls"].append(inputs.copy())
            return np.array([[0.1, 0.8, 0.1]])

    monkeypatch.setattr(viewer_component, "viewer_component", fake_viewer)
    monkeypatch.setattr(pard_core, "load_inference_model", lambda *args: Model())
    st.cache_resource.clear()
    st.cache_data.clear()
    yield state
    st.cache_resource.clear()
    st.cache_data.clear()


def page():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    app.switch_page(PAGE).run()
    assert not app.exception
    return app


def calculate(app, state, token="first", **coordinates):
    state["event"] = {
        "action": "calculate", "image_id": state["viewer"]["image_id"],
        "calc_token": token, "zoom": 1, "panX": 0, "panY": 0,
        "viewport": 900, **coordinates,
    }
    app.run()
    assert not app.exception


def test_defaults_calculate_collapsed_details_and_result_invalidation(inference):
    app = page()
    assert app.slider(key="pard_viewport").value == 900
    assert len(app.multiselect(key="pard_models").value) == 6
    app.button(key="pard_use_dataset").click().run()
    assert not app.exception
    calculate(app, inference)
    assert len(inference["calls"]) == 6
    details = [e for e in app.expander if ". img_classified" in e.label]
    assert len(details) == 6
    assert all(not e.proto.expanded for e in details)
    assert len(app.get("download_button")) == 3
    app.run()
    assert len(inference["calls"]) == 6  # No repeated inference on a rerun.
    calculate(app, inference, token="second", zoom=2)
    assert len(inference["calls"]) == 12
    app.checkbox(key="pard_normalize").check().run()
    assert not app.exception
    assert app.session_state.pard_result is None
    assert len(inference["calls"]) == 12


def test_empty_roi_never_calls_models(inference):
    app = page()
    app.button(key="pard_use_dataset").click().run()
    calculate(app, inference, panX=10000, panY=10000)
    assert not inference["calls"]
    assert any("does not overlap" in item.value for item in app.warning)
    assert app.session_state.pard_result is None


def test_gallery_selection_wins_while_upload_remains(monkeypatch, inference):
    png = io.BytesIO()
    Image.new("RGB", (128, 128), "green").save(png, format="PNG")
    uploaded = SimpleNamespace(name="uploaded.png", getvalue=lambda: png.getvalue())
    monkeypatch.setattr(st, "file_uploader", lambda *args, **kwargs: uploaded)
    app = page()
    uploaded_id = hashlib.sha256(png.getvalue()).hexdigest()
    assert inference["viewer"]["image_id"] == uploaded_id
    app.button(key="pard_use_dataset").click().run()
    assert not app.exception
    assert app.radio(key="pard_source_mode").value == "Dataset gallery"
    assert inference["viewer"]["image_id"] != uploaded_id
    calculate(app, inference)
    assert app.session_state.pard_result["source"].startswith("Dataset:")

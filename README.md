# Parasitic Platform

Streamlit application for parasitology education, research planning, and microscopy image classification.

## Run locally

Use Python **3.13** (tested with 3.13.7 on Windows). From this project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

`requirements.txt` pins the direct dependencies tested with this application. For the complete Windows/Python 3.13 dependency set, install `requirements-lock-win-py313.txt` instead. An existing environment with those dependencies can run `python -m streamlit run app.py` directly.

## Included features

- **Home:** searchable navigation to the four workspaces.
- **Human Parasite:** 14 profiles, keyword search, canonical syndrome filters, comparisons, and an educational candidate helper.
- **Parasitology Research:** nine research branches and a project blueprint builder. Custom organisms are supported; generated drafts stay available during the session and can be downloaded as HTML. Changed inputs are identified without overwriting the saved draft.
- **ParD - Parasite Detection:** upload an image or explicitly select a dataset sample, zoom/pan to frame the center ROI, run selected classifiers, and compare model scores. The default viewport is **900 pixels**, all six bundled models are selected, and per-model details start collapsed. The interface uses pastel backgrounds and larger text; the canvas scales to smaller screens while retaining consistent crop coordinates.
- **About Project:** project context and roadmap.

ParD currently performs **classification of a manually selected ROI**. It does not automatically locate all objects, perform tiled object detection, or produce YOLO bounding-box labels. Its exports are the ROI PNG, model-score CSV, and JSON result with image/model digests, ROI coordinates, preprocessing, errors, and calculation time.

## Model configuration

Models live in `pages_components/`; `model_manifest.json` binds each file to a SHA-256 digest, ordered labels, input shape, and preprocessing. Models are loaded lazily and cached by their content digest. Supported formats are `.keras`, `.h5`/`.hdf5`, and SavedModel classification signatures with one NHWC RGB image input and one classification output. Detection/multiple-output signatures are rejected.

The six bundled manifests preserve the previous application's class order and raw 0-255 preprocessing. These assumptions are explicitly **`legacy_unverified`**: the training class map, preprocessing specification, and labeled evaluation dataset have not been supplied. The app must not be described as clinically validated, and displayed scores are not calibrated diagnostic probabilities.

To add or replace a model:

1. Copy the model into `pages_components/`.
2. Add/update its manifest entry using the actual training label order, input shape, and preprocessing (`raw_0_255` or `rescale_0_1`).
3. Compute its content digest with `pard_core.model_fingerprint(path)` and record `sha256`.
4. Check known-answer images from an independent labeled evaluation set before recording verification/reviewer details.

The **Normalize input (/255)** checkbox is a manual override. Do not infer the correct preprocessing from a high-looking score. On synthetic images, some bundled PACA models returned all-zero scores even after this override; the app rejects these outputs instead of reporting a fabricated class. Nonfinite scores, unsupported shapes, label-count mismatches, empty crops, and tiny edge crops are also rejected. Ensembles align class labels and report when no strict majority exists.

Changing the image, model selection, preprocessing, model manifest/content, or viewport invalidates the previous result. The visible result is labeled **Last calculated result** and retains its own ROI snapshot. Moving the canvas alone does not run inference; press Calculate for a new ROI.

## Atlas content and provenance

`data/parasite_profiles.json` stores the clinical prose and detailed tags separately from the page. `atlas.py` validates types and canonical syndrome IDs before filtering/scoring. Each profile has `sources`, `reviewer`, and `reviewed_on` fields; existing records are explicitly unreviewed with no source URLs recorded. Fill these from a documented subject-matter review rather than assuming the migrated text has been validated.

## Structure

```text
app.py                         Home and navigation cards
atlas.py                       Atlas schema, filtering, and candidate scoring
data/parasite_profiles.json     Atlas content and review metadata
pard_core.py                   Crop, model contracts, inference, ensembles
pard_session.py                Input identity and calculation event validation
pages/                         Streamlit page scripts
pages_components/              Model files and model_manifest.json
pages_dataset/                 Sample images
ui/pard.css                    ParD pastel theme and typography
viewer_component/              Responsive zoom/pan component
tests/                         Python and JavaScript regression checks
```

## Verification

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
node tests/test_viewer.js
```

The Python suite covers Atlas search/filter regressions, persistent research drafts, crop/output validation, model manifests, SavedModel loading, and ParD state/UI behavior. The SavedModel roundtrip uses TensorFlow when available. The Node tests exercise the real viewer script for rerenders, new images, responsive coordinates, and calculation events. A passing smoke check establishes execution, not predictive accuracy.

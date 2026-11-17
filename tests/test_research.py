from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def research_app():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    at.switch_page("pages/2_Parasitology_Research.py").run()
    assert not at.exception
    return at


def test_custom_organism_is_required_and_escaped_in_saved_blueprint():
    at = research_app()
    at.selectbox(key="research_organism").set_value("Other (custom)").run()
    button = next(w for w in at.button if w.label == "Generate blueprint")
    assert button.disabled
    at.text_input(key="research_custom_organism").set_value("Test <organism> & strain").run()
    next(w for w in at.button if w.label == "Generate blueprint").click().run()
    assert not at.exception
    saved = at.session_state.research_blueprint
    assert saved["inputs"]["organism"] == "Test <organism> & strain"
    assert "Test &lt;organism&gt; &amp; strain" in saved["html"]
    assert "Test <organism>" not in saved["html"]
    assert len(at.get("download_button")) == 1


def test_saved_blueprint_persists_after_inputs_change_and_rerun():
    at = research_app()
    next(w for w in at.button if w.label == "Generate blueprint").click().run()
    before = dict(at.session_state.research_blueprint)
    at.selectbox(key="research_organism").set_value("Malaria").run()
    at.run()
    assert not at.exception
    assert at.session_state.research_blueprint == before
    assert any(before["html"].strip() == w.value for w in at.markdown)
    assert any("Inputs have changed" in w.value for w in at.info)
    next(w for w in at.button if w.label == "Generate blueprint").click().run()
    assert at.session_state.research_blueprint["inputs"]["organism"] == "Malaria"
    assert not any("Inputs have changed" in w.value for w in at.info)

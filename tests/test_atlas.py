from dataclasses import replace
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from atlas import GROUPS, PROFILES, SYNDROME_LABELS, match_profile, score_candidate


ROOT = Path(__file__).resolve().parents[1]


def profile_named(prefix):
    return next(profile for profile in PROFILES if profile.name.startswith(prefix))


def test_keyword_search_handles_every_profile_and_finds_giardia():
    matches = [p for p in PROFILES if match_profile(p, GROUPS, [], "Giardia")]
    assert profile_named("Giardia") in matches
    assert isinstance(profile_named("Giardia").short_overview, str)
    assert "acute or chronic" in profile_named("Giardia").short_overview
    matches = [p for p in PROFILES if match_profile(p, GROUPS, [], "operculated")]
    assert profile_named("Opisthorchis") in matches


@pytest.mark.parametrize(
    ("prefix", "syndrome_id"),
    [
        ("Opisthorchis", "hepatobiliary"),
        ("Minute intestinal flukes", "gi_diarrhea"),
        ("Ascaris", "gi_obstruction"),
        ("Ascaris", "pulmonary"),
        ("Ascaris", "hepatobiliary"),
    ],
)
def test_filters_and_candidate_scores_share_canonical_syndromes(prefix, syndrome_id):
    profile = profile_named(prefix)
    assert match_profile(profile, GROUPS, [syndrome_id], "")
    assert match_profile(profile, GROUPS, [SYNDROME_LABELS[syndrome_id]], "")
    assert score_candidate(profile, syndrome_id, "General / unknown") == 4
    assert score_candidate(profile, SYNDROME_LABELS[syndrome_id], "General / unknown") == 4


def test_profile_schema_rejects_the_original_tuple_and_unknown_syndrome():
    with pytest.raises(ValueError, match="short_overview"):
        replace(PROFILES[0], short_overview=("first", "second"))
    with pytest.raises(ValueError, match="unknown syndrome"):
        replace(PROFILES[0], syndrome_ids={"misspelled"})
    with pytest.raises(ValueError, match="transmission"):
        replace(PROFILES[0], transmission=[42])


def test_all_profiles_have_valid_syndromes_and_source_lists():
    for profile in PROFILES:
        assert profile.syndrome_ids
        assert profile.syndrome_ids <= SYNDROME_LABELS.keys()
        assert isinstance(profile.sources, list)


def test_atlas_search_and_syndrome_filter_through_app():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    at.switch_page("pages/1_Human_Parasite.py").run()
    assert not at.exception
    at.text_input(key="atlas_keyword").set_value("Giardia").run()
    assert not at.exception
    assert next(w for w in at.selectbox if w.label == "Parasite").options == [
        "Giardia duodenalis (Giardiasis)"
    ]
    at.text_input(key="atlas_keyword").set_value("")
    at.multiselect(key="atlas_syndromes").set_value(["hepatobiliary"])
    at.run()
    assert not at.exception
    options = next(w for w in at.selectbox if w.label == "Parasite").options
    assert any(name.startswith("Opisthorchis") for name in options)
    assert any(name.startswith("Ascaris") for name in options)

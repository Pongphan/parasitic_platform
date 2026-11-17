import pytest

from pard_session import calculation_event, context_fingerprint, refresh_context, view_for_viewport


def test_saved_pan_scales_with_viewport_and_survives_remount():
    view = {"zoom": 2, "panX": 100, "panY": -50, "viewport": 900}
    resized = view_for_viewport(view, 360)
    assert resized == {"zoom": 2, "panX": 40, "panY": -20, "viewport": 360}
    assert view_for_viewport(resized, 360) == resized


def event(**updates):
    return {"action": "calculate", "image_id": "a", "calc_token": "click1",
            "zoom": 2, "panX": 10, "panY": 20, "viewport": 900, **updates}


def test_input_changes_invalidate_result_but_keep_same_image_framing():
    session = {}
    refresh_context(session, "a", "config1")
    session["pard_view"] = {"zoom": 2, "panX": 10, "panY": 20}
    session["pard_result"] = {"class": "old"}
    assert refresh_context(session, "a", "config2")
    assert session["pard_result"] is None
    assert session["pard_view"]["zoom"] == 2
    refresh_context(session, "b", "config3")
    assert session["pard_view"] == {"zoom": 1, "panX": 0, "panY": 0}


def test_returning_to_image_does_not_replay_consumed_calculate():
    session = {}
    refresh_context(session, "a", "config1")
    session["pard_last_token"] = "click1"
    refresh_context(session, "b", "config2")
    refresh_context(session, "a", "config1")
    assert calculation_event(event(), "a", 900, session["pard_last_token"]) is None


def test_stale_image_viewport_and_consumed_events_are_ignored():
    assert calculation_event(event(), "b", 900, "") is None
    assert calculation_event(event(), "a", 800, "") is None
    assert calculation_event(event(), "a", 900, "click1") is None
    assert calculation_event(event(), "a", 900, "")["panX"] == 10


@pytest.mark.parametrize("updates", [{"zoom": float("nan")}, {"panX": float("inf")}, {"zoom": 0}, {"viewport": "bad"}, {"calc_token": ""}])
def test_malformed_events_are_rejected(updates):
    with pytest.raises(ValueError):
        calculation_event(event(**updates), "a", 900, "")


def test_result_identity_includes_models_preprocessing_image_and_viewport():
    args = ["imageA", {"model": {"sha256": "hashA", "labels": ["a", "b"]}}, False, 900, "source"]
    baseline = context_fingerprint(*args)
    for index, value in enumerate(["imageB", {"model": {"sha256": "hashB"}}, True, 800, "other"]):
        changed = args.copy()
        changed[index] = value
        assert context_fingerprint(*changed) != baseline

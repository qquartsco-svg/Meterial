import pytest

from cooking_process_foundation.surface import run_process_tick, validate_process_tick_payload


def _valid_flow():
    return {
        "flow_id": "s",
        "title": "s",
        "entry_step_id": "a",
        "steps": [
            {
                "step_id": "a",
                "skill": {"tradition": "fr", "technique": "x", "variant": ""},
                "min_duration_s": 0.1,
                "next_on_success": "",
            }
        ],
    }


def test_validate_ok():
    ok, errs = validate_process_tick_payload(
        {"recipe_flow": _valid_flow(), "dt_s": 0.05, "observation": {}}
    )
    assert ok and errs == []


def test_validate_rejects_aof_on_surface():
    ok, errs = validate_process_tick_payload(
        {"recipe_flow": _valid_flow(), "dt_s": 0.05, "aof_min": {}}
    )
    assert not ok
    assert any("aof_min" in e for e in errs)


def test_run_process_tick_raises_on_invalid():
    with pytest.raises(ValueError, match="recipe_flow"):
        run_process_tick({"recipe_flow": {}, "dt_s": 0.1})


def test_run_process_tick_runs():
    out = run_process_tick(
        {"recipe_flow": _valid_flow(), "dt_s": 0.05, "observation": {}}
    )
    assert "kitchen_state" in out
    assert "arbiter_verdict" in out
    assert "actuator_intent" in out
    assert out["actuator_intent"]["schema_version"] == "actuator_intent.v0.2"
    assert "mission_meta" in out

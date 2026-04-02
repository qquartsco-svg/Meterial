from cooking_process_foundation.l4_payload import run_flow_tick_payload


def _flow():
    return {
        "flow_id": "a",
        "title": "a",
        "entry_step_id": "x",
        "steps": [
            {
                "step_id": "x",
                "skill": {"tradition": "fr", "technique": "saute", "variant": ""},
                "min_duration_s": 1.0,
                "next_on_success": "",
            }
        ],
    }


def test_payload_explicit_arbiter_pauses():
    out = run_flow_tick_payload(
        {
            "recipe_flow": _flow(),
            "observation": {},
            "dt_s": 0.2,
            "arbiter": {"pause_mission": True, "heat_cap_0_1": 0.0},
        }
    )
    assert out["arbiter_verdict"]["pause_mission"] is True
    assert out["kitchen_state"]["time_in_step_s"] == 0.0


def test_payload_sik_stimuli_when_sik_available():
    from cooking_process_foundation.sik_ingress import sik_available

    if not sik_available():
        return
    out = run_flow_tick_payload(
        {
            "recipe_flow": _flow(),
            "observation": {},
            "dt_s": 0.05,
            "sik_stimuli": [{"channel": "vision", "intensity": 0.2, "signal": "ambient"}],
        }
    )
    assert "arbiter_verdict" in out
    assert out.get("sik_gut_risk") is not None or out.get("sik_reflex_triggered") is not None

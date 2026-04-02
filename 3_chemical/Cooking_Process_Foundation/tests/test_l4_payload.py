from cooking_process_foundation.l4_payload import run_flow_tick_payload


def _minimal_flow():
    return {
        "flow_id": "t",
        "title": "t",
        "entry_step_id": "a",
        "steps": [
            {
                "step_id": "a",
                "skill": {"tradition": "fr", "technique": "saute", "variant": ""},
                "min_duration_s": 0.15,
                "next_on_success": "b",
            },
            {
                "step_id": "b",
                "skill": {"tradition": "fr", "technique": "rest", "variant": ""},
                "min_duration_s": 0.05,
                "next_on_success": "",
            },
        ],
    }


def test_l4_payload_runs_until_finished():
    flow = _minimal_flow()
    ks = None
    finished = False
    for _ in range(500):
        out = run_flow_tick_payload(
            {
                "recipe_flow": flow,
                "kitchen_state": ks,
                "observation": {"wall_clock_s": 0.0},
                "dt_s": 0.05,
            }
        )
        ks = out["kitchen_state"]
        if out["finished"]:
            finished = True
            assert out["step_outcome"]["reason"] == "flow_complete"
            break
    assert finished

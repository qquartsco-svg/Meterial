"""
Stable integrator surface — use this for embedded / product wiring.

Internal modules (`flow_engine`, `recipe_serde`, …) may evolve; importers who need
long-term stability should depend on `run_process_tick` and `validate_process_tick_payload`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .l4_payload import run_flow_tick_payload
from .recipe_serde import recipe_flow_from_dict
from .sik_ingress import sik_available


def validate_process_tick_payload(payload: Any) -> Tuple[bool, List[str]]:
    """
    Structural validation only (no SIK tick, no physics).

    Returns (ok, error_messages).
    """
    errs: List[str] = []
    if not isinstance(payload, dict):
        return False, ["payload must be a JSON object"]

    rf = payload.get("recipe_flow")
    if not isinstance(rf, dict):
        errs.append("recipe_flow is required and must be an object")
    else:
        try:
            recipe_flow_from_dict(rf)
        except (TypeError, ValueError) as e:
            errs.append(f"recipe_flow: {e}")

    dt = payload.get("dt_s")
    if isinstance(dt, bool) or not isinstance(dt, (int, float)):
        errs.append("dt_s is required and must be a number")
    elif float(dt) <= 0:
        errs.append("dt_s must be positive")

    obs = payload.get("observation")
    if obs is not None and not isinstance(obs, dict):
        errs.append("observation must be an object when present")

    ks = payload.get("kitchen_state")
    if ks is not None and not isinstance(ks, dict):
        errs.append("kitchen_state must be an object or null when present")

    arb = payload.get("arbiter")
    if arb is not None and not isinstance(arb, dict):
        errs.append("arbiter must be an object when present")

    ac = payload.get("arbiter_config")
    if ac is not None and not isinstance(ac, dict):
        errs.append("arbiter_config must be an object when present")

    stim = payload.get("sik_stimuli")
    if stim is not None:
        if not isinstance(stim, list):
            errs.append("sik_stimuli must be an array when present")
        elif not sik_available():
            errs.append(
                "sik_stimuli is set but Sensory_Input_Kernel is not importable; "
                "add _staging/Sensory_Input_Kernel to PYTHONPATH or omit sik_stimuli"
            )

    if payload.get("aof_min") is not None:
        errs.append(
            "aof_min is not supported on surface.run_process_tick — use L4 engine_ref "
            "cooking.process.flow_tick (design_workspace)"
        )
    if payload.get("cooking_observation_overlay") is not None:
        errs.append(
            "cooking_observation_overlay is not supported on surface.run_process_tick — use L4 "
            "cooking.process.flow_tick"
        )

    return (len(errs) == 0, errs)


def run_process_tick(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validated single tick — raises ValueError on invalid payload.

    This is the recommended entry point for host apps and robot controllers.
    """
    ok, errs = validate_process_tick_payload(payload)
    if not ok:
        raise ValueError("; ".join(errs))
    return run_flow_tick_payload(payload)

from __future__ import annotations

from typing import Any, Dict, Optional

from .arbiter import (
    ArbiterConfig,
    ArbiterVerdict,
    arbiter_config_from_payload,
    arbiter_from_sik_tick_result,
    arbiter_verdict_from_dict,
    arbiter_verdict_to_dict,
)
from .actuator_intent import actuator_intent_to_dict, build_actuator_intent_from_runtime
from .contracts import KitchenState
from .flow_engine import FlowEngine
from .recipe_serde import (
    kitchen_observation_from_dict,
    kitchen_state_from_dict,
    kitchen_state_to_dict,
    recipe_flow_from_dict,
    step_outcome_to_dict,
)
from .sik_ingress import merge_kitchen_observation_with_sik, run_sik_process_tick, sik_available


def run_flow_tick_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Single process tick for L4 / HTTP-style callers.

    Required: recipe_flow, dt_s, observation (object, at least wall_clock_s).
    Optional: kitchen_state (omit or null to start at entry_step with defaults).
    """
    if not isinstance(payload, dict):
        raise TypeError("payload must be an object")

    flow = recipe_flow_from_dict(payload.get("recipe_flow") or {})
    entry = flow.entry_step_id

    ks_raw = payload.get("kitchen_state")
    if ks_raw is None:
        state = KitchenState(
            current_step_id=entry,
            time_in_step_s=0.0,
            vessel_surface_temp_c=25.0,
            core_temp_c=None,
            brownness_0_1=0.0,
        )
    else:
        state = kitchen_state_from_dict(ks_raw, entry_step_id=entry)

    obs = kitchen_observation_from_dict(payload.get("observation") if payload.get("observation") is not None else {})

    sik_snapshot: Optional[Dict[str, Any]] = None
    stim = payload.get("sik_stimuli")
    if stim is not None:
        if not isinstance(stim, list):
            raise TypeError("payload.sik_stimuli must be an array when present")
        if not sik_available():
            raise RuntimeError(
                "payload.sik_stimuli set but Sensory_Input_Kernel not importable; "
                "add _staging/Sensory_Input_Kernel to PYTHONPATH"
            )
        sik_snapshot = run_sik_process_tick(stim)
        if bool(payload.get("merge_sik_tags", True)):
            obs = merge_kitchen_observation_with_sik(
                obs,
                wall_clock_s=obs.wall_clock_s,
                sik_result=sik_snapshot,
            )

    arb_cfg = arbiter_config_from_payload(payload.get("arbiter_config"))
    arb: ArbiterVerdict
    if payload.get("arbiter") is not None:
        arb = arbiter_verdict_from_dict(payload["arbiter"])
    elif sik_snapshot is not None:
        arb = arbiter_from_sik_tick_result(sik_snapshot, cfg=arb_cfg)
    else:
        arb = ArbiterVerdict.allow_all()

    dt = payload.get("dt_s")
    if isinstance(dt, bool) or not isinstance(dt, (int, float)):
        raise TypeError("payload.dt_s must be a number")
    dt_f = float(dt)
    if dt_f <= 0:
        raise ValueError("payload.dt_s must be positive")

    eng = FlowEngine(flow, state)
    outcome = eng.tick(
        obs,
        dt_f,
        heat_cap_0_1=arb.heat_cap_0_1,
        mission_pause=arb.pause_mission,
    )
    finished = eng.is_finished()

    omega = 1.0 if not finished else 0.92
    health = "HEALTHY"
    if arb.pause_mission:
        omega = min(omega, 0.85)
        health = "STABLE"

    out: Dict[str, Any] = {
        "kitchen_state": kitchen_state_to_dict(eng.state),
        "step_outcome": step_outcome_to_dict(outcome) if outcome is not None else None,
        "finished": finished,
        "current_step_id": eng.state.current_step_id,
        "omega": omega,
        "verdict": health,
        "arbiter_verdict": arbiter_verdict_to_dict(arb),
    }
    if sik_snapshot is not None:
        fs = sik_snapshot.get("felt_sense")
        rf = sik_snapshot.get("reflex")
        gut = getattr(fs, "gut_risk", None) if fs is not None else None
        if gut is None and isinstance(fs, dict):
            gut = fs.get("gut_risk")
        trig = getattr(rf, "triggered", None) if rf is not None else None
        if trig is None and isinstance(rf, dict):
            trig = rf.get("triggered")
        out["sik_gut_risk"] = float(gut) if gut is not None else None
        out["sik_reflex_triggered"] = bool(trig) if trig is not None else None

    cur = eng.current_step()
    out["mission_meta"] = {
        "flow_id": flow.flow_id,
        "flow_title": flow.title,
        "step_id": eng.state.current_step_id,
        "skill": {
            "tradition": cur.skill.tradition,
            "technique": cur.skill.technique,
            "variant": cur.skill.variant,
        },
    }
    out["actuator_intent"] = actuator_intent_to_dict(
        build_actuator_intent_from_runtime(flow, eng, arb, obs)
    )
    return out

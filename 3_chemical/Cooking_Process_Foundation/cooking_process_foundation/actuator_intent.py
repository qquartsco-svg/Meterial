from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

from .arbiter import ArbiterVerdict
from .contracts import KitchenObservation, RecipeFlow
from .flow_engine import FlowEngine
from .gates import metrology_gates_satisfied, metrology_targets_active, motion_gate_satisfied


ACTUATOR_INTENT_SCHEMA_VERSION = "actuator_intent.v0.2"


@dataclass(frozen=True)
class ActuatorIntent:
    """
    Thin HAL-facing contract: no vendor SDK types.

    Integrators map this JSON-serializable object to motor/relay commands.
    """

    flow_id: str
    step_id: str
    skill_tradition: str
    skill_technique: str
    skill_variant: str
    heat_ceiling_0_1: float
    mission_pause: bool
    estop_recommended: bool
    allow_manipulator_motion: bool
    vessel_surface_temp_c: float
    brownness_0_1: float
    require_motion_ok: bool
    metrology_targets_active: bool
    metrology_satisfied: Optional[bool]


def build_actuator_intent_from_runtime(
    flow: RecipeFlow,
    eng: FlowEngine,
    arb: ArbiterVerdict,
    obs: Optional[KitchenObservation] = None,
) -> ActuatorIntent:
    step = eng.current_step()
    st = eng.state
    pause = arb.pause_mission
    heat_cap = max(0.0, min(1.0, float(arb.heat_cap_0_1)))
    estop = pause and heat_cap <= 0.0
    targets = metrology_targets_active(step)
    if obs is not None:
        motion_clear = motion_gate_satisfied(step, obs)
        met_sat: Optional[bool] = metrology_gates_satisfied(step, obs) if targets else None
    else:
        motion_clear = not step.require_motion_ok
        met_sat = None if not targets else None
    manip = not pause and motion_clear
    return ActuatorIntent(
        flow_id=flow.flow_id,
        step_id=st.current_step_id,
        skill_tradition=step.skill.tradition,
        skill_technique=step.skill.technique,
        skill_variant=step.skill.variant,
        heat_ceiling_0_1=heat_cap,
        mission_pause=pause,
        estop_recommended=estop,
        allow_manipulator_motion=manip,
        vessel_surface_temp_c=float(st.vessel_surface_temp_c),
        brownness_0_1=float(st.brownness_0_1),
        require_motion_ok=bool(step.require_motion_ok),
        metrology_targets_active=targets,
        metrology_satisfied=met_sat,
    )


def actuator_intent_to_dict(intent: ActuatorIntent) -> Dict[str, Any]:
    return {
        "schema_version": ACTUATOR_INTENT_SCHEMA_VERSION,
        "flow_id": intent.flow_id,
        "step_id": intent.step_id,
        "skill": {
            "tradition": intent.skill_tradition,
            "technique": intent.skill_technique,
            "variant": intent.skill_variant,
        },
        "heat_ceiling_0_1": intent.heat_ceiling_0_1,
        "mission_pause": intent.mission_pause,
        "estop_recommended": intent.estop_recommended,
        "allow_manipulator_motion": intent.allow_manipulator_motion,
        "vessel_surface_temp_c": intent.vessel_surface_temp_c,
        "brownness_0_1": intent.brownness_0_1,
        "require_motion_ok": intent.require_motion_ok,
        "metrology_targets_active": intent.metrology_targets_active,
        "metrology_satisfied": intent.metrology_satisfied,
    }


def actuator_intent_from_dict(d: Mapping[str, Any]) -> ActuatorIntent:
    """Parse dict (e.g. from bus) back into ActuatorIntent; raises on mismatch."""
    if not isinstance(d, Mapping):
        raise TypeError("payload must be a mapping")
    sk = d.get("skill") or {}
    if not isinstance(sk, Mapping):
        raise TypeError("skill must be an object")
    return ActuatorIntent(
        flow_id=str(d.get("flow_id") or ""),
        step_id=str(d.get("step_id") or ""),
        skill_tradition=str(sk.get("tradition") or ""),
        skill_technique=str(sk.get("technique") or ""),
        skill_variant=str(sk.get("variant") or ""),
        heat_ceiling_0_1=max(0.0, min(1.0, float(d.get("heat_ceiling_0_1", 0.0)))),
        mission_pause=bool(d.get("mission_pause", False)),
        estop_recommended=bool(d.get("estop_recommended", False)),
        allow_manipulator_motion=bool(d.get("allow_manipulator_motion", True)),
        vessel_surface_temp_c=float(d.get("vessel_surface_temp_c", 0.0)),
        brownness_0_1=float(d.get("brownness_0_1", 0.0)),
        require_motion_ok=bool(d.get("require_motion_ok", False)),
        metrology_targets_active=bool(d.get("metrology_targets_active", False)),
        metrology_satisfied=_parse_optional_bool(d.get("metrology_satisfied"), "metrology_satisfied"),
    )


def _parse_optional_bool(v: Any, field: str) -> Optional[bool]:
    if v is None:
        return None
    if not isinstance(v, bool):
        raise TypeError(f"{field} must be boolean or null")
    return v

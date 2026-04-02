from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

from .contracts import FlowStep, KitchenObservation, KitchenState, RecipeFlow, SkillRef, StepOutcome


def _req_str(d: Mapping[str, Any], key: str, *, ctx: str) -> str:
    v = d.get(key)
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f"{ctx}: {key} must be a non-empty string")
    return v.strip()


def _opt_str(d: Mapping[str, Any], key: str) -> str:
    v = d.get(key)
    if v is None:
        return ""
    if not isinstance(v, str):
        raise TypeError(f"{key} must be a string or null")
    return v


def _opt_float(d: Mapping[str, Any], key: str) -> Optional[float]:
    v = d.get(key)
    if v is None:
        return None
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise TypeError(f"{key} must be a number or null")
    return float(v)


def skill_ref_from_dict(d: Mapping[str, Any], *, ctx: str) -> SkillRef:
    if not isinstance(d, Mapping):
        raise TypeError(f"{ctx}.skill must be an object")
    return SkillRef(
        tradition=_req_str(d, "tradition", ctx=f"{ctx}.skill"),
        technique=_req_str(d, "technique", ctx=f"{ctx}.skill"),
        variant=_opt_str(d, "variant"),
    )


def flow_step_from_dict(d: Mapping[str, Any], *, ctx: str) -> FlowStep:
    if not isinstance(d, Mapping):
        raise TypeError(f"{ctx} must be an object")
    sid = _req_str(d, "step_id", ctx=ctx)
    skill = skill_ref_from_dict(d.get("skill") or {}, ctx=f"{ctx}[{sid}]")
    nob = d.get("next_on_branch") or {}
    if not isinstance(nob, Mapping):
        raise TypeError(f"{ctx}[{sid}].next_on_branch must be an object")
    branch = {str(k): str(v) for k, v in nob.items() if str(v).strip()}
    rmo = d.get("require_motion_ok", False)
    if not isinstance(rmo, bool):
        raise TypeError(f"{ctx}[{sid}].require_motion_ok must be a boolean")
    return FlowStep(
        step_id=sid,
        skill=skill,
        min_duration_s=float(d.get("min_duration_s") or 0.0),
        target_surface_temp_c=_opt_float(d, "target_surface_temp_c"),
        min_brownness_0_1=_opt_float(d, "min_brownness_0_1"),
        target_mass_g=_opt_float(d, "target_mass_g"),
        mass_tolerance_g=_opt_float(d, "mass_tolerance_g"),
        target_volume_ml=_opt_float(d, "target_volume_ml"),
        volume_tolerance_ml=_opt_float(d, "volume_tolerance_ml"),
        require_motion_ok=rmo,
        notes=_opt_str(d, "notes"),
        next_on_success=_opt_str(d, "next_on_success"),
        next_on_branch=dict(branch),
    )


def recipe_flow_from_dict(d: Mapping[str, Any]) -> RecipeFlow:
    if not isinstance(d, Mapping):
        raise TypeError("recipe_flow must be an object")
    fid = _req_str(d, "flow_id", ctx="recipe_flow")
    title = _opt_str(d, "title") or fid
    entry = _req_str(d, "entry_step_id", ctx="recipe_flow")
    steps_raw = d.get("steps")
    if not isinstance(steps_raw, list) or not steps_raw:
        raise ValueError("recipe_flow.steps must be a non-empty array")
    steps: List[FlowStep] = []
    for i, s in enumerate(steps_raw):
        steps.append(flow_step_from_dict(s, ctx=f"recipe_flow.steps[{i}]"))
    ids = {s.step_id for s in steps}
    if entry not in ids:
        raise ValueError(f"recipe_flow.entry_step_id {entry!r} not in steps")
    return RecipeFlow(fid, title, entry, tuple(steps))


def recipe_flow_to_dict(flow: RecipeFlow) -> Dict[str, Any]:
    return {
        "flow_id": flow.flow_id,
        "title": flow.title,
        "entry_step_id": flow.entry_step_id,
        "steps": [flow_step_to_dict(s) for s in flow.steps],
    }


def flow_step_to_dict(s: FlowStep) -> Dict[str, Any]:
    return {
        "step_id": s.step_id,
        "skill": {
            "tradition": s.skill.tradition,
            "technique": s.skill.technique,
            "variant": s.skill.variant,
        },
        "min_duration_s": s.min_duration_s,
        "target_surface_temp_c": s.target_surface_temp_c,
        "min_brownness_0_1": s.min_brownness_0_1,
        "target_mass_g": s.target_mass_g,
        "mass_tolerance_g": s.mass_tolerance_g,
        "target_volume_ml": s.target_volume_ml,
        "volume_tolerance_ml": s.volume_tolerance_ml,
        "require_motion_ok": s.require_motion_ok,
        "notes": s.notes,
        "next_on_success": s.next_on_success,
        "next_on_branch": dict(s.next_on_branch),
    }


def kitchen_state_from_dict(d: Mapping[str, Any], *, entry_step_id: str) -> KitchenState:
    if not isinstance(d, Mapping):
        raise TypeError("kitchen_state must be an object")
    cur = d.get("current_step_id")
    if cur is None or (isinstance(cur, str) and not cur.strip()):
        current = entry_step_id
    else:
        if not isinstance(cur, str):
            raise TypeError("kitchen_state.current_step_id must be a string")
        current = cur.strip()
    extras = d.get("extras") or {}
    if not isinstance(extras, dict):
        raise TypeError("kitchen_state.extras must be an object")
    tags = d.get("phase_tags") or []
    if not isinstance(tags, list):
        raise TypeError("kitchen_state.phase_tags must be an array")
    pt = tuple(str(x) for x in tags)
    return KitchenState(
        current_step_id=current,
        time_in_step_s=float(d.get("time_in_step_s") or 0.0),
        vessel_surface_temp_c=float(d.get("vessel_surface_temp_c") or 25.0),
        core_temp_c=_opt_float(d, "core_temp_c"),
        brownness_0_1=float(d.get("brownness_0_1") or 0.0),
        phase_tags=pt,
        extras=dict(extras),
    )


def kitchen_state_to_dict(s: KitchenState) -> Dict[str, Any]:
    return {
        "current_step_id": s.current_step_id,
        "time_in_step_s": s.time_in_step_s,
        "vessel_surface_temp_c": s.vessel_surface_temp_c,
        "core_temp_c": s.core_temp_c,
        "brownness_0_1": s.brownness_0_1,
        "phase_tags": list(s.phase_tags),
        "extras": dict(s.extras),
    }


def kitchen_observation_from_dict(d: Mapping[str, Any]) -> KitchenObservation:
    if not isinstance(d, Mapping):
        raise TypeError("observation must be an object")
    w = d.get("wall_clock_s", 0.0)
    if isinstance(w, bool) or not isinstance(w, (int, float)):
        raise TypeError("observation.wall_clock_s must be a number")
    tags = d.get("tags") or []
    if not isinstance(tags, list):
        raise TypeError("observation.tags must be an array")
    hg = d.get("human_gate_ok")
    if hg is not None and not isinstance(hg, bool):
        raise TypeError("observation.human_gate_ok must be boolean or null")
    mo = d.get("motion_ok")
    if mo is not None and not isinstance(mo, bool):
        raise TypeError("observation.motion_ok must be boolean or null")
    return KitchenObservation(
        wall_clock_s=float(w),
        reported_surface_temp_c=_opt_float(d, "reported_surface_temp_c"),
        reported_core_temp_c=_opt_float(d, "reported_core_temp_c"),
        vision_brownness_0_1=_opt_float(d, "vision_brownness_0_1"),
        human_gate_ok=hg,
        reported_mass_g=_opt_float(d, "reported_mass_g"),
        reported_volume_ml=_opt_float(d, "reported_volume_ml"),
        motion_ok=mo,
        tags=tuple(str(x) for x in tags),
    )


def kitchen_observation_to_dict(o: KitchenObservation) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "wall_clock_s": o.wall_clock_s,
        "tags": list(o.tags),
    }
    if o.reported_surface_temp_c is not None:
        out["reported_surface_temp_c"] = o.reported_surface_temp_c
    if o.reported_core_temp_c is not None:
        out["reported_core_temp_c"] = o.reported_core_temp_c
    if o.vision_brownness_0_1 is not None:
        out["vision_brownness_0_1"] = o.vision_brownness_0_1
    if o.human_gate_ok is not None:
        out["human_gate_ok"] = o.human_gate_ok
    if o.reported_mass_g is not None:
        out["reported_mass_g"] = o.reported_mass_g
    if o.reported_volume_ml is not None:
        out["reported_volume_ml"] = o.reported_volume_ml
    if o.motion_ok is not None:
        out["motion_ok"] = o.motion_ok
    return out


def step_outcome_to_dict(o: StepOutcome) -> Dict[str, Any]:
    return {
        "completed_step_id": o.completed_step_id,
        "next_step_id": o.next_step_id,
        "reason": o.reason,
    }

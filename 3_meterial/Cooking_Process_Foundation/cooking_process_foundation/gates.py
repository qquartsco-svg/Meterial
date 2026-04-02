from __future__ import annotations

from .contracts import FlowStep, KitchenObservation

# Reserved `FlowStep.next_on_branch` key: jump here when scale/flowmeter reports are
# complete for all declared targets but at least one dimension is out of tolerance.
METROLOGY_FAIL_BRANCH_KEY = "metrology_fail"


def metrology_targets_active(step: FlowStep) -> bool:
    return step.target_mass_g is not None or step.target_volume_ml is not None


def metrology_gates_satisfied(step: FlowStep, obs: KitchenObservation) -> bool:
    """True when every declared mass/volume target is within tolerance vs observation."""
    if step.target_mass_g is not None:
        if obs.reported_mass_g is None:
            return False
        tol = step.mass_tolerance_g
        if tol is None:
            tol = max(0.01, abs(step.target_mass_g) * 0.001)
        if abs(obs.reported_mass_g - step.target_mass_g) > tol:
            return False
    if step.target_volume_ml is not None:
        if obs.reported_volume_ml is None:
            return False
        tol = step.volume_tolerance_ml
        if tol is None:
            tol = max(0.5, abs(step.target_volume_ml) * 0.002)
        if abs(obs.reported_volume_ml - step.target_volume_ml) > tol:
            return False
    return True


def metrology_reports_complete(step: FlowStep, obs: KitchenObservation) -> bool:
    """True when every declared target has a non-null reported value on the observation."""
    if not metrology_targets_active(step):
        return False
    if step.target_mass_g is not None and obs.reported_mass_g is None:
        return False
    if step.target_volume_ml is not None and obs.reported_volume_ml is None:
        return False
    return True


def metrology_failure_branch_eligible(step: FlowStep, obs: KitchenObservation) -> bool:
    """
    True when metrology is active, all required reports are present, and tolerance fails.
    (Distinguishes 'still measuring' from 'measured OOT'.)
    """
    return (
        metrology_targets_active(step)
        and metrology_reports_complete(step, obs)
        and not metrology_gates_satisfied(step, obs)
    )


def motion_gate_satisfied(step: FlowStep, obs: KitchenObservation) -> bool:
    """If the step requires a motion planner OK, only True when obs.motion_ok is explicitly True."""
    if not step.require_motion_ok:
        return True
    return obs.motion_ok is True

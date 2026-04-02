from __future__ import annotations

from dataclasses import dataclass

from .contracts import CaptureAssessment


@dataclass(frozen=True)
class CaptureOrbitOperationsReport:
    orbits_per_day: float
    daily_capture_kg: float
    orbital_omega_0_1: float
    drag_health_0_1: float
    maneuver_budget_health_0_1: float
    endurance_score_0_1: float
    mission_feasible: bool
    recommendation: str


def assess_capture_orbit_operations(
    *,
    assessment: CaptureAssessment,
    orbital_omega_0_1: float,
    drag_health_0_1: float,
    maneuver_budget_health_0_1: float,
    period_s: float,
) -> CaptureOrbitOperationsReport:
    safe_period_s = max(period_s, 1.0)
    orbits_per_day = 86400.0 / safe_period_s
    daily_capture_kg = assessment.orbital_yield_per_pass_kg * orbits_per_day
    endurance = max(
        0.0,
        min(
            1.0,
            0.35 * assessment.omega_capture
            + 0.25 * orbital_omega_0_1
            + 0.20 * drag_health_0_1
            + 0.20 * maneuver_budget_health_0_1,
        ),
    )
    mission_feasible = (
        assessment.capture_possible
        and daily_capture_kg > 0.0
        and orbital_omega_0_1 >= 0.35
        and drag_health_0_1 >= 0.20
        and maneuver_budget_health_0_1 >= 0.20
    )
    if not assessment.capture_possible:
        recommendation = "capture stack does not clear pass-level feasibility yet"
    elif drag_health_0_1 < 0.35:
        recommendation = "orbit is too drag-burdened; raise altitude or reduce collector area"
    elif maneuver_budget_health_0_1 < 0.35:
        recommendation = "delta-v reserve is too shallow for sustained skimming operations"
    elif endurance < 0.5:
        recommendation = "orbit operations are marginal; restrict skimming to short campaigns"
    else:
        recommendation = "orbit supports sustained capture campaigns within current toy assumptions"
    return CaptureOrbitOperationsReport(
        orbits_per_day=orbits_per_day,
        daily_capture_kg=daily_capture_kg,
        orbital_omega_0_1=orbital_omega_0_1,
        drag_health_0_1=drag_health_0_1,
        maneuver_budget_health_0_1=maneuver_budget_health_0_1,
        endurance_score_0_1=endurance,
        mission_feasible=mission_feasible,
        recommendation=recommendation,
    )

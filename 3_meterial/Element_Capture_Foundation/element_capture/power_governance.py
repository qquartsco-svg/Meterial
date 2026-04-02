from __future__ import annotations

from dataclasses import dataclass

from .contracts import CaptureAssessment


@dataclass(frozen=True)
class PowerBudget:
    generation_w: float
    habitat_load_w: float
    propulsion_reserve_w: float = 0.0
    research_load_w: float = 0.0


@dataclass(frozen=True)
class PowerGovernanceReport:
    available_for_capture_w: float
    capture_power_demand_w: float
    power_margin_w: float
    capture_power_scale_0_1: float
    capture_allowed: bool
    recommendation: str


def govern_capture_power(
    assessment: CaptureAssessment,
    budget: PowerBudget,
) -> PowerGovernanceReport:
    available = max(
        0.0,
        budget.generation_w - budget.habitat_load_w - budget.propulsion_reserve_w - budget.research_load_w,
    )
    demand = assessment.storage_power_w
    margin = available - demand
    scale = 1.0 if demand <= 1e-12 else max(0.0, min(1.0, available / demand))
    allowed = available > 0.0 and scale >= 0.20
    if not allowed:
        recommendation = "capture paused; preserve habitat and propulsion loads first"
    elif scale < 1.0:
        recommendation = "capture can run in derated mode under current power budget"
    else:
        recommendation = "capture can run at planned power"
    return PowerGovernanceReport(
        available_for_capture_w=available,
        capture_power_demand_w=demand,
        power_margin_w=margin,
        capture_power_scale_0_1=scale,
        capture_allowed=allowed,
        recommendation=recommendation,
    )

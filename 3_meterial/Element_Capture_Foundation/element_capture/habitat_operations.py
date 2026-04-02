from __future__ import annotations

from dataclasses import dataclass

from .bridges.life_support_bridge import LifeSupportSnapshot, LifeSupportDemandProfile
from .planning import ResourcePlan
from .power_governance import PowerGovernanceReport
from .waste_regeneration import WasteRegenerationReport


@dataclass(frozen=True)
class HabitatOperationsReport:
    priority: str
    actions: tuple[str, ...]
    habitat_risk_0_1: float
    self_sufficiency_0_1: float
    recommendation: str


def assess_habitat_operations(
    *,
    life_support: LifeSupportSnapshot,
    demand: LifeSupportDemandProfile,
    co2_plan: ResourcePlan | None = None,
    h2_plan: ResourcePlan | None = None,
    power: PowerGovernanceReport | None = None,
    regeneration: WasteRegenerationReport | None = None,
) -> HabitatOperationsReport:
    actions: list[str] = []

    co2_risk = min(1.0, max(0.0, (life_support.atmosphere_co2_ppm - 800.0) / 4200.0))
    o2_risk = min(1.0, max(0.0, (0.19 - life_support.atmosphere_o2_fraction) / 0.05))
    water_risk = 1.0 - max(0.0, min(1.0, life_support.water_margin_0_1))
    buffer_risk = 0.0 if co2_plan is None else max(0.0, min(1.0, 1.0 - co2_plan.inventory_horizon_days / max(co2_plan.meets_buffer_target and co2_plan.inventory_horizon_days or 7.0, 7.0)))
    power_risk = 0.0 if power is None else 1.0 - power.capture_power_scale_0_1
    regen_gain = 0.0 if regeneration is None else regeneration.closure_gain_0_1

    habitat_risk = max(0.0, min(1.0, 0.30 * co2_risk + 0.25 * o2_risk + 0.25 * water_risk + 0.20 * buffer_risk))
    self_sufficiency = max(0.0, min(1.0, 0.35 * (1.0 - habitat_risk) + 0.25 * (1.0 - power_risk) + 0.20 * regen_gain + 0.20 * max(0.0, min(1.0, life_support.water_margin_0_1))))

    if life_support.atmosphere_co2_ppm > 5000.0:
        actions.append("raise CO2 scrubbing priority immediately")
    elif life_support.atmosphere_co2_ppm > 2000.0:
        actions.append("increase CO2 capture throughput")

    if life_support.atmosphere_o2_fraction < 0.19:
        actions.append("prioritize O2 support and electrolysis")

    if life_support.water_margin_0_1 < 0.4:
        actions.append("conserve water and increase water recovery")

    if power is not None and not power.capture_allowed:
        actions.append("shed capture load to preserve habitat and propulsion reserves")
    elif power is not None and power.capture_power_scale_0_1 < 1.0:
        actions.append("run capture in derated mode under power budget")

    if regeneration is not None and regeneration.closure_gain_0_1 < 0.5:
        actions.append("strengthen regeneration loop before expanding science loads")

    if co2_plan is not None and not co2_plan.meets_buffer_target:
        actions.append("increase storage buffer or parallelize CO2 recovery")

    if h2_plan is not None and h2_plan.net_daily_margin_kg < 0.0:
        actions.append("reduce H2 draw or expand electrolysis capacity")

    if habitat_risk >= 0.75:
        priority = "survival"
        recommendation = "habitat loop is outside comfortable margins; stabilize atmosphere, water, and power first"
    elif habitat_risk >= 0.45:
        priority = "stabilize"
        recommendation = "habitat remains operable but needs tighter loop control before extending mission loads"
    else:
        priority = "optimize"
        recommendation = "habitat loop is stable enough to optimize efficiency and research throughput"

    if not actions:
        actions.append("maintain current loop and continue monitoring")

    return HabitatOperationsReport(
        priority=priority,
        actions=tuple(actions),
        habitat_risk_0_1=habitat_risk,
        self_sufficiency_0_1=self_sufficiency,
        recommendation=recommendation,
    )

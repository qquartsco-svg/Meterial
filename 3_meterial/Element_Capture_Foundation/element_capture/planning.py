from __future__ import annotations

from dataclasses import dataclass

from .contracts import CaptureAssessment


@dataclass(frozen=True)
class ResourceDemandProfile:
    species: str
    daily_demand_kg: float
    target_buffer_days: float = 7.0
    current_inventory_kg: float = 0.0


@dataclass(frozen=True)
class ResourcePlan:
    species: str
    capture_rate_kg_s: float
    daily_capture_kg: float
    daily_demand_kg: float
    net_daily_margin_kg: float
    storage_fill_days: float
    inventory_horizon_days: float
    meets_buffer_target: bool
    recommendation: str


def plan_resource_horizon(
    assessment: CaptureAssessment,
    demand: ResourceDemandProfile,
) -> ResourcePlan:
    daily_capture_kg = assessment.net_capture_rate_kg_s * 86400.0
    net_daily_margin_kg = daily_capture_kg - demand.daily_demand_kg
    free_capacity_kg = max(0.0, assessment.storage.capacity_kg - assessment.storage.stored_mass_kg)
    if daily_capture_kg > 1e-12:
        storage_fill_days = free_capacity_kg / daily_capture_kg
    else:
        storage_fill_days = float("inf")
    if demand.daily_demand_kg > 1e-12:
        inventory_horizon_days = (demand.current_inventory_kg + assessment.storage.stored_mass_kg) / demand.daily_demand_kg
    else:
        inventory_horizon_days = float("inf")
    meets_buffer_target = inventory_horizon_days >= demand.target_buffer_days
    if not assessment.capture_possible:
        recommendation = "capture path not currently viable"
    elif net_daily_margin_kg < 0.0:
        recommendation = "capture below daily demand; reduce load or add parallel recovery"
    elif not meets_buffer_target:
        recommendation = "daily balance positive but inventory buffer still shallow"
    else:
        recommendation = "capture supports demand and target buffer"
    return ResourcePlan(
        species=demand.species,
        capture_rate_kg_s=assessment.net_capture_rate_kg_s,
        daily_capture_kg=daily_capture_kg,
        daily_demand_kg=demand.daily_demand_kg,
        net_daily_margin_kg=net_daily_margin_kg,
        storage_fill_days=storage_fill_days,
        inventory_horizon_days=inventory_horizon_days,
        meets_buffer_target=meets_buffer_target,
        recommendation=recommendation,
    )

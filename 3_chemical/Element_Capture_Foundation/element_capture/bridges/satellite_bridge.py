from __future__ import annotations

from dataclasses import replace
from typing import Any

from ..contracts import CaptureAssessment, IntakeGeometry, SeparationStage, StorageStage


def _power_surplus_w(blueprint: Any) -> float:
    eps = getattr(blueprint, "eps", None)
    mission = getattr(blueprint, "mission", None)
    generated = float(getattr(eps, "generated_power_w", 0.0) or 0.0)
    required = float(getattr(mission, "power_req_w", 0.0) or 0.0)
    return max(0.0, generated - required)


def _mass_budget_kg(blueprint: Any) -> float:
    structure = getattr(blueprint, "structure", None)
    total = float(getattr(structure, "total_mass_kg", 0.0) or 0.0)
    margin_ratio = float(getattr(structure, "mass_margin_ratio", 0.0) or 0.0)
    return max(0.0, total * margin_ratio)


def constrain_capture_stack(
    blueprint: Any,
    *,
    intake: IntakeGeometry,
    separation: SeparationStage,
    storage: StorageStage,
    collector_area_share_0_1: float = 0.35,
    capture_mass_share_0_1: float = 0.45,
) -> tuple[IntakeGeometry, SeparationStage, StorageStage, dict[str, float | str]]:
    eps = getattr(blueprint, "eps", None)
    solar_area = float(getattr(eps, "solar_panel_area_m2", 0.0) or 0.0)
    power_budget_w = _power_surplus_w(blueprint)
    mass_budget_kg = _mass_budget_kg(blueprint)
    area_budget_m2 = max(0.05, solar_area * max(0.0, min(1.0, collector_area_share_0_1)))
    power_demand_w = separation.process_power_w + storage.compression_power_w
    power_scale = 1.0 if power_demand_w <= 0.0 else max(0.0, min(1.0, power_budget_w / power_demand_w))
    area_scale = min(1.0, area_budget_m2 / max(intake.area_m2, 1e-9))
    constrained_area = intake.area_m2 * min(power_scale, area_scale)
    constrained_capacity = min(storage.capacity_kg, storage.stored_mass_kg + mass_budget_kg * max(0.0, min(1.0, capture_mass_share_0_1)))
    evidence = {
        "platform_power_surplus_w": power_budget_w,
        "platform_mass_budget_kg": mass_budget_kg,
        "platform_collector_area_budget_m2": area_budget_m2,
        "platform_power_scale_0_1": power_scale,
        "platform_area_scale_0_1": area_scale,
        "platform_mass_budget_exhausted": "true" if mass_budget_kg <= 0.0 else "false",
        "platform_storage_locked": "true" if constrained_capacity <= storage.stored_mass_kg else "false",
    }
    return (
        replace(intake, area_m2=max(0.0, constrained_area)),
        separation,
        replace(storage, capacity_kg=max(storage.stored_mass_kg, constrained_capacity)),
        evidence,
    )


def apply_satellite_thermal_constraints(
    blueprint: Any,
    *,
    storage: StorageStage,
) -> tuple[StorageStage, dict[str, float | str]]:
    thermal = getattr(blueprint, "thermal", None)
    if thermal is None:
        return storage, {}
    heater_power_w = float(getattr(thermal, "heater_power_w", 0.0) or 0.0)
    radiator_area_m2 = float(getattr(thermal, "radiator_area_m2", 0.0) or 0.0)
    hot_margin = float(getattr(thermal, "thermal_margin_hot_c", lambda: 0.0)() if callable(getattr(thermal, "thermal_margin_hot_c", None)) else getattr(thermal, "thermal_margin_hot_c", 0.0) or 0.0)
    cold_margin = float(getattr(thermal, "thermal_margin_cold_c", lambda: 0.0)() if callable(getattr(thermal, "thermal_margin_cold_c", None)) else getattr(thermal, "thermal_margin_cold_c", 0.0) or 0.0)
    viable = bool(getattr(thermal, "is_thermally_viable", True))
    thermal_scale = 1.0
    if not viable:
        thermal_scale *= 0.4
    if cold_margin < 0.0:
        thermal_scale *= max(0.2, min(1.0, 1.0 + cold_margin / 50.0))
    if hot_margin < 0.0:
        thermal_scale *= max(0.2, min(1.0, 1.0 + hot_margin / 50.0))
    adjusted = replace(
        storage,
        capacity_kg=max(storage.stored_mass_kg, storage.capacity_kg * thermal_scale),
        compression_power_w=storage.compression_power_w + heater_power_w,
    )
    evidence = {
        "thermal_storage_scale_0_1": thermal_scale,
        "thermal_heater_power_w": heater_power_w,
        "thermal_radiator_area_m2": radiator_area_m2,
        "thermal_viable": str(viable).lower(),
    }
    return adjusted, evidence


def apply_satellite_constraints(
    assessment: CaptureAssessment,
    *,
    constraint_evidence: dict[str, float | str],
) -> CaptureAssessment:
    merged = dict(assessment.evidence)
    merged.update(constraint_evidence)
    power_scale = float(constraint_evidence.get("platform_power_scale_0_1", 1.0))
    area_scale = float(constraint_evidence.get("platform_area_scale_0_1", 1.0))
    feasible = power_scale > 0.15 and area_scale > 0.05 and assessment.intake.area_m2 > 0.0
    return replace(
        assessment,
        capture_possible=assessment.capture_possible and feasible,
        evidence=merged,
    )


def design_capture_service_bus(
    blueprint: Any,
    *,
    intake: IntakeGeometry,
    separation: SeparationStage,
    storage: StorageStage,
    dedicated_power_w: float = 400.0,
    collector_area_m2: float = 4.0,
    payload_mass_allowance_kg: float = 20.0,
    thermal_storage_scale_0_1: float = 0.7,
) -> tuple[IntakeGeometry, SeparationStage, StorageStage, dict[str, float | str]]:
    power_demand_w = separation.process_power_w + storage.compression_power_w
    power_scale = 1.0 if power_demand_w <= 0.0 else max(0.0, min(1.0, dedicated_power_w / power_demand_w))
    area_scale = min(1.0, collector_area_m2 / max(intake.area_m2, 1e-9))
    constrained_area = intake.area_m2 * min(power_scale, area_scale)
    constrained_capacity = min(storage.capacity_kg, storage.stored_mass_kg + max(0.0, payload_mass_allowance_kg))
    adjusted_storage = replace(
        storage,
        capacity_kg=max(storage.stored_mass_kg, constrained_capacity * max(0.0, min(1.0, thermal_storage_scale_0_1))),
    )
    evidence = {
        "service_bus_mode": "capture_optimized",
        "service_bus_dedicated_power_w": dedicated_power_w,
        "service_bus_collector_area_m2": collector_area_m2,
        "service_bus_payload_mass_allowance_kg": payload_mass_allowance_kg,
        "platform_power_scale_0_1": power_scale,
        "platform_area_scale_0_1": area_scale,
        "platform_mass_budget_exhausted": "false",
        "platform_storage_locked": "false" if adjusted_storage.capacity_kg > storage.stored_mass_kg else "true",
        "thermal_storage_scale_0_1": thermal_storage_scale_0_1,
    }
    return (
        replace(intake, area_m2=max(0.0, constrained_area)),
        separation,
        adjusted_storage,
        evidence,
    )


def apply_capture_platform_profile(
    profile: Any,
    *,
    intake: IntakeGeometry,
    separation: SeparationStage,
    storage: StorageStage,
) -> tuple[IntakeGeometry, SeparationStage, StorageStage, dict[str, float | str]]:
    dedicated_power_w = float(getattr(profile, "dedicated_power_w", 0.0) or 0.0)
    collector_area_m2 = float(getattr(profile, "collector_area_m2", 0.0) or 0.0)
    payload_mass_allowance_kg = float(getattr(profile, "payload_mass_allowance_kg", 0.0) or 0.0)
    thermal_storage_scale_0_1 = float(getattr(profile, "thermal_storage_scale_0_1", 1.0) or 1.0)
    satellite_class = str(getattr(profile, "satellite_class", "unknown"))
    mode = str(getattr(profile, "mode", "capture_service_bus"))
    recommendation = str(getattr(profile, "recommendation", ""))
    power_demand_w = separation.process_power_w + storage.compression_power_w
    power_scale = 1.0 if power_demand_w <= 0.0 else max(0.0, min(1.0, dedicated_power_w / power_demand_w))
    area_scale = min(1.0, collector_area_m2 / max(intake.area_m2, 1e-9))
    constrained_area = intake.area_m2 * min(power_scale, area_scale)
    adjusted_storage = replace(
        storage,
        capacity_kg=max(
            storage.stored_mass_kg,
            min(storage.capacity_kg, storage.stored_mass_kg + max(0.0, payload_mass_allowance_kg))
            * max(0.0, min(1.0, thermal_storage_scale_0_1)),
        ),
    )
    evidence = {
        "service_bus_mode": mode,
        "service_bus_satellite_class": satellite_class,
        "service_bus_dedicated_power_w": dedicated_power_w,
        "service_bus_collector_area_m2": collector_area_m2,
        "service_bus_payload_mass_allowance_kg": payload_mass_allowance_kg,
        "service_bus_recommendation": recommendation,
        "platform_power_scale_0_1": power_scale,
        "platform_area_scale_0_1": area_scale,
        "platform_mass_budget_exhausted": "false",
        "platform_storage_locked": "false" if adjusted_storage.capacity_kg > storage.stored_mass_kg else "true",
        "thermal_storage_scale_0_1": thermal_storage_scale_0_1,
    }
    return (
        replace(intake, area_m2=max(0.0, constrained_area)),
        separation,
        adjusted_storage,
        evidence,
    )

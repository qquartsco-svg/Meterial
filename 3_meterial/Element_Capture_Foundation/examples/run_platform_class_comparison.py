from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from element_capture import (
    CaptureEnvironment,
    CaptureMode,
    ElementCaptureAdapter,
    IntakeGeometry,
    SeparationStage,
    Species,
    StorageStage,
    apply_capture_platform_profile,
    apply_satellite_constraints,
    apply_satellite_thermal_constraints,
    constrain_capture_stack,
)


def _assess_with_evidence(
    *,
    intake: IntakeGeometry,
    separation: SeparationStage,
    storage: StorageStage,
    evidence: dict[str, float | str],
) -> object:
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.225,
            bulk_velocity_ms=1.5,
            species_fraction_0_1=600e-6,
            collection_accessibility_0_1=0.9,
            energetic_cost_index=0.5,
        ),
        intake=intake,
        separation=separation,
        storage=storage,
    )
    return apply_satellite_constraints(assessment, constraint_evidence=evidence)


def _reason_string(assessment: object) -> str:
    evidence = assessment.evidence
    reason = []
    if evidence.get("platform_mass_budget_exhausted") == "true":
        reason.append("mass_budget_exhausted")
    if evidence.get("platform_storage_locked") == "true":
        reason.append("storage_locked")
    if evidence.get("thermal_storage_scale_0_1", 1.0) < 0.2:
        reason.append("thermal_limited")
    if evidence.get("service_bus_mode") == "capture_optimized":
        reason.append("service_bus")
    return ",".join(reason) if reason else "fit_ok"


def evaluate_platform(satellite_class_name: str) -> None:
    sys.path.insert(0, str(ROOT.parent / "Satellite_Design_Stack"))
    from satellite_design_stack import (
        OrbitType,
        PayloadType,
        SatelliteClass,
        SatelliteDesignPipeline,
        SatelliteMission,
        capture_service_bus_profile,
    )

    satellite_class = getattr(SatelliteClass, satellite_class_name)
    mission = SatelliteMission(
        satellite_class=satellite_class,
        orbit_type=OrbitType.LEO,
        altitude_km=550.0,
        payload_type=PayloadType.COMMS,
        design_life_years=2.0,
        data_rate_kbps=512.0,
        pointing_req_deg=1.5,
        power_req_w=180.0 if satellite_class is SatelliteClass.SMALLSAT else 450.0,
        mission_label=f"capture_compare_{satellite_class.value}",
    )
    blueprint, report = SatelliteDesignPipeline().run(mission)
    intake, separation, storage, evidence = constrain_capture_stack(
        blueprint,
        intake=IntakeGeometry(area_m2=6.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.8, process_power_w=220.0),
        storage=StorageStage(capacity_kg=18.0, stored_mass_kg=2.0, compression_power_w=80.0),
    )
    storage, thermal_evidence = apply_satellite_thermal_constraints(blueprint, storage=storage)
    merged_evidence = dict(evidence)
    merged_evidence.update(thermal_evidence)
    assessment = _assess_with_evidence(
        intake=intake,
        separation=separation,
        storage=storage,
        evidence=merged_evidence,
    )

    print(
        f"{blueprint.satellite_class.value}: "
        f"verdict={report.verdict.value} "
        f"capture_possible={assessment.capture_possible} "
        f"power_scale={assessment.evidence.get('platform_power_scale_0_1', 0.0):.3f} "
        f"thermal_scale={assessment.evidence.get('thermal_storage_scale_0_1', 0.0):.3f} "
        f"mass_margin={blueprint.structure.mass_margin_ratio:.4f} "
        f"reason={_reason_string(assessment)}"
    )

    service_profile = capture_service_bus_profile(blueprint)
    service_intake, service_separation, service_storage, service_evidence = apply_capture_platform_profile(
        service_profile,
        intake=IntakeGeometry(area_m2=1.5),
        separation=SeparationStage(recovery_efficiency_0_1=0.82, process_power_w=90.0),
        storage=StorageStage(capacity_kg=4.0, stored_mass_kg=0.3, compression_power_w=18.0),
    )
    service_assessment = _assess_with_evidence(
        intake=service_intake,
        separation=service_separation,
        storage=service_storage,
        evidence=service_evidence,
    )
    print(
        f"  service_bus: "
        f"capture_possible={service_assessment.capture_possible} "
        f"power_scale={service_assessment.evidence.get('platform_power_scale_0_1', 0.0):.3f} "
        f"thermal_scale={service_assessment.evidence.get('thermal_storage_scale_0_1', 0.0):.3f} "
        f"reason={_reason_string(service_assessment)}"
    )


def main() -> None:
    print("=== Platform Class Comparison ===")
    for satellite_class_name in ("CUBESAT_12U", "SMALLSAT", "LEO_COMSAT"):
        evaluate_platform(satellite_class_name)


if __name__ == "__main__":
    main()

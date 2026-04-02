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
    apply_satellite_constraints,
    apply_satellite_thermal_constraints,
    constrain_capture_stack,
)


def main() -> None:
    sys.path.insert(0, str(ROOT.parent / "Satellite_Design_Stack"))
    from satellite_design_stack import OrbitType, PayloadType, SatelliteClass, SatelliteDesignPipeline, SatelliteMission

    mission = SatelliteMission(
        satellite_class=SatelliteClass.SMALLSAT,
        orbit_type=OrbitType.LEO,
        altitude_km=550.0,
        payload_type=PayloadType.COMMS,
        design_life_years=2.0,
        data_rate_kbps=512.0,
        pointing_req_deg=1.5,
        power_req_w=180.0,
        mission_label="capture_hab_demo",
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
    assessment = apply_satellite_constraints(assessment, constraint_evidence=merged_evidence)

    print("=== Satellite Blueprint Capture Demo ===")
    print(f"satellite_class={blueprint.satellite_class.value}")
    print(f"readiness_verdict={report.verdict.value}")
    print(f"power_margin={blueprint.eps.power_margin:.4f}")
    print(f"mass_margin_ratio={blueprint.structure.mass_margin_ratio:.4f}")
    if blueprint.thermal is not None:
        print(f"thermal_hot_c={blueprint.thermal.hot_case_temp_c:.1f}")
        print(f"thermal_cold_c={blueprint.thermal.cold_case_temp_c:.1f}")
    print(f"capture_possible={assessment.capture_possible}")
    print(f"platform_power_scale_0_1={assessment.evidence.get('platform_power_scale_0_1', 0.0)}")
    print(f"thermal_storage_scale_0_1={assessment.evidence.get('thermal_storage_scale_0_1', 0.0)}")


if __name__ == "__main__":
    main()

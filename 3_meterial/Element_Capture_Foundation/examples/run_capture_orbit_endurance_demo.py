from __future__ import annotations

from dataclasses import replace
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_satellite_candidates = (
    ROOT.parent / "Satellite_Design_Stack",
    ROOT.parents[2] / "2_operational" / "60_APPLIED_LAYER" / "Satellite_Design_Stack",
    ROOT.parents[3] / "_staging" / "Satellite_Design_Stack",
)
for _candidate in _satellite_candidates:
    if _candidate.is_dir():
        _s = str(_candidate)
        if _s not in sys.path:
            sys.path.insert(0, _s)
        break

from element_capture import (
    CaptureMode,
    ElementCaptureAdapter,
    IntakeGeometry,
    OrbitalCaptureBridge,
    SeparationStage,
    Species,
    StorageStage,
    apply_capture_platform_profile,
    design_capture_service_bus,
)

try:
    from satellite_design_stack import (
        OrbitType,
        PayloadType,
        SatelliteClass,
        SatelliteDesignPipeline,
        SatelliteMission,
    )
    try:
        from satellite_design_stack import capture_service_bus_profile
    except ImportError:
        capture_service_bus_profile = None
except ImportError:
    OrbitType = None
    PayloadType = None
    SatelliteClass = None
    SatelliteDesignPipeline = None
    SatelliteMission = None
    capture_service_bus_profile = None


def _build_capture_profile(blueprint):
    if capture_service_bus_profile is not None:
        return capture_service_bus_profile(blueprint)
    return SimpleNamespace(
        mode="capture_service_bus",
        satellite_class=getattr(getattr(blueprint, "satellite_class", None), "value", "unknown"),
        dedicated_power_w=400.0,
        collector_area_m2=2.5,
        payload_mass_allowance_kg=12.0,
        thermal_storage_scale_0_1=0.70,
        recommendation="fallback local capture service bus profile",
    )


def main() -> None:
    if SatelliteMission is not None and SatelliteDesignPipeline is not None:
        mission = SatelliteMission(
            satellite_class=SatelliteClass.SMALLSAT,
            orbit_type=OrbitType.LEO,
            altitude_km=180.0,
            payload_type=PayloadType.EXPERIMENTAL,
            design_life_years=0.5,
            data_rate_kbps=64.0,
            pointing_req_deg=5.0,
            power_req_w=40.0,
            mission_label="capture_orbit_demo",
        )
        blueprint, report = SatelliteDesignPipeline().run(mission)
    else:
        blueprint = SimpleNamespace(
            satellite_class=SimpleNamespace(value="fallback_smallsat"),
            eps=SimpleNamespace(generated_power_w=480.0, solar_panel_area_m2=7.0),
            mission=SimpleNamespace(power_req_w=40.0),
            structure=SimpleNamespace(total_mass_kg=520.0, mass_margin_ratio=0.08),
        )
        report = SimpleNamespace(verdict=SimpleNamespace(value="fallback"))
    profile = _build_capture_profile(blueprint)
    intake, separation, storage, evidence = apply_capture_platform_profile(
        profile,
        intake=IntakeGeometry(area_m2=1.5),
        separation=SeparationStage(recovery_efficiency_0_1=0.82, process_power_w=90.0),
        storage=StorageStage(capacity_kg=4.0, stored_mass_kg=0.3, compression_power_w=18.0),
    )
    orbital_bridge = OrbitalCaptureBridge()
    env = orbital_bridge.orbital_skimming_environment(
        altitude_m=180_000.0,
        velocity_ms=7_800.0,
        species=Species.O2,
        species_fraction_0_1=0.2,
        collection_accessibility_0_1=0.6,
        energetic_cost_index=2.0,
        residence_time_s=120.0,
        platform_mass_kg=500.0,
    )
    assessment = ElementCaptureAdapter().assess(
        environment=env,
        intake=intake,
        separation=separation,
        storage=storage,
    )
    assessment = replace(assessment, evidence={**assessment.evidence, **evidence})
    ops = orbital_bridge.assess_capture_operations(
        assessment=assessment,
        altitude_m=180_000.0,
        inclination_deg=51.6,
        delta_v_remaining_ms=180.0,
        mass_kg=500.0,
        area_m2=intake.area_m2,
    )

    print("=== Capture Orbit Endurance Demo ===")
    print(f"satellite_class={blueprint.satellite_class.value}")
    print(f"readiness_verdict={report.verdict.value}")
    print(f"capture_possible={assessment.capture_possible}")
    print(f"orbital_yield_per_pass_kg={assessment.orbital_yield_per_pass_kg:.8f}")
    print(f"orbits_per_day={ops.orbits_per_day:.4f}")
    print(f"daily_capture_kg={ops.daily_capture_kg:.6f}")
    print(f"orbital_omega_0_1={ops.orbital_omega_0_1:.4f}")
    print(f"endurance_score_0_1={ops.endurance_score_0_1:.4f}")
    print(f"mission_feasible={ops.mission_feasible}")
    print(f"recommendation={ops.recommendation}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from element_capture import (
    CaptureFrequencyBridge,
    ElementCaptureAdapter,
    IntakeGeometry,
    OceanusCaptureBridge,
    SeparationStage,
    StorageStage,
    assess_terracore_regeneration,
    apply_frequency_health_to_capture,
    apply_satellite_constraints,
    apply_satellite_thermal_constraints,
    constrain_capture_stack,
)


class DemoSignal:
    def __init__(self, pump_rpm: float, membrane_dp: float, compressor_vibration: float) -> None:
        self.pump_rpm = pump_rpm
        self.membrane_dp = membrane_dp
        self.compressor_vibration = compressor_vibration


class DemoEPS:
    solar_panel_area_m2 = 6.0
    generated_power_w = 1800.0


class DemoMission:
    power_req_w = 1100.0


class DemoStructure:
    total_mass_kg = 420.0
    mass_margin_ratio = 0.12


class DemoBlueprint:
    eps = DemoEPS()
    mission = DemoMission()
    structure = DemoStructure()
    class thermal:
        heater_power_w = 35.0
        radiator_area_m2 = 0.4
        is_thermally_viable = True
        thermal_margin_hot_c = 8.0
        thermal_margin_cold_c = -5.0


def main() -> None:
    env = OceanusCaptureBridge().dissolved_co2_environment(
        {
            "rho_kg_m3": 1027.0,
            "u_ms": 0.6,
            "v_ms": 0.2,
            "S_psu": 35.5,
            "T_k": 285.0,
            "p_bottom_pa": 3.0e6,
            "water_column_m": 250.0,
        }
    )
    intake, separation, storage, constraint_evidence = constrain_capture_stack(
        DemoBlueprint(),
        intake=IntakeGeometry(area_m2=4.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.78, process_power_w=420.0),
        storage=StorageStage(capacity_kg=30.0, stored_mass_kg=4.0, compression_power_w=120.0),
    )
    storage, thermal_evidence = apply_satellite_thermal_constraints(
        DemoBlueprint(),
        storage=storage,
    )
    assessment = ElementCaptureAdapter().assess(
        environment=env,
        intake=intake,
        separation=separation,
        storage=storage,
    )
    merged_evidence = dict(constraint_evidence)
    merged_evidence.update(thermal_evidence)
    assessment = apply_satellite_constraints(assessment, constraint_evidence=merged_evidence)

    freq_bridge = CaptureFrequencyBridge(sample_rate_hz=50.0)
    for idx in range(64):
        freq_bridge.push(DemoSignal(2500.0, 1.2, 0.03 if idx % 2 == 0 else -0.03))
    assessment = apply_frequency_health_to_capture(
        assessment,
        machinery_health=freq_bridge.health("compressor_vibration"),
    )
    regen = assess_terracore_regeneration(
        atmosphere={"co2_ppm": 1800.0, "o2_fraction": 0.208},
        hydrosphere={"water_margin": 0.72, "h2_produced_mol_s": 0.015, "o2_from_water_mol_s": 0.0075},
        biosphere={"co2_uptake_mol_s": 0.01},
    )

    print("=== Spacecraft Resource Loop Demo ===")
    print(f"mode={assessment.environment.mode.value}")
    print(f"species={assessment.environment.species.value}")
    print(f"net_capture_rate_kg_s={assessment.net_capture_rate_kg_s:.8f}")
    print(f"omega_capture={assessment.omega_capture:.4f}")
    print(f"capture_possible={assessment.capture_possible}")
    print(f"platform_power_surplus_w={assessment.evidence.get('platform_power_surplus_w', 0.0)}")
    print(f"thermal_storage_scale_0_1={assessment.evidence.get('thermal_storage_scale_0_1', 1.0)}")
    print(f"machinery_omega_freq={assessment.evidence.get('machinery_omega_freq', 0.0)}")
    print(f"regeneration_closure_gain_0_1={regen.closure_gain_0_1:.4f}")


if __name__ == "__main__":
    main()

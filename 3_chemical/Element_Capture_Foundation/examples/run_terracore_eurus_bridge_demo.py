from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from element_capture import (
    ElementCaptureAdapter,
    IntakeGeometry,
    SeparationStage,
    StorageStage,
    co2_capture_environment_from_terracore,
    h2_extraction_environment_from_terracore,
    EurusCaptureBridge,
    OrbitalCaptureBridge,
)


def main() -> None:
    adapter = ElementCaptureAdapter()

    terra_atmosphere = {
        "total_pressure_pa": 101325.0,
        "co2_partial_pa": 42.5,
        "temperature_k": 288.15,
    }
    terra_hydrosphere = {
        "electrolysis_rate_mol_s": 120.0,
        "h2_produced_mol_s": 60.0,
        "power_consumed_mw": 2.0,
        "water_total_mol": 1_000_000.0,
    }

    co2_env = co2_capture_environment_from_terracore(terra_atmosphere)
    h2_env = h2_extraction_environment_from_terracore(terra_hydrosphere)
    eurus_env = EurusCaptureBridge().atmosphere_capture_environment(altitude_m=5000.0)
    orbital_env = OrbitalCaptureBridge().orbital_skimming_environment(
        altitude_m=180000.0,
        velocity_ms=7800.0,
        residence_time_s=180.0,
        platform_mass_kg=1200.0,
    )

    for name, env in (
        ("TerraCore CO2", co2_env),
        ("TerraCore H2", h2_env),
        ("Eurus altitude CO2", eurus_env),
        ("Orbital skim He", orbital_env),
    ):
        report = adapter.assess(
            environment=env,
            intake=IntakeGeometry(area_m2=5.0),
            separation=SeparationStage(recovery_efficiency_0_1=0.8, process_power_w=500.0),
            storage=StorageStage(capacity_kg=100.0, stored_mass_kg=10.0, storage_efficiency_0_1=0.98),
        )
        print(name)
        print(f"  net_capture_rate_kg_s={report.net_capture_rate_kg_s:.8f}")
        print(f"  omega_capture={report.omega_capture:.4f}")
        print(f"  capture_possible={report.capture_possible}")
        if env.mode.value == "orbital_skimming":
            print(f"  orbital_yield_per_pass_kg={report.orbital_yield_per_pass_kg:.12f}")
            print(f"  drag_penalty_proxy_0_1={report.drag_penalty_proxy_0_1:.8f}")


if __name__ == "__main__":
    main()

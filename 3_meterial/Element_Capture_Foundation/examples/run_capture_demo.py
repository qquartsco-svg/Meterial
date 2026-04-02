from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from element_capture import (
    CaptureMode,
    Species,
    CaptureEnvironment,
    IntakeGeometry,
    SeparationStage,
    StorageStage,
    ElementCaptureAdapter,
)


def main() -> None:
    adapter = ElementCaptureAdapter()

    cases = [
        (
            "CO2 DAC",
            CaptureEnvironment(
                mode=CaptureMode.ATMOSPHERIC_CAPTURE,
                species=Species.CO2,
                density_kg_m3=1.225,
                bulk_velocity_ms=2.0,
                species_fraction_0_1=420e-6,
                collection_accessibility_0_1=0.95,
                energetic_cost_index=0.45,
            ),
        ),
        (
            "H2 electrolysis proxy",
            CaptureEnvironment(
                mode=CaptureMode.ELECTROCHEMICAL_EXTRACTION,
                species=Species.H2,
                density_kg_m3=1000.0,
                bulk_velocity_ms=0.005,
                species_fraction_0_1=0.111,
                collection_accessibility_0_1=0.90,
                energetic_cost_index=0.70,
            ),
        ),
        (
            "He cryogenic separation",
            CaptureEnvironment(
                mode=CaptureMode.CRYOGENIC_SEPARATION,
                species=Species.HE,
                density_kg_m3=2.0,
                bulk_velocity_ms=1.0,
                species_fraction_0_1=0.05,
                collection_accessibility_0_1=0.80,
                energetic_cost_index=0.90,
            ),
        ),
        (
            "Orbital skimming (very thin environment)",
            CaptureEnvironment(
                mode=CaptureMode.ORBITAL_SKIMMING,
                species=Species.HE,
                density_kg_m3=1e-10,
                bulk_velocity_ms=7600.0,
                species_fraction_0_1=1e-6,
                collection_accessibility_0_1=0.1,
                energetic_cost_index=5.0,
                residence_time_s=600.0,
                platform_mass_kg=26_000.0,
            ),
        ),
    ]

    for name, env in cases:
        report = adapter.assess(
            environment=env,
            intake=IntakeGeometry(area_m2=10.0),
            separation=SeparationStage(recovery_efficiency_0_1=0.82, process_power_w=1200.0),
            storage=StorageStage(capacity_kg=50.0, stored_mass_kg=5.0, storage_efficiency_0_1=0.96, compression_power_w=300.0),
        )
        print(name)
        print(f"  net_capture_rate_kg_s={report.net_capture_rate_kg_s:.8f}")
        print(f"  omega_capture={report.omega_capture:.4f}")
        print(f"  capture_possible={report.capture_possible}")
        if env.mode is CaptureMode.ORBITAL_SKIMMING:
            print(f"  orbital_yield_per_pass_kg={report.orbital_yield_per_pass_kg:.12f}")
            print(f"  drag_penalty_proxy_0_1={report.drag_penalty_proxy_0_1:.8f}")


if __name__ == "__main__":
    main()

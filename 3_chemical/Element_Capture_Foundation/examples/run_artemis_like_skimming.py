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

    # Deep-space / cis-lunar style toy case:
    # very low density, long transit, large scoop.
    report = adapter.assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ORBITAL_SKIMMING,
            species=Species.HE,
            density_kg_m3=1e-18,
            bulk_velocity_ms=10_000.0,
            species_fraction_0_1=1e-6,
            collection_accessibility_0_1=0.05,
            energetic_cost_index=8.0,
            residence_time_s=10.0 * 24.0 * 3600.0,
            platform_mass_kg=26_000.0,
        ),
        intake=IntakeGeometry(area_m2=50.0, intake_efficiency_0_1=0.8),
        separation=SeparationStage(
            recovery_efficiency_0_1=0.5,
            selectivity_0_1=0.8,
            process_power_w=2000.0,
        ),
        storage=StorageStage(
            capacity_kg=20.0,
            stored_mass_kg=0.0,
            storage_efficiency_0_1=0.98,
            compression_power_w=200.0,
        ),
    )

    print("Artemis-like deep-space skimming case")
    print(f"  net_capture_rate_kg_s={report.net_capture_rate_kg_s:.20f}")
    print(f"  orbital_yield_per_pass_kg={report.orbital_yield_per_pass_kg:.20f}")
    print(f"  drag_penalty_proxy_0_1={report.drag_penalty_proxy_0_1:.12f}")
    print(f"  omega_capture={report.omega_capture:.4f}")
    print(f"  capture_possible={report.capture_possible}")
    print(f"  notes={report.health.notes}")


if __name__ == "__main__":
    main()

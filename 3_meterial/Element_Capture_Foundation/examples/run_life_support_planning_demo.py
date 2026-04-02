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
    PowerBudget,
    ResourceDemandProfile,
    SeparationStage,
    Species,
    StorageStage,
    assess_waste_loop,
    demand_profile_from_snapshot,
    govern_capture_power,
    plan_resource_horizon,
    snapshot_from_terracore,
)


def main() -> None:
    life = snapshot_from_terracore(
        atmosphere={"co2_ppm": 1800.0, "o2_fraction": 0.208},
        hydrosphere={"water_margin": 0.72, "h2_produced_mol_s": 0.015, "o2_from_water_mol_s": 0.0075},
        crew_count=6,
    )
    demand = demand_profile_from_snapshot(life)
    assessment = ElementCaptureAdapter().assess(
        environment=CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=Species.CO2,
            density_kg_m3=1.225,
            bulk_velocity_ms=2.0,
            species_fraction_0_1=1800e-6,
            collection_accessibility_0_1=0.95,
            energetic_cost_index=0.45,
        ),
        intake=IntakeGeometry(area_m2=12.0),
        separation=SeparationStage(recovery_efficiency_0_1=0.86, process_power_w=900.0),
        storage=StorageStage(capacity_kg=80.0, stored_mass_kg=10.0, storage_efficiency_0_1=0.97),
    )
    plan = plan_resource_horizon(
        assessment,
        ResourceDemandProfile(
            species="co2",
            daily_demand_kg=demand.co2_scrub_demand_kg_day,
            current_inventory_kg=14.0,
            target_buffer_days=10.0,
        ),
    )
    power = govern_capture_power(
        assessment,
        PowerBudget(
            generation_w=2400.0,
            habitat_load_w=1100.0,
            propulsion_reserve_w=250.0,
            research_load_w=100.0,
        ),
    )
    waste = assess_waste_loop(assessment)
    print("=== Life Support Planning Demo ===")
    print(f"crew_count={life.crew_count}")
    print(f"co2_scrub_demand_kg_day={demand.co2_scrub_demand_kg_day:.6f}")
    print(f"daily_capture_kg={plan.daily_capture_kg:.6f}")
    print(f"net_daily_margin_kg={plan.net_daily_margin_kg:.6f}")
    print(f"inventory_horizon_days={plan.inventory_horizon_days:.4f}")
    print(f"power_capture_allowed={power.capture_allowed}")
    print(f"power_margin_w={power.power_margin_w:.2f}")
    print(f"loop_closure_score_0_1={waste.loop_closure_score_0_1:.4f}")
    print(f"recommendation={plan.recommendation}")


if __name__ == "__main__":
    main()

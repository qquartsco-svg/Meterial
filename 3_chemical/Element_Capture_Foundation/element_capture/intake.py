from __future__ import annotations

from .contracts import CaptureEnvironment, IntakeGeometry


def intake_mass_flow_kg_s(environment: CaptureEnvironment, intake: IntakeGeometry) -> float:
    return environment.density_kg_m3 * environment.bulk_velocity_ms * intake.area_m2 * intake.intake_efficiency_0_1


def species_inflow_kg_s(environment: CaptureEnvironment, intake: IntakeGeometry) -> float:
    return intake_mass_flow_kg_s(environment, intake) * environment.species_fraction_0_1

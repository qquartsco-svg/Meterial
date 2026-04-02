from __future__ import annotations

from .contracts import CaptureEnvironment, IntakeGeometry, SeparationStage
from .intake import species_inflow_kg_s


def captured_mass_flow_kg_s(
    environment: CaptureEnvironment,
    intake: IntakeGeometry,
    separation: SeparationStage,
) -> float:
    inflow = species_inflow_kg_s(environment, intake)
    return inflow * separation.recovery_efficiency_0_1 * separation.selectivity_0_1 * environment.collection_accessibility_0_1

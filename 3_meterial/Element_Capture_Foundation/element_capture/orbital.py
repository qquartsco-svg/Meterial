from __future__ import annotations

from .contracts import CaptureEnvironment, IntakeGeometry, SeparationStage
from .separation import captured_mass_flow_kg_s


def orbital_yield_per_pass_kg(
    environment: CaptureEnvironment,
    intake: IntakeGeometry,
    separation: SeparationStage,
) -> float:
    return captured_mass_flow_kg_s(environment, intake, separation) * environment.residence_time_s


def drag_penalty_proxy_0_1(
    environment: CaptureEnvironment,
    intake: IntakeGeometry,
) -> float:
    if environment.platform_mass_kg is None or environment.platform_mass_kg <= 0.0:
        return 0.0
    dynamic_pressure = 0.5 * environment.density_kg_m3 * environment.bulk_velocity_ms ** 2
    area_loading = intake.area_m2 / environment.platform_mass_kg
    proxy = dynamic_pressure * area_loading / 1000.0
    return max(0.0, min(1.0, proxy))


def orbital_skimming_feasible(
    environment: CaptureEnvironment,
    intake: IntakeGeometry,
    separation: SeparationStage,
) -> bool:
    yield_per_pass = orbital_yield_per_pass_kg(environment, intake, separation)
    drag_proxy = drag_penalty_proxy_0_1(environment, intake)
    return yield_per_pass >= 1e-6 and drag_proxy <= 0.25

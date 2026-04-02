from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _get(source: Any, key: str, default: float = 0.0) -> float:
    if isinstance(source, dict):
        return float(source.get(key, default))
    return float(getattr(source, key, default))


@dataclass(frozen=True)
class WasteRegenerationReport:
    recoverable_water_kg_day: float
    recoverable_o2_kg_day: float
    recoverable_co2_kg_day: float
    closure_gain_0_1: float
    recommendation: str


def assess_terracore_regeneration(
    *,
    atmosphere: Any,
    hydrosphere: Any,
    biosphere: Any | None = None,
    crew_count: int = 6,
    crew_water_consumption_mol_s_per_person: float = 4.6e-5,
) -> WasteRegenerationReport:
    water_margin = _get(hydrosphere, "water_margin", 0.0)
    o2_from_water_mol_s = _get(hydrosphere, "o2_from_water_mol_s", 0.0)
    co2_ppm = _get(atmosphere, "co2_ppm", 0.0)
    co2_uptake_mol_s = _get(biosphere, "co2_uptake_mol_s", 0.0) if biosphere is not None else 0.0
    crew_water_mol_s = crew_count * crew_water_consumption_mol_s_per_person

    recoverable_water_kg_day = crew_water_mol_s * 0.018015 * 86400.0 * max(0.0, min(1.0, water_margin))
    recoverable_o2_kg_day = o2_from_water_mol_s * 0.03200 * 86400.0
    recoverable_co2_kg_day = max(co2_uptake_mol_s, co2_ppm / 1e6 * 0.01) * 0.04401 * 86400.0

    closure_gain = max(
        0.0,
        min(
            1.0,
            0.4 * min(1.0, recoverable_water_kg_day / 5.0)
            + 0.3 * min(1.0, recoverable_o2_kg_day / 5.0)
            + 0.3 * min(1.0, recoverable_co2_kg_day / 5.0),
        ),
    )
    recommendation = (
        "regeneration loop materially improves habitat closure"
        if closure_gain >= 0.5
        else "regeneration exists but still needs stronger water or oxygen recovery"
    )
    return WasteRegenerationReport(
        recoverable_water_kg_day=recoverable_water_kg_day,
        recoverable_o2_kg_day=recoverable_o2_kg_day,
        recoverable_co2_kg_day=recoverable_co2_kg_day,
        closure_gain_0_1=closure_gain,
        recommendation=recommendation,
    )

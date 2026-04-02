from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _get(source: Any, key: str, default: float = 0.0) -> float:
    if isinstance(source, dict):
        return float(source.get(key, default))
    return float(getattr(source, key, default))


@dataclass(frozen=True)
class LifeSupportSnapshot:
    crew_count: int
    crew_co2_output_mol_s: float
    crew_o2_consumption_mol_s: float
    crew_water_consumption_mol_s: float
    atmosphere_co2_ppm: float
    atmosphere_o2_fraction: float
    water_margin_0_1: float
    h2_production_mol_s: float
    o2_from_water_mol_s: float


@dataclass(frozen=True)
class CrewMetabolicProfile:
    name: str
    co2_output_mol_s_per_person: float
    o2_consumption_mol_s_per_person: float
    water_consumption_mol_s_per_person: float


@dataclass(frozen=True)
class LifeSupportDemandProfile:
    co2_scrub_demand_kg_day: float
    o2_support_demand_kg_day: float
    water_recovery_demand_kg_day: float
    h2_recovery_potential_kg_day: float


def crew_metabolic_profile(name: str = "nominal") -> CrewMetabolicProfile:
    normalized = name.strip().lower().replace("-", "_")
    if normalized == "reduced_activity":
        return CrewMetabolicProfile(
            name="reduced_activity",
            co2_output_mol_s_per_person=1.9e-4,
            o2_consumption_mol_s_per_person=1.7e-4,
            water_consumption_mol_s_per_person=3.8e-5,
        )
    if normalized == "eva_recovery":
        return CrewMetabolicProfile(
            name="eva_recovery",
            co2_output_mol_s_per_person=2.7e-4,
            o2_consumption_mol_s_per_person=2.3e-4,
            water_consumption_mol_s_per_person=5.4e-5,
        )
    return CrewMetabolicProfile(
        name="nominal",
        co2_output_mol_s_per_person=2.3e-4,
        o2_consumption_mol_s_per_person=2.0e-4,
        water_consumption_mol_s_per_person=4.6e-5,
    )


def snapshot_from_terracore(
    *,
    atmosphere: Any,
    hydrosphere: Any,
    crew_count: int = 6,
    metabolic_profile: CrewMetabolicProfile | None = None,
    crew_co2_output_mol_s_per_person: float = 2.3e-4,
    crew_o2_consumption_mol_s_per_person: float = 2.0e-4,
    crew_water_consumption_mol_s_per_person: float = 4.6e-5,
) -> LifeSupportSnapshot:
    profile = metabolic_profile
    if profile is not None:
        crew_co2_output_mol_s_per_person = profile.co2_output_mol_s_per_person
        crew_o2_consumption_mol_s_per_person = profile.o2_consumption_mol_s_per_person
        crew_water_consumption_mol_s_per_person = profile.water_consumption_mol_s_per_person
    return LifeSupportSnapshot(
        crew_count=crew_count,
        crew_co2_output_mol_s=crew_co2_output_mol_s_per_person * crew_count,
        crew_o2_consumption_mol_s=crew_o2_consumption_mol_s_per_person * crew_count,
        crew_water_consumption_mol_s=crew_water_consumption_mol_s_per_person * crew_count,
        atmosphere_co2_ppm=_get(atmosphere, "co2_ppm", 0.0),
        atmosphere_o2_fraction=_get(atmosphere, "o2_fraction", 0.0),
        water_margin_0_1=_get(hydrosphere, "water_margin", 0.0),
        h2_production_mol_s=_get(hydrosphere, "h2_produced_mol_s", 0.0),
        o2_from_water_mol_s=_get(hydrosphere, "o2_from_water_mol_s", 0.0),
    )


def demand_profile_from_snapshot(snapshot: LifeSupportSnapshot) -> LifeSupportDemandProfile:
    co2_kg_day = snapshot.crew_co2_output_mol_s * 0.04401 * 86400.0
    o2_kg_day = snapshot.crew_o2_consumption_mol_s * 0.03200 * 86400.0
    water_kg_day = snapshot.crew_water_consumption_mol_s * 0.018015 * 86400.0
    h2_kg_day = snapshot.h2_production_mol_s * 0.002016 * 86400.0
    return LifeSupportDemandProfile(
        co2_scrub_demand_kg_day=co2_kg_day,
        o2_support_demand_kg_day=o2_kg_day,
        water_recovery_demand_kg_day=water_kg_day,
        h2_recovery_potential_kg_day=h2_kg_day,
    )

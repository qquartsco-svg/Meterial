from __future__ import annotations

from typing import Any

from ..contracts import CaptureEnvironment, CaptureMode, Species


def _get(source: Any, key: str, default: float = 0.0) -> float:
    if isinstance(source, dict):
        value = source.get(key, default)
    else:
        value = getattr(source, key, default)
    return float(value)


def co2_capture_environment_from_terracore(
    atmosphere: Any,
    *,
    bulk_velocity_ms: float = 2.0,
    collection_accessibility_0_1: float = 0.95,
    energetic_cost_index: float = 0.45,
) -> CaptureEnvironment:
    total_pressure = _get(atmosphere, "total_pressure_pa", 101325.0)
    co2_partial = _get(atmosphere, "co2_partial_pa", 0.0)
    temperature = _get(atmosphere, "temperature_k", 288.15)
    density = max(0.0, total_pressure) / max(287.058 * max(temperature, 1.0), 1.0)
    species_fraction = max(0.0, min(1.0, co2_partial / max(total_pressure, 1.0)))
    return CaptureEnvironment(
        mode=CaptureMode.ATMOSPHERIC_CAPTURE,
        species=Species.CO2,
        density_kg_m3=density,
        bulk_velocity_ms=bulk_velocity_ms,
        species_fraction_0_1=species_fraction,
        collection_accessibility_0_1=collection_accessibility_0_1,
        energetic_cost_index=energetic_cost_index,
        pressure_pa=total_pressure,
        temperature_k=temperature,
    )


def h2_extraction_environment_from_terracore(
    hydrosphere: Any,
    *,
    liquid_density_kg_m3: float = 1000.0,
    collection_accessibility_0_1: float = 0.9,
    energetic_cost_index: float = 0.7,
) -> CaptureEnvironment:
    electrolysis_rate = _get(hydrosphere, "electrolysis_rate_mol_s", 0.0)
    h2_produced = _get(hydrosphere, "h2_produced_mol_s", 0.0)
    power_consumed_mw = _get(hydrosphere, "power_consumed_mw", 0.0)
    water_total_mol = _get(hydrosphere, "water_total_mol", 0.0)

    species_fraction = 0.0
    if electrolysis_rate > 0.0:
        species_fraction = max(0.0, min(1.0, h2_produced / electrolysis_rate))

    return CaptureEnvironment(
        mode=CaptureMode.ELECTROCHEMICAL_EXTRACTION,
        species=Species.H2,
        density_kg_m3=liquid_density_kg_m3,
        bulk_velocity_ms=max(electrolysis_rate * 1e-4, 1e-6),
        species_fraction_0_1=species_fraction,
        collection_accessibility_0_1=collection_accessibility_0_1,
        energetic_cost_index=max(energetic_cost_index, power_consumed_mw / 10.0),
        source_density_kg_m3=water_total_mol * 0.018,
    )

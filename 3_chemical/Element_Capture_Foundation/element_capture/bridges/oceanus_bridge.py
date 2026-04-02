from __future__ import annotations

from typing import Any

from ..contracts import CaptureEnvironment, CaptureMode, Species
from ._resolver import import_sibling_package


def _get(source: Any, key: str, default: float = 0.0) -> float:
    if isinstance(source, dict):
        return float(source.get(key, default))
    return float(getattr(source, key, default))


class OceanusCaptureBridge:
    def __init__(self) -> None:
        self._available = False
        try:
            import_sibling_package("oceanus_engine", "Oceanus_Engine")
            self._available = True
        except ImportError:
            self._available = False

    @property
    def is_available(self) -> bool:
        return self._available

    def dissolved_co2_environment(
        self,
        cell: Any,
        *,
        thermohaline: Any | None = None,
        dissolved_co2_fraction_0_1: float | None = None,
        collection_accessibility_0_1: float = 0.82,
        energetic_cost_index: float = 0.65,
    ) -> CaptureEnvironment:
        rho = _get(cell, "rho_kg_m3", None) or _get(thermohaline, "rho_kg_m3_mean", 1025.0)
        current_speed = max(1e-4, _get(cell, "speed_ms", 0.0) or (_get(cell, "u_ms", 0.0) ** 2 + _get(cell, "v_ms", 0.0) ** 2) ** 0.5)
        salinity = _get(cell, "S_psu", None) or _get(thermohaline, "S_psu_mean", 35.0)
        temperature_k = _get(cell, "T_k", None) or _get(thermohaline, "T_k_mean", 288.15)
        if dissolved_co2_fraction_0_1 is None:
            # Cooler, saltier water can retain dissolved gases more easily.
            temp_factor = max(0.2, min(1.2, (300.0 - temperature_k) / 40.0))
            salinity_factor = max(0.4, min(1.2, salinity / 35.0))
            dissolved_co2_fraction_0_1 = max(1e-5, min(0.02, 0.0025 * temp_factor * salinity_factor))
        return CaptureEnvironment(
            mode=CaptureMode.DISSOLVED_EXTRACTION,
            species=Species.CO2,
            density_kg_m3=max(0.0, rho),
            bulk_velocity_ms=current_speed,
            species_fraction_0_1=max(0.0, min(1.0, dissolved_co2_fraction_0_1)),
            collection_accessibility_0_1=collection_accessibility_0_1,
            energetic_cost_index=energetic_cost_index,
            temperature_k=temperature_k,
            pressure_pa=_get(cell, "p_bottom_pa", 101325.0),
            gravity_mps2=9.80665,
            residence_time_s=max(10.0, _get(cell, "water_column_m", 100.0) / current_speed),
        )

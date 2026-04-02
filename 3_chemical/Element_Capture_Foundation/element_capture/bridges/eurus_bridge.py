from __future__ import annotations

from typing import Any

from ..contracts import CaptureEnvironment, CaptureMode, Species
from ._resolver import import_sibling_package


class EurusCaptureBridge:
    def __init__(self) -> None:
        self._eurus: Any | None = None
        self._available = False
        try:
            self._eurus = import_sibling_package("eurus_engine", "Eurus_Engine")
            self._available = True
        except ImportError:
            self._available = False

    @property
    def is_available(self) -> bool:
        return self._available

    def atmosphere_capture_environment(
        self,
        *,
        altitude_m: float,
        species: Species = Species.CO2,
        species_fraction_0_1: float = 420e-6,
        bulk_velocity_ms: float = 2.0,
        collection_accessibility_0_1: float = 0.95,
        energetic_cost_index: float = 0.45,
    ) -> CaptureEnvironment:
        if self._available:
            profile = self._eurus.standard_atmosphere_profile(
                planet=self._eurus.EARTH,
                z_top_m=max(50_000.0, altitude_m + 500.0),
                dz_m=500.0,
            )
            T_k, p_pa, rho = self._eurus.interpolate_profile_at_altitude(profile, altitude_m)
            gravity = self._eurus.EARTH.gravity_ms2
        else:
            scale_height_m = 8500.0
            p_pa = 101325.0 * (2.718281828 ** (-altitude_m / scale_height_m))
            T_k = 288.15
            rho = p_pa / (287.058 * T_k)
            gravity = 9.80665

        return CaptureEnvironment(
            mode=CaptureMode.ATMOSPHERIC_CAPTURE,
            species=species,
            density_kg_m3=float(rho),
            bulk_velocity_ms=bulk_velocity_ms,
            species_fraction_0_1=species_fraction_0_1,
            collection_accessibility_0_1=collection_accessibility_0_1,
            energetic_cost_index=energetic_cost_index,
            pressure_pa=float(p_pa),
            temperature_k=float(T_k),
            gravity_mps2=float(gravity),
        )

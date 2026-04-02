from __future__ import annotations

import math
from typing import Any

from ..orbital_operations import CaptureOrbitOperationsReport, assess_capture_orbit_operations
from ..contracts import CaptureEnvironment, CaptureMode, Species
from ._resolver import import_sibling_package


class OrbitalCaptureBridge:
    def __init__(self) -> None:
        self._orbital: Any | None = None
        self._density_at_altitude: Any | None = None
        self._adapter_cls: Any | None = None
        self._elements_cls: Any | None = None
        self._available = False
        try:
            self._orbital = import_sibling_package("orbital_core", "OrbitalCore_Engine")
            atmosphere_ext = import_sibling_package("orbital_core.atmosphere_ext", "OrbitalCore_Engine")
            self._density_at_altitude = getattr(atmosphere_ext, "density_at_altitude", None)
            self._adapter_cls = getattr(self._orbital, "OrbitalAdapter", None)
            self._elements_cls = getattr(self._orbital, "OrbitalElements", None)
            self._available = True
        except ImportError:
            self._available = False

    @property
    def is_available(self) -> bool:
        return self._available

    def orbital_skimming_environment(
        self,
        *,
        altitude_m: float,
        velocity_ms: float,
        species: Species = Species.HE,
        species_fraction_0_1: float = 1e-6,
        collection_accessibility_0_1: float = 0.2,
        energetic_cost_index: float = 4.0,
        residence_time_s: float = 300.0,
        platform_mass_kg: float | None = None,
        ballistic_coeff_kg_m2: float | None = None,
    ) -> CaptureEnvironment:
        if self._available and self._density_at_altitude is not None:
            rho = float(self._density_at_altitude(altitude_m))
            gravity = 9.80665
        else:
            scale_height_m = 8500.0
            rho0 = 1.225
            rho = rho0 * (2.718281828 ** (-altitude_m / scale_height_m))
            gravity = 9.80665

        return CaptureEnvironment(
            mode=CaptureMode.ORBITAL_SKIMMING,
            species=species,
            density_kg_m3=max(0.0, rho),
            bulk_velocity_ms=max(0.0, velocity_ms),
            species_fraction_0_1=species_fraction_0_1,
            collection_accessibility_0_1=collection_accessibility_0_1,
            energetic_cost_index=energetic_cost_index,
            gravity_mps2=gravity,
            residence_time_s=residence_time_s,
            platform_mass_kg=platform_mass_kg,
            ballistic_coeff_kg_m2=ballistic_coeff_kg_m2,
        )

    def assess_capture_operations(
        self,
        *,
        assessment: Any,
        altitude_m: float,
        inclination_deg: float = 51.6,
        eccentricity: float = 0.001,
        delta_v_remaining_ms: float = 200.0,
        mass_kg: float = 100.0,
        cd: float = 2.2,
        area_m2: float | None = None,
    ) -> CaptureOrbitOperationsReport:
        intake_area = float(area_m2 if area_m2 is not None else getattr(assessment.intake, "area_m2", 1.0))
        if self._available and self._adapter_cls is not None and self._elements_cls is not None:
            adapter = self._adapter_cls()
            semi_major_axis_m = 6_378_137.0 + altitude_m
            elements = self._elements_cls(
                semi_major_axis_m=semi_major_axis_m,
                eccentricity=eccentricity,
                inclination_rad=math.radians(inclination_deg),
                raan_rad=0.0,
                arg_of_perigee_rad=0.0,
                mean_anomaly_rad=0.0,
                epoch_s=0.0,
            )
            state = adapter.from_elements(elements)
            health = adapter.health(
                state,
                mass_kg=mass_kg,
                cd=cd,
                area_m2=intake_area,
                delta_v_remaining_ms=delta_v_remaining_ms,
            )
            return assess_capture_orbit_operations(
                assessment=assessment,
                orbital_omega_0_1=health.omega_orb,
                drag_health_0_1=health.drag_health,
                maneuver_budget_health_0_1=health.maneuver_budget_health,
                period_s=state.period_s,
            )

        period_s = 2.0 * math.pi * math.sqrt(((6_378_137.0 + altitude_m) ** 3) / 3.986004418e14)
        orbital_omega = 0.4 if altitude_m < 200_000.0 else 0.7
        drag_health = 0.2 if altitude_m < 180_000.0 else 0.6
        budget_health = max(0.0, min(1.0, delta_v_remaining_ms / 200.0))
        return assess_capture_orbit_operations(
            assessment=assessment,
            orbital_omega_0_1=orbital_omega,
            drag_health_0_1=drag_health,
            maneuver_budget_health_0_1=budget_health,
            period_s=period_s,
        )

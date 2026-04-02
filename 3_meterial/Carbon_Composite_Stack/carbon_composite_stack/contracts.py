from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Literal


@dataclass(frozen=True)
class CarbonMaterialCandidate:
    name: str
    density_kg_m3: float
    tensile_strength_mpa: float
    youngs_modulus_gpa: float
    thermal_conductivity_w_mk: float
    electrical_conductivity_s_m: float
    fatigue_strength_mpa: float
    recycle_content_ratio: float = 0.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must be non-empty")
        if self.density_kg_m3 <= 0:
            raise ValueError("density_kg_m3 must be > 0")
        if self.tensile_strength_mpa <= 0:
            raise ValueError("tensile_strength_mpa must be > 0")
        if self.youngs_modulus_gpa <= 0:
            raise ValueError("youngs_modulus_gpa must be > 0")
        if self.fatigue_strength_mpa <= 0:
            raise ValueError("fatigue_strength_mpa must be > 0")
        if not (0.0 <= self.recycle_content_ratio <= 1.0):
            raise ValueError("recycle_content_ratio must be in [0,1]")


@dataclass(frozen=True)
class CompositeProcessConfig:
    cure_temp_c: float
    cure_pressure_bar: float
    cycle_time_min: float
    scrap_rate: float
    energy_kwh_per_kg: float

    def __post_init__(self) -> None:
        if self.cycle_time_min <= 0:
            raise ValueError("cycle_time_min must be > 0")
        if self.cure_pressure_bar < 0:
            raise ValueError("cure_pressure_bar must be >= 0")
        if self.energy_kwh_per_kg <= 0:
            raise ValueError("energy_kwh_per_kg must be > 0")
        if not (0.0 <= self.scrap_rate <= 1.0):
            raise ValueError("scrap_rate must be in [0,1]")


@dataclass(frozen=True)
class ProductSpec:
    target_specific_strength_kn_m_kg: float
    target_specific_stiffness_mn_m_kg: float
    max_mass_kg: float
    min_fatigue_margin: float
    safety_class: Literal["general", "aerospace", "marine", "automotive"] = "general"

    def __post_init__(self) -> None:
        if self.target_specific_strength_kn_m_kg <= 0:
            raise ValueError("target_specific_strength_kn_m_kg must be > 0")
        if self.target_specific_stiffness_mn_m_kg <= 0:
            raise ValueError("target_specific_stiffness_mn_m_kg must be > 0")
        if self.max_mass_kg <= 0:
            raise ValueError("max_mass_kg must be > 0")
        if self.min_fatigue_margin <= 0:
            raise ValueError("min_fatigue_margin must be > 0")


@dataclass(frozen=True)
class MaterialPerformanceReport:
    specific_strength_kn_m_kg: float
    specific_stiffness_mn_m_kg: float
    fatigue_margin: float
    thermal_suitability_score: float
    electrical_suitability_score: float
    mass_budget_proxy_score: float
    omega_material: float


@dataclass(frozen=True)
class ProcessPerformanceReport:
    processability_index: float
    energy_intensity_score: float
    omega_process: float


@dataclass(frozen=True)
class CircularityReport:
    recycle_score: float
    scrap_penalty: float
    omega_circularity: float


@dataclass(frozen=True)
class CarbonCompositeReadinessReport:
    omega_material: float
    omega_process: float
    omega_circularity: float
    omega_total: float
    verdict: Literal["HEALTHY", "STABLE", "FRAGILE", "CRITICAL"]
    evidence: Dict[str, float] = field(default_factory=dict)

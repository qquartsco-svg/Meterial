from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class RefiningMethod(Enum):
    CARBOTHERMIC_REDUCTION = "carbothermic_reduction"
    SIEMENS_PROCESS = "siemens_process"
    FZ_CZ_CRYSTAL_GROWTH = "fz_cz_crystal_growth"


class DomainMode(Enum):
    SEMICONDUCTOR = "semiconductor"
    PHOTOVOLTAIC = "photovoltaic"


class Verdict(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    CAUTIOUS = "cautious"
    NEGATIVE = "negative"


class HealthVerdict(Enum):
    HEALTHY = "healthy"
    STABLE = "stable"
    FRAGILE = "fragile"
    CRITICAL = "critical"


@dataclass(frozen=True)
class SiProperties:
    molar_mass_g_per_mol: float
    density_g_per_cm3: float
    melting_point_k: float
    bandgap_ev_300k: float


@dataclass
class RefiningAssessment:
    method: RefiningMethod
    purity_six_nines_fraction: float
    energy_intensity_kwh_per_kg_si: float
    notes: List[str] = field(default_factory=list)


@dataclass
class DeviceAssessment:
    domain: DomainMode
    efficiency_fraction: float
    defect_density_cm2: float
    thermal_margin_c: float
    notes: List[str] = field(default_factory=list)


@dataclass
class SiliconClaimPayload:
    claim_text: str
    claimed_zero_defects: bool = False
    claimed_unlimited_efficiency: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class SiliconScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)


@dataclass
class SiliconHealthReport:
    omega_refining: float
    omega_device_performance: float
    omega_yield: float
    omega_thermal: float
    omega_economics: float
    composite_omega: float = 0.0
    verdict: HealthVerdict = HealthVerdict.STABLE
    warnings: List[str] = field(default_factory=list)


@dataclass
class ConceptLayer:
    name: str
    description: str
    key_equations: List[str] = field(default_factory=list)


@dataclass
class SiliconFoundationReport:
    refining: Optional[RefiningAssessment] = None
    device: Optional[DeviceAssessment] = None
    screening: Optional[SiliconScreeningReport] = None
    health: Optional[SiliconHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)

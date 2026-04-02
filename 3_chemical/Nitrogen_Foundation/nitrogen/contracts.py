"""L0 — Nitrogen_Foundation contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class SeparationMethod(Enum):
    CRYOGENIC_DISTILLATION = "cryogenic_distillation"
    PSA = "pressure_swing_adsorption"
    MEMBRANE = "membrane"


class StorageMethod(Enum):
    LIQUID_N2 = "liquid_n2"
    HIGH_PRESSURE_GAS = "high_pressure_gas"


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
class N2Properties:
    molar_mass_g_per_mol: float
    boiling_point_k: float
    liquid_density_kg_per_m3_at_bp: float


@dataclass
class SeparationAssessment:
    method: SeparationMethod
    purity_n2_fraction: float
    specific_energy_kwh_per_kg_n2: float
    notes: List[str] = field(default_factory=list)


@dataclass
class FixationAssessment:
    temperature_k: float
    pressure_bar: float
    nh3_equilibrium_mole_fraction: float
    notes: List[str] = field(default_factory=list)


@dataclass
class StorageAssessment:
    method: StorageMethod
    boiloff_percent_per_day: float
    pressure_mpa: float
    temperature_k: float
    notes: List[str] = field(default_factory=list)


@dataclass
class NitrogenClaimPayload:
    claim_text: str
    claimed_free_fertilizer: bool = False
    claimed_air_is_pure_n2: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class NitrogenScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)


@dataclass
class NitrogenHealthReport:
    omega_separation: float
    omega_fixation: float
    omega_storage: float
    omega_safety: float
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
class NitrogenFoundationReport:
    separation: Optional[SeparationAssessment] = None
    fixation: Optional[FixationAssessment] = None
    storage: Optional[StorageAssessment] = None
    screening: Optional[NitrogenScreeningReport] = None
    health: Optional[NitrogenHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)

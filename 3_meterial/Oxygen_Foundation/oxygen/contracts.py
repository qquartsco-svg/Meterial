"""L0 — Oxygen_Foundation contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ProductionMethod(Enum):
    CRYOGENIC_AIR_SEP = "cryogenic_air_separation"
    PSA_VSA = "psa_vsa"
    WATER_ELECTROLYSIS = "water_electrolysis"


class StorageMethod(Enum):
    LOX = "liquid_oxygen"
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
class O2Properties:
    molar_mass_g_per_mol: float
    boiling_point_k: float
    liquid_density_kg_per_m3_at_bp: float


@dataclass
class ProductionAssessment:
    method: ProductionMethod
    purity_o2_fraction: float
    specific_energy_kwh_per_kg_o2: float
    notes: List[str] = field(default_factory=list)


@dataclass
class StorageAssessment:
    method: StorageMethod
    boiloff_percent_per_day: float
    pressure_mpa: float
    temperature_k: float
    notes: List[str] = field(default_factory=list)


@dataclass
class OxygenClaimPayload:
    claim_text: str
    claimed_pure_o2_safe: bool = False
    claimed_moxie_no_energy: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class OxygenScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)


@dataclass
class OxygenHealthReport:
    omega_production: float
    omega_storage: float
    omega_oxidation_risk: float
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
class OxygenFoundationReport:
    production: Optional[ProductionAssessment] = None
    storage: Optional[StorageAssessment] = None
    screening: Optional[OxygenScreeningReport] = None
    health: Optional[OxygenHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)

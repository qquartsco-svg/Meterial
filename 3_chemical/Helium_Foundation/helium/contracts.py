"""L0 — Data contracts for Helium_Foundation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class SourcingMethod(Enum):
    NATURAL_GAS_STRIPPING = "natural_gas_stripping"
    LNG_BOILOFF = "lng_boiloff"
    AIR_FRACTIONATION_TRACE = "air_trace"


class StorageMethod(Enum):
    LIQUID_DEWAR = "liquid_dewar"
    HIGH_PRESSURE_CYLINDER = "high_pressure_cylinder"
    BULK_GASEOUS = "bulk_gaseous"


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
class HeProperties:
    molar_mass_g_per_mol: float
    density_kg_per_m3_stp: float
    boiling_point_k: float
    liquid_density_kg_per_m3_at_bp: float


@dataclass
class SourcingAssessment:
    method: SourcingMethod
    he_recovery_fraction: float
    energy_intensity_kwh_per_kg: float
    notes: List[str] = field(default_factory=list)


@dataclass
class StorageAssessment:
    method: StorageMethod
    boiloff_percent_per_day: float
    pressure_mpa: float
    temperature_k: float
    round_trip_efficiency: float
    notes: List[str] = field(default_factory=list)


@dataclass
class HeliumClaimPayload:
    claim_text: str
    claimed_abundance_unlimited: bool = False
    claimed_cost_usd_per_m3: Optional[float] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class HeliumScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)


@dataclass
class HeliumHealthReport:
    omega_sourcing: float
    omega_storage: float
    omega_utilization: float
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
class HeliumFoundationReport:
    sourcing: Optional[SourcingAssessment] = None
    storage: Optional[StorageAssessment] = None
    screening: Optional[HeliumScreeningReport] = None
    health: Optional[HeliumHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

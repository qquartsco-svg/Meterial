"""L0 contracts for Lithium_Foundation."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ExtractionMethod(Enum):
    BRINE_EVAPORATION = "brine_evaporation"
    HARD_ROCK_SPODUMENE = "hard_rock_spodumene"
    DIRECT_LITHIUM_EXTRACTION = "direct_lithium_extraction"


class BatteryChemistry(Enum):
    LFP = "lfp"
    NMC = "nmc"
    NCA = "nca"
    LTO = "lto"


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
class LiProperties:
    molar_mass_g_per_mol: float
    density_g_per_cm3: float
    melting_point_k: float


@dataclass
class ExtractionAssessment:
    method: ExtractionMethod
    li2co3_equivalent_kg_per_ton_feed: float
    water_intensity_l_per_kg_lce: float
    co2_intensity_kg_per_kg_lce: float
    notes: List[str] = field(default_factory=list)


@dataclass
class BatteryAssessment:
    chemistry: BatteryChemistry
    nominal_voltage_v: float
    specific_energy_wh_per_kg: float
    cycle_life_80pct: int
    thermal_runaway_risk: str
    notes: List[str] = field(default_factory=list)


@dataclass
class LithiumClaimPayload:
    claim_text: str
    claimed_unlimited_supply: bool = False
    claimed_zero_degradation: bool = False
    claimed_zero_recycling_need: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class LithiumScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)


@dataclass
class LithiumHealthReport:
    omega_extraction: float
    omega_battery_performance: float
    omega_safety: float
    omega_recycling: float
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
class LithiumFoundationReport:
    extraction: Optional[ExtractionAssessment] = None
    battery: Optional[BatteryAssessment] = None
    screening: Optional[LithiumScreeningReport] = None
    health: Optional[LithiumHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)

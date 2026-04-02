from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class ProcessMethod(Enum):
    CHLOR_ALKALI = "chlor_alkali"
    EVAPORATION_SALT = "evaporation_salt"

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

@dataclass
class ProcessAssessment:
    method: ProcessMethod
    naoh_kg_per_ton_brine: float
    cl2_kg_per_ton_brine: float
    h2_kg_per_ton_brine: float
    notes: List[str] = field(default_factory=list)

@dataclass
class SaltSystemAssessment:
    salinity_g_per_l: float
    corrosion_risk: str
    scaling_risk: str
    notes: List[str] = field(default_factory=list)

@dataclass
class NaClClaimPayload:
    claim_text: str
    claimed_no_corrosion_in_saltwater: bool = False
    claimed_free_cl2_no_power: bool = False

@dataclass
class NaClScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)

@dataclass
class NaClHealthReport:
    omega_process: float
    omega_materials: float
    omega_safety: float
    omega_waste_control: float
    omega_economics: float
    composite_omega: float = 0.0
    verdict: HealthVerdict = HealthVerdict.STABLE

@dataclass
class ConceptLayer:
    name: str
    description: str

@dataclass
class SodiumChlorineFoundationReport:
    process: Optional[ProcessAssessment] = None
    salt_system: Optional[SaltSystemAssessment] = None
    screening: Optional[NaClScreeningReport] = None
    health: Optional[NaClHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)

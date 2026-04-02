from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class DomainMode(Enum):
    BIOMEDICAL = "biomedical"
    MATERIALS = "materials"

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
class ElectrolyteAssessment:
    serum_ca_mg_dl: float
    serum_mg_mg_dl: float
    risk_level: str
    notes: List[str] = field(default_factory=list)

@dataclass
class AlloyAssessment:
    mg_fraction: float
    ca_fraction: float
    corrosion_risk: str
    notes: List[str] = field(default_factory=list)

@dataclass
class MgCaClaimPayload:
    claim_text: str
    claimed_no_electrolyte_risk: bool = False
    claimed_no_corrosion: bool = False

@dataclass
class MgCaScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)

@dataclass
class MgCaHealthReport:
    omega_biological: float
    omega_materials: float
    omega_safety: float
    omega_recycling: float
    omega_economics: float
    composite_omega: float = 0.0
    verdict: HealthVerdict = HealthVerdict.STABLE

@dataclass
class ConceptLayer:
    name: str
    description: str

@dataclass
class MagnesiumCalciumFoundationReport:
    electrolyte: Optional[ElectrolyteAssessment] = None
    alloy: Optional[AlloyAssessment] = None
    screening: Optional[MgCaScreeningReport] = None
    health: Optional[MgCaHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)

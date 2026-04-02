from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class ProcessMethod(Enum):
    BLAST_FURNACE = "blast_furnace"
    DRI_EAF = "dri_eaf"
    ELECTROLYTIC_IRON = "electrolytic_iron"

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
class FeProperties:
    molar_mass_g_per_mol: float
    density_g_per_cm3: float
    melting_point_k: float

@dataclass
class ProcessAssessment:
    method: ProcessMethod
    co2_intensity_kg_per_ton_steel: float
    energy_gj_per_ton: float
    notes: List[str] = field(default_factory=list)

@dataclass
class CorrosionAssessment:
    corrosion_rate_mm_per_year: float
    mitigation_required: bool
    notes: List[str] = field(default_factory=list)

@dataclass
class IronClaimPayload:
    claim_text: str
    claimed_zero_corrosion: bool = False
    claimed_zero_co2_steel: bool = False

@dataclass
class IronScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)

@dataclass
class IronHealthReport:
    omega_process: float
    omega_corrosion_control: float
    omega_recycling: float
    omega_safety: float
    omega_economics: float
    composite_omega: float = 0.0
    verdict: HealthVerdict = HealthVerdict.STABLE

@dataclass
class ConceptLayer:
    name: str
    description: str

@dataclass
class IronFoundationReport:
    process: Optional[ProcessAssessment] = None
    corrosion: Optional[CorrosionAssessment] = None
    screening: Optional[IronScreeningReport] = None
    health: Optional[IronHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)

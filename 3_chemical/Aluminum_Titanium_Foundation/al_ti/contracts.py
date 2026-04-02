from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class DomainMode(Enum):
    AEROSPACE = "aerospace"
    MARINE = "marine"
    BIOIMPLANT = "bioimplant"

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
class MaterialAssessment:
    al_strength_mpa: float
    ti_strength_mpa: float
    corrosion_risk: str
    notes: List[str] = field(default_factory=list)

@dataclass
class ProcessAssessment:
    al_energy_kwh_per_kg: float
    ti_energy_kwh_per_kg: float
    co2_risk: str
    notes: List[str] = field(default_factory=list)

@dataclass
class AlTiClaimPayload:
    claim_text: str
    claimed_no_galvanic_corrosion: bool = False
    claimed_zero_process_energy: bool = False

@dataclass
class AlTiScreeningReport:
    verdict: Verdict
    omega: float
    flags: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)

@dataclass
class AlTiHealthReport:
    omega_material_choice: float
    omega_process_energy: float
    omega_corrosion_control: float
    omega_safety: float
    omega_economics: float
    composite_omega: float = 0.0
    verdict: HealthVerdict = HealthVerdict.STABLE

@dataclass
class ConceptLayer:
    name: str
    description: str

@dataclass
class AluminumTitaniumFoundationReport:
    material: Optional[MaterialAssessment] = None
    process: Optional[ProcessAssessment] = None
    screening: Optional[AlTiScreeningReport] = None
    health: Optional[AlTiHealthReport] = None
    concept_layers: List[ConceptLayer] = field(default_factory=list)

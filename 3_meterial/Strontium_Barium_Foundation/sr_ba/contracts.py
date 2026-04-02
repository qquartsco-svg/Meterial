from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum):
 POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum):
 HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class ApplicationAssessment:
 ferrite_sr: str; drilling_ba: str; notes: List[str]=field(default_factory=list)
@dataclass
class SpeciationAssessment:
 baso4_insoluble_vs_soluble: str; sr90_waste_note: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload:
 claim_text: str; claimed_all_barium_safe_like_contrast_agent: bool=False; claimed_strontium_always_benign: bool=False
@dataclass
class ScreeningReport:
 verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport:
 omega_tech_fit: float; omega_safety: float; omega_env: float; omega_supply: float; omega_economics: float
 composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer:
 name: str; description: str
@dataclass
class FoundationReport:
 applications: Optional[ApplicationAssessment]=None; speciation: Optional[SpeciationAssessment]=None
 screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None
 concept_layers: List[ConceptLayer]=field(default_factory=list)

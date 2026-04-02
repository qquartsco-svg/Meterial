from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum):
 POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum):
 HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class ResistAssessment:
 polymer_solvent_ehs: str; euvextreme_notes: str; notes: List[str]=field(default_factory=list)
@dataclass
class SlurryAssessment:
 particle_abrasion: str; waste_water: str; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload:
 claim_text: str; claimed_resist_zero_ehs_tail: bool=False; claimed_cmp_slurry_harmless: bool=False
@dataclass
class ScreeningReport:
 verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport:
 omega_supply: float; omega_process: float; omega_quality: float; omega_env: float; omega_economics: float
 composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer:
 name: str; description: str
@dataclass
class FoundationReport:
 resist: Optional[ResistAssessment]=None; slurry: Optional[SlurryAssessment]=None
 screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None
 concept_layers: List[ConceptLayer]=field(default_factory=list)

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Grade(Enum): SS304='ss304'; SS316='ss316'; SS430='ss430'
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class AlloyAssessment: grade: Grade; cr_fraction: float; ni_fraction: float; pitting_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class ProcessAssessment: recycling_fraction: float; co2_intensity_kg_per_ton: float; notes: List[str]=field(default_factory=list)
@dataclass
class ClaimPayload: claim_text: str; claimed_no_pitting: bool=False; claimed_zero_nickel_supply_risk: bool=False
@dataclass
class ScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class HealthReport: omega_corrosion: float; omega_supply: float; omega_process: float; omega_safety: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class FoundationReport: alloy: Optional[AlloyAssessment]=None; process: Optional[ProcessAssessment]=None; screening: Optional[ScreeningReport]=None; health: Optional[HealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)

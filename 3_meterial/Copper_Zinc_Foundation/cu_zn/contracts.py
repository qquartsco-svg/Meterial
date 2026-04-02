from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class AlloyType(Enum): BRASS='brass'; BRONZE='bronze'; PURE_CU='pure_cu'
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class ConductivityAssessment: conductivity_ms_m: float; corrosion_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class AlloyAssessment: alloy: AlloyType; cu_fraction: float; zn_fraction: float; machinability: str; notes: List[str]=field(default_factory=list)
@dataclass
class CuZnClaimPayload: claim_text: str; claimed_no_corrosion: bool=False; claimed_perfect_conductivity: bool=False
@dataclass
class CuZnScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class CuZnHealthReport: omega_conductivity: float; omega_corrosion: float; omega_materials: float; omega_safety: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class CopperZincFoundationReport: conductivity: Optional[ConductivityAssessment]=None; alloy: Optional[AlloyAssessment]=None; screening: Optional[CuZnScreeningReport]=None; health: Optional[CuZnHealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)

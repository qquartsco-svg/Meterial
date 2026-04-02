from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class Verdict(Enum): POSITIVE='positive'; NEUTRAL='neutral'; CAUTIOUS='cautious'; NEGATIVE='negative'
class HealthVerdict(Enum): HEALTHY='healthy'; STABLE='stable'; FRAGILE='fragile'; CRITICAL='critical'
@dataclass
class ElectrolyteAssessment: serum_k_mmol_l: float; risk_level: str; notes: List[str]=field(default_factory=list)
@dataclass
class FertilizerAssessment: k2o_equivalent_kg_per_ton: float; leaching_risk: str; notes: List[str]=field(default_factory=list)
@dataclass
class PotassiumClaimPayload: claim_text: str; claimed_no_hyperkalemia_risk: bool=False; claimed_no_leaching: bool=False
@dataclass
class PotassiumScreeningReport: verdict: Verdict; omega: float; flags: List[str]=field(default_factory=list); reasoning: List[str]=field(default_factory=list)
@dataclass
class PotassiumHealthReport: omega_electrolyte: float; omega_agri: float; omega_safety: float; omega_recycling: float; omega_economics: float; composite_omega: float=0.0; verdict: HealthVerdict=HealthVerdict.STABLE
@dataclass
class ConceptLayer: name: str; description: str
@dataclass
class PotassiumFoundationReport: electrolyte: Optional[ElectrolyteAssessment]=None; fertilizer: Optional[FertilizerAssessment]=None; screening: Optional[PotassiumScreeningReport]=None; health: Optional[PotassiumHealthReport]=None; concept_layers: List[ConceptLayer]=field(default_factory=list)

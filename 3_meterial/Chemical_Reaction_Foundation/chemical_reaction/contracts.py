"""L0 — Data contracts for Chemical_Reaction_Foundation.

Every layer imports from here. Contracts are frozen dataclasses
so that state is immutable once created.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


# ── Enums ────────────────────────────────────────────────────────────────

class Phase(str, Enum):
    GAS = "gas"
    LIQUID = "liquid"
    SOLID = "solid"
    AQUEOUS = "aqueous"
    PLASMA = "plasma"


class Verdict(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    CAUTIOUS = "cautious"
    NEGATIVE = "negative"


class HealthVerdict(str, Enum):
    CONSISTENT = "CONSISTENT"
    PLAUSIBLE = "PLAUSIBLE"
    QUESTIONABLE = "QUESTIONABLE"
    IMPOSSIBLE = "IMPOSSIBLE"


# ── Species & Bonds ──────────────────────────────────────────────────────

@dataclass(frozen=True)
class ChemicalSpecies:
    """Minimal representation of a chemical species."""
    formula: str
    molar_mass_g_per_mol: float
    phase: Phase = Phase.GAS
    charge: int = 0


@dataclass(frozen=True)
class ReactionTerm:
    """A species with its stoichiometric coefficient."""
    species: ChemicalSpecies
    coefficient: float


@dataclass(frozen=True)
class BondInfo:
    """Order-of-magnitude bond energy lookup."""
    bond_type: str
    energy_kj_per_mol: float


# ── Reaction ─────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Reaction:
    """A chemical reaction: reactants → products, with optional thermo/kinetic data."""
    reactants: Tuple[ReactionTerm, ...]
    products: Tuple[ReactionTerm, ...]
    delta_h_kj_per_mol: Optional[float] = None
    delta_s_j_per_mol_k: Optional[float] = None
    activation_energy_kj_per_mol: Optional[float] = None
    label: str = ""


# ── Thermodynamic state ──────────────────────────────────────────────────

@dataclass(frozen=True)
class ThermodynamicState:
    temperature_k: float
    pressure_pa: float = 101325.0
    delta_g_kj_per_mol: Optional[float] = None
    delta_h_kj_per_mol: Optional[float] = None
    delta_s_j_per_mol_k: Optional[float] = None
    spontaneous: Optional[bool] = None


# ── Kinetic state ────────────────────────────────────────────────────────

@dataclass(frozen=True)
class KineticState:
    rate_constant_k: float
    order: float = 1.0
    half_life_s: Optional[float] = None
    catalyst_effect: str = "none"


# ── Electrochemistry ─────────────────────────────────────────────────────

@dataclass(frozen=True)
class ElectrochemicalCell:
    """Simplified electrochemical half-cell / full-cell representation."""
    anode_half_reaction_label: str
    cathode_half_reaction_label: str
    standard_potential_v: float
    n_electrons: int
    actual_potential_v: Optional[float] = None
    overpotential_v: float = 0.0


# ── Screening ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ChemicalClaimPayload:
    claim_text: str
    violates_mass_conservation: bool = False
    violates_energy_conservation: bool = False
    violates_thermodynamic_feasibility: bool = False
    claims_over_unity: bool = False
    claims_perpetual_reaction: bool = False
    ignores_activation_barrier: bool = False
    ignores_equilibrium_limit: bool = False


@dataclass(frozen=True)
class ChemicalScreeningReport:
    claim_text: str
    verdict: Verdict
    omega: float
    flags_triggered: Tuple[str, ...]
    notes: Tuple[str, ...] = ()


# ── Health ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ChemicalHealthReport:
    omega_thermodynamic: float
    omega_kinetic: float
    omega_equilibrium: float
    omega_conservation: float
    omega_electrochemical: float
    composite_omega: float
    verdict: HealthVerdict
    notes: Tuple[str, ...] = ()


# ── Foundation report ────────────────────────────────────────────────────

@dataclass(frozen=True)
class ChemicalFoundationReport:
    layers_inspected: int
    omega: float
    verdict: str
    thermodynamic_feasibility: str
    kinetic_accessibility: str
    equilibrium_position: str
    key_risk: str
    notes: List[str] = field(default_factory=list)


# ── Pedagogical concept layer ────────────────────────────────────────────

@dataclass(frozen=True)
class ConceptLayer:
    name: str
    summary: str
    detail: str = ""

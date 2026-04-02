"""Meterial v0.3.1

E5 Chemistry layer for the 00_BRAIN Epistemic Stack.
Defines species, bonds, thermodynamics, kinetics, equilibrium,
electrochemistry, and ATHENA screening for chemical claims.
"""

__version__ = "0.3.1"

from .contracts import (
    BondInfo,
    ChemicalClaimPayload,
    ChemicalFoundationReport,
    ChemicalHealthReport,
    ChemicalScreeningReport,
    ChemicalSpecies,
    ConceptLayer,
    ElectrochemicalCell,
    HealthVerdict,
    KineticState,
    Phase,
    Reaction,
    ReactionTerm,
    ThermodynamicState,
    Verdict,
)
from .constants import (
    FARADAY_C_PER_MOL,
    R_GAS_J_PER_MOL_K,
    R_GAS_KJ_PER_MOL_K,
    STANDARD_PRESSURE_PA,
    STANDARD_TEMPERATURE_K,
    WATER_ELECTROLYSIS_E0_V,
)
from .foundation import all_concept_layers, assess_chemical_foundation

__all__ = [
    "__version__",
    "BondInfo",
    "ChemicalClaimPayload",
    "ChemicalFoundationReport",
    "ChemicalHealthReport",
    "ChemicalScreeningReport",
    "ChemicalSpecies",
    "ConceptLayer",
    "ElectrochemicalCell",
    "HealthVerdict",
    "KineticState",
    "Phase",
    "Reaction",
    "ReactionTerm",
    "ThermodynamicState",
    "Verdict",
    "FARADAY_C_PER_MOL",
    "R_GAS_J_PER_MOL_K",
    "R_GAS_KJ_PER_MOL_K",
    "STANDARD_PRESSURE_PA",
    "STANDARD_TEMPERATURE_K",
    "WATER_ELECTROLYSIS_E0_V",
    "all_concept_layers",
    "assess_chemical_foundation",
]

"""L1 — Species, bonds, and conservation laws.

Defines what exists before any reaction takes place:
chemical species, bond energies, and mass/charge conservation checks.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Dict, List

from .contracts import (
    BondInfo,
    ChemicalSpecies,
    ConceptLayer,
    Phase,
    Reaction,
    ReactionTerm,
)


# ── Pedagogical axes ─────────────────────────────────────────────────────

def species_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="chemical_species",
            summary="A distinct chemical entity: atom, molecule, ion, or radical.",
            detail=(
                "Defined by its formula and phase. H2O(l) and H2O(g) are "
                "the same molecule in different phases. Na+ and Na are different species."
            ),
        ),
        ConceptLayer(
            name="bond_energy",
            summary="Energy required to break one mole of a specific bond (homolytic, gas phase).",
            detail=(
                "C-H ≈ 413 kJ/mol, O=O ≈ 498, C=O ≈ 799, O-H ≈ 463, N≡N ≈ 945. "
                "These are averages; actual values depend on molecular environment."
            ),
        ),
        ConceptLayer(
            name="mass_conservation",
            summary="Atoms are neither created nor destroyed in a chemical reaction.",
            detail=(
                "The total count of each element on the reactant side must equal "
                "the product side. Nuclear reactions break this rule — chemistry does not."
            ),
        ),
        ConceptLayer(
            name="charge_conservation",
            summary="Net electric charge is conserved across a reaction.",
            detail=(
                "Sum of charges on reactants equals sum on products. "
                "Crucial for ionic and electrochemical reactions."
            ),
        ),
    ]


# ── Bond energy table (order-of-magnitude, kJ/mol) ──────────────────────

_BOND_TABLE: Dict[str, float] = {
    "H-H": 436.0,
    "O-H": 463.0,
    "O=O": 498.0,
    "C-H": 413.0,
    "C-C": 348.0,
    "C=C": 614.0,
    "C≡C": 839.0,
    "C-O": 360.0,
    "C=O": 799.0,
    "C-N": 305.0,
    "C=N": 615.0,
    "C≡N": 891.0,
    "N-H": 391.0,
    "N-N": 163.0,
    "N=N": 418.0,
    "N≡N": 945.0,
    "S-H": 363.0,
    "C-S": 272.0,
    "C-Cl": 339.0,
    "C-F": 485.0,
    "H-F": 567.0,
    "H-Cl": 431.0,
}


def bond_energy_kj_per_mol(bond_type: str) -> float:
    """Return average bond energy for *bond_type* (e.g. ``'C-H'``).

    Raises ``KeyError`` if the bond is not in the built-in table.
    """
    return _BOND_TABLE[bond_type]


def available_bonds() -> List[BondInfo]:
    return [BondInfo(k, v) for k, v in sorted(_BOND_TABLE.items())]


# ── Formula parsing (simple) ─────────────────────────────────────────────

_ELEMENT_RE = re.compile(r"([A-Z][a-z]?)(\d*)")


def parse_formula(formula: str) -> Dict[str, float]:
    """Parse a simple molecular formula into element counts.

    Handles formulas like ``H2O``, ``CO2``, ``CH3COOH`` (flat only; no
    parentheses grouping).
    """
    counts: Dict[str, float] = {}
    for match in _ELEMENT_RE.finditer(formula):
        elem = match.group(1)
        num = match.group(2)
        if elem:
            counts[elem] = counts.get(elem, 0.0) + (float(num) if num else 1.0)
    return counts


# ── Conservation checks ──────────────────────────────────────────────────

def _side_element_counts(terms: tuple[ReactionTerm, ...]) -> Dict[str, float]:
    totals: Dict[str, float] = {}
    for term in terms:
        atoms = parse_formula(term.species.formula)
        for elem, cnt in atoms.items():
            totals[elem] = totals.get(elem, 0.0) + cnt * term.coefficient
    return totals


def verify_mass_balance(reaction: Reaction) -> bool:
    """Return *True* if atom counts balance across the reaction."""
    lhs = _side_element_counts(reaction.reactants)
    rhs = _side_element_counts(reaction.products)
    all_elems = set(lhs) | set(rhs)
    return all(
        abs(lhs.get(e, 0.0) - rhs.get(e, 0.0)) < 1e-9
        for e in all_elems
    )


def verify_charge_balance(reaction: Reaction) -> bool:
    """Return *True* if net charge is conserved."""
    def _side_charge(terms: tuple[ReactionTerm, ...]) -> float:
        return sum(t.species.charge * t.coefficient for t in terms)

    return abs(_side_charge(reaction.reactants) - _side_charge(reaction.products)) < 1e-9


def estimate_delta_h_from_bonds(
    bonds_broken: Dict[str, float],
    bonds_formed: Dict[str, float],
) -> float:
    """Estimate reaction enthalpy from bond energies.

    ΔH ≈ Σ(bonds broken) − Σ(bonds formed).
    Positive → endothermic, Negative → exothermic.
    """
    energy_in = sum(bond_energy_kj_per_mol(b) * n for b, n in bonds_broken.items())
    energy_out = sum(bond_energy_kj_per_mol(b) * n for b, n in bonds_formed.items())
    return energy_in - energy_out

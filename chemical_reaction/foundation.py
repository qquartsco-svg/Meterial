"""Unified entry point — assess_chemical_foundation.

Collects all layers and produces a ChemicalFoundationReport.
"""

from __future__ import annotations

from typing import List, Optional

from .contracts import ChemicalFoundationReport, Reaction
from .species_and_bonds import (
    species_concept_layers,
    verify_charge_balance,
    verify_mass_balance,
)
from .thermodynamics import gibbs_free_energy, thermodynamic_concept_layers
from .kinetics import kinetic_concept_layers
from .equilibrium import equilibrium_constant, equilibrium_concept_layers
from .electrochemistry import electrochemistry_concept_layers
from .screening import screening_concept_layers
from .domain_battery import battery_domain_layers
from .domain_life_support import life_support_domain_layers
from .domain_materials import materials_domain_layers


def all_concept_layers() -> list:
    """Collect all pedagogical concept layers across the engine."""
    layers = []
    layers.extend(species_concept_layers())
    layers.extend(thermodynamic_concept_layers())
    layers.extend(kinetic_concept_layers())
    layers.extend(equilibrium_concept_layers())
    layers.extend(electrochemistry_concept_layers())
    layers.extend(screening_concept_layers())
    layers.extend(battery_domain_layers())
    layers.extend(life_support_domain_layers())
    layers.extend(materials_domain_layers())
    return layers


def assess_chemical_foundation(
    reaction: Optional[Reaction] = None,
    temperature_k: float = 298.15,
) -> ChemicalFoundationReport:
    """Run the full foundation assessment.

    If a reaction is provided, inspects mass/charge balance, thermodynamics,
    and equilibrium. Otherwise returns a layer-count-only report.
    """
    layers = all_concept_layers()
    notes: List[str] = []
    omega_parts: dict[str, float] = {}

    # ── Conservation ─────────────────────────────────────────────────
    if reaction is not None:
        mass_ok = verify_mass_balance(reaction)
        charge_ok = verify_charge_balance(reaction)
        omega_parts["conservation"] = 1.0 if (mass_ok and charge_ok) else 0.2
        if not mass_ok:
            notes.append("Mass balance violated.")
        if not charge_ok:
            notes.append("Charge balance violated.")
    else:
        omega_parts["conservation"] = 0.5
        notes.append("No reaction provided; conservation not checked.")

    # ── Thermodynamics ───────────────────────────────────────────────
    thermo_str = "not_assessed"
    if reaction is not None and reaction.delta_h_kj_per_mol is not None and reaction.delta_s_j_per_mol_k is not None:
        dg = gibbs_free_energy(reaction.delta_h_kj_per_mol, reaction.delta_s_j_per_mol_k, temperature_k)
        if dg < -50:
            thermo_str = "strongly_favorable"
            omega_parts["thermodynamic"] = 0.85
        elif dg < 0:
            thermo_str = "favorable"
            omega_parts["thermodynamic"] = 0.75
        elif dg < 50:
            thermo_str = "marginal"
            omega_parts["thermodynamic"] = 0.50
        else:
            thermo_str = "unfavorable"
            omega_parts["thermodynamic"] = 0.30
        notes.append(f"ΔG = {dg:.1f} kJ/mol at {temperature_k:.0f} K → {thermo_str}.")
    else:
        omega_parts["thermodynamic"] = 0.5

    # ── Kinetics (placeholder — needs Ea input) ──────────────────────
    kinetic_str = "not_assessed"
    if reaction is not None and reaction.activation_energy_kj_per_mol is not None:
        ea = reaction.activation_energy_kj_per_mol
        if ea < 40:
            kinetic_str = "fast"
            omega_parts["kinetic"] = 0.80
        elif ea < 100:
            kinetic_str = "moderate"
            omega_parts["kinetic"] = 0.65
        else:
            kinetic_str = "slow_without_catalyst"
            omega_parts["kinetic"] = 0.40
        notes.append(f"Ea = {ea:.0f} kJ/mol → {kinetic_str}.")
    else:
        omega_parts["kinetic"] = 0.5

    # ── Equilibrium ──────────────────────────────────────────────────
    eq_str = "not_assessed"
    if "thermodynamic" in omega_parts and reaction is not None and reaction.delta_h_kj_per_mol is not None and reaction.delta_s_j_per_mol_k is not None:
        dg = gibbs_free_energy(reaction.delta_h_kj_per_mol, reaction.delta_s_j_per_mol_k, temperature_k)
        try:
            k_eq = equilibrium_constant(dg, temperature_k)
            if k_eq > 1e6:
                eq_str = "products_dominant"
                omega_parts["equilibrium"] = 0.80
            elif k_eq > 1:
                eq_str = "products_favored"
                omega_parts["equilibrium"] = 0.70
            elif k_eq > 1e-6:
                eq_str = "reactants_favored"
                omega_parts["equilibrium"] = 0.45
            else:
                eq_str = "reactants_dominant"
                omega_parts["equilibrium"] = 0.25
            notes.append(f"K_eq ≈ {k_eq:.2e} → {eq_str}.")
        except (ValueError, OverflowError):
            omega_parts["equilibrium"] = 0.5
    else:
        omega_parts["equilibrium"] = 0.5

    # ── Electrochemical (placeholder for cells) ──────────────────────
    omega_parts["electrochemical"] = 0.5

    # ── Composite ────────────────────────────────────────────────────
    values = list(omega_parts.values())
    composite = sum(values) / len(values) if values else 0.5
    composite = min(composite, 0.95)

    if composite >= 0.70:
        verdict_str = "CONSISTENT"
    elif composite >= 0.50:
        verdict_str = "PLAUSIBLE"
    elif composite >= 0.30:
        verdict_str = "QUESTIONABLE"
    else:
        verdict_str = "IMPOSSIBLE"

    key_risk = "none"
    if omega_parts.get("conservation", 1.0) < 0.5:
        key_risk = "conservation_violation"
    elif omega_parts.get("thermodynamic", 1.0) < 0.4:
        key_risk = "thermodynamically_unfavorable"
    elif omega_parts.get("kinetic", 1.0) < 0.4:
        key_risk = "kinetically_inaccessible"

    return ChemicalFoundationReport(
        layers_inspected=len(layers),
        omega=round(composite, 4),
        verdict=verdict_str,
        thermodynamic_feasibility=thermo_str,
        kinetic_accessibility=kinetic_str,
        equilibrium_position=eq_str,
        key_risk=key_risk,
        notes=notes,
    )

"""L5 — Electrochemistry: what happens when electrons are exchanged?

Core equations:
  Nernst: E = E° − (RT/nF) ln Q
  Faraday: m = ItM / nF
  Butler-Volmer: j = j₀[exp(αₐFη/RT) − exp(−αcFη/RT)]
"""

from __future__ import annotations

import math
from typing import List

from .constants import (
    FARADAY_C_PER_MOL,
    R_GAS_J_PER_MOL_K,
    STANDARD_TEMPERATURE_K,
    WATER_ELECTROLYSIS_E0_V,
)
from .contracts import ConceptLayer, ElectrochemicalCell


# ── Pedagogical axes ─────────────────────────────────────────────────────

def electrochemistry_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="nernst_equation",
            summary="E = E° − (RT/nF)·ln Q — actual cell potential under non-standard conditions.",
            detail=(
                "E° = standard reduction potential. n = electrons transferred. "
                "F = Faraday constant. Q = reaction quotient of the cell reaction."
            ),
        ),
        ConceptLayer(
            name="faraday_laws",
            summary="Mass of substance produced/consumed at an electrode is proportional to charge passed.",
            detail=(
                "m = ItM/(nF). I = current [A], t = time [s], M = molar mass [g/mol], "
                "n = electrons per formula unit, F = 96485 C/mol."
            ),
        ),
        ConceptLayer(
            name="overpotential",
            summary="Extra voltage beyond E° required to drive a reaction at practical rates.",
            detail=(
                "Overpotential η = E_applied − E_reversible. "
                "Has three components: activation (electrode kinetics), ohmic (IR drop), "
                "concentration (mass transport limitation)."
            ),
        ),
        ConceptLayer(
            name="butler_volmer",
            summary="j = j₀[exp(αₐFη/RT) − exp(−αcFη/RT)] — electrode kinetics.",
            detail=(
                "j₀ = exchange current density. α = transfer coefficient. "
                "At low η → linear (ohmic) regime. At high η → Tafel regime."
            ),
        ),
    ]


# ── Computational helpers ────────────────────────────────────────────────

def nernst_potential(
    e_standard_v: float,
    n_electrons: int,
    q: float,
    temperature_k: float = STANDARD_TEMPERATURE_K,
) -> float:
    """Nernst equation: E = E° − (RT/nF)·ln Q."""
    if n_electrons <= 0:
        raise ValueError("n_electrons must be positive")
    if q <= 0:
        raise ValueError("reaction quotient Q must be positive")
    return e_standard_v - (R_GAS_J_PER_MOL_K * temperature_k) / (n_electrons * FARADAY_C_PER_MOL) * math.log(q)


def cell_voltage(e_cathode_v: float, e_anode_v: float) -> float:
    """E_cell = E_cathode − E_anode (standard reduction potentials)."""
    return e_cathode_v - e_anode_v


def faraday_mass_g(
    current_a: float,
    time_s: float,
    molar_mass_g_per_mol: float,
    n_electrons: int,
) -> float:
    """Faraday's law: mass deposited/liberated at an electrode.

    m = I·t·M / (n·F)
    """
    if n_electrons <= 0:
        raise ValueError("n_electrons must be positive")
    return (current_a * time_s * molar_mass_g_per_mol) / (n_electrons * FARADAY_C_PER_MOL)


def faraday_mol(current_a: float, time_s: float, n_electrons: int) -> float:
    """Moles of substance from Faraday's law: mol = I·t / (n·F)."""
    if n_electrons <= 0:
        raise ValueError("n_electrons must be positive")
    return (current_a * time_s) / (n_electrons * FARADAY_C_PER_MOL)


def butler_volmer_current_density(
    j0: float,
    alpha_a: float,
    alpha_c: float,
    overpotential_v: float,
    temperature_k: float = STANDARD_TEMPERATURE_K,
) -> float:
    """Butler-Volmer equation for electrode current density.

    j = j₀ · [exp(αₐ·F·η / RT) − exp(−αc·F·η / RT)]

    Parameters
    ----------
    j0 : exchange current density [A/m²]
    alpha_a, alpha_c : anodic/cathodic transfer coefficients (typically α_a + α_c ≈ 1)
    overpotential_v : η [V]
    temperature_k : temperature [K]
    """
    f_over_rt = FARADAY_C_PER_MOL / (R_GAS_J_PER_MOL_K * temperature_k)
    anodic = math.exp(alpha_a * f_over_rt * overpotential_v)
    cathodic = math.exp(-alpha_c * f_over_rt * overpotential_v)
    return j0 * (anodic - cathodic)


def water_electrolysis_minimum_voltage(temperature_k: float = STANDARD_TEMPERATURE_K) -> float:
    """Thermodynamic minimum voltage for water splitting.

    At STP: E° ≈ 1.229 V.  Adjusts slightly with temperature (simplified).
    """
    dt = temperature_k - 298.15
    return WATER_ELECTROLYSIS_E0_V - 0.00085 * dt


def electrolysis_efficiency(
    e_reversible_v: float,
    e_actual_v: float,
) -> float:
    """Voltage efficiency η_V = E_reversible / E_actual."""
    if e_actual_v <= 0:
        raise ValueError("actual voltage must be positive")
    return e_reversible_v / e_actual_v

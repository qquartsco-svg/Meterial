"""Domain mapping: battery electrochemistry.

Bridges Chemical_Reaction_Foundation concepts to Battery_Dynamics_Engine parameters.
"""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def battery_domain_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="ocv_as_nernst",
            summary="Open-Circuit Voltage is the Nernst potential at a given state of charge.",
            detail=(
                "Battery_Dynamics ECMParams.ocv_table maps SOC → OCV. "
                "This is effectively E = E° − (RT/nF)·ln(Q) where Q depends on "
                "lithium-ion activity ratios at the electrodes."
            ),
        ),
        ConceptLayer(
            name="arrhenius_resistance",
            summary="Internal resistance R(T) follows Arrhenius temperature dependence.",
            detail=(
                "ECMParams.Ea_r_ev is the activation energy for ionic transport. "
                "R(T) = R_ref · exp(Ea/kB · (1/T − 1/T_ref)). "
                "This is a kinetic effect: ion mobility is temperature-activated."
            ),
        ),
        ConceptLayer(
            name="sei_as_side_reaction",
            summary="SEI growth is a parasitic electrochemical reaction consuming lithium.",
            detail=(
                "Solid Electrolyte Interface forms from electrolyte decomposition. "
                "Modeled as a slow side reaction with its own Arrhenius kinetics. "
                "This is why Calendar aging is temperature-dependent."
            ),
        ),
        ConceptLayer(
            name="overpotential_budget",
            summary="Battery voltage loss = activation + ohmic + concentration overpotentials.",
            detail=(
                "V_terminal = OCV − I·R_ohmic − η_activation − η_concentration. "
                "Butler-Volmer describes η_activation; Fick's law describes η_concentration."
            ),
        ),
    ]

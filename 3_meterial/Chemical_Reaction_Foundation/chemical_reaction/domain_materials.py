"""Domain mapping: materials chemistry.

Bridges to Carbon_Composite_Stack and Cooking_Process_Foundation.
"""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def materials_domain_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="resin_cure_kinetics",
            summary="Thermoset curing is a crosslinking reaction governed by Arrhenius kinetics.",
            detail=(
                "Carbon_Composite_Stack uses cure_temp and cure_time. "
                "These map to k = A·exp(−Ea/RT) where Ea is the activation energy "
                "for the resin's crosslinking reaction (epoxy ring-opening, etc.)."
            ),
        ),
        ConceptLayer(
            name="maillard_kinetics",
            summary="Maillard browning is a complex cascade of amino-carbonyl reactions.",
            detail=(
                "Cooking_Process_Foundation treats Maillard as a heuristic proxy. "
                "The underlying chemistry: reducing sugars + amino acids → melanoidins, "
                "following approximate Arrhenius kinetics with Ea ≈ 40–120 kJ/mol "
                "depending on the specific sugar-amino acid pair."
            ),
        ),
        ConceptLayer(
            name="corrosion_electrochemistry",
            summary="Corrosion is an electrochemical process: anodic dissolution + cathodic reduction.",
            detail=(
                "Metal → Metal^n+ + ne⁻ (anode). O₂ + 2H₂O + 4e⁻ → 4OH⁻ (cathode in neutral). "
                "Nernst equation determines corrosion potential; Butler-Volmer determines rate."
            ),
        ),
        ConceptLayer(
            name="sintering_diffusion",
            summary="Solid-state reactions (sintering, diffusion bonding) follow Arrhenius-activated diffusion.",
            detail=(
                "D = D₀·exp(−Q/RT) where Q is the activation energy for diffusion. "
                "Relevant for ceramic processing, powder metallurgy, and semiconductor doping."
            ),
        ),
    ]

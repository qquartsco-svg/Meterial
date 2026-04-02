"""Domain mapping: life-support electrochemistry and gas cycling.

Bridges to TerraCore_Stack and Element_Capture_Foundation.
"""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def life_support_domain_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="water_electrolysis",
            summary="2H₂O → 2H₂ + O₂ — the primary oxygen-generation pathway in closed habitats.",
            detail=(
                "E° = 1.229 V at STP. Actual cell voltage is 1.8–2.0 V due to "
                "overpotentials (activation at electrodes + ohmic losses in membrane). "
                "Faraday's law gives mol(O₂)/s = I/(4F) for each electrolysis cell."
            ),
        ),
        ConceptLayer(
            name="sabatier_co2_reduction",
            summary="CO₂ + 4H₂ → CH₄ + 2H₂O — CO₂ recycling into methane and water.",
            detail=(
                "Exothermic (ΔH ≈ −165 kJ/mol). Favorable thermodynamically at low T, "
                "but kinetically requires a Ni or Ru catalyst and ~300–400 °C. "
                "Key for Mars ISRU and space-station CO₂ management."
            ),
        ),
        ConceptLayer(
            name="electrochemical_extraction",
            summary="Selective extraction of species via applied potential.",
            detail=(
                "Element_Capture_Foundation's ELECTROCHEMICAL_EXTRACTION mode. "
                "Nernst potential determines threshold voltage for each species. "
                "Faradaic efficiency measures real yield vs theoretical."
            ),
        ),
        ConceptLayer(
            name="gas_equilibrium",
            summary="Partial pressures and ideal gas equilibria in closed habitats.",
            detail=(
                "N₂/O₂ ratio maintenance, CO₂ accumulation/scrubbing. "
                "Le Chatelier governs how pressure/temperature changes shift gas balances."
            ),
        ),
    ]

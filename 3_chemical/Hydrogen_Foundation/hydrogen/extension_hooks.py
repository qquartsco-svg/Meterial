"""L7 — Extension hooks and sibling engine bridge notes.

This module documents how Hydrogen_Foundation connects to other engines
and what future expansions are planned.
"""

from __future__ import annotations

from typing import Dict, List

from .contracts import ConceptLayer


# ── Sibling engine bridges ─────────────────────────────────────────────

SIBLING_BRIDGES: Dict[str, str] = {
    "Chemical_Reaction_Foundation": (
        "Direct.  Shares ΔG, Arrhenius, Nernst, Faraday.  "
        "Hydrogen electrolysis and fuel cells are special cases of "
        "chemical_reaction.electrochemistry."
    ),
    "Element_Capture_Foundation": (
        "Direct.  H₂ is a first-class capture species (Species.H2).  "
        "Element_Capture provides assess_h2_electrolysis() and TerraCore bridge."
    ),
    "Carbon_Composite_Stack": (
        "Direct.  Type IV compressed H₂ tanks use CFRP liners.  "
        "Carbon_Composite provides cure kinetics and fatigue for tank design."
    ),
    "TerraCore_Stack": (
        "Direct.  WaterCycle.h2_from_electrolysis() produces H₂ for habitat life-support.  "
        "Hydrogen_Foundation can receive the mol/s feed and evaluate storage/safety."
    ),
    "FusionCore_Stack": (
        "Isotopic link.  D-T fusion fuels (deuterium, tritium) are hydrogen isotopes.  "
        "Hydrogen_Foundation covers molecular H₂; FusionCore covers nuclear H."
    ),
    "Battery_Dynamics_Engine": (
        "Complementary.  Battery = electrochemical charge/discharge.  "
        "Fuel cell = electrochemical H₂-to-electricity.  "
        "Both share Nernst, overpotential, degradation concepts."
    ),
    "Token_Dynamics_Foundation": (
        "Conceptual analogy.  H₂ can be modelled as an 'energy token' — "
        "produced (mint), stored (reservoir), consumed (burn), with decay (boil-off)."
    ),
    "Antimatter_Phenomenology_Engine": (
        "Conceptual.  Both deal with energy carriers: H₂ is chemical energy, "
        "antimatter is rest-mass energy.  Orders of magnitude apart."
    ),
    "VectorSpace_102": (
        "Hub connection.  axis_registry can define hydrogen axes "
        "(production_omega, storage_omega, safety_omega, fc_omega, econ_omega) "
        "for GlobalSystemVectorV0 integration."
    ),
}


# ── Future expansion tags ──────────────────────────────────────────────

FUTURE_TAGS: List[str] = [
    "pemfc_degradation_model",
    "sofc_anode_poisoning",
    "electrolyser_stack_optimisation",
    "ammonia_cracking_kinetics",
    "lohc_dehydrogenation",
    "pipeline_h2_blending",
    "geological_storage_cavern",
    "hydrogen_embrittlement_fatigue_model",
    "photoelectrochemical_cell",
    "biological_h2_production",
    "hydrogen_combustion_turbine",
    "lcoh_techno_economic_model",
    "hydrogen_colour_lifecycle_lca",
]


# ── Concept layers ─────────────────────────────────────────────────────

def extension_hooks_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Sibling Engine Bridges",
            description=(
                f"Direct connections to {len([k for k,v in SIBLING_BRIDGES.items() if v.startswith('Direct')])} engines, "
                f"conceptual links to {len([k for k,v in SIBLING_BRIDGES.items() if 'Conceptual' in v or 'analogy' in v.lower()])} more, "
                f"hub link via VectorSpace_102."
            ),
        ),
        ConceptLayer(
            name="Future Expansion",
            description=(
                f"{len(FUTURE_TAGS)} tagged hooks for future modules: "
                "degradation models, ammonia cracking, LOHC, pipeline blending, "
                "geological storage, techno-economic analysis, LCA."
            ),
        ),
    ]

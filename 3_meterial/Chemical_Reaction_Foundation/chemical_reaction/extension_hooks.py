"""L7 — Extension hooks and sibling-engine bridge notes.

Documents how Chemical_Reaction_Foundation connects to other engines
and lists future expansion tags.
"""

from __future__ import annotations

from typing import Dict, List


def extension_roadmap_tags() -> List[str]:
    """Tags for future expansion beyond the current MVP."""
    return [
        "molecular_dynamics_bridge",
        "quantum_chemistry_bridge",
        "biochemistry_reaction_networks",
        "corrosion_and_degradation_models",
        "combustion_kinetics",
        "atmospheric_photochemistry",
        "polymer_chain_growth_kinetics",
        "enzyme_michaelis_menten",
        "surface_catalysis_langmuir_hinshelwood",
        "phase_diagrams_and_phase_transitions",
    ]


def bridge_notes_for_sibling_engines() -> Dict[str, str]:
    """Documented bridge points to sibling engines."""
    return {
        "Battery_Dynamics_Engine": (
            "DIRECT bridge. "
            "OCV ↔ Nernst potential, Arrhenius Ea ↔ kinetics L3, "
            "Butler-Volmer ↔ electrode kinetics L5. "
            "SEI growth as side-reaction kinetics."
        ),
        "Element_Capture_Foundation": (
            "DIRECT bridge. "
            "CaptureMode.ELECTROCHEMICAL_EXTRACTION ↔ Nernst potential L5. "
            "Species separation thresholds from standard reduction potentials."
        ),
        "TerraCore_Stack": (
            "DIRECT bridge. "
            "Water electrolysis cell voltage ↔ electrochemistry L5. "
            "Sabatier CO₂ reduction ↔ thermodynamics L2 + kinetics L3. "
            "Gas inventory mol/s ↔ Faraday's law."
        ),
        "Carbon_Composite_Stack": (
            "DIRECT bridge. "
            "Cure temperature/time ↔ Arrhenius kinetics L3. "
            "Degree of cure as conversion fraction."
        ),
        "Cooking_Process_Foundation": (
            "DIRECT bridge. "
            "Maillard reaction kinetics ↔ Arrhenius L3. "
            "Gelatinization, caramelization as thermal reactions."
        ),
        "Token_Dynamics_Foundation": (
            "CONCEPTUAL ANALOGY — not a physics equivalence. "
            "Equilibrium Q/K ↔ supply/demand balance. "
            "Chemical potential gradient ↔ token flow driver. "
            "Reaction stoichiometry ↔ token exchange ratio."
        ),
        "Higgs_Phenomenology_Foundation": (
            "CONCEPTUAL ANALOGY — not a chemistry equivalence. "
            "Binding energy contributes to composite mass (QCD, not Higgs). "
            "Higgs gives fundamental particle mass; bond energy is electromagnetic."
        ),
        "Antimatter_Phenomenology_Engine": (
            "CONCEPTUAL ANALOGY. "
            "Pair annihilation energy ↔ E=mc² (nuclear/particle, not chemistry). "
            "Chemistry deals with electron rearrangement; antimatter deals with "
            "complete matter-antimatter conversion."
        ),
        "VectorSpace_102": (
            "HUB connection. "
            "from_chemical_assessment adapter planned for v0.3. "
            "5-axis health report maps to VectorAxisSpec presets."
        ),
    }

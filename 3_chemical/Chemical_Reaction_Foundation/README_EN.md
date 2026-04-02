# Chemical_Reaction_Foundation v0.1.0

> **English.** Korean (정본): [README.md](README.md)

---

**"What is a chemical reaction?"** — This engine does not claim to answer that question.  
Instead, it provides an **environment for observing the dynamical flow** of species transformation, energy exchange, equilibrium, and electron transfer.

> **Working definition adopted by this engine:** Chemical reaction ≈ a process in which bonds between atoms are rearranged, transforming matter and energy. This definition is a starting point for exploration, not a fixed conclusion.

---

## Epistemic Position: E5 Chemistry

See [EPISTEMIC_LAYER_MAP_EN.md](../../EPISTEMIC_LAYER_MAP_EN.md).

```
E4 Engineering ← Battery, TerraCore, Carbon_Composite consume chemistry as parameters
   ↓
E5 Chemistry   ← ★ This engine: defines where those parameters come from
   ↓
E6 Biology     ← ATP, blood, neurons operate on top of chemistry
```

---

## What This Engine Is NOT

- Not a molecular dynamics (MD) simulator
- Not a quantum chemistry calculator
- Not a chemical plant process design tool
- Not a precision thermophysical (NIST) database

It uses tree-level equations and order-of-magnitude estimates to observe the skeletal structure of reactions and screen exaggerated claims — a **phenomenology foundation layer**.

---

## Layer Structure

| Layer | Module | Core Question |
|-------|--------|---------------|
| L0 | `contracts.py`, `constants.py` | Data contracts and physical constants |
| L1 | `species_and_bonds.py` | What exists? (species, bonds, conservation laws) |
| L2 | `thermodynamics.py` | Can this reaction occur? (ΔG, ΔH, ΔS) |
| L3 | `kinetics.py` | How fast? (Arrhenius, half-life, catalysts) |
| L4 | `equilibrium.py` | Where does it stop? (K_eq, Q vs K, Le Chatelier) |
| L5 | `electrochemistry.py` | What if electrons are exchanged? (Nernst, Butler-Volmer, Faraday) |
| L6 | `screening.py` | Is this claim valid? (ATHENA 4-tier verdict) |
| L7 | `extension_hooks.py` | Sibling engine bridges, future scope |

---

## Key Equations

| # | Name | Equation | Meaning |
|---|------|----------|---------|
| 1 | Gibbs free energy | $\Delta G = \Delta H - T\Delta S$ | Is it spontaneous? |
| 2 | Arrhenius rate constant | $k = A \exp(-E_a / RT)$ | How fast? |
| 3 | First-order half-life | $t_{1/2} = \ln 2 / k$ | Time for half to react |
| 4 | Rate law | $r = k [A]^a [B]^b$ | Rate vs. concentration |
| 5 | Equilibrium constant | $K_{eq} = \exp(-\Delta G° / RT)$ | Equilibrium position |
| 6 | Nernst equation | $E = E° - (RT/nF) \ln Q$ | Electrochemical potential |
| 7 | Faraday electrolysis | $m = ItM / nF$ | Mass deposited at electrode |
| 8 | Butler-Volmer | $j = j_0 [\exp(\alpha_a F\eta/RT) - \exp(-\alpha_c F\eta/RT)]$ | Electrode current density |

---

## Quick Start

```python
from chemical_reaction import (
    assess_chemical_foundation,
    ChemicalSpecies, Phase, Reaction, ReactionTerm,
)

H2 = ChemicalSpecies("H2", 2.016, Phase.GAS)
O2 = ChemicalSpecies("O2", 32.0, Phase.GAS)
H2O = ChemicalSpecies("H2O", 18.015, Phase.LIQUID)

water_formation = Reaction(
    reactants=(ReactionTerm(H2, 2.0), ReactionTerm(O2, 1.0)),
    products=(ReactionTerm(H2O, 2.0),),
    delta_h_kj_per_mol=-571.6,
    delta_s_j_per_mol_k=-326.8,
    activation_energy_kj_per_mol=75.0,
)

report = assess_chemical_foundation(water_formation, temperature_k=298.15)
print(report.verdict)                   # CONSISTENT
print(report.thermodynamic_feasibility) # strongly_favorable
print(report.omega)                     # 0.74
```

---

## Sibling Engine Bridges

| Sibling | Connection | Nature |
|---------|-----------|--------|
| `Battery_Dynamics_Engine` | OCV ↔ Nernst, Ea ↔ Arrhenius, Butler-Volmer | Direct |
| `Element_Capture_Foundation` | Electrochemical extraction ↔ Nernst | Direct |
| `TerraCore_Stack` | Electrolysis cell voltage ↔ electrochemistry | Direct |
| `Carbon_Composite_Stack` | Cure kinetics ↔ Arrhenius | Direct |
| `Cooking_Process_Foundation` | Maillard kinetics ↔ Arrhenius | Direct |
| `Token_Dynamics_Foundation` | Q/K balance ↔ supply/demand | Conceptual analogy |
| `VectorSpace_102` | `from_chemical_assessment` adapter planned | Hub connection |

---

## ATHENA Screening

| Verdict | Example |
|---------|---------|
| **Positive** | "Water electrolysis requires at least 1.23V" |
| **Neutral** | "This catalyst achieves 90% Faradaic efficiency" |
| **Cautious** | "Room-temp superconductivity enables lossless electrolysis" |
| **Negative** | "This device produces more energy than consumed via water splitting" |

---

## Tests

```
80 passed (0.10s)
```

---

## Current Limitations

- No precision thermophysical data (NIST) — order-of-magnitude estimates only
- No automatic reaction network analysis (multi-step cascades)
- Molecular orbitals and electronic structure are out of scope
- All formulas are tree-level; precision comparison with experiments is the user's responsibility
- High Ω does not guarantee correct chemistry — always cross-validate with experimental data

---

*Chemical_Reaction_Foundation v0.1.0 — E5 Chemistry foundation layer.*

# Chemical_Reaction_Foundation — Design Specification

> **English.** Korean (정본): [DESIGN_SPEC.md](DESIGN_SPEC.md)  
> Epistemic position: **E5 Chemistry** — [EPISTEMIC_LAYER_MAP_EN.md](../../../EPISTEMIC_LAYER_MAP_EN.md)

---

## 1. Why This Engine Is Needed — Gap Analysis

### Current state: many engines **use** chemistry, but none **define** it

| Existing engine | Implicit chemistry usage | What's missing |
|-----------------|------------------------|----------------|
| `Element_Capture_Foundation` | `ELECTROCHEMICAL_EXTRACTION` mode, species capture | Nernst potential, Butler-Volmer kinetics, adsorption isotherms |
| `TerraCore_Stack` | Water electrolysis `2H₂O → 2H₂ + O₂`, mol-based inventory | Cell voltage model, overpotential, efficiency |
| `Battery_Dynamics_Engine` | Arrhenius temperature-dependent resistance, OCV curves | Electrode reaction mechanisms, SEI chemistry, concentration gradients |
| `Carbon_Composite_Stack` | Cure temperature/pressure, cycle time | Resin cure kinetics, degree of polymerization |
| `Cooking_Process_Foundation` | Maillard reaction treated as "heuristic" | Actual reaction kinetics |
| `FusionCore_Stack` | Nuclear reaction `D + T → He + n` | (Nuclear physics — outside chemistry scope) |
| `Token_Dynamics_Foundation` | "Chemical potential" used as gradient-driver analogy | Actual chemical potential definition |

### Core gap

```
No foundation layer defines "What is a chemical reaction?"
```

Each engineering engine **consumes** chemistry as parameters, but no layer **explains where those parameters come from**. This is like using mass without defining how the Higgs field generates it.

---

## 2. Engine Identity — "What is a chemical reaction?"

### One-line definition

> **Chemical_Reaction_Foundation** = A foundation layer that tracks species transformation, energy exchange, equilibrium, and reaction rates. It provides an environment to observe **why reactions happen** (thermodynamics), **how fast** (kinetics), and **where they stop** (equilibrium).

### What this engine is **not**

- Not a molecular dynamics (MD) simulator
- Not a quantum chemistry calculator
- Not a chemical plant process design tool
- Not a precision thermophysical (NIST) database

Like `Higgs_Phenomenology_Foundation`, this is a **phenomenology foundation** that decomposes chemistry into layers, provides tree-level equations and order-of-magnitude estimates, and screens exaggerated claims.

---

## 3. Core Questions

| # | Question | Layer |
|---|----------|-------|
| 1 | What is a chemical species? What is a bond? | L1 |
| 2 | Is this reaction energetically favorable? (ΔG < 0?) | L2 |
| 3 | How fast is this reaction? (activation energy, catalysts) | L3 |
| 4 | Where does this reaction stop? (equilibrium constant, Le Chatelier) | L4 |
| 5 | What happens when electrons are exchanged? (electrochemistry) | L5 |
| 6 | Is this chemical claim physically valid? | L6 |

---

## 4. Layer Structure

```
chemical_reaction/
├── __init__.py
├── contracts.py          ← L0: all data contracts
├── constants.py          ← fundamental constants (R, kB, F, NA)
├── species_and_bonds.py  ← L1: species, bonds, mass conservation
├── thermodynamics.py     ← L2: ΔG, ΔH, ΔS, spontaneity
├── kinetics.py           ← L3: Arrhenius, rate orders, half-life, catalysts
├── equilibrium.py        ← L4: K_eq, Q vs K, Le Chatelier
├── electrochemistry.py   ← L5: Nernst, Butler-Volmer, Faraday
├── screening.py          ← L6: ATHENA 4-tier verdict
├── extension_hooks.py    ← L7: sibling engine bridges, future scope
├── foundation.py         ← unified entry point
├── domain_battery.py     ← domain mapping: battery electrochemistry
├── domain_life_support.py ← domain mapping: life support (electrolysis, gas cycling)
└── domain_materials.py   ← domain mapping: materials (cure, polymerization, corrosion)
```

---

## 5. Key Equations (MVP)

| # | Name | Equation | Layer |
|---|------|----------|-------|
| 1 | Gibbs free energy | $\Delta G = \Delta H - T\Delta S$ | L2 |
| 2 | Arrhenius rate constant | $k = A \exp(-E_a / RT)$ | L3 |
| 3 | First-order half-life | $t_{1/2} = \ln 2 / k$ | L3 |
| 4 | Rate law | $r = k [A]^a [B]^b$ | L3 |
| 5 | Equilibrium constant | $K_{eq} = \exp(-\Delta G° / RT)$ | L4 |
| 6 | Nernst equation | $E = E° - (RT/nF) \ln Q$ | L5 |
| 7 | Faraday electrolysis | $m = ItM / nF$ | L5 |
| 8 | Butler-Volmer | $j = j_0 [\exp(\alpha_a F\eta/RT) - \exp(-\alpha_c F\eta/RT)]$ | L5 |

---

## 6. Sibling Engine Bridges

| Sibling | Bridge content | Nature |
|---------|---------------|--------|
| `Battery_Dynamics_Engine` | Arrhenius Ea ↔ kinetics, OCV ↔ Nernst, Butler-Volmer | **Direct** |
| `Element_Capture_Foundation` | Electrochemical extraction ↔ Nernst potential | **Direct** |
| `TerraCore_Stack` | Electrolysis cell voltage ↔ electrochemistry | **Direct** |
| `Carbon_Composite_Stack` | Cure reaction ↔ Arrhenius kinetics | **Direct** |
| `Cooking_Process_Foundation` | Maillard reaction ↔ kinetics | **Direct** |
| `Token_Dynamics_Foundation` | Q/K balance ↔ supply/demand balance | **Conceptual analogy** |
| `VectorSpace_102` | `from_chemical_assessment` adapter | **Hub connection** |

---

## 7. ATHENA Screening

| Verdict | Example |
|---------|---------|
| **Positive** | "Water electrolysis requires at least 1.23V at standard conditions" |
| **Neutral** | "This catalyst achieves 90% Faradaic efficiency" (plausible, data needed) |
| **Cautious** | "Room-temperature superconductivity enables lossless electrolysis" (speculation risk) |
| **Negative** | "This device produces more energy than consumed via water splitting" (thermodynamics violation) |

---

## 8. Health Report (5-axis Ω)

| Axis | Measures |
|------|----------|
| `omega_thermodynamic` | ΔG direction/magnitude rationality |
| `omega_kinetic` | Reaction rate plausibility |
| `omega_equilibrium` | Equilibrium position rationality |
| `omega_conservation` | Mass/charge/energy conservation |
| `omega_electrochemical` | Electrochemical consistency (when applicable) |

Cold audit: composite Ω > 0.95 triggers warning; any single axis < 0.3 forces verdict to QUESTIONABLE or lower.

---

## 9. Implementation Order

| Step | Content | Depends on |
|------|---------|------------|
| 1 | `contracts.py` + `constants.py` | None |
| 2 | `species_and_bonds.py` | L0 |
| 3 | `thermodynamics.py` | L0, L1 |
| 4 | `kinetics.py` | L0, L2 |
| 5 | `equilibrium.py` | L0, L2 |
| 6 | `electrochemistry.py` | L0, L2, L3 |
| 7 | `screening.py` | L0 |
| 8 | `domain_*.py` (3 files) | L1–L5 |
| 9 | `foundation.py` | All |
| 10 | `extension_hooks.py` | All |
| 11 | Tests + README + signature | All |

---

*Chemical_Reaction_Foundation design spec v0.1. Fills the E5 (Chemistry) gap in the Epistemic Layer Map.*

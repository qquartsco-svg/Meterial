# Chemical_Reaction_Foundation v0.2.0

> **English.** Korean canonical version: [README.md](README.md)

Chemical reactions are often treated as if they were closed answers.  
This engine takes a different stance: it provides an environment for observing **how species transform, how energy is exchanged, how rates change, where equilibrium sits, and how electrons move**.

`Chemical_Reaction_Foundation` is an **E5 Chemistry foundation layer**.  
It does not claim to settle “what chemistry is” once and for all. It provides a shared language for reading reaction structure conservatively.

## What It Is

This engine helps:

- express species and reactions as contracts
- verify mass and charge conservation
- estimate thermodynamic favorability
- estimate kinetic accessibility
- inspect equilibrium bias
- evaluate electrochemical context
- screen exaggerated chemical claims with ATHENA-style verdicts

In short, it is a **chemical observer-ready foundation**.

## What It Is Not

- not a molecular dynamics simulator
- not a quantum chemistry solver
- not a plant-scale process design suite
- not a precision thermophysical database
- not an engine that declares experimental truth for you

Its current role is mostly **tree-level / order-of-magnitude structural reasoning**.

## Why It Matters

Many engineering engines already consume chemistry as parameters:

- batteries
- hydrogen production and storage
- element capture
- carbon composite curing
- cooking chemistry

Without a common chemistry layer, those parameters drift apart into isolated local languages.

This engine is meant to reduce that drift.

## Epistemic Position

See [EPISTEMIC_LAYER_MAP_EN.md](../../EPISTEMIC_LAYER_MAP_EN.md).

```text
E4 Engineering
  -> batteries, hydrogen, capture, materials, processes
E5 Chemistry
  -> Chemical_Reaction_Foundation
E6 Biology
  -> ATP, blood, neurons, memory, cognition
```

## Working Definition

This engine adopts the following working definition:

> A chemical reaction can be read as a process in which bonds are rearranged and matter/energy are transformed through species change and electron transfer.

This is not presented as final truth. It is a starting frame for structured observation.

## Layer Map

| Layer | Module | Question |
|---|---|---|
| L0 | `contracts.py`, `constants.py` | how do we represent the system? |
| L1 | `species_and_bonds.py` | what species and bonds exist? |
| L2 | `thermodynamics.py` | is the reaction favorable? |
| L3 | `kinetics.py` | how fast or slow might it be? |
| L4 | `equilibrium.py` | where does it tend to settle? |
| L5 | `electrochemistry.py` | what changes when electrons are exchanged? |
| L6 | `screening.py` | is the claim overstated? |
| L7 | `extension_hooks.py` | how does it connect to sibling engines? |

## Core Equations

| Name | Equation | Intuition |
|---|---|---|
| Gibbs free energy | `ΔG = ΔH - TΔS` | direction of spontaneity |
| Arrhenius constant | `k = A exp(-Ea/RT)` | temperature and barrier control rate |
| Half-life | `t1/2 = ln 2 / k` | timescale for a first-order process |
| Rate law | `r = k [A]^a [B]^b` | concentration-to-rate relation |
| Equilibrium constant | `K_eq = exp(-ΔG°/RT)` | equilibrium position |
| Nernst equation | `E = E° - (RT/nF) ln Q` | reaction quotient vs cell potential |
| Faraday law | `m = ItM / nF` | charge-to-mass estimate |
| Butler-Volmer | `j = j0 [exp(αaFη/RT) - exp(-αcFη/RT)]` | overpotential vs current density |

## Quick Start

```python
from chemical_reaction import (
    ChemicalSpecies,
    Phase,
    Reaction,
    ReactionTerm,
    assess_chemical_foundation,
)

H2 = ChemicalSpecies("H2", 2.016, Phase.GAS)
O2 = ChemicalSpecies("O2", 32.0, Phase.GAS)
H2O = ChemicalSpecies("H2O", 18.015, Phase.LIQUID)

rxn = Reaction(
    reactants=(ReactionTerm(H2, 2.0), ReactionTerm(O2, 1.0)),
    products=(ReactionTerm(H2O, 2.0),),
    delta_h_kj_per_mol=-571.6,
    delta_s_j_per_mol_k=-326.8,
    activation_energy_kj_per_mol=75.0,
)

report = assess_chemical_foundation(rxn, temperature_k=298.15)
print(report.verdict)
print(report.thermodynamic_feasibility)
print(report.kinetic_accessibility)
print(report.omega)
```

## Sibling Engine Links

| Sibling | Connection |
|---|---|
| `Battery_Dynamics_Engine` | Nernst, Arrhenius, Butler-Volmer |
| `Element_Capture_Foundation` | electrochemical extraction and separation |
| `Hydrogen_Foundation` | electrolysis, fuel cells, storage |
| `Carbon_Composite_Stack` | cure kinetics and thermal budget |
| `Cooking_Process_Foundation` | Maillard and process chemistry |
| `TerraCore_Stack` | life-support and gas-cycle chemistry |
| `VectorSpace_102` | planned adapter into the mathematical hub |

## ATHENA Screening

This engine uses four conservative claim-reading modes:

- `Positive`
- `Neutral`
- `Cautious`
- `Negative`

Examples:

- “Water electrolysis has a reversible-voltage context” -> `Positive`
- “This catalyst improves selectivity” -> `Neutral`
- “Special superconducting conditions may reduce losses” -> `Cautious`
- “This chemical loop yields free energy above input with no external cost” -> `Negative`

## What The Foundation Report Gives

The current roll-up emphasizes:

- `verdict`
- `thermodynamic_feasibility`
- `kinetic_accessibility`
- `equilibrium_position`
- `omega`
- `key_risk`
- `recommendation`

So the goal is not to declare a final answer, but to show **where the reaction should be read carefully**.

## Tests

```text
80 passed
```

Coverage currently includes:

- contracts
- species and conservation
- thermodynamics
- kinetics
- equilibrium
- electrochemistry
- screening
- domain mappings
- extension hooks
- foundation roll-up
- health
- package integrity

## Integrity

- [SIGNATURE.sha256](SIGNATURE.sha256)
- [BLOCKCHAIN_INFO_EN.md](BLOCKCHAIN_INFO_EN.md)
- [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md)

Scripts:

- `python3 scripts/generate_signature.py`
- `python3 scripts/verify_signature.py`
- `python3 scripts/verify_package_identity.py`
- `python3 scripts/release_check.py`

## Current Limits

- no precision thermophysical database
- limited automatic handling of multi-step reaction networks
- no orbital/electronic-structure modeling
- equations are structural approximations, not replacements for high-end chemical simulators
- a high `omega` can indicate structural consistency, but it does not certify experimental truth

## Extension Direction

Natural next steps:

1. `Chemical_Observer_Foundation`
2. element foundations
3. applied chemistry engines
4. `VectorSpace_102` bridge

This repository is therefore not the end of the chemistry layer. It is the root.

## For Standalone Clone Users

Inside the broader `00_BRAIN` workspace this project links to sibling engines,  
but the public repository is kept readable and testable as a **standalone foundation package**.

Sibling links describe extension direction, not a hard runtime dependency.

---

*Chemical_Reaction_Foundation v0.2.0 — E5 chemistry foundation for observing reaction structure rather than declaring final chemical truth.*

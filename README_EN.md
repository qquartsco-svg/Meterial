# Meterial v0.3.0

> **English.** Korean canonical version: [README.md](README.md)

`Meterial` no longer refers only to a single chemical-reaction package.  
This repository now acts as an **umbrella chemistry repository** for the chemistry work that has already been built.

It currently has two layers:

1. a stable root Python package: [`chemical_reaction`](chemical_reaction)
2. a managed chemistry hub snapshot: [`3_meterial/`](3_meterial)

> The public repository name is `Meterial`.  
> The internal Python import remains `chemical_reaction` for compatibility.

---

## What This Repository Is

This repository is meant to help us observe and organize:

- which species exist
- which reactions appear structurally possible
- how energy tends to flow
- how kinetic barriers shape accessibility
- where equilibria may sit
- how electrochemistry changes the picture
- how element foundations and applied chemistry engines connect

So `Meterial` is **not** a repository that declares final chemical truth.  
It is a public umbrella for a chemistry layer that is still being built carefully.

---

## What It Contains Right Now

### 1. Stable chemical root package

The root package [`chemical_reaction`](chemical_reaction) provides:

- species and reaction contracts
- mass and charge conservation checks
- thermodynamic direction via `ΔG = ΔH - TΔS`
- kinetic accessibility via Arrhenius-style reasoning
- equilibrium bias via `K_eq = exp(-ΔG°/RT)`
- electrochemical context via Nernst / Faraday / Butler-Volmer
- ATHENA-style screening for exaggerated claims

This remains the stable **E5 chemistry root foundation**.

### 2. Managed chemistry hub snapshot

The folder [`3_meterial/`](3_meterial) bundles the current meterial layer tree:

- chemical root
  - `Chemical_Reaction_Foundation`
- element foundations
  - `Hydrogen_Foundation`
  - `Helium_Foundation`
  - `Lithium_Foundation`
  - `Nitrogen_Foundation`
  - `Oxygen_Foundation`
  - `Phosphorus_Foundation`
  - `Silicon_Foundation`
  - and additional element/material foundations now being added
- applied chemistry engines
  - `Element_Capture_Foundation`
  - `Battery_Dynamics_Engine`
  - `Carbon_Composite_Stack`
  - `Cooking_Process_Foundation`

This is not presented as a completed periodic-table system.  
It is a **managed snapshot of the chemistry layer as it currently exists**.

---

## How To Read It

The repository is easiest to read in this order:

1. [`chemical_reaction/`](chemical_reaction)
   - the core grammar for reading reactions
2. [`3_meterial/README.md`](3_meterial/README.md)
   - the chemistry hub structure
3. [`3_meterial/ELEMENT_REGISTRY.md`](3_meterial/ELEMENT_REGISTRY.md)
   - which element foundations are active or planned
4. individual foundation / applied engine READMEs
   - specific chemistry domains

In short:

- `chemical_reaction` = core grammar
- `3_meterial` = managed layer map

---

## Current Chemistry Flow

The current flow can be read like this:

```text
chemical_reaction
  -> 3_meterial/Chemical_Reaction_Foundation
  -> element foundations
     -> Hydrogen / Helium / Lithium / Nitrogen / Oxygen / ...
  -> applied chemistry engines
     -> Element_Capture / Battery / Carbon_Composite / Cooking
```

The point is not to claim that this flow is finished forever.  
The point is to keep the chemistry layer readable as it grows.

---

## Why An Umbrella Repository

Once chemistry-related engines begin to multiply, a single foundation README is no longer enough.

For example:

- hydrogen connects to electrolysis, storage, fuel cells, and safety
- oxygen connects to ASU, LOX, and electrolysis
- lithium connects directly to battery chemistry
- phosphorus and nitrogen connect to biology, fertilizers, and ATP loops
- carbon composites connect chemistry to materials and process control
- element capture connects chemistry to life-support and resource recovery

Because of that, `Meterial` now manages both:

- the root package
- the broader chemistry hub snapshot

---

## What It Does Not Do

This repository does **not** currently aim to:

- settle chemistry once and for all
- replace a precision chemistry database
- run quantum chemistry or molecular dynamics
- pretend that every element foundation is equally mature
- claim that the whole periodic table is already complete here

It is a repository for **structured expansion**, not for premature closure.

---

## Core Equations In The Root Package

The root `chemical_reaction` package uses these equations as a shared structural language:

| Name | Equation | Intuition |
|---|---|---|
| Gibbs free energy | `ΔG = ΔH - TΔS` | reaction direction |
| Arrhenius constant | `k = A exp(-Ea/RT)` | barriers and temperature shape rates |
| Rate law | `r = k [A]^a [B]^b` | concentration-to-rate relation |
| Equilibrium constant | `K_eq = exp(-ΔG°/RT)` | equilibrium bias |
| Nernst equation | `E = E° - (RT/nF) ln Q` | potential vs reaction quotient |
| Faraday law | `m = ItM / nF` | charge-to-mass estimate |
| Butler-Volmer | `j = j0 [exp(αaFη/RT) - exp(-αcFη/RT)]` | current density vs overpotential |

These are used as a **conservative reading framework**, not as final proof.

---

## Quick Start

### Use the root package

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
    label="2H2 + O2 -> 2H2O",
)

report = assess_chemical_foundation(rxn, temperature_k=298.15)
print(report.verdict)
print(report.thermodynamic_feasibility)
print(report.kinetic_accessibility)
print(report.omega)
```

### Explore the chemistry hub

Start with:

- [`3_meterial/README.md`](3_meterial/README.md)
- [`3_meterial/ELEMENT_REGISTRY.md`](3_meterial/ELEMENT_REGISTRY.md)
- [`3_meterial/CHEMICAL_GOVERNANCE.md`](3_meterial/CHEMICAL_GOVERNANCE.md)

Then move into the specific element or applied engine you want.

---

## Tests And Verification

Root package tests:

```text
85 passed
```

Current verification scripts:

- `python3 scripts/verify_package_identity.py`
- `python3 scripts/verify_hub_snapshot.py`
- `python3 scripts/verify_signature.py`
- `python3 scripts/release_check.py`

So the repository now checks not only the root package, but also whether the `3_meterial` hub snapshot is actually present.

---

## Integrity

- [SIGNATURE.sha256](SIGNATURE.sha256)
- [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)
- [BLOCKCHAIN_INFO_EN.md](BLOCKCHAIN_INFO_EN.md)
- [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md)

The integrity manifest now tracks the umbrella repository contents, including `3_meterial/`.

This should be read as a repository-level **blockchain-style integrity layer**, not as an absolute truth guarantee.

---

## Current Limits

- not every element foundation is equally mature yet
- `3_meterial` is a managed snapshot, not a claim of final completeness
- the root package does not replace high-end chemistry simulators
- links between the root package and all chemistry sub-engines are still expanding
- the repository prioritizes manageability and coherence over premature certainty

---

## Extension Direction

Natural next steps include:

1. expanding the element foundations
2. adding a `Chemical_Observer_Foundation`
3. strengthening bridges to applied chemistry engines
4. improving `VectorSpace_102` adapters
5. introducing broader hub-wide smoke/release rules for `3_meterial`

So `Meterial` is not the end of the chemistry layer.  
It is the public umbrella used to manage that layer as it grows.

---

## For Standalone Clone Users

This repository remains readable and testable even without the full `00_BRAIN` workspace.

The main distinction is:

- use `chemical_reaction` if you want the stable Python foundation package
- browse `3_meterial` if you want the current chemistry layer map

That split is intentional.

---

*Meterial v0.3.0 — a stable chemical root package plus a managed `3_meterial` umbrella snapshot for the evolving chemistry layer.*

# Changelog

## v0.3.1

- renamed the managed hub snapshot from `3_chemical` to `3_meterial`
- synchronized the public repository snapshot with the expanded ENGINE_HUB meterial layer
- refreshed README / README_EN and hub governance docs to explain the material flow more clearly
- updated hub verification so release checks validate the `3_meterial` layout
- refreshed umbrella integrity metadata for the renamed snapshot tree

## v0.3.0

- expanded `Meterial` from a single public chemistry foundation into an umbrella repository
- bundled the managed `3_chemical/` hub snapshot inside the public repository
- rewrote the root README / README_EN to explain the umbrella structure and current chemistry layers
- added `verify_hub_snapshot.py` so release checks now validate the chemistry hub layout
- broadened the SHA-256 manifest to cover the umbrella repository contents, including `3_chemical`
- updated cleanup logic to remove cache artifacts recursively across the umbrella tree

## v0.2.0

- expanded public README / README_EN for standalone readers
- added blockchain-style integrity docs
- added cleanup / package identity / release check scripts
- added package integrity tests
- aligned release metadata for public repository preparation

## v0.2.1

- renamed public repository branding to `Meterial`
- kept internal `chemical_reaction` package import stable for compatibility
- refreshed README / metadata to reflect the new public name

## 0.1.0 — 2026-04-02

- Initial release: E5 Chemistry layer for the 00_BRAIN Epistemic Stack.
- L0: Contracts (species, reaction, thermodynamic/kinetic/electrochemical states, screening, health).
- L1: Species & Bonds (formula parsing, bond energy table, mass/charge conservation).
- L2: Thermodynamics (Gibbs free energy, enthalpy, entropy, spontaneity).
- L3: Kinetics (Arrhenius, rate law, half-life, catalyst effect).
- L4: Equilibrium (K_eq, reaction quotient, Le Chatelier, van 't Hoff).
- L5: Electrochemistry (Nernst, Faraday, Butler-Volmer, overpotential, electrolysis).
- L6: ATHENA screening (7 flags, 4-tier verdict).
- L7: Extension hooks (9 sibling bridges, 10 future tags).
- Domain mappings: battery, life-support, materials.
- Foundation entry point: `assess_chemical_foundation()`.

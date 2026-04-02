> **English.** Korean (canonical): [README.md](README.md)

# Element_Capture_Foundation v0.2.0

**Domain-neutral engineering kernel for elemental and gas capture, extraction, storage, and self-sufficiency screening**

`Element_Capture_Foundation` does not treat CO2, H2, He, He-3, or dissolved resources as one vague problem.
Instead, it models:

- source density
- species fraction
- intake flux
- separation efficiency
- storage margin
- energy burden
- platform constraints
- machinery health
- life-support demand
- orbital endurance

and asks a more honest engineering question:

**does this resource-recovery loop actually close under the given environment and platform?**

## Core Idea

This engine distinguishes:

- `capture`
  - collect species already dispersed in gas flow or mixed atmosphere
- `extraction`
  - separate or produce target species from liquid, dissolved, or electrochemical source

It also distinguishes:

- “the resource exists”
- “the resource is operationally accessible”

That is why the environment contract carries not only density/fraction, but also:

- `collection_accessibility_0_1`
- `energetic_cost_index`
- `residence_time_s`
- `platform_mass_kg`

## Supported Modes

- `atmospheric_capture`
- `dissolved_extraction`
- `electrochemical_extraction`
- `cryogenic_separation`
- `orbital_skimming`

## Core Equations

Inflow mass rate:

`m_dot_in = rho * v * A`

Species inflow mass rate:

`m_dot_species_in = y_i * rho * v * A`

Captured mass rate:

`m_dot_capture = eta * y_i * rho * v * A * accessibility`

Energy intensity:

`energy_intensity = power_input_w / max(m_dot_capture, eps)`

These equations are intentionally simple. They are used for **screening and feasibility**, not high-fidelity certification.

## Architecture

```text
environment -> intake -> separation -> storage -> health
                                 \-> planning -> power -> waste -> habitat ops
                                 \-> orbital endurance
```

Modules:

- `environment.py`
- `intake.py`
- `separation.py`
- `storage.py`
- `health.py`
- `specializations.py`
- `planning.py`
- `power_governance.py`
- `waste_loop.py`
- `waste_regeneration.py`
- `habitat_operations.py`
- `orbital.py`
- `orbital_operations.py`
- `bridges/`

## What It Connects To

- [Eurus_Engine](/Users/jazzin/Desktop/00_BRAIN/_staging/Eurus_Engine/README.md)
  - atmosphere density, pressure, altitude profile
- [TerraCore_Stack](/Users/jazzin/Desktop/00_BRAIN/_staging/TerraCore_Stack/README.md)
  - CO2 / H2O / H2 inventories, hydrosphere, electrolysis context
- [Oceanus_Engine](/Users/jazzin/Desktop/00_BRAIN/_staging/Oceanus_Engine)
  - dissolved resource extraction
- [OrbitalCore_Engine](/Users/jazzin/Desktop/00_BRAIN/_staging/OrbitalCore_Engine/README.md)
  - orbital skimming yield, drag penalty, endurance
- [Satellite_Design_Stack](/Users/jazzin/Desktop/00_BRAIN/_staging/Satellite_Design_Stack/README.md)
  - area/power/mass/thermal constraints
- [FrequencyCore_Engine](/Users/jazzin/Desktop/00_BRAIN/_staging/FrequencyCore_Engine/README.md)
  - machinery vibration health

## Current Scope

Implemented:

- CO2 atmospheric capture screening
- H2 electrochemical extraction screening
- He cryogenic separation screening
- orbital skimming feasibility
- life-support demand normalization
- storage horizon planning
- power governance
- waste/regeneration loop scoring
- habitat operation assessment
- orbital capture endurance scoring

## Current Limits

This engine is **not**:

- a CFD engine
- a full chemical process simulator
- a cryogenic plant simulator
- a certified spacecraft ECLSS solver
- a mission-grade orbital resource economics model

It is best read as an **L1/L2 resource-capture feasibility and self-sufficiency kernel**.

Especially important:

- deep-space direct capture remains highly yield-limited
- orbital skimming is evaluated conservatively
- platform feasibility is often blocked by thermal and mass limits before raw capture equations

## Spacecraft Self-Sufficiency Reading

This engine already supports a foundational loop:

- source environment
- recovery / extraction
- storage
- platform constraints
- machinery health
- crew demand
- power allocation
- waste regeneration
- habitat operations
- orbital endurance

Details:

- [docs/SPACECRAFT_SELF_SUFFICIENCY_STACK.md](docs/SPACECRAFT_SELF_SUFFICIENCY_STACK.md)
- [docs/INTEGRATION_MAP.md](docs/INTEGRATION_MAP.md)

## Example Entry Points

- [examples/run_capture_demo.py](examples/run_capture_demo.py)
- [examples/run_artemis_like_skimming.py](examples/run_artemis_like_skimming.py)
- [examples/run_terracore_eurus_bridge_demo.py](examples/run_terracore_eurus_bridge_demo.py)
- [examples/run_spacecraft_resource_loop.py](examples/run_spacecraft_resource_loop.py)
- [examples/run_life_support_planning_demo.py](examples/run_life_support_planning_demo.py)
- [examples/run_platform_class_comparison.py](examples/run_platform_class_comparison.py)
- [examples/run_satellite_blueprint_capture_demo.py](examples/run_satellite_blueprint_capture_demo.py)
- [examples/run_capture_orbit_endurance_demo.py](examples/run_capture_orbit_endurance_demo.py)

## Current Validation State

- `35 passed` after public-release hardening
- example entrypoints are smoke-tested in release validation
- integrity verification: `python scripts/verify_signature.py`
- release validation: `python scripts/release_check.py`

## Integrity (“Blockchain Signature”)

Here, “blockchain signature” means a repository SHA-256 integrity manifest in `SIGNATURE.sha256`.

- Provides:
  - tamper checks for code/doc surface at release time
- Does not provide:
  - private-key signing
  - on-chain storage
  - smart contracts

See:

- [BLOCKCHAIN_INFO_EN.md](BLOCKCHAIN_INFO_EN.md)
- [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)

## Quick Start

```bash
python3 -m pytest tests -q
python3 scripts/verify_signature.py
python3 scripts/release_check.py
```

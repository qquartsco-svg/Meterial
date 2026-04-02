> **English.** Korean (정본): [README.md](README.md)

# Carbon Composite Stack

This is not a one-shot platform for all carbon industries.
It is an **L1 independent engine for carbon-composite design/process/circularity readiness screening**.

Version: `0.1.2`

One-line definition:
**a carbon-composite design kernel that merges material + process + circularity into one omega verdict**.

## Scope

What it does:

- evaluates candidate composite material performance (strength/stiffness/fatigue)
- evaluates processability from cure/pressure/cycle/scrap settings
- evaluates circularity from recycle/scrap signals
- emits `HEALTHY/STABLE/FRAGILE/CRITICAL` readiness verdict

What it does not do:

- new material discovery replacement
- high-fidelity multiphysics solver replacement
- production qualification/regulatory replacement

Current maturity (conservative reading):

- `v0.1.2` is an **early L1 scaffold** with concept/contract/input-output boundaries fixed first.
- The current test snapshot (`4 passed`) validates baseline operability; broader material/process physics regression depth is a next-stage expansion target.

## Layers

- `contracts`: `CarbonMaterialCandidate`, `CompositeProcessConfig`, `ProductSpec`
- `material`: specific strength/stiffness/fatigue margin + thermal/electrical suitability + mass-budget proxy
- `process`: processability/energy intensity (captures process difficulty, energy intensity, and scrap-loss penalties)
- `circularity`: recycle score/scrap penalty (planned expansion: virgin/recycled ratio, scrap reuse path, repair/rework, embodied energy)
- `observer`: `omega_total` + verdict (readiness aggregation layer over material/process/circularity signals)
- `pipeline`: `run_composite_assessment()` (execution orchestration layer for the assessment flow)
- `engine_ref_adapter`: `carbon.composite.readiness`
- `cli`: `carbon-composite-assess --input-json ... --json`

## Core Concepts

- `specific_strength = tensile_strength / density`
- `specific_stiffness = modulus / density`
- `omega_total = 0.45*omega_material + 0.35*omega_process + 0.20*omega_circularity`

This model is a design-stage screening proxy, not an absolute performance guarantee.

### Unit Notes (Target Spec)

- `target_specific_strength_kn_m_kg`: target specific strength in `kN·m/kg`
- `target_specific_stiffness_mn_m_kg`: target specific stiffness in `MN·m/kg`
- Keep external input units and internal calculation units aligned through docs/version updates.
- `max_mass_kg`: not yet a full geometry-derived mass solver input; currently used as a **density-based lightweight pressure proxy**.
- `safety_class`: a conservative selector that tightens or relaxes thermal/electrical targets and mass proxy behavior.

## Quick Start

```python
from carbon_composite_stack import (
    CarbonMaterialCandidate, CompositeProcessConfig, ProductSpec, run_composite_assessment
)

material = CarbonMaterialCandidate(
    name="CFRP-A",
    density_kg_m3=1550.0,
    tensile_strength_mpa=1800.0,
    youngs_modulus_gpa=140.0,
    thermal_conductivity_w_mk=8.5,
    electrical_conductivity_s_m=15000.0,
    fatigue_strength_mpa=900.0,
    recycle_content_ratio=0.2,
)
process = CompositeProcessConfig(
    cure_temp_c=180.0,
    cure_pressure_bar=6.0,
    cycle_time_min=95.0,
    scrap_rate=0.08,
    energy_kwh_per_kg=9.0,
)
spec = ProductSpec(
    target_specific_strength_kn_m_kg=1.0,
    target_specific_stiffness_mn_m_kg=70.0,
    max_mass_kg=120.0,
    min_fatigue_margin=0.45,
    safety_class="aerospace",
)

readiness, material_report, process_report, circularity_report = run_composite_assessment(material, process, spec)
print(readiness.verdict, readiness.omega_total)
```

CLI:

```bash
cd _staging/Carbon_Composite_Stack
python3 -m carbon_composite_stack.cli --input-json examples/sample_payload.json --json
```

## design_workspace Integration

- `engine_ref`: `carbon.composite.readiness`
- payload:
  - `material`: candidate material properties
  - `process`: cure/cycle/scrap/energy settings
  - `spec`: target specific-strength/specific-stiffness/fatigue margin/safety class

## Test

```bash
cd _staging/Carbon_Composite_Stack
python3 -m pytest tests/ -q --tb=no
```

Current local check snapshot:

- `4 passed`
- categories: contracts validation, readiness aggregation, engine_ref/CLI payload flow

Next test-depth priorities:

- material axis: anisotropy/fiber-orientation and environment degradation (temperature/humidity) cases
- process axis: cycle/scrap/energy boundary cases and penalty monotonicity checks
- circularity axis: omega stability regression across recycle/scrap combinations

## Changelog / Integrity

- changelog: [CHANGELOG.md](CHANGELOG.md)
- integrity note: [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)
- continuity log: [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md)
- SHA-256 manifest: [SIGNATURE.sha256](SIGNATURE.sha256)

Verification:

```bash
python3 scripts/generate_signature.py
python3 scripts/verify_signature.py
```

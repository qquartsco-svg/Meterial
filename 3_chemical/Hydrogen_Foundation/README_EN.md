> **English.** Korean (정본): [README.md](README.md)

# Hydrogen_Foundation v0.1.0

**"What is hydrogen?"**

This engine organises everything about hydrogen into a single foundation layer.
Production, storage, fuel cells, safety, economics, and screening — each layer
provides an environment in which one can observe
*why hydrogen matters*, *where it hits walls*, and *what is overstated*.

This engine does not present a single answer.
It presents an environment in which answers can be inferred through dynamical flow.

---

## Epistemic Position

| Layer | Role |
|-------|------|
| **E5 Chemistry** | `3_chemical/` hub — Chemical_Reaction → Element_Capture → Carbon_Composite → **Hydrogen** |
| **E2 Math Core** | `VectorSpace_102` — hydrogen axes (production, storage, safety, fc, econ) into state vector |

---

## What Is Hydrogen?

Hydrogen (H₂) is the most abundant element in the universe and the lightest molecule.

| Property | Value |
|----------|-------|
| Molar mass | 2.016 g/mol |
| Density (STP) | 0.0899 kg/m³ |
| LHV | 120 MJ/kg (33.3 kWh/kg) |
| HHV | 141.8 MJ/kg |
| Boiling point | 20.28 K (−253 °C) |
| Flammable range | 4–75 vol% in air |
| Auto-ignition | 585 °C |

**Key caveat**: Hydrogen is an energy *carrier*, not an energy *source*.
Making it requires energy, and losses are inevitable in storage, transport, and conversion.

---

## Layer Structure

```
L0  contracts.py           — data contracts
L1  properties.py          — H₂ property card, ideal gas / Van der Waals, Z
L2  production.py          — electrolysis (PEM/Alkaline/SOEC), SMR, colour code
L3  storage.py             — compressed gas, liquid H₂, metal hydrides
L4  fuel_cell.py           — Nernst OCV, PEMFC/SOFC/AFC efficiency
L5  safety.py              — flammable range, ventilation, embrittlement, overpressure
L6  screening.py           — ATHENA 7-flag, 4-tier verdict
L7  extension_hooks.py     — 9 sibling bridges, 13 future tags
    domain_space.py        — LOX/LH₂, ISRU, life-support
    domain_grid.py         — P2G round-trip, LCOH
    domain_transport.py    — FCEV range, refuelling
    foundation.py          — unified entry point + 5-axis health
```

---

## Core Equations

| # | Name | Equation | Layer |
|---|------|----------|-------|
| 1 | Electrolysis cell voltage | $V_{cell} = E_{rev} + \eta_{act} + j \cdot R_{ohm}$ | L2 |
| 2 | Faraday production | $\dot{m}_{H_2} = \eta_F \cdot I / (n \cdot F)$ | L2 |
| 3 | Electrolysis efficiency | $\eta = E°_{rev} / V_{cell} \times \eta_F$ | L2 |
| 4 | SMR equilibrium | $K_{eq} = \exp(-\Delta H° / RT + C)$ | L2 |
| 5 | Compression work | $W = nRT \ln(P_2/P_1) / \eta_{is}$ | L3 |
| 6 | Boil-off | $\dot{m}_{boiloff} = Q_{leak} / L_{vap}$ | L3 |
| 7 | Metal hydride | $\ln(P/P_{ref}) = (\Delta H/R)(1/T_{ref} - 1/T)$ | L3 |
| 8 | Nernst OCV | $E = E°(T) + \frac{RT}{2F} \ln\frac{P_{H_2}\sqrt{P_{O_2}}}{P_{H_2O}}$ | L4 |
| 9 | Thermodynamic limit | $\eta_{max} = \Delta G / \Delta H \approx 83\%$ | L4 |
| 10 | Ventilation flow | $Q = (\dot{m}/\rho_{H_2}) / (C_{target}/100)$ | L5 |

---

## Quick Start

```python
from hydrogen import run_hydrogen_foundation, HydrogenClaimPayload

report = run_hydrogen_foundation()
print(f"Production eff: {report.production.efficiency:.1%}")
print(f"Storage RTE:    {report.storage.round_trip_efficiency:.1%}")
print(f"FC electric eff: {report.fuel_cell.efficiency_electric:.1%}")
print(f"Safety level:   {report.safety.risk_level}")
print(f"Health verdict: {report.health.verdict.value}")
print(f"  Ω_composite:  {report.health.composite_omega:.3f}")
```

---

## Tests

```
pytest tests/ -v
95 passed in 0.08s
```

---

## Current Limitations

- All equations are tree-level cartoons, not NIST-grade thermodynamics.
- Fuel cells: no polarisation-curve fitting; single operating-point evaluation.
- Safety: TNT-equivalent overpressure is screening-level only.
- Economics: LCOH is a simplified estimate; real projects need DCF models.
- Transport: pipeline blending and ammonia cracking not yet implemented.

---

*Hydrogen_Foundation v0.1.0 — a foundation layer for observing hydrogen production, storage, conversion, safety, and economics.*

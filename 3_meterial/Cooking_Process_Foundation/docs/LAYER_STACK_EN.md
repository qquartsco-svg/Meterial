# Cooking_Process_Foundation — layer stack (v0.1)

> **English.** Korean (정본): [LAYER_STACK.md](LAYER_STACK.md)

## L0 — Contracts

- `RecipeFlow`, `FlowStep`, `KitchenState`, `KitchenObservation` as in the Korean doc.

## L1 — Culinary skills (country / technique layers)

- `SkillRef(tradition, technique, variant)` — identifiers only in v0.1; later sub-kernels for viscosity, emulsion state, etc.

## L2 — Heat / browning proxy

- Toy physics for teaching; replace with calibrated equipment models in product use.

## L3 — Process executor

- `FlowEngine.tick(..., heat_cap_0_1=1, mission_pause=False)` integrates state and evaluates exit gates and branches.
- **L3.5 Arbiter (robot)**: SIK tick → `ArbiterVerdict` (`arbiter.py`); tag merge via `sik_ingress.py`.

## Upstack

- **L4**: `engine_ref` **`cooking.process.flow_tick`** — JSON round-trip via `recipe_serde`; bind `observation.kitchen_state` across nodes for multi-tick sessions.
- **Personal agent roadmap**: tool allow-lists can include stove / appliance APIs for real actuation.

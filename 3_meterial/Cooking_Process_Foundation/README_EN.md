# Cooking_Process_Foundation

> **English.** Korean (정본): [README.md](README.md)

**Not a recipe list app.** This draft package treats a recipe as a **process graph** driven by **state, time, and observation gates**—a small **dynamics program**.  
Culinary traditions (e.g. French, Japanese) stack as **`SkillRef` layers**; real heat, sensors, and vision enter via **`KitchenObservation`**.

---

## What this package does / does not do

### It does

- **Run the process graph**: walk `FlowStep`s inside `RecipeFlow`, update a simple **heat / browning proxy** each tick, and evaluate **exit rules** (time, temperature, browning, **metrology / motion gates**).  
- **Summarize safety for actuators**: combine optional SIK / explicit arbiter into **`pause_mission`**, **heat cap**, etc., and pack them into **`actuator_intent`** so the next layer (robot / relays) can enforce them mechanically.  
- **Stable entrypoint**: product code should prefer **`cooking_process_foundation.surface.run_process_tick`**; shapes are moving toward JSON Schema.

### It does not (by design)

- **Real motor / relay drivers** — no PWM, ROS, Modbus, vendor SDKs here. That belongs in [Cooking_Robot_Adapter](../Cooking_Robot_Adapter/README_EN.md) (or a product-specific package).  
- **Recipe databases, recommender UIs, nutrition** — out of scope (see Non-goals below).

### Relationship to **Cooking_Robot_Adapter**

| Concern | CPF (this folder) | Robot Adapter (sibling folder) |
|---------|-------------------|----------------------------------|
| Advance the process FSM | ✅ `FlowEngine` | ❌ |
| Decide heat ceiling, ESTOP, manipulator allow | ✅ builds `actuator_intent` | ❌ (consumes it) |
| Turn that into **hardware commands** | ❌ | ✅ |

CPF answers **what is allowed**; the adapter answers **how pins and buses implement it**.

### One tick (concept)

1. Host calls `run_process_tick` with `recipe_flow`, `kitchen_state`, `observation`, `dt_s` (L4 uses the same payload shape via `run_flow_tick_payload`).  
2. CPF runs `FlowEngine.tick`, optionally merges SIK / arbiter.  
3. Response includes **`actuator_intent`** → host or adapter passes that dict to **real actuators**.

---

## Suggested reading order

1. COOKing bundle root on GitHub [qquartsco-svg/COOKing](https://github.com/qquartsco-svg/COOKing) — `README_EN.md` (why two folders).  
2. This file (overview) → [docs/LAYER_STACK_EN.md](docs/LAYER_STACK_EN.md)  
3. Robot / SIK / Idea: [docs/ROBOT_SIK_IDEA_INTEGRATION_EN.md](docs/ROBOT_SIK_IDEA_INTEGRATION_EN.md)  
4. Precision / motion / emergence: [docs/PRECISION_MOTION_AND_EMERGENCE_PIPELINE_EN.md](docs/PRECISION_MOTION_AND_EMERGENCE_PIPELINE_EN.md)  
5. Commercial boundaries and **HAL `actuator_intent.v0.2`**: [COMMERCIAL_READINESS_EN.md](COMMERCIAL_READINESS_EN.md) (banner + footer lock schema revision).

---

## How it mobilizes existing 00_BRAIN / staging engines

| Asset | Role in this cooking layer |
|-------|----------------------------|
| **L4 (`design_workspace`)** | Process graph isomorphic to `engine_graph`; nodes = `FlowStep` / `SkillRef` (scenario JSON later). |
| **AOF** | Bridge `KitchenObservation` ↔ multimodal `ObservationFrame`. |
| **SIK** | Prioritize which channel to attend to next. |
| **Autonomy_Runtime_Stack** | Fuse temperatures / motion state (EKF-style). |
| **MemoryPhase / MAK** | Long-term user preference and past run outcomes. |
| **Battery / Zephyr / Air_Jordan** | Optional environment / oven thermal models. |
| **Fabless** | Metaphor only: process readiness gates, not silicon. |

## Layers

See [docs/LAYER_STACK_EN.md](docs/LAYER_STACK_EN.md). Robot / SIK / Idea: [docs/ROBOT_SIK_IDEA_INTEGRATION_EN.md](docs/ROBOT_SIK_IDEA_INTEGRATION_EN.md). **Pastry-grade precision, motion, emergence pipeline**: [docs/PRECISION_MOTION_AND_EMERGENCE_PIPELINE_EN.md](docs/PRECISION_MOTION_AND_EMERGENCE_PIPELINE_EN.md).

## Commercial integration (stable surface)

- **`cooking_process_foundation.surface`**: `run_process_tick`, `validate_process_tick_payload` — preferred for product hosts.
- **`aof_min`** is **L4-only** (`cooking.process.flow_tick`); rejected on `run_process_tick` to preserve layer boundaries.
- Checklist: [COMMERCIAL_READINESS_EN.md](COMMERCIAL_READINESS_EN.md) · payload schema [schemas/cooking.process.tick.payload.schema.json](schemas/cooking.process.tick.payload.schema.json) · **HAL** [schemas/actuator_intent.v0.2.schema.json](schemas/actuator_intent.v0.2.schema.json) · stub [../Cooking_Robot_Adapter/README_EN.md](../Cooking_Robot_Adapter/README_EN.md)

## L4 / JSON

- **`recipe_serde`**: dict ↔ `RecipeFlow`, `KitchenState`, `KitchenObservation`.
- **`engine_ref`**: `cooking.process.flow_tick` in `_staging/design_workspace` `l4_runner`.
- **Payload**: `recipe_flow`, `kitchen_state` (null = start at entry), `observation`, `dt_s`.
- **AOF**: if **`aof_min`** is set, the plain **`observation` field is replaced** by the AOF-derived kitchen observation. Optional **`cooking_observation_overlay`** merges temps/tags. Use `cooking_tag:branch_key` in channel `notes`.
- **SIK / arbiter (v0.3)**: `arbiter.py`, `sik_ingress.py` — optional `sik_stimuli` runs SIK (add `_staging/Sensory_Input_Kernel` to `PYTHONPATH`), merges tags into `KitchenObservation`, derives `ArbiterVerdict` unless **`arbiter`** is explicit. Payload keys: `arbiter`, `arbiter_config`, `merge_sik_tags`. See [docs/ROBOT_SIK_IDEA_INTEGRATION_EN.md](docs/ROBOT_SIK_IDEA_INTEGRATION_EN.md).
- **Examples**: single tick [design_workspace/examples/single_cooking_process_flow_tick_scenario.json](../design_workspace/examples/single_cooking_process_flow_tick_scenario.json) · **multi-tick chain** [design_workspace/examples/cooking_process_flow_tick_chained_scenario.json](../design_workspace/examples/cooking_process_flow_tick_chained_scenario.json) via `upstream_bindings` (L4 echoes `observation.recipe_flow` for `payload.recipe_flow` binding).

## Run tests

```bash
cd _staging/Cooking_Process_Foundation   # or this package root
python3 -m pytest tests/ -q
```

## Non-goals (v0.1)

Huge recipe databases, calorie recommenders, glamour photo generation, fine-grained food chemistry.

## Version

`0.4.1` — `VERSION`, `pyproject.toml`, and `cooking_process_foundation.__version__` aligned.

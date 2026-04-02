# Precision process · motion · experience → emergence (design alignment)

> **English.** Korean (정본): [PRECISION_MOTION_AND_EMERGENCE_PIPELINE.md](PRECISION_MOTION_AND_EMERGENCE_PIPELINE.md)

## 1. Is your described flow correct?

**Yes**, in one line:

1. **Recipe in** → **dynamics** (time, state, gates) runs toward **cooking outcomes**.  
2. Repetition and logs become **skill / habit** (per robot or user).  
3. Persistent **stimuli and data** feed low-latency loops (SIK) and slow loops (**ideation** via e.g. ionia.idea).

**“Zero error”** in product language must mean **tolerances, verification, and audit**—not a literal promise without metrology.

## 2. Pastry-chef-grade dosing and operations

| Aspect | Meaning | Current CPF | Next contract (recommended) |
|--------|---------|-------------|-----------------------------|
| Recipe logic | Order, time, temp, browning gates | ✅ `RecipeFlow` / `FlowEngine` | Per-step **target mass / volume / viscosity proxy** |
| Metrology | g, ml, °C with uncertainty σ | ⚠️ heat/browning **proxies** | **`MetrologyStep`** or step `extras` + scale/flowmeter adapters |
| Error-free run | Branch on fail, retry, scrap | ⚠️ gates exist; **dosing pass/fail** TBD | `next_on_branch` + thresholds + **audit log** |

Keep **precision metrology** as a **sibling layer**, not crammed inside the same module as generic flow physics.

## 3. Robot, trajectory checks, “autonomous driving–like” motion

A recipe alone does **not** define joint trajectories or AMR paths. Split roles:

| Layer | Role | 00_BRAIN candidates |
|-------|------|---------------------|
| Cooking process | *What* and *when* (intent) | CPF + `ActuatorIntent` |
| Manipulator motion | Workspace, collision-free paths | Dedicated motion stack or autonomy bridge |
| Mobility | Obstacles, route, speed | `Autonomy_Runtime_Stack`, `Vehicle_Platform_Foundation`, `4WD`, TAM, … |
| Fusion | Pause / ESTOP / permit | **`Arbiter`** + future **`motion_ok`** gate |

**Recipe → dynamics** = **process state machine**. **Trajectory check** = **geometry / constraint checker** running **in parallel**, both green before actuation.

## 4. Experience → habit → information → stimulus → ideas

See [ROBOT_SIK_IDEA_INTEGRATION_EN.md](ROBOT_SIK_IDEA_INTEGRATION_EN.md) and [INTELLIGENCE_AND_PERSONAL_AGENT_ROADMAP_EN.md](../../design_workspace/INTELLIGENCE_AND_PERSONAL_AGENT_ROADMAP_EN.md).

## 5. One-line verdict

- The **narrative** (recipe → dynamics → outcome → skill → stimuli → ideas) **matches** the intended architecture.  
- **Pastry-grade precision** needs an explicit **metrology + calibration** layer **above** raw flow proxies.  
- **Motion / AMR** belongs in a **separate stack**, merged via **gates** with CPF—not inside the recipe graph alone.

---

**Implemented (CPF 0.4.0)**: `FlowStep` targets/tolerances and `require_motion_ok`; `KitchenObservation` `reported_mass_g` / `reported_volume_ml` / `motion_ok`; gates in `FlowEngine.tick` before branch/success exit; `ActuatorIntent` v0.2 — see `CHANGELOG`.  
**0.4.1**: AOF `cooking_observation_overlay` reads the same fields; `next_on_branch["metrology_fail"]` exits to a dedicated step when all required reports are present but out of tolerance.

*v0.1 — design alignment.*

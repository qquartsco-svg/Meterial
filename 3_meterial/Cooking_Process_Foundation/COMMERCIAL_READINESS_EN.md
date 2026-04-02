# Cooking_Process_Foundation — commercial boundaries & readiness

> **English.** Korean (정본): [COMMERCIAL_READINESS.md](COMMERCIAL_READINESS.md)  
> **Document revision:** aligned with CPF **0.4.x** and HAL **`actuator_intent.v0.2`**. The file `schemas/actuator_intent.v0.1.schema.json` is **legacy / reference**; new integrations should use **v0.2**.

## 1. Keep layers straight

| Layer | Responsibility | Do **not** put inside this package |
|-------|----------------|-------------------------------------|
| **L1 domain** | Cooking **process dynamics & contracts** | Robot SDKs, cloud APIs, product UI |
| **L4 orchestration** | Scenarios, nodes, `upstream_bindings` | Guarantee of internal physics fidelity |
| **Integration / commercial** | Hardware, certification, ops | Duplicating Fabless/AOF core logic |

**Stable public surface**: `cooking_process_foundation.surface` — `run_process_tick`, `validate_process_tick_payload`.  
Direct imports of internal modules may change on **major** bumps.

**HAL intent**: every tick includes **`actuator_intent`** (`actuator_intent.v0.2`) — heat ceiling, pause, ESTOP recommendation, manipulator allow, plus (v0.2) metrology/motion gate fields.  
Map to hardware only in **`Cooking_Robot_Adapter`** (or a vendor-specific package).

**L4 / AOF**: `cooking_observation_overlay` may pass `reported_mass_g`, `reported_volume_ml`, `motion_ok`; `kitchen_observation_from_aof` maps them into `KitchenObservation`. Metrology steps can wire `next_on_branch["metrology_fail"]` for out-of-tolerance rework (`CHANGELOG` 0.4.1).

## 2. What we warrant vs not

**Warranted (tests + schema)**  
- Deterministic single-tick behavior for a validated `recipe_flow` at a pinned version.  
- Pre-flight validation via `validate_process_tick_payload`.  
- Arbiter / optional SIK path for **pause / heat cap** hooks.

**Not warranted (integrator)**  
- Food-safety certification, liability for burns/fire.  
- Real sensor/actuator closed-loop accuracy.  
- SLA for optional stacks (SIK, ionia, memory).

## 3. Commercial checklist

1. Pin **version** (`VERSION`, `pyproject.toml`, `__version__`).  
2. **CI**: `pytest` + optional `verify_staging_stacks.sh` including this package.  
3. **Payload gate**: JSON Schema and/or `validate_process_tick_payload`.  
4. **Robots**: keep **arbiter** on; duplicate ESTOP in the host.  
5. **Logging**: persist `kitchen_state`, `arbiter_verdict`, `step_outcome`.

## 4. Next steps toward product

1. Host app calls **`run_process_tick` only**.  
2. Wire JSON Schema into OpenAPI/CI.  
3. Put motor drivers in a **separate adapter package**; CPF already emits **`actuator_intent` v0.2** (`ActuatorIntent` contract) each tick.  
4. Add LAW/audit via **L4 nodes**, not by inlining policy into CPF.

## 5. References

- Process overview / layers: [README_EN.md](README_EN.md) · Robot / SIK: [ROBOT_SIK_IDEA_INTEGRATION_EN.md](docs/ROBOT_SIK_IDEA_INTEGRATION_EN.md)  
- Full L1/L4 stack: [DESIGN_SYSTEM_LAYER_STACK_EN.md](../DESIGN_SYSTEM_LAYER_STACK_EN.md).

---

*Integration guide — HAL `actuator_intent.v0.2` baseline. Not legal or safety advice.*

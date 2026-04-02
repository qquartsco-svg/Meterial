# Cooking process × robot control × SIK (sixth sense) × Idea engine — integration analysis (v0.1)

> **English.** Korean (정본): [ROBOT_SIK_IDEA_INTEGRATION.md](ROBOT_SIK_IDEA_INTEGRATION.md)

## 1. Requirements (aligned)

1. The cooking stack is **primarily for real robot execution**, not recipe recommendation.
2. **Default mode**: a recipe (process graph) drives **dynamics and gates** for correct mission execution.
3. **Skill formation**: repeated, calibrated runs become **embodied skill** (parameters, tolerances, exceptions).
4. **Senses**: robot inputs map to **five channels + sixth sense** — in-repo this aligns with **SIK** (salience → reflex → `FeltSenseState` → action handoff).
5. **Ideation**: novel stimuli and failures can feed **ionia.idea** (`IdeaPool` / `IdeaEngine`) on a **slower cognitive path**.

This note separates **feasible now**, **feasible with adapters**, and **not implemented yet**.

## 2. Existing assets

| Layer | Location | Relation to cooking / robot |
|-------|----------|------------------------------|
| Process dynamics | `_staging/Cooking_Process_Foundation` | Mission graph + tick; observations are open to sensor dicts. |
| Senses / reflex / sixth sense | `_staging/Sensory_Input_Kernel` | Low-latency stimulus–response; outputs are structured dicts, not motor drivers. |
| Idea / emergence | `03_DISCIPLINES/ionia/idea` | Slower loop; orbit / candidate shapes from state and insights. |
| Memory | MemoryPhase_Kernel, MAK docs | Long-term skill and preference storage (to be wired). |

## 3. Two time scales (required)

- **Mission loop** (recipe-bound): `FlowEngine` / L4 ticks; actuator commands within safety envelopes.
- **Reflex loop** (SIK): faster attention / reflex / `gut_risk`.

An **arbiter** must resolve conflicts (e.g. reflex ESTOP vs “next recipe step”). Setup is **possible**; **policy** is mandatory.

## 4. Mapping SIK → cooking / robot

- Map channels into `KitchenObservation` or `extras`, or drive **arbiter** and **sensor priority** from salience.
- Do **not** hide safety inside `tick()` only; keep reflex → arbiter → actuators explicit.

## 5. Skills

Architecturally **yes** via structured logs + MemoryPhase; **not yet** in CPF as auto skill promotion (needs calibration + human gate).

## 6. Idea engine

Connect **after** sessions or with human approval; avoid putting `IdeaEngine.step` inside the millisecond motor loop.

## 7. Verdict

| Question | Answer |
|----------|--------|
| Wire SIK for stimulus–response? | **Yes**, with adapters + arbiter + robot SDK. |
| Recipe-accurate dynamics mission? | **CPF is still proxy-level**; production needs real sensing and actuation. |
| Skills from repetition? | **Possible** with logging and memory pipelines (to build). |
| Single pipeline with ideation? | **One conceptual pipeline**, **two time scales** in implementation. |

## 8. Suggested build order

1. Dual ingress: same timestamp → SIK + `KitchenObservation`.
2. Arbiter v0 (**shipped in v0.3**): `arbiter.py` / `sik_ingress.py`; L4 payload `sik_stimuli` or explicit `arbiter`; `FlowEngine.tick` supports `mission_pause` and `heat_cap_0_1`.
3. Session log schema.
4. Optional ionia bridge: summarized insight queue → approved `IdeaPool.add`.

## 9. References

- [Sensory_Input_Kernel README](../../Sensory_Input_Kernel/README_EN.md)
- [ionia README](../../../03_DISCIPLINES/ionia/README.md)
- [Cooking README](../README_EN.md)
- [INTELLIGENCE_AND_PERSONAL_AGENT_ROADMAP](../../design_workspace/INTELLIGENCE_AND_PERSONAL_AGENT_ROADMAP_EN.md)

---

*v0.1 — design analysis.*

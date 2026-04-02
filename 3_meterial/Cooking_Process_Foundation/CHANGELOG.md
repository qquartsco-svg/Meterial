# Changelog

## 0.4.1

- **`aof_bridge.kitchen_observation_from_aof`**: overlay에 `reported_mass_g`, `reported_volume_ml`, `motion_ok` 흡수.
- **`gates`**: `METROLOGY_FAIL_BRANCH_KEY` (`"metrology_fail"`), `metrology_reports_complete`, `metrology_failure_branch_eligible`.
- **`FlowEngine.tick`**: `next_on_branch["metrology_fail"]` 가 있고 측정은 끝났으나 허용오차 실패일 때 해당 스텝으로 이탈 (`branch:metrology_fail`); 모션 게이트 통과 시에만.

## 0.4.0

- **`FlowStep`**: `target_mass_g` / `mass_tolerance_g`, `target_volume_ml` / `volume_tolerance_ml`, `require_motion_ok`.
- **`KitchenObservation`**: `reported_mass_g`, `reported_volume_ml`, `motion_ok`.
- **`gates`**: `metrology_gates_satisfied`, `motion_gate_satisfied`, `metrology_targets_active` — used by `FlowEngine.tick` (success and branch exits) and actuator intent.
- **`ActuatorIntent` v0.2**: `require_motion_ok`, `metrology_targets_active`, `metrology_satisfied`; `allow_manipulator_motion` false when mission paused or motion gate not satisfied; `build_actuator_intent_from_runtime(..., obs=...)`.
- 스키마: `schemas/actuator_intent.v0.2.schema.json` (v0.1 유지).

## 0.3.2

- **`ActuatorIntent`** (`actuator_intent.py`): HAL용 JSON 계약 `actuator_intent.v0.1`; 틱 결과에 **`actuator_intent`**, **`mission_meta`** 포함.
- 스키마: `schemas/actuator_intent.v0.1.schema.json`.
- **`Cooking_Robot_Adapter`** (`_staging/Cooking_Robot_Adapter/`): 스텁 드라이버·테스트 — 벤더 SDK는 여기만 확장.

## 0.3.1

- **`surface`**: `run_process_tick`, `validate_process_tick_payload` (integrator-stable API).
- **`VERSION`** file; **COMMERCIAL_READINESS** (KO/EN); JSON Schema draft under `schemas/`.
- **`aof_min` / `cooking_observation_overlay`** rejected on `surface` — L4-only (layer separation).
- `_staging/scripts/verify_staging_stacks.sh` includes this package.

## 0.3.0

- **`arbiter`**: `ArbiterVerdict`, `arbiter_from_sik_tick_result`, explicit dict via `arbiter_verdict_from_dict`, `arbiter_config_from_payload`.
- **`sik_ingress`**: optional SIK import, `run_sik_process_tick`, `merge_kitchen_observation_with_sik`, `stimuli_from_dicts`.
- **`FlowEngine.tick`**: `heat_cap_0_1`, `mission_pause` (SIK / safety arbitration).
- **`run_flow_tick_payload`**: `arbiter`, `arbiter_config`, `sik_stimuli`, `merge_sik_tags`; returns `arbiter_verdict`, optional `sik_gut_risk` / `sik_reflex_triggered`.
- L4 `cooking.process.flow_tick` submetrics: `arbiter_pause`, `heat_cap_0_1`.

## 0.2.0

- `recipe_serde`: JSON ↔ `RecipeFlow`, `KitchenState`, `KitchenObservation`.
- `aof_bridge`: `kitchen_observation_from_aof`, `observation_frame_from_aof_min`, `cooking_tag:` notes convention.
- `l4_payload.run_flow_tick_payload` for `cooking.process.flow_tick` in `design_workspace` L4 runner.
- L4 engines: optional `payload.aof_min` + `cooking_observation_overlay` to build observation from AOF.

## 0.1.0

- Initial package: `RecipeFlow`, `FlowEngine`, heat/browning proxy, tests.
- README / layer docs (KO+EN).

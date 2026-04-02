# Cooking_Process_Foundation — 레이어 스택 (v0.1)

> **한국어 (정본).** English: [LAYER_STACK_EN.md](LAYER_STACK_EN.md)

## L0 — 계약

- `RecipeFlow`: 공정 그래프 정본 (`entry_step_id` + `FlowStep` 집합).
- `FlowStep`: 스킬, 최소 시간, 표면 온도·갈변 게이트, 성공 시 다음 스텝, `next_on_branch` 로 관측 태그 분기.
- `KitchenState`: 엔진이 소유하는 **가변** 상태.
- `KitchenObservation`: 틱마다 들어오는 외부 정보 (나중에 AOF로 매핑).

## L1 — 요리 스킬 (국가·기법 레이어)

- `SkillRef(tradition, technique, variant)`  
  예: `("fr","sauce","bechamel")`, `("jp","dashi","primary")`, `("mx","mole","seed_toast")`  
- v0.1 에서는 **ID만**; 향후 각 기법별 전제조건(점도, pH 프록시, 유화 상태)을 서브커널로 확장.

## L2 — 열·갈변 프록시

- `physics_proxy.integrate_heat`: 1차 열 관성 + 단순 멜라드 누적 (교육·데모용).
- 실제 제품에서는 캘리브레이션·장비별 모델로 교체.

## L3 — 공정 실행기

- `FlowEngine.tick(obs, dt, *, heat_cap_0_1=1, mission_pause=False)`: (1) 스킬 목표에 맞춘 열 입력 프록시 (2) 상태 적분 (3) 이탈 조건 (4) 분기 또는 `next_on_success`.
- **L3.5 아비터 (로봇)**: SIK 틱 결과 → `ArbiterVerdict` (`arbiter.py`) → 일시정지·화력 상한; `sik_ingress.py`로 관측 태그 병합.

## 상위 통합

- **L4**: `engine_ref` **`cooking.process.flow_tick`** — `recipe_serde` 로 `RecipeFlow`·`KitchenState` JSON 왕복; 노드 출력의 `observation.kitchen_state` 를 다음 틱 입력으로 바인딩하면 다틱 세션 구성.
- **개인 에이전트 로드맵**: `UserProfile` 의 도구 허용에 “화구 제어 API” 등을 넣으면 **실행** 층과 연결.

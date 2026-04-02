# Cooking_Process_Foundation

> **한국어 (정본).** English: [README_EN.md](README_EN.md)

**레시피 문장을 나열하는 앱이 아니다.** 레시피를 **상태·시간·관측 조건**으로 풀어 **동역학 프로그램**(공정 그래프)으로 돌리는 초안 패키지다.  
프랑스·일본 등 **요리 전통(tradition) + 기법(technique)** 은 `SkillRef` 레이어로 쌓고, 실제 화구·센서·비전은 `KitchenObservation` 으로 주입한다.

---

## 이 패키지가 하는 일 / 하지 않는 일

### 하는 일

- **공정 그래프 실행**: `RecipeFlow` 안의 `FlowStep`들을 시간 순으로 밟으며, 매 틱마다 **열·멜라드(가짜 물리)** 를 갱신하고, **이탈 조건**(시간, 온도, 멜라드, **계량·모션 게이트**)을 검사한다.  
- **안전·권한 요약**: 아비터(SIK·명시 페이로드)로 **미션 일시정지**, **화력 상한** 등을 정하고, 그 결과를 **`actuator_intent`** JSON에 넣어 **다음 층(로봇/릴레이)** 이 지키기 쉽게 한다.  
- **표준 입구**: 호스트 앱은 가급적 **`cooking_process_foundation.surface.run_process_tick`** 만 부른다. 입력·출력 형식은 JSON 스키마로 고정하는 방향이다.

### 하지 않는 일 (의도적)

- **실제 모터·릴레이 제어 코드** — PWM, ROS, Modbus, 벤더 SDK 등은 **넣지 않는다**. 그건 [Cooking_Robot_Adapter](../Cooking_Robot_Adapter/README.md) (또는 제품 전용 패키지)의 역할이다.  
- **레시피 DB·추천 UI·영양 분석** — 비목표(아래 “비목표” 참고).

### Cooking_Robot_Adapter 와의 관계 (정확히)

| 항목 | CPF (이 폴더) | Robot Adapter (옆 폴더) |
|------|----------------|---------------------------|
| 공정이 다음 스텝으로 넘어갈지 | ✅ `FlowEngine` | ❌ |
| 열 상한·ESTOP·조작기 허용 **판단** | ✅ `actuator_intent` 생성 | ❌ (받기만 함) |
| 그 판단을 **하드웨어 명령**으로 변환 | ❌ | ✅ |

즉, CPF는 **“무엇이 허용되는가”** 까지이고, 어댑터는 **“허용 범위 안에서 실제로 핀을 어떻게 움직일까”** 다.

### 한 틱의 흐름 (개념)

1. 호스트가 `recipe_flow`, `kitchen_state`, `observation`, `dt_s` 등을 넣어 `run_process_tick` (또는 L4가 같은 페이로드로 `run_flow_tick_payload`) 호출.  
2. CPF가 `FlowEngine.tick` 으로 상태를 갱신하고, 필요 시 SIK·아비터를 합성.  
3. 응답에 **`actuator_intent`** 가 포함된다 → 호스트 또는 어댑터가 이 dict를 읽어 **실제 구동기**에 전달.

---

## 처음 읽을 때 순서 (추천)

1. **COOKing** 공개 번들 루트 설명 — GitHub [qquartsco-svg/COOKing](https://github.com/qquartsco-svg/COOKing) 의 `README.md` (왜 폴더가 둘인지).  
2. 본 문서(개요) → [docs/LAYER_STACK.md](docs/LAYER_STACK.md)  
3. 로봇·SIK·이데아: [docs/ROBOT_SIK_IDEA_INTEGRATION.md](docs/ROBOT_SIK_IDEA_INTEGRATION.md)  
4. 계량·동선·창발 정렬: [docs/PRECISION_MOTION_AND_EMERGENCE_PIPELINE.md](docs/PRECISION_MOTION_AND_EMERGENCE_PIPELINE.md)  
5. 상용 책임·**HAL `actuator_intent.v0.2` 명시**: [COMMERCIAL_READINESS.md](COMMERCIAL_READINESS.md) (문서 상단 배너와 각주로 스키마 버전 정렬).

---

## 00_BRAIN / 기존 엔진과의 연결 (동원 맵)

| 자산 | 이 쿠킹 층에서의 역할 |
|------|------------------------|
| **L4 (`design_workspace`)** | 레시피 공정 = `engine_graph` 와 동형. 노드 = `FlowStep` / `SkillRef` 호출; 시나리오 JSON으로 재현 가능하게 확장 예정. |
| **AOF** | `KitchenObservation` ↔ `ObservationFrame` 다채널(온도·비전·사람 확인) 브리지. |
| **SIK** | 다채널 신호에서 **다음 관측** 우선순위 (어떤 센서를 볼지). |
| **Autonomy_Runtime_Stack** | 연속 상태 추정(EKF 등)으로 **온도·교반 상태** 융합. |
| **MemoryPhase / MAK** | 사용자 취향·과거 성공 공정 **장기 기억**. |
| **Battery / Zephyr / Air_Jordan** | 직접 필수는 아님; **오븐·환경 열** 확장 시 환경 모델에 연결 가능. |
| **Fabless** | 비유: 공정 단계·게이트 — 칩이 아니라 **조리 공정 준비도** 메타포로만 참조 가능. |

## 레이어 (개념)

상세: [docs/LAYER_STACK.md](docs/LAYER_STACK.md) · 로봇·SIK·이데아: [docs/ROBOT_SIK_IDEA_INTEGRATION.md](docs/ROBOT_SIK_IDEA_INTEGRATION.md) · **제과 급 정밀·동선·창발 흐름 정렬**: [docs/PRECISION_MOTION_AND_EMERGENCE_PIPELINE.md](docs/PRECISION_MOTION_AND_EMERGENCE_PIPELINE.md)

- **L0** — 계약: `RecipeFlow`, `FlowStep`, `KitchenState`, `KitchenObservation`
- **L1** — 기법 커널: `SkillRef` (국가·기법·변형); 향후 소스·에멀션·글라스 등 서브커널
- **L2** — 물리 프록시: `physics_proxy` (1차 열·멜라드 흉내; 화학 정밀도는 비목표)
- **L3** — 공정 엔진: `FlowEngine.tick` — 매 틱 물리 갱신 → 이탈 조건 → 다음 스텝

## 상용 통합 (안정 표면)

- **`cooking_process_foundation.surface`**: `run_process_tick` / `validate_process_tick_payload` — 제품·로봇 호스트는 **이 진입점 우선** (내부 모듈은 메이저에서 바뀔 수 있음).
- **`aof_min`** 은 **L4** `cooking.process.flow_tick` 전용; `run_process_tick` 에 넣으면 **검증 실패**(레이어 분리).
- 절차·책임 분리: [COMMERCIAL_READINESS.md](COMMERCIAL_READINESS.md) · 페이로드 스키마 [schemas/cooking.process.tick.payload.schema.json](schemas/cooking.process.tick.payload.schema.json) · **`actuator_intent`** [schemas/actuator_intent.v0.2.schema.json](schemas/actuator_intent.v0.2.schema.json) · HAL 스텁 [../Cooking_Robot_Adapter/README.md](../Cooking_Robot_Adapter/README.md)

## L4 / JSON 직렬화

- **`recipe_serde`**: `recipe_flow_from_dict` / `recipe_flow_to_dict`, `kitchen_state_*`, `kitchen_observation_*`.
- **`engine_ref`**: `cooking.process.flow_tick` — `_staging/design_workspace` 의 `l4_runner` 에 등록됨.
- **페이로드**: `recipe_flow`, `kitchen_state`(null 이면 엔트리 스텝에서 시작), `observation`, `dt_s`.
- **AOF 연동**: L4 페이로드에 **`aof_min`** 이 있으면 **`observation` 필드는 대체됨**(AOF→주방 관측 합성). `aof_min` 은 축약 프레임(`case_id`, `raw_channels[]`, `duration_s`, `signal_intensity`); 선택 **`cooking_observation_overlay`** 로 온도·태그 덧씌움. 채널 `notes` 에 `cooking_tag:분기키`.
- **SIK·아비터 (v0.3)**: `arbiter.py` — 반사/식스센스 요약 → `pause_mission`·`heat_cap_0_1`. `sik_ingress.py` — `sik_stimuli[]` 로 SIK 틱( `PYTHONPATH`에 `_staging/Sensory_Input_Kernel` )·`KitchenObservation.tags` 병합. L4 페이로드: **`arbiter`**(명시), **`sik_stimuli`**(자동 아비터), **`arbiter_config`**(임계값), **`merge_sik_tags`**. 상세: [docs/ROBOT_SIK_IDEA_INTEGRATION.md](docs/ROBOT_SIK_IDEA_INTEGRATION.md).
- **예시**: 단일 틱 [design_workspace/examples/single_cooking_process_flow_tick_scenario.json](../design_workspace/examples/single_cooking_process_flow_tick_scenario.json) · **`upstream_bindings` 다틱 체인** [design_workspace/examples/cooking_process_flow_tick_chained_scenario.json](../design_workspace/examples/cooking_process_flow_tick_chained_scenario.json) (`payload.kitchen_state` ← `observation.kitchen_state`, `payload.recipe_flow` ← `observation.recipe_flow`; L4가 노드 출력에 **`observation.recipe_flow` 에코**)

## 실행

```bash
cd _staging/Cooking_Process_Foundation   # 또는 본 패키지 루트
python3 -m pytest tests/ -q
```

## 비목표 (v0.1)

- 만 개 레시피 DB, 칼로리 추천, 인스타용 사진 생성.
- 미슐랭급 화학 시뮬레이션.

## 버전

`0.4.1` — `VERSION` · `pyproject.toml` · `cooking_process_foundation.__version__` 과 맞춤.

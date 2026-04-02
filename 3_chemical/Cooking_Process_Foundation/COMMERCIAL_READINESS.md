# Cooking_Process_Foundation — 상용화 경계·준비도

> **한국어 (정본).** English: [COMMERCIAL_READINESS_EN.md](COMMERCIAL_READINESS_EN.md)  
> **문서 개정:** 상용 가이드 본문은 CPF **0.4.x** 및 HAL **`actuator_intent.v0.2`** 에 맞춤. 저장소의 `schemas/actuator_intent.v0.1.schema.json` 은 **이력·호환 참고용**이며, 신규 통합은 **v0.2** 를 사용한다.

## 1. 레이어가 꼬이지 않게 (필수)

| 층 | 책임 | 이 패키지 안에 넣지 말 것 |
|----|------|---------------------------|
| **L1 도메인** | 조리 **공정 동역학·계약** (`RecipeFlow`, `FlowEngine`, arbiter, SIK 어댑터) | 로봇 SDK, 클라우드 API, UI |
| **L4 오케스트레이션** | 시나리오·노드·`upstream_bindings` | 엔진 내부 물리 정밀도 보장 |
| **통합·상용** | 하드웨어·인증·배포·모니터링 | Fabless/AOF 본체 로직 복제 |

**공개 안정 표면**: `cooking_process_foundation.surface` — `run_process_tick`, `validate_process_tick_payload`.  
내부 모듈 직접 import는 **메이저 버전**에서 바뀔 수 있다.

**구동 의도(HAL)**: 매 틱 **`actuator_intent`** (스키마 `actuator_intent.v0.2`) — 열 상한·일시정지·ESTOP 권고·조작기 허용·(v0.2) 계량·모션 게이트 플래그.  
실제 릴레이/서보는 **`Cooking_Robot_Adapter`**(또는 벤더 패키지)에서만 매핑.

**L4·AOF**: `cooking_observation_overlay`에 `reported_mass_g` / `reported_volume_ml` / `motion_ok` 전달 시 `kitchen_observation_from_aof`가 동일 필드로 흡수. 계량 목표 스텝은 `next_on_branch["metrology_fail"]`로 허용오차 실패 시 재작업 스텝 연결 가능(`CHANGELOG` 0.4.1).

## 2. 이 패키지가 보장하는 것 / 보장하지 않는 것

**보장 (테스트·스키마로 고정)**  
- JSON `recipe_flow` → `FlowEngine` 한 틱의 **결정적** 동작(동일 입력·동일 버전).  
- `validate_process_tick_payload` 로 **배포 전 계약 검증**.  
- `arbiter` / `sik_stimuli` 경로의 **안전 상한(일시정지·화력 캡)** 훅.

**보장하지 않음 (통합사 책임)**  
- 식품 안전 인증(HACCP 등), 화상·화재 법적 책임.  
- 실제 온도·토크 센서 정확도, 액추에이터 폐루프.  
- SIK/이데아/메모리 엔진의 **운영 SLA** — 옵션 의존성으로만 연결.

## 3. 상용 배포 체크리스트

1. **버전 고정**: `VERSION` / `pyproject.toml` / `cooking_process_foundation.__version__` 일치 유지.  
2. **CI**: `python3 -m pytest tests/ -q` + (선택) `_staging/scripts/verify_staging_stacks.sh` 에 본 패키지 포함.  
3. **페이로드**: `schemas/cooking.process.tick.payload.schema.json` 으로 게이트 또는 `validate_process_tick_payload` 호출.  
4. **로봇**: 반드시 **아비터** 켜기 — 명시 `arbiter` 또는 `sik_stimuli`; ESTOP은 호스트에서도 이중화.  
5. **로그**: `kitchen_state`, `arbiter_verdict`, `step_outcome` 영구 저장(감사·재현).

## 4. 다음 상용 단계 (권장 순)

1. 호스트 앱에서 **`run_process_tick`만** 호출하도록 래핑.  
2. JSON Schema를 OpenAPI/CI에 연결.  
3. 로봇 드라이버는 **별도 패키지** `*_robot_adapter`(제안) — CPF는 매 틱 **`actuator_intent` v0.2** (`ActuatorIntent` 계약)만 출력하면 된다.  
4. 율법·감사(L2) 필요 시 L4 시나리오에 노드 추가 — **CPF 코드에 LAW 삽입 금지**.

## 5. 참고

- 공정 엔진 개요·레이어: [README.md](README.md) · 로봇·SIK: [docs/ROBOT_SIK_IDEA_INTEGRATION.md](docs/ROBOT_SIK_IDEA_INTEGRATION.md)  
- L1/L4 전체 설계 스택: [DESIGN_SYSTEM_LAYER_STACK.md](../DESIGN_SYSTEM_LAYER_STACK.md).

---

*상용 통합 가이드 — HAL `actuator_intent.v0.2` 기준. 법적·안전 조언 아님.*

# 쿠킹 공정 × 로봇 제어 × SIK(식스센스) × 이데아 — 연결 분석 (v0.1)

> **한국어 (정본).** English: [ROBOT_SIK_IDEA_INTEGRATION_EN.md](ROBOT_SIK_IDEA_INTEGRATION_EN.md)

## 1. 요구 이해 (정렬)

아래를 **전제**로 분석한다.

1. **쿠킹 시스템의 1차 목적**은 레시피 추천이 아니라 **실제 로봇이 조리 임무를 수행**하는 쪽에 가깝다.
2. **기본 모드**: 레시피(공정 그래프)가 들어오면 **동역학·게이트**에 따라 **정확한 임무 수행**이 우선이다.
3. **축적**: 같은 공정이 반복·교정되면 **개체(로봇/사용자)의 스킬**로 굳어 간다(파라미터·성공 분포·예외 처리).
4. **감각**: **로봇 입력 채널 = 오감 + 여섯 번째 감(식스센스)** — 여기서는 코드베이스의 **SIK**가 “5채널 → salience/reflex → `FeltSenseState`(sixth sense) → 액션 브리지”로 구현된 층에 대응한다.
5. **창발**: 새 자극·실패·통찰이 **이데아 엔진(`ionia.idea`의 IdeaPool / IdeaEngine 등)** 과 연결될 수 있는 **상위 인지 경로**가 있어야 한다.

이 문서는 **“지금 당장 다 연결됐다”가 아니라**, **셋업 가능한지(가능/조건부/부족)** 를 나눈다.

---

## 2. 현재 코드 자산 (사실)

| 층 | 위치(대표) | 쿠킹/로봇과의 관계 |
|----|------------|---------------------|
| **공정 동역학** | `_staging/Cooking_Process_Foundation` — `FlowEngine`, `KitchenObservation`, L4 `cooking.process.flow_tick` | **임무 그래프 + 틱**; 관측은 구조적으로 “센서 dict”에 열려 있음. |
| **감각·반사·식스센스** | `_staging/Sensory_Input_Kernel` — `SensoryInputKernel`, salience, `decide_reflex`, `infer_felt_sense`, `build_action_input` | **저지연 자극–반응** 후보; 출력은 dict/`ReflexDecision` 수준(로봇 API 직결은 별도). |
| **이데아·창발** | `03_DISCIPLINES/ionia/idea` — `IdeaPool`, `IdeaEngine`, 브리지 문서 | **느린 축**; insight/state를 넣으면 궤도·후보 형상 갱신(실시간 제어 루프와 분리하는 것이 안전). |
| **메모리·페이즈** | MemoryPhase_Kernel, MAK 설계 등 | 스킬·선호·실패 로그 **장기 저장** 후보. |

---

## 3. 두 개의 시간 축 (필수 설계)

로봇 조리에서는 **한 루프로 못 합친다**가 정상이다.

### A. 임무 루프 (deliberative / recipe-bound)

- **주기**: 수 Hz ~ 수십 Hz 틱(시뮬·상태기계).
- **역할**: `RecipeFlow` 단계, 온도·갈변 게이트, 다음 스텝.
- **입력**: 프로브·비전·토크(요리 특화) → `KitchenObservation` / L4 페이로드.
- **출력**: **허용된 액추에이터 명령**(화력, 교반, 이동) — 안전 상한 내.

### B. 반사 루프 (reflex / SIK)

- **주기**: 더 짧게 가져가고 싶은 축(카메라/접촉/소리 스파이크).
- **역할**: `startle_or_evade`, `orient_attention`, `FeltSenseState`(gut_risk 등).
- **출력**: `build_action_input` 수준의 **트리거·주의·저우선 액션 힌트**.

**중재(arbiter)** 가 없으면 “레시피대로”와 “지금 당장 손 떼”가 충돌한다.  
→ **셋업 가능**하지만, **정책 모듈**(위험 시 임무 일시정지·감속·ESTOP)이 **반드시** 필요하다.

---

## 4. SIK → 쿠킹/로봇으로의 매핑 (가능한 연결)

| SIK 측 (개념) | 쿠킹/로봇 측에 넣는 방법 |
|----------------|-------------------------|
| vision/hearing/touch/… intensity | **동일 물리량이면** `KitchenObservation` 필드 확장 또는 `extras`에 넣고 `FlowEngine`/게이트에서 읽기. |
| salience / novelty | **다음에 볼 채널** 우선순위(어떤 카메라·프로브를 믿을지). |
| reflex `triggered` | **임무 일시정지**, 화력 컷, 그리퍼 오픈 등 **하드 게이트**(arbiter). |
| `FeltSenseState.gut_risk` 높음 | **사람 개입 요청** 또는 **안전 서브루틴** (이데아와 직접 연결하기보다 먼저 안전). |
| `build_action_input` | **로봇 SDK 어댑터**로 매핑(속도·관절·그리퍼는 도메인별). |

**즉시 행동 반영**은 가능하다. 다만 그 경로는 **`FlowEngine.tick` 안에 직접 넣기보다**, **(1) SIK 틱 → arbiter → 액추에이터** 와 **(2) 조리 틱 → 허용 범위 내 명령**을 **명시적으로 합성**하는 형태가 유지보수에 유리하다.

---

## 5. 레시피 임무 → 스킬 축적 (가능 조건)

- **가능**: 실행 로그(단계별 온도 곡선, 성공/실패, 사람 수정)를 **구조화 저장**하면, 다음엔 동일 `SkillRef`에 **초기 파라미터·허용 오차**를 덧씌우는 식으로 “스킬”화할 수 있다.
- **아직 CPF에 없음**: 자동 스킬 라이브러리 업데이트, 개인별 보정 루프 — **MemoryPhase / MAK / 에이전트 로드맵**과 합쳐야 완성.
- **주의**: “스킬”을 **안전 검증 없이** 자동 승격하면 위험하므로 **오프라인 검증·휴먼 게이트**를 권장.

---

## 6. 이데아 엔진(ionia.idea) 연결 (느린 축)

- **역할**: 새로운 실패 패턴, 재료 조합, “왜 타는가” 같은 **통찰 후보**를 **형상/가중 후보**로 올리는 층.
- **연결점(문서상)**: `IdeaPool.add`, `IdeaEngine.step(state)`, CreativeIdeaBridge — `ionia` README·흐름도에 정의됨.
- **실시간 제어와의 거리**: 이데아 쪽은 **밀리초 단위 로봇 루프에 끼우지 않는 것**이 맞고, **세션 종료 후·야간 배치·사용자 확인 후**가 자연스럽다.
- **쿠킹과의 시나리오**: “비정형 자극(냄새 급변, 비정상 소음) + 임무 편차” → 로그 요약 → **insight** → `IdeaPool` 후보 (confidence 낮게 시작).

---

## 7. 종합 판단

| 질문 | 판단 |
|------|------|
| SIK(식스센스)와 연결 **셋업 가능?** | **가능.** 다만 **어댑터 + arbiter + 로봇 SDK**가 필요. |
| 자극–반응이 **즉시 행동**에 반영? | **가능**(반사 루프). 레시피 루프와 **합성 규칙**을 문서·코드로 고정해야 함. |
| 레시피대로 **정확한 동역학 임무**? | **현재 CPF는 프록시·틱 수준**; 실기는 **센서·구동기·식별**이 병행되어야 함. |
| 임무가 쌓여 **스킬**이 되나? | **아키텍처상 가능**; 구현은 **메모리·로그·보정 파이프라인** 추가 작업. |
| 이데아 창발까지 한 덩어리? | **개념적으로 한 파이프라인**으로 그릴 수 있음; **시간 분리**(느린 창발 vs 빠른 반사) 필수. |

---

## 8. 권장 구현 순서 (짧게)

1. **로봇 I/O 어댑터**: 실센서 → `KitchenObservation` / SIK `SensoryStimulus` 동시 주입(같은 타임스탬프).
2. **Arbiter v0 (구현됨, v0.3)**: 패키지 내 `arbiter.py`·`sik_ingress.py` — `run_flow_tick_payload`의 **`sik_stimuli`** 또는 명시 **`arbiter`**; `FlowEngine.tick(..., mission_pause=, heat_cap_0_1=)`.
3. **로그 스키마**: 스텝 ID, 관측 스냅샷, 명령, 결과(성공/스킵/사람 개입).
4. **(선택) ionia 브리지**: 세션 요약 → insight 큐 → 사람 승인 후 `IdeaPool.add`.

---

## 9. 참고 링크 (저장소 내)

- SIK: [_staging/Sensory_Input_Kernel/README.md](../../Sensory_Input_Kernel/README.md)
- ionia idea: [03_DISCIPLINES/ionia/README.md](../../../03_DISCIPLINES/ionia/README.md)
- 쿠킹 패키지: [../README.md](../README.md)
- 개인 에이전트·계약: [../../design_workspace/INTELLIGENCE_AND_PERSONAL_AGENT_ROADMAP.md](../../design_workspace/INTELLIGENCE_AND_PERSONAL_AGENT_ROADMAP.md)

---

*v0.1 — 설계 분석. 구현 커밋과 독립적으로 개정 가능.*

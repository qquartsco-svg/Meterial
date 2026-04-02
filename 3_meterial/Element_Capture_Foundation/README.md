# Element_Capture_Foundation v0.2.0

도메인 중립 원소/기체 포집 · 추출 · 저장 · 자급자족 screening 엔진

> 한국어 정본. English: [README_EN.md](README_EN.md)

`Element_Capture_Foundation` 는 “탄소·수소·헬륨을 어떻게 얻을 것인가”를 한 문제로 뭉개지 않고,
환경별 source density, species fraction, intake flux, separation efficiency,
storage cost 를 계산해 **실제 성립 가능한 회수 시스템인지**를 screening 하는 공통 엔진이다.

## 무엇을 하는 엔진인가

이 엔진은 “탄소 포집”, “수소 확보”, “헬륨 분리”, “우주에서 원소를 모은다” 같은 문제를 막연한 상상으로 두지 않고,
아래 질문을 공학적으로 계산한다.

- 어디에 자원이 있는가
- 그 자원은 얼마나 들어오는가
- 분리/추출 효율은 얼마나 되는가
- 저장/압축/액화 비용은 감당 가능한가
- 장치가 실제 플랫폼 질량/열/전력 제약 안에 들어가는가
- 생명유지/자급자족 루프 안에서 실제로 의미가 있는가

즉 이 엔진은 “원소를 모을 수 있을까?”가 아니라
**“이 환경과 플랫폼에서 이 회수 루프가 실제로 성립하는가?”**를 판정하는 커널이다.

## 핵심 원칙

- `capture` 와 `extraction` 을 구분한다.
- “존재한다”와 “쓸 수 있다”를 구분한다.
- 먼저 `flux / yield`, 그 다음 `storage / energy`, 마지막에 `health` 를 본다.

## 지원 모드

- `atmospheric_capture`
- `dissolved_extraction`
- `electrochemical_extraction`
- `cryogenic_separation`
- `orbital_skimming`

## 개념 구분

### `capture` vs `extraction`

- `capture`
  - 이미 기체 흐름이나 혼합기체 안에 퍼진 종을 모은다
  - 예: 대기 CO2, 혼합기체 속 He, orbital skim gas
- `extraction`
  - 액체·용존·전기화학 과정에서 목표 종을 얻는다
  - 예: 물에서 H2, 용존 CO2, 재생 루프 부산물 회수

### “존재” vs “접근 가능”

이 엔진은 `species_fraction_0_1`만 보지 않고

- `collection_accessibility_0_1`
- `energetic_cost_index`
- `residence_time_s`
- `platform_mass_kg`

까지 같이 본다.

즉 “있다”와 “쓸 수 있다”를 구분한다.

## 기본 수식

유입 질량 유량:

`m_dot_in = rho * v * A`

종별 유입 질량 유량:

`m_dot_species_in = y_i * rho * v * A`

회수 질량 유량:

`m_dot_capture = eta * y_i * rho * v * A * accessibility`

에너지 집약도:

`energy_intensity = power_input_w / max(m_dot_capture, eps)`

## 구조

```text
element_capture/
├── contracts.py
├── environment.py
├── intake.py
├── separation.py
├── storage.py
├── health.py
├── planning.py
├── power_governance.py
├── waste_loop.py
├── waste_regeneration.py
├── habitat_operations.py
├── adapter.py
└── bridges/
```

## 기존 엔진과 연결 방향

- `Eurus_Engine` -> 밀도, 압력, 대기 프로파일
- `TerraCore_Stack` -> CO2/H2O/H2/He 재고와 전기분해 문맥
- `Oceanus_Engine` -> 용존 자원 추출
- `OrbitalCore_Engine` -> 궤도 skim 체류 시간과 drag penalty
- `Satellite_Design_Stack` -> scoop 면적/전력/질량 제약
- `Superconducting_Magnet_Stack` -> cryogenic/field-assisted separation 장치 문맥
- `FusionCore_Stack` -> H2 / He / He-3 연료 수요 문맥
- `FrequencyCore_Engine` -> 펌프/막/압축기 health observer

## 실브리지

- `co2_capture_environment_from_terracore(atmosphere, ...)`
  - TerraCore 대기 상태를 CO2 capture 환경으로 변환
- `h2_extraction_environment_from_terracore(hydrosphere, ...)`
  - TerraCore 수권/전기분해 상태를 H2 extraction 환경으로 변환
- `EurusCaptureBridge().atmosphere_capture_environment(...)`
  - Eurus 대기 프로파일에서 고도별 capture 환경 생성
- `OrbitalCaptureBridge().orbital_skimming_environment(...)`
  - OrbitalCore 고도/속도 문맥에서 orbital skimming 환경 생성
- `OceanusCaptureBridge().dissolved_co2_environment(...)`
  - Oceanus 셀/열염 상태를 dissolved CO2 extraction 환경으로 변환
- `constrain_capture_stack(blueprint, intake, separation, storage)`
  - Satellite blueprint 기반 장치 면적/전력/질량 제약 적용
- `CaptureFrequencyBridge(...).health(...)`
  - FrequencyCore 스타일 장치 vibration health 계산
- `snapshot_from_terracore(...)` / `demand_profile_from_snapshot(...)`
  - TerraCore 생명유지 상태를 일일 CO2/O2/H2O 수요 문맥으로 정규화
- `crew_metabolic_profile("nominal" | "reduced_activity" | "eva_recovery")`
  - 승무원 활동 수준에 따라 CO2/O2/H2O 소비 프로파일 선택
- `plan_resource_horizon(assessment, demand)`
  - 하루 수요, 탱크 버퍼, inventory horizon 계산
- `govern_capture_power(demand_power_w=..., ...)`
  - 생명유지, 추진, 연구, 포집 장치 사이 전력 우선순위 계산
- `assess_terracore_regeneration(...)`
  - 물/산소/CO2 재생률과 loop closure gain 추정
- `assess_habitat_operations(...)`
  - habitat risk, self-sufficiency, 운영 우선순위와 행동 권고 계산

## 활용 시나리오

- 행성 대기에서 CO2 direct air capture feasibility
- 수권/전기분해 기반 H2 recovery feasibility
- 고밀도 혼합기체에서 He cryogenic separation screening
- 우주선/위성 자급자족 루프의 폐쇄성 평가
- orbital skimming의 수율 vs drag penalty 비교
- capture payload가 실제 플랫폼 class에 얹히는지 판단

## 확장성

- 더 정교한 화학 프로세스 모델을 separation 층에 추가 가능
- cryogenic / magnetic filter 장치를 device constraint 층으로 추가 가능
- `FrequencyCore`와 더 깊게 묶어 machinery degradation observer 확장 가능
- `FusionCore`와 연결해 H2 / He-3 demand planning으로 확장 가능
- `TerraCore` habitat operations와 묶어 mission horizon planner로 확장 가능

## 현재 한계

이 엔진은 아직 다음을 하지 않는다.

- 고정밀 CFD
- full chemical plant simulation
- 실제 cryogenic boil-off 상세 해석
- 인증용 ECLSS 시뮬레이션
- mission-grade orbital economics

특히 중요한 한계:

- deep-space direct capture는 여전히 수율이 매우 낮다
- orbital skimming은 보수적으로 infeasible 판정이 자주 나온다
- 실제 플랫폼 적용성은 질량/열 제약에 의해 먼저 막히는 경우가 많다

즉 이 엔진은 “모든 원소를 우주에서 수확하는 장치”가 아니라,
**무엇을 어디서 어떻게 회수해야 실제 공학적으로 성립하는가를 screening 하는 kernel**로 읽는 게 정확하다.

## 빠른 예시

```python
from element_capture import (
    CaptureMode,
    Species,
    CaptureEnvironment,
    IntakeGeometry,
    SeparationStage,
    StorageStage,
    ElementCaptureAdapter,
)

adapter = ElementCaptureAdapter()
report = adapter.assess(
    environment=CaptureEnvironment(
        mode=CaptureMode.ATMOSPHERIC_CAPTURE,
        species=Species.CO2,
        density_kg_m3=1.225,
        bulk_velocity_ms=2.0,
        species_fraction_0_1=420e-6,
        collection_accessibility_0_1=0.95,
        energetic_cost_index=0.45,
    ),
    intake=IntakeGeometry(area_m2=10.0),
    separation=SeparationStage(recovery_efficiency_0_1=0.82),
    storage=StorageStage(capacity_kg=50.0, stored_mass_kg=5.0, storage_efficiency_0_1=0.96),
)

print(report.capture_rate_kg_s, report.omega_capture, report.capture_possible)
```

## MVP 범위

- CO2 atmospheric capture
- H2 electrochemical extraction
- He cryogenic separation from dense mixture
- orbital skimming feasibility

## 현재 적용 가능 엔진

| 엔진 | 지금 붙는 방식 | 상태 |
|---|---|---|
| `TerraCore_Stack` | 대기/수권 상태 -> CO2/H2 환경 | `implemented` |
| `Eurus_Engine` | 고도 기반 대기 capture 환경 | `implemented` |
| `OrbitalCore_Engine` | skim 환경 생성, yield/pass screening | `implemented` |
| `Oceanus_Engine` | 용존 자원 추출 환경 | `implemented` |
| `Satellite_Design_Stack` | scoop/tank/power/mass budget 제약 | `implemented` |
| `Superconducting_Magnet_Stack` | cryogenic / field-assisted separation 장치 제약 | `planned` |
| `FusionCore_Stack` | H2/He/He-3 수요/연료 문맥 | `planned` |
| `FrequencyCore_Engine` | 펌프/막/압축기 health observer | `implemented` |

## 아직 부족한 레이어

- `resource_planning` 레이어
  - mission demand
  - daily yield
  - storage depletion / refill horizon
- `power_governance` 레이어
  - capture vs propulsion vs habitat load sharing
- `life_support_bridge`
  - scrubber / O2 loop / water recovery direct coupling

지금은 `life_support_bridge`와 `resource_planning`의 첫 버전이 구현돼 있고,
`power_governance`와 `waste_loop`의 첫 버전도 들어가 있습니다.
`waste_regeneration`과 `thermal storage constraints`의 첫 버전도 들어가 있습니다.
다음 단계는 이들을 TerraCore와 Satellite blueprint 실데이터에 더 깊게 묶는 것입니다.

## 우주선이 움직이면서 원소를 모을 수 있나

가능성은 있지만, 먼저 `수율 / pass` 와 `drag penalty` 를 같이 봐야 한다.

특히 우주공간 희박 환경에서는:

- `orbital_yield_per_pass_kg`
- `drag_penalty_proxy_0_1`

가 핵심이다.

즉 “포집 장치가 있느냐”보다 먼저
**지나가는 동안 실제로 얼마나 들어오고, 그 대가로 궤도 손실이 얼마나 큰가**를 봐야 한다.

이 MVP는 `orbital_skimming` 모드에서 그 feasibility 를 screening 한다.

## 우주선 자급자족 문맥

지금 구조는 이미 아래 루프의 기초를 갖고 있다.

- `environment source`
- `capture / extraction`
- `storage`
- `platform constraints`
- `machinery health`
- `crew demand`
- `power governance`
- `waste regeneration`
- `habitat operations`

관련 문서와 데모:

- `/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/docs/SPACECRAFT_SELF_SUFFICIENCY_STACK.md`
- `/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/examples/run_spacecraft_resource_loop.py`
- `/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/examples/run_life_support_planning_demo.py`
- `/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/examples/run_satellite_blueprint_capture_demo.py`
- `/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/examples/run_platform_class_comparison.py`
- `/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/examples/run_capture_orbit_endurance_demo.py`

`run_platform_class_comparison.py` 는 두 시각을 함께 보여준다.

- 기본 bridge
  - 현재 위성/우주선 blueprint 안에서 남는 전력, 질량, 열 마진으로 capture stack이 들어갈 수 있는지 평가
- `design_capture_service_bus(...)`
  - 처음부터 자원회수 장치를 싣는 전용 bus를 가정하는 what-if 경로
  - 즉 "현재 플랫폼에는 안 맞지만, 전용 자원회수 버스를 쓰면 경계점이 어디인가"를 볼 수 있다
  - 최신 경로는 `Satellite_Design_Stack.capture_service_bus_profile(...)` -> `apply_capture_platform_profile(...)` 계약으로 연결된다

지금의 해석은 보수적이다.

- 행성 대기/수권 기반 CO2/H2 회수는 현실적인 공학 문제
- 용존 CO2 추출과 habitat loop closure는 자급자족 문맥에서 유망
- 심우주를 지나가며 희박 원소를 직접 긁어모으는 orbital skimming은 여전히 수율이 매우 낮다
- 따라서 이 엔진은 "우주에서 아무거나 모으는 장치"보다, "어디서 무엇을 어떻게 회수해야 자급자족이 성립하는가"를 판정하는 커널로 읽는 것이 정확하다

## 운영 루프 예시

1. `TerraCore` 또는 `Eurus/Oceanus`에서 환경 source를 읽는다.
2. `ElementCaptureAdapter`로 capture/extraction feasibility를 계산한다.
3. `Satellite_Design` 제약을 적용해 실제 플랫폼 power/area/mass 한계를 반영한다.
4. `FrequencyCore`로 펌프/막/압축기 health를 감시한다.
5. `life_support_bridge`, `planning`, `power_governance`, `waste_regeneration`, `habitat_operations`으로 자급자족 운영 판단을 만든다.
6. `OrbitalCaptureBridge.assess_capture_operations(...)`로
   `orbits_per_day`, `daily_capture_kg`, `orbital_omega_0_1`, `endurance_score_0_1`
   를 계산해 궤도 운영 유지 가능성을 본다.

여기서 `Satellite_Design` 기본 bridge는 보수적인 truth source 쪽이고,
`capture_service_bus_profile(...)`는 탐색적 engineering what-if 쪽이다.

## 현실화 포인트

- `run_satellite_blueprint_capture_demo.py`
  - 실제 `SatelliteDesignPipeline` blueprint 기준으로 현재 장치가 너무 무거운지, 전력이 부족한지, thermal margin이 얕은지 확인한다.
- `run_platform_class_comparison.py`
  - `CUBESAT_12U`, `SMALLSAT`, `LEO_COMSAT`처럼 플랫폼 class를 바꿔가며 capture stack 탑재 가능성을 비교한다.
  - 지금은 단순 `가능/불가능`뿐 아니라 `mass_budget_exhausted`, `storage_locked`, `thermal_limited` 이유도 같이 보여준다.
- `run_capture_orbit_endurance_demo.py`
  - `Satellite_Design`의 capture service bus profile과 `OrbitalCore` 건강도를 같이 써서
    하루 회수량과 궤도 운영 endurance를 계산한다.
- `crew_metabolic_profile(...)`
  - nominal / reduced activity / EVA recovery 같은 활동 수준 차이를 life-support 수요에 직접 반영한다.

## 현재 검증 상태

- `35 passed`
- 공개 예제 entrypoint smoke test 포함
- 무결성 검증:
  - `python3 scripts/verify_signature.py`
- 릴리스 검증:
  - `python3 scripts/release_check.py`

## 무결성 / 블록체인 서명

이 저장소에서 말하는 “블록체인 서명”은 온체인 계약이 아니라,
루트 [SIGNATURE.sha256](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/SIGNATURE.sha256)에 담긴
**SHA-256 무결성 매니페스트**다.

- 자세한 설명:
  - [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)
  - [BLOCKCHAIN_INFO_EN.md](BLOCKCHAIN_INFO_EN.md)

## 테스트

```bash
python3 -m pytest -q /Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/tests
```

현재 기준: `35 passed`

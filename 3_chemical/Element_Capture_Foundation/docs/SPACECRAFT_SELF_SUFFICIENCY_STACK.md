# Spacecraft Self-Sufficiency Stack

`Element_Capture_Foundation`는 자원 회수 feasibility를 평가하는 커널이다.
우주선 자급자족 문맥에서는 아래 엔진들을 한 루프로 묶는 역할이 자연스럽다.

## 현재 연결

- `TerraCore_Stack`
  - 대기 CO2 회수
  - 수권/전기분해 기반 H2 추출
- `Eurus_Engine`
  - 고도별 대기 밀도/압력/온도 기반 capture 환경
- `Oceanus_Engine`
  - 용존 CO2 기반 `dissolved_extraction`
- `OrbitalCore_Engine`
  - orbital skimming feasibility
- `Satellite_Design_Stack`
  - collector area / power surplus / mass budget 제약
- `FrequencyCore_Engine`
  - 펌프, 막, 압축기 vibration health

## 아직 비어 있는 층

- `resource_planning`
  - 하루/궤도당 목표 회수량
  - 저장 탱크 교대 전략
- `power_governance`
  - 추진, 생명유지, 포집 장치 사이 전력 분배
- `waste_loop`
  - 포집 부산물과 재생 루프
- `life_support_bridge`
  - CO2 scrubber / O2 loop / water recovery와 직접 연결

## 이제 구현된 추가 층

- `life_support_bridge`
  - TerraCore atmosphere / hydrosphere 상태를
    `crew CO2 output`, `O2 consumption`, `water demand`, `H2 recovery potential`
    문맥으로 정규화
- `resource_planning`
  - 일일 회수량
  - 일일 수요
  - 저장 탱크 fill time
  - inventory horizon
  - 목표 buffer 충족 여부
- `power_governance`
  - capture, habitat, propulsion, research load 사이 전력 우선순위
- `waste_loop`
  - 회수 부산물과 loop closure score 추정
- `waste_regeneration`
  - TerraCore atmosphere / hydrosphere / biosphere 상태를 다시 물·산소·CO2 재생률로 읽음
- `thermal storage constraints`
  - Satellite thermal margin과 heater load를 storage capacity / compression power에 반영
- `habitat_operations`
  - habitat risk
  - self-sufficiency
  - crew safety 우선순위
  - 운영 행동 권고
- `crew metabolic profile`
  - nominal / reduced activity / EVA recovery 문맥에 따라
    CO2 / O2 / H2O 일일 수요를 다르게 추정
- `satellite blueprint capture demo`
  - 실제 `SatelliteDesignPipeline` blueprint를 받아
    capture stack power / mass / thermal 제약을 적용하는 현실화 예제
- `platform class comparison`
  - smallsat / larger LEO platform 급에서
    capture stack이 어느 클래스부터 현실적으로 탑재 가능한지 비교
  - 현재는 `mass budget exhausted`, `storage locked`, `thermal limited`
    같은 실패 이유를 함께 읽을 수 있음
- `capture service bus what-if`
  - 현재 blueprint truth source는 그대로 두고
    dedicated power / collector area / payload mass allowance를 가진
    전용 자원회수 버스를 별도 engineering 가정으로 비교할 수 있음
- `capture orbit operations`
  - `OrbitalCore_Engine`의 주기/건강 지표를 이용해
    하루 회수량, drag 부담, Δv 여유, 운영 endurance를 계산할 수 있음

## 실무적 해석

- 심우주 직접 포집은 현재 screening 기준으로 수율이 너무 낮다.
- 행성 대기, 수권, 고밀도 혼합기체는 자원 회수 대상으로 현실적이다.
- 우주선 자급자족은 결국:
  - `환경 source`
  - `플랫폼 제약`
  - `장치 health`
  - `저장/재생`
  를 한 루프로 다뤄야 한다.

## 지금까지 닫힌 운영 판단

- `capture_possible`
  - 지금 환경에서 회수가 성립하는가
- `inventory_horizon_days`
  - 현재 저장량 기준으로 몇 일 버틸 수 있는가
- `power_capture_allowed`
  - 지금 포집 장치를 돌려도 되는가
- `loop_closure_score_0_1`
  - 폐기물/부산물 재생이 자급자족 루프에 얼마나 기여하는가
- `habitat_risk_0_1`
  - 승무원 생존/거주 측면에서 현재 루프가 얼마나 불안정한가
- `self_sufficiency_0_1`
  - 이 시스템이 외부 resupply 없이 얼마나 자립적으로 돌아가는가
- `endurance_score_0_1`
  - 현재 궤도와 capture stack이 단기 feasibility를 넘어
    반복적 회수 운영을 얼마나 오래 유지할 수 있는가

즉 현재 ECF는 단순 포집 feasibility를 넘어서,
`환경 source -> 회수 -> 저장 -> 전력 -> 재생 -> 승무원 운영 -> 궤도 endurance`
까지 이어지는 기초 운영 커널로 읽는 게 맞다.

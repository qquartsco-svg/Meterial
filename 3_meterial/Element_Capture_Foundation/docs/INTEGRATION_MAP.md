# Element Capture Integration Map

`Element_Capture_Foundation` 이 00_BRAIN 전체 엔진 포트폴리오 안에서
어디에 붙고, 무엇이 이미 구현됐고, 무엇이 아직 비어 있는지 정리한다.

## 1. 현재 구현된 연결

### TerraCore_Stack

- 대기 상태 -> `CO2 atmospheric capture`
- 수권/전기분해 상태 -> `H2 electrochemical extraction`

실제 브리지:

- [terracore_bridge.py](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/element_capture/bridges/terracore_bridge.py)

### Eurus_Engine

- 고도 기반 밀도/압력 -> atmospheric capture 환경

실제 브리지:

- [eurus_bridge.py](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/element_capture/bridges/eurus_bridge.py)

### OrbitalCore_Engine

- 고도/속도 문맥 -> `orbital_skimming` 환경
- `yield/pass`, `drag penalty` screening

실제 브리지:

- [orbital_core_bridge.py](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/element_capture/bridges/orbital_core_bridge.py)

## 2. 다음 연결 우선순위

### Oceanus_Engine

목적:

- 용존 CO2
- 용존 H2
- 염도/수온이 추출성에 미치는 영향

실제 브리지:

- [oceanus_bridge.py](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/element_capture/bridges/oceanus_bridge.py)

### Satellite_Design_Stack

목적:

- scoop area
- tank mass
- compression power budget
- platform mass constraints

실제 브리지:

- [satellite_bridge.py](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/element_capture/bridges/satellite_bridge.py)

### Superconducting_Magnet_Stack

목적:

- cryogenic separation 장치 제약
- low-temperature storage
- field-assisted separator feasibility

권장 새 레이어:

- `cryogenic_device.py`
- `magnet_bridge.py`

### FrequencyCore_Engine

목적:

- pump vibration
- membrane oscillation
- compressor anomaly

실제 브리지:

- [frequency_bridge.py](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/element_capture/bridges/frequency_bridge.py)

## 2.5 현재 남은 레이어

- `resource_planning`
- `power_governance`
- `life_support_bridge`

## 3. 최종 판정

지금 `Element_Capture_Foundation` 은
“원소 포집 장치가 있을 것 같다” 수준이 아니라,

- source quality
- intake flux
- separation efficiency
- storage cost
- orbital feasibility

를 실제 기존 엔진 문맥으로 계산하는 **resource capture screening kernel** 로 읽는 것이 맞다.

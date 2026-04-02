> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# Carbon Composite Stack

탄소 기반 산업 전환을 한 번에 다루는 거대 플랫폼이 아니라,
**탄소 복합재의 설계·공정·순환성 readiness를 빠르게 판정하는 L1 독립 엔진**입니다.

Version: `0.1.2`

한 줄 정의:
**재료 물성 + 공정성 + 순환성 지표를 하나의 Ω 판정으로 묶는 탄소 복합재 설계 커널**.

## 범위

하는 일:

- 후보 복합재 물성(강도/강성/피로) 평가
- 공정 조건(경화 온도/압력/사이클/스크랩) 기반 processability 평가
- recycle/scrap 기반 circularity 평가
- 최종 `HEALTHY/STABLE/FRAGILE/CRITICAL` readiness 판정

하지 않는 일:

- 신규 소재 발견 실험 대체
- 고정밀 다중물리 시뮬레이터 대체
- 생산 인증/규제 문서 대체

현재 성숙도(보수적 해석):

- `v0.1.2`는 **초기 L1 스캐폴드**이며, 개념/계약/입출력 경계가 우선 고정된 단계입니다.
- 현재 테스트 스냅샷(`4 passed`)은 기본 동작성 검증 중심이며, 재료·공정 세부 물리의 폭넓은 회귀 검증은 다음 단계 확장 대상입니다.

## 레이어

- `contracts`: `CarbonMaterialCandidate`, `CompositeProcessConfig`, `ProductSpec`
- `material`: specific strength/stiffness/fatigue margin + thermal/electrical suitability + mass budget proxy
- `process`: processability/energy intensity (공정 난이도·에너지 집약도·스크랩 손실 패널티 반영)
- `circularity`: recycle score/scrap penalty (향후 virgin/recycled ratio, scrap reuse path, repair/rework, embodied energy 축으로 확장)
- `observer`: `omega_total` + verdict (재료·공정·순환성 신호를 readiness로 집계하는 판정 레이어)
- `pipeline`: `run_composite_assessment()` (평가 실행 흐름을 묶는 오케스트레이션 레이어)
- `engine_ref_adapter`: `carbon.composite.readiness`
- `cli`: `carbon-composite-assess --input-json ... --json`

## 핵심 개념

- `specific_strength = tensile_strength / density`
- `specific_stiffness = modulus / density`
- `omega_total = 0.45*omega_material + 0.35*omega_process + 0.20*omega_circularity`

> 이 수식은 설계 초기 screening proxy이며, 절대 성능 보증 수식이 아닙니다.

### 단위 메모 (목표 스펙)

- `target_specific_strength_kn_m_kg`: `kN·m/kg` 기준 목표 비강도
- `target_specific_stiffness_mn_m_kg`: `MN·m/kg` 기준 목표 비강성
- 단위 혼선 방지를 위해 실제 입력 데이터와 내부 계산 단위를 docs 단계에서 지속 정렬합니다.
- `max_mass_kg`: 아직 실제 형상/치수 기반 질량 해석은 아니며, 현재는 **density 기반 lightweight pressure proxy**에 반영됩니다.
- `safety_class`: `aerospace/marine/automotive/general` 별로 thermal/electrical target 과 mass proxy 강도를 조정하는 보수적 입력입니다.

## 빠른 시작

```python
from carbon_composite_stack import (
    CarbonMaterialCandidate, CompositeProcessConfig, ProductSpec, run_composite_assessment
)

material = CarbonMaterialCandidate(
    name="CFRP-A",
    density_kg_m3=1550.0,
    tensile_strength_mpa=1800.0,
    youngs_modulus_gpa=140.0,
    thermal_conductivity_w_mk=8.5,
    electrical_conductivity_s_m=15000.0,
    fatigue_strength_mpa=900.0,
    recycle_content_ratio=0.2,
)
process = CompositeProcessConfig(
    cure_temp_c=180.0,
    cure_pressure_bar=6.0,
    cycle_time_min=95.0,
    scrap_rate=0.08,
    energy_kwh_per_kg=9.0,
)
spec = ProductSpec(
    target_specific_strength_kn_m_kg=1.0,
    target_specific_stiffness_mn_m_kg=70.0,
    max_mass_kg=120.0,
    min_fatigue_margin=0.45,
    safety_class="aerospace",
)

readiness, material_report, process_report, circularity_report = run_composite_assessment(material, process, spec)
print(readiness.verdict, readiness.omega_total)
```

CLI:

```bash
cd _staging/Carbon_Composite_Stack
python3 -m carbon_composite_stack.cli --input-json examples/sample_payload.json --json
```

## design_workspace 연결

- `engine_ref`: `carbon.composite.readiness`
- payload:
  - `material`: 탄소 복합재 후보 물성
  - `process`: 경화/사이클/스크랩/에너지 조건
  - `spec`: 목표 비강도/비강성/피로마진/안전등급

## 테스트

```bash
cd _staging/Carbon_Composite_Stack
python3 -m pytest tests/ -q --tb=no
```

현재 로컬 점검 기준:

- `4 passed`
- 범주: contracts validation, readiness aggregation, engine_ref/CLI payload flow

다음 테스트 확장 우선순위:

- 재료 축: 방향성(섬유 배향)·환경 열화(온도/습기) 민감도 케이스
- 공정 축: cycle/scrap/energy 경계값 및 페널티 단조성 검증
- 순환 축: recycle/scrap 조합 변화에 대한 Ω 안정성 회귀

## 변경 이력 / 무결성

- 변경 요약: [CHANGELOG.md](CHANGELOG.md)
- 무결성 설명: [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)
- 연속 기록 로그: [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md)
- SHA-256 매니페스트: [SIGNATURE.sha256](SIGNATURE.sha256)

검증:

```bash
python3 scripts/generate_signature.py
python3 scripts/verify_signature.py
```

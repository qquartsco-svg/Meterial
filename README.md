# Meterial v0.2.1

> **한국어 정본.** English: [README_EN.md](README_EN.md)

화학 반응은 “정답 하나로 닫히는 사건”이라기보다,  
종이 어떻게 바뀌고, 에너지가 어떻게 드나들고, 속도가 어떻게 달라지고, 평형이 어디쯤 형성되는지를 **동역학 흐름으로 읽어야 하는 문제**에 가깝다.

`Meterial` 은 그 흐름을 관찰하고 구조화하는 **E5 Chemistry foundation layer** 다.  
이 엔진은 “화학 반응이 무엇인지 확정한다”기보다, 반응을 읽기 위한 최소 공통 문법과 screening 환경을 제공한다.

> 공개 저장소 이름은 `Meterial` 이다.  
> 내부 Python 패키지 import 는 호환성을 위해 현재도 `chemical_reaction` 을 사용한다.

## What It Is

이 엔진은 다음을 위한 기초 레이어다.

- 화학 종과 반응식을 계약으로 표현
- 질량/전하 보존 확인
- 열역학적으로 유리한지 추정
- 동역학적으로 빠른지 느린지 추정
- 평형이 어느 쪽에 치우치는지 관찰
- 전기화학 셀 전위와 전자 이동을 계산
- 과장된 화학 주장을 ATHENA 4단계로 screening

즉 이 엔진은 **chemical observer-ready foundation** 이다.

## What It Is Not

- 분자 동역학(MD) 시뮬레이터가 아니다
- 양자 화학 해석기나 전자구조 계산기가 아니다
- 상업용 공정 설계 소프트웨어가 아니다
- NIST 급 정밀 데이터베이스가 아니다
- 실험 결과를 대신 확정해 주는 엔진이 아니다

현재 구현은 주로 **tree-level / order-of-magnitude** 수준의 구조를 다룬다.

## 왜 중요한가

많은 공학 엔진은 화학을 이미 “파라미터”로 소비한다.

- 배터리: OCV, SOC, 열화, 전극 반응
- 수소: 전기분해, 저장, 연료전지
- 원소 포집: 전기화학 추출, 분리, 저장
- 탄소 복합재: 경화, 열예산, 수지 반응
- 요리 공정: Maillard, 열전달, 수분 활성도

그런데 그 파라미터가 **어디서 오는지**를 설명하는 공통 화학 코어가 없으면, 위 엔진들은 서로 다른 언어로 드리프트하기 쉽다.

이 엔진은 그 빈칸을 메우는 역할을 한다.

## 인식론적 위치

[EPISTEMIC_LAYER_MAP.md](../../EPISTEMIC_LAYER_MAP.md) 기준으로 보면:

```text
E4 Engineering
  -> 배터리, 수소, 포집, 재료, 공정
E5 Chemistry
  -> Meterial
E6 Biology
  -> ATP, 혈액, 감각, 기억, 인지 토큰
```

즉 E4 공학 엔진이 소비하는 많은 화학 파라미터의 뿌리를 E5에서 정리한다.

## 화학 반응을 어떻게 읽는가

이 엔진이 채택하는 작업 정의:

> 화학 반응은 원자 간 결합 재배열과 전자 이동을 통해 물질과 에너지가 변환되는 과정으로 **읽을 수 있다**.

이 정의는 고정 결론이 아니라, 관찰을 정리하기 위한 출발점이다.

핵심 질문은 다음 다섯 가지다.

1. 무엇이 반응하는가
2. 열역학적으로 가능한가
3. 얼마나 빠른가
4. 어디서 멈추는가
5. 전자가 오가면 무엇이 달라지는가

## 레이어 구조

| 레이어 | 모듈 | 질문 |
|---|---|---|
| L0 | `contracts.py`, `constants.py` | 무엇을 어떻게 표현하는가 |
| L1 | `species_and_bonds.py` | 어떤 species와 결합이 있는가 |
| L2 | `thermodynamics.py` | 열역학적으로 유리한가 |
| L3 | `kinetics.py` | 반응 속도는 어느 정도인가 |
| L4 | `equilibrium.py` | 평형은 어느 방향인가 |
| L5 | `electrochemistry.py` | 전자 이동이 들어가면 어떻게 바뀌는가 |
| L6 | `screening.py` | 주장이 과장되었는가 |
| L7 | `extension_hooks.py` | 형제 엔진과 어떻게 연결되는가 |

## 핵심 수식

| 이름 | 수식 | 직관 |
|---|---|---|
| Gibbs 자유 에너지 | `ΔG = ΔH - TΔS` | 자발성의 방향 |
| Arrhenius 속도 상수 | `k = A exp(-Ea/RT)` | 온도와 장벽이 속도에 미치는 영향 |
| 1차 반감기 | `t1/2 = ln 2 / k` | 절반이 반응하는 데 걸리는 시간 |
| 속도 법칙 | `r = k [A]^a [B]^b` | 농도와 속도의 관계 |
| 평형 상수 | `K_eq = exp(-ΔG°/RT)` | 평형 위치 |
| Nernst | `E = E° - (RT/nF) ln Q` | 반응지수와 전위의 관계 |
| Faraday | `m = ItM / nF` | 전하로부터 생성 질량 추정 |
| Butler-Volmer | `j = j0 [exp(αaFη/RT) - exp(-αcFη/RT)]` | 과전압과 전류 밀도 관계 |

## Quick Start

```python
from chemical_reaction import (
    ChemicalSpecies,
    Phase,
    Reaction,
    ReactionTerm,
    assess_chemical_foundation,
)

H2 = ChemicalSpecies("H2", 2.016, Phase.GAS)
O2 = ChemicalSpecies("O2", 32.0, Phase.GAS)
H2O = ChemicalSpecies("H2O", 18.015, Phase.LIQUID)

rxn = Reaction(
    reactants=(ReactionTerm(H2, 2.0), ReactionTerm(O2, 1.0)),
    products=(ReactionTerm(H2O, 2.0),),
    delta_h_kj_per_mol=-571.6,
    delta_s_j_per_mol_k=-326.8,
    activation_energy_kj_per_mol=75.0,
    label="2H2 + O2 -> 2H2O",
)

report = assess_chemical_foundation(rxn, temperature_k=298.15)
print(report.verdict)
print(report.thermodynamic_feasibility)
print(report.kinetic_accessibility)
print(report.omega)
```

예상 해석:

- 질량/전하 보존은 맞는가
- `ΔG` 기준으로 유리한 방향인가
- 활성화 장벽 때문에 느릴 수 있는가
- 평형은 생성물 쪽으로 치우치는가

## 형제 엔진과의 연결

| 형제 엔진 | 연결 방식 |
|---|---|
| `Battery_Dynamics_Engine` | Nernst, Arrhenius, Butler-Volmer |
| `Element_Capture_Foundation` | 전기화학 추출, 분리 전위 |
| `Hydrogen_Foundation` | 전기분해, 연료전지, 저장 |
| `Carbon_Composite_Stack` | 경화 동역학, 열예산 |
| `Cooking_Process_Foundation` | Maillard, 열전달, 수분 활성도 |
| `TerraCore_Stack` | 전기분해, 가스 순환, life-support chemistry |
| `VectorSpace_102` | 향후 `from_chemical_assessment` 허브 어댑터 |

## ATHENA Screening

이 엔진은 화학 claim을 다음 네 단계로 읽는다.

- `Positive`
  - 알려진 화학과 잘 정렬됨
- `Neutral`
  - 정보가 부족하거나 추가 데이터가 필요함
- `Cautious`
  - 특수 조건, 촉매, 극한 환경, 추가 가정이 필요함
- `Negative`
  - 보존 법칙이나 차수 추정과 강하게 어긋남

예:

- “물 전기분해에는 최소한의 가역 전압 문맥이 필요하다” -> `Positive`
- “이 촉매가 선택도를 높였다” -> `Neutral`
- “상온에서 무손실 조건으로 모든 반응이 해결된다” -> `Cautious`
- “투입 에너지보다 더 큰 에너지를 화학 반응이 공짜로 낸다” -> `Negative`

## 현재 구현이 주는 것

현재 foundation report는 대략 다음을 요약한다.

- `verdict`
- `thermodynamic_feasibility`
- `kinetic_accessibility`
- `equilibrium_position`
- `omega`
- `key_risk`
- `recommendation`

즉 정답 선언보다, **반응을 어디서 조심해서 읽어야 하는지**를 보여준다.

## 테스트와 정합성

현재 테스트:

```text
80 passed
```

포함 범주:

- contracts
- species and conservation
- thermodynamics
- kinetics
- equilibrium
- electrochemistry
- screening
- domain mappings
- extension hooks
- foundation roll-up
- health
- package integrity

## 무결성

- [SIGNATURE.sha256](SIGNATURE.sha256)
- [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)
- [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md)

관련 스크립트:

- `python3 scripts/generate_signature.py`
- `python3 scripts/verify_signature.py`
- `python3 scripts/verify_package_identity.py`
- `python3 scripts/release_check.py`

## 현재 한계

- 정밀 열물성 데이터베이스를 내장하지 않는다
- 다단 반응 네트워크 자동 해석은 아직 약하다
- 분자 오비탈/전자 구조 해석은 범위 밖이다
- 수식은 구조 관찰용 근사이며, 정밀 공정 시뮬레이터를 대체하지 않는다
- 높은 `omega`는 “말이 되는 구조”를 뜻할 수는 있어도, 실험적 진실을 확정하지는 않는다

## 확장 방향

가장 자연스러운 다음 단계:

1. `Chemical_Observer_Foundation`
2. element foundations
   - Hydrogen / Oxygen / Nitrogen / Lithium / Phosphorus / Silicon
3. applied chemistry engines
   - battery
   - capture
   - materials
   - cooking
4. VectorSpace bridge

즉 이 엔진은 화학의 끝이 아니라, 화학 레이어의 뿌리다.

## 단독 클론 사용자에게

`00_BRAIN` 전체 워크스페이스에서는 여러 형제 엔진과 연결되지만,
이 공개 저장소는 **단독으로도 읽고 테스트할 수 있는 foundation package** 로 유지된다.

형제 엔진 링크는 확장 방향을 설명하기 위한 것이지,
이 저장소가 그 엔진들 없이는 동작하지 않는다는 뜻은 아니다.

---

*Meterial v0.2.1 — E5 chemistry foundation for observing reaction structure, not declaring final chemical truth.*

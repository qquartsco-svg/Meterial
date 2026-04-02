# Meterial v0.3.0

> **한국어 정본.** English: [README_EN.md](README_EN.md)

`Meterial` 은 단일 화학 반응 패키지만을 뜻하지 않는다.  
이 저장소는 지금까지 만들어진 화학 관련 foundation, element, applied engine 들을 **한 번에 관리하기 위한 umbrella chemistry repository** 다.

즉 이 레포는 두 층을 함께 가진다.

1. 루트 Python 패키지 [`chemical_reaction`](chemical_reaction)
   - 안정적인 E5 chemistry root foundation
   - species, thermodynamics, kinetics, equilibrium, electrochemistry, screening 제공
2. 허브 스냅샷 [`3_chemical/`](3_chemical)
   - 원소 foundation과 응용 chemistry 엔진을 묶어 보는 chemistry layer tree
   - 현재 만들어진 것들을 기준으로 계속 확장되는 관리 허브

> 공개 저장소 이름은 `Meterial` 이다.  
> 내부 Python import 는 호환성을 위해 여전히 `chemical_reaction` 을 사용한다.

---

## 이 레포는 무엇인가

이 저장소는 화학을 “정답 하나로 닫힌 학문”으로 다루기보다,

- 어떤 species 가 존재하는가
- 어떤 반응이 가능한가
- 에너지가 어느 방향으로 흐르는가
- 속도와 장벽이 어떻게 작용하는가
- 평형이 어디쯤 형성되는가
- 전기화학 맥락에서 무엇이 바뀌는가
- 원소와 재료, 공정이 어떻게 이어지는가

를 **보수적으로 관찰하고 연결하는 환경**에 가깝다.

즉 `Meterial` 은 “화학을 확정해 주는 엔진”이 아니라,  
**화학 레이어를 관리하고 확장하기 위한 공통 문법 + 허브 저장소**다.

---

## 이 레포가 지금 하는 일

현재 `Meterial` 은 다음 역할을 동시에 가진다.

### 1. Chemical root

루트 패키지 [`chemical_reaction`](chemical_reaction) 는 다음을 담당한다.

- 화학 종 / 반응식 계약
- 질량 보존 / 전하 보존 확인
- `ΔG = ΔH - TΔS` 기반 열역학 방향성
- `k = A exp(-Ea/RT)` 기반 동역학 접근성
- `K_eq = exp(-ΔG°/RT)` 기반 평형 편향
- Nernst / Faraday / Butler-Volmer 기반 전기화학 맥락
- ATHENA 방식의 claim screening

이 패키지는 **E5 Chemistry root foundation** 으로 유지된다.

### 2. Chemistry hub snapshot

[`3_chemical/`](3_chemical) 는 현재 화학 레이어를 이렇게 묶는다.

- chemical root
  - `Chemical_Reaction_Foundation`
- element foundations
  - `Hydrogen_Foundation`
  - `Helium_Foundation`
  - `Lithium_Foundation`
  - `Oxygen_Foundation`
  - `Nitrogen_Foundation`
  - `Phosphorus_Foundation`
  - `Silicon_Foundation`
  - 그리고 계속 추가되는 원소/재료 foundation
- applied chemistry engines
  - `Element_Capture_Foundation`
  - `Battery_Dynamics_Engine`
  - `Carbon_Composite_Stack`
  - `Cooking_Process_Foundation`

이 허브는 “완성된 주기율표”가 아니라,  
**현재 만들어진 chemistry layer 를 계속 쌓아 가는 관리용 스냅샷**이다.

---

## 어떻게 읽어야 하는가

이 레포는 아래 순서로 읽는 것이 가장 자연스럽다.

1. [`chemical_reaction/`](chemical_reaction)
   - 화학 반응을 읽는 공통 문법
2. [`3_chemical/README.md`](3_chemical/README.md)
   - 전체 chemistry layer 허브 구조
3. [`3_chemical/ELEMENT_REGISTRY.md`](3_chemical/ELEMENT_REGISTRY.md)
   - 어떤 원소 foundation 이 이미 있고 무엇이 planned 인지
4. 각 element / applied engine README
   - 특정 원소나 공정, 재료, 전기화학 응용의 맥락

즉 루트 패키지는 **core grammar**,  
`3_chemical` 은 **managed layer map** 으로 읽으면 된다.

---

## 현재 포함된 chemistry hub 흐름

현재 흐름은 대략 이렇게 읽을 수 있다.

```text
chemical_reaction
  -> 3_chemical/Chemical_Reaction_Foundation
  -> element foundations
     -> Hydrogen / Helium / Lithium / Nitrogen / Oxygen / ...
  -> applied chemistry engines
     -> Element_Capture / Battery / Carbon_Composite / Cooking
```

이 흐름의 목적은 “무엇이 참인지 단번에 선언”하는 것이 아니라,

- 화학 root 가 어디인가
- 어떤 원소 foundation 이 어떤 응용과 연결되는가
- 어느 지점에서 흐름이 끊기거나 과장되는가

를 지속적으로 점검하는 데 있다.

---

## 왜 umbrella repository 가 필요한가

화학 관련 엔진이 늘어나기 시작하면, 단일 패키지 README 만으로는 전체 구조를 통제하기 어렵다.

예를 들면:

- 수소는 생산/저장/연료전지/안전과 연결된다
- 산소는 ASU, LOX, 전기분해와 연결된다
- 리튬은 배터리와 직접 이어진다
- 인과 질소는 생물/비료/ATP 루프와 이어진다
- 탄소 복합재는 재료 공정과 이어진다
- element capture 는 자원 회수와 life-support chemistry 로 이어진다

그래서 `Meterial` 은 이제 **chemical root package + chemistry hub snapshot** 을 함께 관리한다.

---

## What It Does Not Do

이 저장소는 현재 다음을 목표로 하지 않는다.

- 화학의 최종 정답을 선언하는 것
- NIST 급 정밀 데이터베이스를 대체하는 것
- 양자화학 / 전자구조 / MD 를 직접 수행하는 것
- 모든 원소를 이미 완성된 상태로 제공하는 것
- 모든 element foundation 이 동일한 성숙도라고 주장하는 것

현재는 **이미 만들어진 것들을 중심으로 chemistry layer 를 정리하고 확장하는 단계**다.

---

## 루트 패키지 핵심 수식

루트 `chemical_reaction` 패키지는 다음 수식을 기초 뼈대로 삼는다.

| 이름 | 수식 | 직관 |
|---|---|---|
| Gibbs 자유 에너지 | `ΔG = ΔH - TΔS` | 반응 방향성 |
| Arrhenius 속도 상수 | `k = A exp(-Ea/RT)` | 온도와 장벽이 속도를 바꿈 |
| 속도 법칙 | `r = k [A]^a [B]^b` | 농도와 속도의 관계 |
| 평형 상수 | `K_eq = exp(-ΔG°/RT)` | 평형 위치 |
| Nernst | `E = E° - (RT/nF) ln Q` | 전위와 반응지수의 관계 |
| Faraday | `m = ItM / nF` | 전하와 생성 질량의 관계 |
| Butler-Volmer | `j = j0 [exp(αaFη/RT) - exp(-αcFη/RT)]` | 과전압과 전류 밀도 관계 |

이 수식들은 “완전한 해답”이 아니라,  
**화학 흐름을 구조적으로 읽는 최소 공통 언어**로 쓰인다.

---

## Quick Start

### 루트 패키지 사용

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

### 허브 탐색 시작

먼저 이 문서를 보고:

- [`3_chemical/README.md`](3_chemical/README.md)
- [`3_chemical/ELEMENT_REGISTRY.md`](3_chemical/ELEMENT_REGISTRY.md)
- [`3_chemical/CHEMICAL_GOVERNANCE.md`](3_chemical/CHEMICAL_GOVERNANCE.md)

그다음 관심 있는 원소 foundation 으로 내려가면 된다.

---

## 현재 테스트와 검증

루트 패키지 테스트:

```text
85 passed
```

루트 검증 스크립트:

- `python3 scripts/verify_package_identity.py`
- `python3 scripts/verify_hub_snapshot.py`
- `python3 scripts/verify_signature.py`
- `python3 scripts/release_check.py`

즉 지금은 루트 패키지 정합성뿐 아니라,  
`3_chemical` 허브 스냅샷이 레포 안에 존재하는지도 같이 확인한다.

---

## 무결성

- [SIGNATURE.sha256](SIGNATURE.sha256)
- [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)
- [BLOCKCHAIN_INFO_EN.md](BLOCKCHAIN_INFO_EN.md)
- [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md)

현재 서명은 루트 패키지뿐 아니라,  
레포에 포함된 `3_chemical` 트리까지 함께 추적한다.

이 무결성 층은 “절대 진실 보증”이 아니라,  
**현재 공개 저장소 상태를 추적하고 drift 를 빨리 발견하기 위한 저장소 레벨 서명**이다.

---

## 현재 한계

- 모든 원소 foundation 이 같은 성숙도에 도달한 것은 아니다
- `3_chemical` 은 관리 스냅샷이며, 일부 항목은 다른 허브/정본 위치와 관계를 가진다
- 고정밀 화학 데이터베이스나 고급 시뮬레이터를 대체하지 않는다
- root package 와 chemistry hub 사이의 연결은 계속 확장 중이다
- 이 레포는 “완성 선언”보다 **확장 가능한 chemistry layer 관리**를 우선한다

---

## 앞으로의 확장 방향

가장 자연스러운 다음 단계:

1. element foundation 계속 확장
2. `Chemical_Observer_Foundation` 계열 추가
3. applied chemistry engine 과의 bridge 강화
4. `VectorSpace_102` 와의 hub adapter 보강
5. `3_chemical` 전체 공통 smoke/release 규칙 정리

즉 `Meterial` 은 chemistry layer 의 끝이 아니라,  
**화학 레이어를 한 번에 관리하기 위한 public umbrella repository** 다.

---

## 단독 클론 사용자에게

이 저장소는 `00_BRAIN` 전체 없이도 읽고 테스트할 수 있다.  
다만 공개 저장소 안의 `3_chemical` 은 “현재 chemistry layer 의 관리 스냅샷”이라는 점을 기억하면 좋다.

정리하면:

- 패키지를 쓰고 싶으면 `chemical_reaction`
- 전체 화학 레이어를 보고 싶으면 `3_chemical`

이 두 진입점을 기억하면 된다.

---

*Meterial v0.3.0 — stable chemical root package plus a managed `3_chemical` umbrella snapshot for the evolving chemistry layer.*

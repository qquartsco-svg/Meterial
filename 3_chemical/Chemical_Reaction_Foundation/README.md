# Chemical_Reaction_Foundation v0.1.0

> **한국어 (정본).** English: [README_EN.md](README_EN.md)

---

**"화학 반응이란 무엇인가?"** — 이 엔진은 그 질문에 답을 내리지 않는다.  
대신 화학 종(species)이 변환되고, 에너지가 교환되고, 평형에 도달하고, 전자가 이동하는 **동역학적 흐름을 관찰할 수 있는 환경**을 제공한다.

> **이 엔진이 채택한 작업 정의:** 화학 반응 ≈ 원자 간 결합이 재배열되면서 물질과 에너지가 변환되는 과정. 이 정의는 고정된 결론이 아니라 탐색의 출발점이다.

---

## 인식론적 위치: E5 화학

[EPISTEMIC_LAYER_MAP.md](../../EPISTEMIC_LAYER_MAP.md) 참조.

```
E4 공학 ← Battery, TerraCore, Carbon_Composite가 화학을 "파라미터로 소비"
   ↓
E5 화학 ← ★ 이 엔진: 그 파라미터가 어디서 오는지를 정의
   ↓
E6 생물 ← ATP, 혈액, 뉴런이 화학 위에서 작동
```

---

## 이 엔진이 아닌 것

- 분자 동역학(MD) 시뮬레이터가 아니다
- 양자 화학 계산기가 아니다
- 화학 공장 공정 설계 소프트웨어가 아니다
- 정밀 열물성(NIST) 데이터베이스가 아니다

Tree-level 수식과 order-of-magnitude 추정으로 반응의 뼈대 구조를 관찰하고, 과장된 주장을 걸러내는 **현상학 기초 레이어**다.

---

## 레이어 구조

| 레이어 | 모듈 | 핵심 질문 |
|--------|------|-----------|
| L0 | `contracts.py`, `constants.py` | 데이터 계약과 기본 상수 |
| L1 | `species_and_bonds.py` | 무엇이 존재하는가? (종, 결합, 보존 법칙) |
| L2 | `thermodynamics.py` | 이 반응은 일어날 수 있는가? (ΔG, ΔH, ΔS) |
| L3 | `kinetics.py` | 얼마나 빠른가? (Arrhenius, 반감기, 촉매) |
| L4 | `equilibrium.py` | 어디서 멈추는가? (K_eq, Q vs K, 르샤틀리에) |
| L5 | `electrochemistry.py` | 전자가 교환되면? (Nernst, Butler-Volmer, Faraday) |
| L6 | `screening.py` | 이 주장은 타당한가? (ATHENA 4단 판정) |
| L7 | `extension_hooks.py` | 형제 엔진 브리지, 미래 확장 |

---

## 핵심 수식

| # | 이름 | 수식 | 의미 |
|---|------|------|------|
| 1 | Gibbs 자유 에너지 | $\Delta G = \Delta H - T\Delta S$ | 반응이 자발적인가? |
| 2 | Arrhenius 속도 상수 | $k = A \exp(-E_a / RT)$ | 얼마나 빠른가? |
| 3 | 1차 반감기 | $t_{1/2} = \ln 2 / k$ | 절반이 반응하는 데 걸리는 시간 |
| 4 | 속도 법칙 | $r = k [A]^a [B]^b$ | 농도에 따른 반응 속도 |
| 5 | 평형 상수 | $K_{eq} = \exp(-\Delta G° / RT)$ | 평형 위치 |
| 6 | Nernst 전위 | $E = E° - (RT/nF) \ln Q$ | 전기화학 셀 전위 |
| 7 | Faraday 전기분해 | $m = ItM / nF$ | 전극에서 생성되는 질량 |
| 8 | Butler-Volmer | $j = j_0 [\exp(\alpha_a F\eta/RT) - \exp(-\alpha_c F\eta/RT)]$ | 전극 반응 전류 밀도 |

---

## 빠른 시작

```python
from chemical_reaction import (
    assess_chemical_foundation,
    ChemicalSpecies, Phase, Reaction, ReactionTerm,
)

H2 = ChemicalSpecies("H2", 2.016, Phase.GAS)
O2 = ChemicalSpecies("O2", 32.0, Phase.GAS)
H2O = ChemicalSpecies("H2O", 18.015, Phase.LIQUID)

water_formation = Reaction(
    reactants=(ReactionTerm(H2, 2.0), ReactionTerm(O2, 1.0)),
    products=(ReactionTerm(H2O, 2.0),),
    delta_h_kj_per_mol=-571.6,
    delta_s_j_per_mol_k=-326.8,
    activation_energy_kj_per_mol=75.0,
)

report = assess_chemical_foundation(water_formation, temperature_k=298.15)
print(report.verdict)                   # CONSISTENT
print(report.thermodynamic_feasibility) # strongly_favorable
print(report.omega)                     # 0.74
```

---

## 형제 엔진 브리지

| 형제 엔진 | 연결 | 성격 |
|-----------|------|------|
| `Battery_Dynamics_Engine` | OCV ↔ Nernst, Ea ↔ Arrhenius, Butler-Volmer | 직접 연결 |
| `Element_Capture_Foundation` | 전기화학적 추출 ↔ Nernst 전위 | 직접 연결 |
| `TerraCore_Stack` | 전기분해 셀 전압 ↔ 전기화학 | 직접 연결 |
| `Carbon_Composite_Stack` | 경화 반응 ↔ Arrhenius 동역학 | 직접 연결 |
| `Cooking_Process_Foundation` | Maillard 반응 ↔ 동역학 | 직접 연결 |
| `Token_Dynamics_Foundation` | Q/K 균형 ↔ 공급/수요 균형 | 개념적 아날로지 |
| `VectorSpace_102` | `from_chemical_assessment` 어댑터 예정 | 허브 연결 |

---

## ATHENA 스크리닝

| 판정 | 예시 |
|------|------|
| **Positive** | "물 전기분해는 최소 1.23V가 필요하다" |
| **Neutral** | "이 촉매로 Faradaic 효율 90%를 달성했다" |
| **Cautious** | "상온 초전도가 무손실 전기분해를 가능케 한다" |
| **Negative** | "물 분해로 투입 에너지보다 더 많은 에너지를 생산한다" |

**스크리닝 플래그**: 질량 보존 위반, 에너지 보존 위반, 열역학적 비가능성, 영구기관 주장, 활성화 장벽 무시, 평형 한계 무시.

---

## 도메인 매핑

| 도메인 | 모듈 | 핵심 매핑 |
|--------|------|-----------|
| 배터리 전기화학 | `domain_battery.py` | OCV ↔ Nernst, R(T) ↔ Arrhenius, SEI ↔ 부반응 |
| 생명유지 | `domain_life_support.py` | 전기분해, Sabatier CO₂ 환원, 가스 평형 |
| 재료 화학 | `domain_materials.py` | 수지 경화, Maillard, 부식, 소결 |

---

## 현재 한계

- 정밀한 열물성 데이터(NIST)를 내장하지 않는다 — order-of-magnitude 추정만 제공
- 반응 네트워크(다중 연쇄 반응)를 자동으로 해석하지 않는다
- 분자 오비탈, 전자 구조는 범위 밖이다
- 모든 수식은 tree-level이며, 실험 데이터와의 정밀한 비교는 사용자 책임이다
- 높은 Ω가 반드시 정확한 화학을 의미하지 않는다 — 항상 실험 데이터와 교차 검증할 것

---

## 테스트

```
80 passed (0.10s)
```

| 범주 | 테스트 수 |
|------|----------|
| contracts (계약 생성/검증) | 8 |
| species_and_bonds (종/보존) | 8 |
| thermodynamics (열역학) | 10 |
| kinetics (동역학) | 11 |
| equilibrium (평형) | 8 |
| electrochemistry (전기화학) | 10 |
| screening (ATHENA 판정) | 7 |
| domains (도메인 매핑) | 3 |
| extension_hooks | 2 |
| foundation (통합) | 6 |
| health (건강도) | 2 |
| integrity (패키지 정합성) | 5 |

---

*Chemical_Reaction_Foundation v0.1.0 — E5 화학 기초 레이어.*

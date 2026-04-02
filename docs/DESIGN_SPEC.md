# Meterial — 설계 사양서

> **한국어 (정본).** English: [DESIGN_SPEC_EN.md](DESIGN_SPEC_EN.md)  
> 인식론적 위치: **E5 화학** — [EPISTEMIC_LAYER_MAP.md](../../../EPISTEMIC_LAYER_MAP.md)

---

## 1. 왜 이 엔진이 필요한가 — 빈칸 분석

### 현재 상태: 화학을 **쓰는** 엔진은 많지만, **정의하는** 엔진은 없다

| 기존 엔진 | 암묵적으로 쓰는 화학 | 빠진 것 |
|-----------|---------------------|---------|
| `Element_Capture_Foundation` | `ELECTROCHEMICAL_EXTRACTION` 모드, 종별 포집 | Nernst 전위, Butler-Volmer 동역학, 흡착 등온선 |
| `TerraCore_Stack` | 물 전기분해 `2H₂O → 2H₂ + O₂`, mol 기반 인벤토리 | 셀 전압 모델, 과전위, 효율 계산 |
| `Battery_Dynamics_Engine` | Arrhenius 온도 의존 저항, OCV 곡선 | 전극 반응 메커니즘, SEI 화학, 농도 구배 |
| `Carbon_Composite_Stack` | 경화 온도/압력, 사이클 타임 | 수지 경화 반응 동역학, 중합도 |
| `Cooking_Process_Foundation` | Maillard 반응을 "휴리스틱"으로 처리 | 실제 반응 속도론 |
| `FusionCore_Stack` | 핵반응 `D + T → He + n` | (핵물리이므로 화학 범위 밖) |
| `Token_Dynamics_Foundation` | "화학 퍼텐셜"을 구배 동력 아날로지로 사용 | 실제 화학 퍼텐셜 정의 |

### 핵심 빈칸

```
"화학 반응이란 무엇인가?"를 정의하는 기초 레이어가 없다.
```

각 공학 엔진이 화학을 **파라미터로 소비**하지만, 그 파라미터가 **어디서 오는지** 설명하는 층이 없다.  
이것은 "힉스 장이 질량을 만든다"를 정의하지 않고 질량을 쓰는 것과 같다.

---

## 2. 이 엔진의 정체성 — "화학 반응이란 무엇인가?"

### 한 줄 정의

> **Meterial** = 화학 종(species)의 변환, 에너지 교환, 평형, 속도를 추적하는 기초 레이어.  
> 반응이 **왜 일어나는지**(열역학), **얼마나 빨리 일어나는지**(동역학), **어디서 멈추는지**(평형)를 관측할 수 있는 환경을 제공한다.

### 이 엔진이 **아닌** 것

- 분자 동역학(MD) 시뮬레이터가 아니다
- 양자 화학 계산기가 아니다
- 화학 공장 공정 설계 소프트웨어가 아니다
- 정밀한 열물성(NIST) 데이터베이스가 아니다

이 엔진은 Higgs_Phenomenology처럼 **"화학이 무엇인가"를 층으로 쪼개는 현상학 기초 레이어**다.  
tree-level 수식과 order-of-magnitude 추정으로 **반응의 뼈대 구조**를 관측하고,  
과장된 주장을 걸러내는 스크리닝을 제공한다.

---

## 3. 핵심 질문 — 이 엔진이 답하는 것

| # | 질문 | 해당 레이어 |
|---|------|------------|
| 1 | 화학 종(species)이란 무엇인가? 결합(bond)이란 무엇인가? | L1 |
| 2 | 이 반응은 에너지적으로 유리한가? (ΔG < 0?) | L2 |
| 3 | 이 반응은 얼마나 빠른가? (활성화 에너지, 촉매) | L3 |
| 4 | 이 반응은 어디서 멈추는가? (평형 상수, 르샤틀리에) | L4 |
| 5 | 전자가 교환되면 어떤 일이 생기는가? (전기화학) | L5 |
| 6 | 이 화학적 주장은 물리적으로 타당한가? | L6 |

---

## 4. 레이어 구조

```
chemical_reaction/
├── __init__.py
├── contracts.py          ← L0: 모든 데이터 계약
├── constants.py          ← 기본 상수 (R, kB, F, NA)
├── species_and_bonds.py  ← L1: 종, 결합, 질량 보존
├── thermodynamics.py     ← L2: ΔG, ΔH, ΔS, 자발성
├── kinetics.py           ← L3: Arrhenius, 반응 차수, 반감기, 촉매
├── equilibrium.py        ← L4: K_eq, Q vs K, 르샤틀리에
├── electrochemistry.py   ← L5: Nernst, Butler-Volmer, 패러데이
├── screening.py          ← L6: ATHENA 4단 판정
├── extension_hooks.py    ← L7: 형제 엔진 브리지, 미래 확장
├── foundation.py         ← 통합 진입점
├── domain_battery.py     ← 도메인 매핑: 배터리 전기화학
├── domain_life_support.py ← 도메인 매핑: 생명유지 (전기분해, 가스 순환)
└── domain_materials.py   ← 도메인 매핑: 재료 (경화, 중합, 부식)
```

---

### L0 — Contracts (계약)

```python
@dataclass(frozen=True)
class ChemicalSpecies:
    formula: str                    # "H2O", "CO2", "ATP"
    molar_mass_g_per_mol: float
    phase: Phase                    # GAS, LIQUID, SOLID, AQUEOUS, PLASMA
    charge: int = 0                 # 이온 전하

class Phase(str, Enum):
    GAS = "gas"
    LIQUID = "liquid"
    SOLID = "solid"
    AQUEOUS = "aqueous"
    PLASMA = "plasma"

@dataclass(frozen=True)
class Reaction:
    """화학 반응의 최소 계약."""
    reactants: tuple[ReactionTerm, ...]   # (계수, 종)
    products: tuple[ReactionTerm, ...]    # (계수, 종)
    delta_h_kj_per_mol: float | None = None   # 반응 엔탈피
    delta_s_j_per_mol_k: float | None = None  # 반응 엔트로피
    activation_energy_kj_per_mol: float | None = None

@dataclass(frozen=True)
class ReactionTerm:
    species: ChemicalSpecies
    coefficient: float              # 화학양론 계수

@dataclass(frozen=True)
class ThermodynamicState:
    temperature_k: float
    pressure_pa: float = 101325.0   # 1 atm
    delta_g_kj_per_mol: float | None = None
    spontaneous: bool | None = None

@dataclass(frozen=True)
class KineticState:
    rate_constant_k: float
    order: float
    half_life_s: float | None = None
    catalyst_effect: str = "none"

@dataclass(frozen=True)
class ElectrochemicalCell:
    anode_reaction: Reaction
    cathode_reaction: Reaction
    standard_potential_v: float     # E°
    n_electrons: int
    actual_potential_v: float | None = None

@dataclass(frozen=True)
class ChemicalClaimPayload:
    claim_text: str
    violates_mass_conservation: bool = False
    violates_energy_conservation: bool = False
    violates_thermodynamic_feasibility: bool = False
    claims_over_unity: bool = False
    claims_perpetual_reaction: bool = False
    ignores_activation_barrier: bool = False
    ignores_equilibrium_limit: bool = False

@dataclass(frozen=True)
class ChemicalFoundationReport:
    layers_inspected: int
    omega: float                    # 0.0–1.0
    verdict: str
    thermodynamic_feasibility: str
    kinetic_accessibility: str
    equilibrium_position: str
    key_risk: str
    notes: list[str]
```

---

### L1 — Species & Bonds: "무엇이 존재하는가?"

**핵심**: 반응 전에 먼저 **"무엇이 있는가"**를 정의해야 한다.

| 개념 | 설명 |
|------|------|
| 화학 종 (Species) | 화학식, 몰질량, 상(phase), 전하 |
| 결합 에너지 (Bond Energy) | 결합을 끊는 데 필요한 에너지 (order-of-magnitude) |
| 질량 보존 | 반응 전후 원자 수 보존 검증 |
| 전하 보존 | 반응 전후 전하 합 보존 검증 |

```python
def verify_mass_balance(reaction: Reaction) -> bool:
    """반응식의 원자 수 보존을 검증."""

def verify_charge_balance(reaction: Reaction) -> bool:
    """반응식의 전하 보존을 검증."""

def estimate_bond_energy_kj_per_mol(bond_type: str) -> float:
    """대표적 결합 에너지 반환 (C-H: ~413, O=O: ~498, C=O: ~799 등)."""
```

**중요한 경계**: 이 엔진은 원자 구조나 오비탈을 다루지 않는다.  
"H₂O는 H 2개와 O 1개로 구성된다"는 다루지만,  
"산소의 2p 오비탈이 어떻게 혼성되는가"는 범위 밖이다.

---

### L2 — Thermodynamics: "이 반응은 일어날 수 있는가?"

**핵심 수식**:

$$\Delta G = \Delta H - T \Delta S$$

- $\Delta G < 0$: 자발적 (exergonic)
- $\Delta G > 0$: 비자발적 (endergonic) — 외부 에너지 필요
- $\Delta G = 0$: 평형

| 함수 | 역할 |
|------|------|
| `gibbs_free_energy(delta_h, delta_s, T)` | ΔG 계산 |
| `is_spontaneous(delta_g)` | 자발성 판정 |
| `enthalpy_from_bond_energies(reaction)` | 결합 에너지 차이로 ΔH 추정 |
| `entropy_sign_heuristic(reaction)` | 기체 몰수 변화로 ΔS 부호 추정 |

**주의점 (ATHENA용)**:
- ΔG < 0이라고 반드시 빠른 반응은 아니다 (동역학 필요)
- 실제 ΔH, ΔS는 정밀 데이터가 필요하며, 이 엔진은 order-of-magnitude 추정만 제공
- "에너지가 나오니까 무조건 쓸모있다"는 과장 (효율·수율 별도)

---

### L3 — Kinetics: "얼마나 빠른가?"

**핵심 수식**:

$$k = A \cdot \exp\left(-\frac{E_a}{RT}\right) \quad \text{(Arrhenius)}$$

| 함수 | 역할 |
|------|------|
| `arrhenius_rate(A, Ea, T)` | 속도 상수 계산 |
| `half_life(k, order)` | 반감기 (1차: $t_{1/2} = \ln 2 / k$) |
| `rate_law(k, concentrations, orders)` | $r = k [A]^a [B]^b$ |
| `catalyst_effect_on_ea(Ea_uncatalyzed, Ea_catalyzed)` | Ea 감소율로 촉매 효과 관측 |
| `temperature_doubling_rule(k1, k2, T1, T2)` | "온도 10K 올리면 속도 2배" 규칙 검증 |

**주의점**:
- Arrhenius는 가장 단순한 모델이며, 실제 반응은 더 복잡할 수 있다
- 촉매는 Ea를 낮출 뿐, 평형 위치를 바꾸지 않는다 ← 이것이 ATHENA 스크리닝 포인트

**Battery_Dynamics 연결**:  
배터리 엔진의 `ECMParams`에 이미 `Ea_r_ev`(Arrhenius 활성화 에너지)가 있다.  
이 엔진의 `arrhenius_rate()`가 그 파라미터의 **이론적 뒷받침**이 된다.

---

### L4 — Equilibrium: "어디서 멈추는가?"

**핵심 수식**:

$$K_{eq} = \exp\left(-\frac{\Delta G°}{RT}\right)$$

| 함수 | 역할 |
|------|------|
| `equilibrium_constant(delta_g_standard, T)` | K_eq 계산 |
| `reaction_quotient(concentrations, reaction)` | Q 계산 |
| `le_chatelier_shift(Q, K)` | Q < K → 정반응 진행, Q > K → 역반응 진행 |
| `equilibrium_composition_estimate(K, initial_concentrations)` | 간단한 평형 조성 추정 |

**Token_Dynamics 연결**:  
Q vs K 비교는 Token의 "공급-수요 균형"과 구조적으로 동일하다.  
Q < K는 "공급 부족" (정반응으로 더 만들어야), Q > K는 "공급 과잉" (역반응으로 소비).  
이것은 **개념적 아날로지**이며, 물리적 동치가 아니다.

---

### L5 — Electrochemistry: "전자가 교환되면?"

**핵심 수식**:

$$E = E° - \frac{RT}{nF} \ln Q \quad \text{(Nernst)}$$

| 함수 | 역할 |
|------|------|
| `nernst_potential(E_standard, n, Q, T)` | 실제 전위 계산 |
| `cell_voltage(anode_E, cathode_E)` | 셀 전압 = E_cathode - E_anode |
| `faraday_mass(I, t, M, n)` | 전기분해 생성물 질량 ($m = ItM / nF$) |
| `overpotential_estimate(eta_activation, eta_ohmic, eta_concentration)` | 과전위 분류 |
| `butler_volmer_current_density(j0, alpha, eta, T)` | 전극 반응 전류밀도 (tree-level) |

**Element_Capture 연결**:  
`CaptureMode.ELECTROCHEMICAL_EXTRACTION`은 Nernst 전위가 뒷받침해야 한다.  
"어떤 전위에서 이 종이 분리되는가?"를 이 엔진이 제공.

**TerraCore 연결**:  
물 전기분해의 이론 전압 (1.23V at STP)과 실제 전압 (1.8–2.0V)의 차이가  
과전위 모델로 설명된다.

**Battery_Dynamics 연결**:  
`ECMParams.ocv_table`의 OCV는 사실 Nernst 전위의 SOC 의존 버전이다.  
Butler-Volmer는 배터리 엔진이 "범위 밖"으로 명시한 부분인데,  
이 화학 엔진에서 tree-level로 제공할 수 있다.

---

### L6 — Screening / ATHENA: "이 화학적 주장은 타당한가?"

| 판정 | 예시 |
|------|------|
| **Positive** | "물 전기분해는 최소 1.23V가 필요하다" |
| **Neutral** | "이 촉매로 Faradaic 효율 90%를 달성했다" (가능하지만 데이터 필요) |
| **Cautious** | "상온 초전도가 무손실 전기분해를 가능케 한다" (관련은 있지만 과장 위험) |
| **Negative** | "이 장치는 물 분해로 투입 에너지보다 더 많은 에너지를 생산한다" (열역학 위반) |

**스크리닝 플래그**:
- `violates_mass_conservation`: 원자가 생성/소멸됨
- `violates_energy_conservation`: 에너지 보존 위반
- `violates_thermodynamic_feasibility`: ΔG 방향과 반대되는 주장
- `claims_over_unity`: 투입 대비 출력 > 1 (영구 기관)
- `claims_perpetual_reaction`: 무한 반복 반응 (평형 무시)
- `ignores_activation_barrier`: 촉매 없이 빠른 반응 주장
- `ignores_equilibrium_limit`: 평형 상수를 무시한 수율 주장

---

### L7 — Extension Hooks: 형제 엔진 브리지

| 형제 엔진 | 브리지 내용 | 성격 |
|-----------|------------|------|
| `Battery_Dynamics_Engine` | Arrhenius Ea ↔ kinetics, OCV ↔ Nernst, Butler-Volmer | **직접 연결** |
| `Element_Capture_Foundation` | electrochemical extraction ↔ Nernst 전위 | **직접 연결** |
| `TerraCore_Stack` | 전기분해 셀 전압 ↔ electrochemistry | **직접 연결** |
| `Carbon_Composite_Stack` | 경화 반응 ↔ kinetics (Arrhenius) | **직접 연결** |
| `Cooking_Process_Foundation` | Maillard 반응 ↔ kinetics | **직접 연결** |
| `Token_Dynamics_Foundation` | Q/K 균형 ↔ 공급/수요 균형 | **개념적 아날로지** |
| `Higgs_Phenomenology_Foundation` | 질량 생성 ↔ 결합 에너지 | **개념적 아날로지** |
| `Antimatter_Phenomenology_Engine` | 쌍소멸 ↔ 반응 에너지학 | **개념적 아날로지** |
| VectorSpace_102 | `from_chemical_assessment` 어댑터 | **허브 연결** |

**미래 확장 태그**:
- `molecular_dynamics_bridge`
- `quantum_chemistry_bridge`
- `biochemistry_reaction_networks`
- `corrosion_and_degradation`
- `combustion_kinetics`
- `atmospheric_photochemistry`

---

## 5. 핵심 수식 요약 (MVP)

| # | 이름 | 수식 | 레이어 |
|---|------|------|--------|
| 1 | Gibbs 자유 에너지 | $\Delta G = \Delta H - T\Delta S$ | L2 |
| 2 | Arrhenius 속도 상수 | $k = A \exp(-E_a / RT)$ | L3 |
| 3 | 1차 반감기 | $t_{1/2} = \ln 2 / k$ | L3 |
| 4 | 속도 법칙 | $r = k [A]^a [B]^b$ | L3 |
| 5 | 평형 상수 | $K_{eq} = \exp(-\Delta G° / RT)$ | L4 |
| 6 | Nernst 전위 | $E = E° - (RT/nF) \ln Q$ | L5 |
| 7 | Faraday 전기분해 | $m = ItM / nF$ | L5 |
| 8 | Butler-Volmer | $j = j_0 [\exp(\alpha_a F \eta / RT) - \exp(-\alpha_c F \eta / RT)]$ | L5 |

---

## 6. 도메인 매핑 (L3 확장)

### domain_battery.py — 배터리 전기화학

| 개념 | 매핑 |
|------|------|
| OCV(SOC) | Nernst 전위의 SOC 함수 |
| 내부 저항 R(T) | Arrhenius 동역학의 저항 버전 |
| SEI 성장 | 부반응 동역학 (tree-level) |
| 과전위 | activation + ohmic + concentration |

### domain_life_support.py — 생명유지 전기분해/가스 순환

| 개념 | 매핑 |
|------|------|
| 물 전기분해 | $2H_2O \rightarrow 2H_2 + O_2$, E° = 1.23V |
| Sabatier 반응 | $CO_2 + 4H_2 \rightarrow CH_4 + 2H_2O$ |
| 이론 전압 vs 실제 전압 | 과전위 모델 |
| mol/s 수율 | Faraday 법칙 |

### domain_materials.py — 재료 화학

| 개념 | 매핑 |
|------|------|
| 수지 경화 | Arrhenius + 반응 차수 모델 |
| 부식 | 전기화학적 부식 셀 (anode/cathode) |
| 소결/확산 | 고체 반응 동역학 |

---

## 7. ATHENA 건강도

```python
@dataclass(frozen=True)
class ChemicalHealthReport:
    omega_thermodynamic: float    # ΔG 방향/크기 합리성
    omega_kinetic: float          # 반응 속도 합리성
    omega_equilibrium: float      # 평형 위치 합리성
    omega_conservation: float     # 질량/전하/에너지 보존
    omega_electrochemical: float  # 전기화학 일관성 (해당 시)
    composite_omega: float        # 가중 평균
    verdict: str                  # CONSISTENT, PLAUSIBLE, QUESTIONABLE, IMPOSSIBLE
```

**Cold audit 원칙 유지**: 
- composite_omega > 0.95면 경고 (현실 마찰 미반영 의심)
- 단일 축이 0.3 미만이면 verdict를 QUESTIONABLE 이하로 강제

---

## 8. 테스트 계획

| 범주 | 예상 테스트 수 | 내용 |
|------|---------------|------|
| contracts | 8 | 데이터 계약 생성·검증 |
| species_and_bonds | 6 | 질량/전하 보존, 결합 에너지 |
| thermodynamics | 10 | ΔG 계산, 자발성, 엔탈피 추정 |
| kinetics | 10 | Arrhenius, 반감기, 속도 법칙, 촉매 효과 |
| equilibrium | 8 | K_eq, Q vs K, 르샤틀리에 |
| electrochemistry | 10 | Nernst, Faraday, Butler-Volmer, 과전위 |
| screening | 12 | ATHENA 4단 판정 (보존법칙 위반, 영구기관 등) |
| domain mappings | 8 | 배터리/생명유지/재료 |
| health | 6 | 5축 건강도, cold audit |
| integrity | 6 | 패키지 정합성 |
| **합계** | **~84** | |

---

## 9. 파일 구조 (전체)

```
Chemical_Reaction_Foundation/
├── chemical_reaction/
│   ├── __init__.py
│   ├── contracts.py
│   ├── constants.py
│   ├── species_and_bonds.py
│   ├── thermodynamics.py
│   ├── kinetics.py
│   ├── equilibrium.py
│   ├── electrochemistry.py
│   ├── screening.py
│   ├── extension_hooks.py
│   ├── foundation.py
│   ├── domain_battery.py
│   ├── domain_life_support.py
│   └── domain_materials.py
├── tests/
│   ├── conftest.py
│   ├── test_chemical_foundation.py
│   └── test_package_integrity.py
├── scripts/
│   ├── generate_signature.py
│   └── verify_signature.py
├── docs/
│   ├── DESIGN_SPEC.md          ← 이 문서
│   ├── DESIGN_SPEC_EN.md
│   ├── LAYER_STACK.md
│   └── LAYER_STACK_EN.md
├── README.md
├── README_EN.md
├── VERSION
├── pyproject.toml
├── CHANGELOG.md
└── SIGNATURE.sha256
```

---

## 10. VectorSpace 연결 계획

`VectorSpace_102`에 추가할 어댑터:

```python
def from_chemical_assessment(report) -> EngineStepResult:
    return EngineStepResult(
        engine_id="chemical_reaction",
        state={
            "chemical_reaction.omega": _safe_float(report, "composite_omega"),
            "chemical_reaction.thermo": _safe_float(report, "omega_thermodynamic"),
            "chemical_reaction.kinetic": _safe_float(report, "omega_kinetic"),
        },
        derived={...},
        observation={...},
    )
```

`axis_registry.py`에 추가할 프리셋:

```python
CR_THERMO = VectorAxisSpec(key="omega_thermodynamic", label="thermodynamic feasibility", unit="0-1", domain="chemical")
CR_KINETIC = VectorAxisSpec(key="omega_kinetic", label="kinetic accessibility", unit="0-1", domain="chemical")
CR_EQUILIBRIUM = VectorAxisSpec(key="omega_equilibrium", label="equilibrium position", unit="0-1", domain="chemical")
CR_CONSERVATION = VectorAxisSpec(key="omega_conservation", label="conservation compliance", unit="0-1", domain="chemical")
CR_ELECTROCHEM = VectorAxisSpec(key="omega_electrochemical", label="electrochemical consistency", unit="0-1", domain="chemical")
```

---

## 11. 구현 순서

| 단계 | 내용 | 의존성 |
|------|------|--------|
| 1 | `contracts.py` + `constants.py` | 없음 |
| 2 | `species_and_bonds.py` | L0 |
| 3 | `thermodynamics.py` | L0, L1 |
| 4 | `kinetics.py` | L0, L2 |
| 5 | `equilibrium.py` | L0, L2 |
| 6 | `electrochemistry.py` | L0, L2, L3 |
| 7 | `screening.py` | L0 |
| 8 | `domain_*.py` (3개) | L1–L5 |
| 9 | `foundation.py` | 전체 |
| 10 | `extension_hooks.py` | 전체 |
| 11 | 테스트 + README + 서명 | 전체 |

---

*Meterial 설계 사양서 v0.1. CONCEPT.md §4.1 인식론적 계층도의 E5(화학) 빈칸을 채우기 위한 설계.*

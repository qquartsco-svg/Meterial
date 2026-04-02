# Element Registry

> `3_chemical` 안 원소 foundation의 상태, 정본 위치, 연결 대상을 추적하는 등록부.

## 목적

원소 폴더가 늘어날수록 먼저 필요한 건 새 폴더가 아니라 **통제 기준**이다.  
이 문서는 원소 foundation을 추가하거나 승격할 때 다음을 먼저 고정한다.

- 원소명 / 기호 / 원자번호
- 현재 상태: `planned / scaffold / active`
- 허브 내 역할
- 정본 위치
- 직접 연결되는 형제 엔진

---

## Registry

| Z | Symbol | Name | Status | Hub Role | Source of Truth | Primary Links |
|---|--------|------|--------|----------|-----------------|---------------|
| 1 | H | Hydrogen | `active` | element foundation | `3_chemical/Hydrogen_Foundation` | `Chemical_Reaction_Foundation`, `Element_Capture_Foundation`, `Battery_Dynamics_Engine`, `Carbon_Composite_Stack` |
| 2 | He | Helium | `active` | element foundation | `3_chemical/Helium_Foundation` | `Chemical_Reaction_Foundation`, `Element_Capture_Foundation`, `FusionCore_Stack` |
| 3 | Li | Lithium | `active` | element foundation | `3_chemical/Lithium_Foundation` | `Chemical_Reaction_Foundation`, `Battery_Dynamics_Engine` |
| 7 | N | Nitrogen | `active` | element foundation | `3_chemical/Nitrogen_Foundation` | `Chemical_Reaction_Foundation`, `Element_Capture_Foundation`, `TerraCore_Stack` |
| 8 | O | Oxygen | `active` | element foundation | `3_chemical/Oxygen_Foundation` | `Chemical_Reaction_Foundation`, `Element_Capture_Foundation`, `Hydrogen_Foundation`, `TerraCore_Stack` |
| 14 | Si | Silicon | `active` | element foundation | `3_chemical/Silicon_Foundation` | `Chemical_Reaction_Foundation`, `Foundry_Implementation_Engine`, `Fabless` |
| 15 | P | Phosphorus | `active` | element foundation | `3_chemical/Phosphorus_Foundation` | `Chemical_Reaction_Foundation`, `Token_Dynamics_Foundation`, `TerraCore_Stack` |
| 6 | C | Carbon | `planned` | element foundation | `planned` | `Chemical_Reaction_Foundation`, `Carbon_Composite_Stack`, `Element_Capture_Foundation`, `TerraCore_Stack` |
| 11 | Na | Sodium | `planned` | element foundation | `planned` | `Chemical_Reaction_Foundation`, `Battery_Dynamics_Engine` |
| 12 | Mg | Magnesium | `planned` | element foundation | `planned` | `Chemical_Reaction_Foundation`, `Battery_Dynamics_Engine`, `Carbon_Composite_Stack` |
| 17 | Cl | Chlorine | `planned` | element foundation | `planned` | `Chemical_Reaction_Foundation`, `Hydrogen_Foundation`, `TerraCore_Stack` |

---

## Reading Rules

1. `active`
   - README / tests / signature가 있고 foundation로 읽을 수 있다.
2. `scaffold`
   - 폴더는 있으나 규약이 아직 덜 닫혔다.
3. `planned`
   - 아직 폴더를 만들기 전, 필요성과 연결만 registry에 적는다.

새 원소를 추가할 때는 **폴더를 먼저 만들지 말고 이 registry를 먼저 갱신**하는 것이 원칙이다.

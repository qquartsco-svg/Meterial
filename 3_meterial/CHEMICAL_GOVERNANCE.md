# Chemical Governance

> `3_meterial` 허브가 커져도 드리프트하지 않도록 하기 위한 운영 규칙.

## 1. Three-Layer Rule

`3_meterial` 안의 엔진은 반드시 아래 셋 중 하나로 분류한다.

1. **Chemical root**
   - 예: `Chemical_Reaction_Foundation`
   - 역할: 모든 화학 엔진의 공통 문법
2. **Element foundation**
   - 예: `Hydrogen_Foundation`, `Helium_Foundation`, `Lithium_Foundation`
   - 역할: 특정 원소의 조달·저장·안전·스크리닝
3. **Applied chemistry engine**
   - 예: `Battery_Dynamics_Engine`, `Carbon_Composite_Stack`, `Cooking_Process_Foundation`
   - 역할: root/element foundation을 소비하는 응용 엔진

이 셋이 섞이면 구조가 금방 꼬인다.

---

## 2. Source-of-Truth Rule

모든 폴더는 아래 둘 중 하나여야 한다.

- **정본**
- **허브 복사본**

복사본이라면 README나 별도 문서에 반드시 정본 위치를 남긴다.

원칙:

1. 기능 수정은 정본에서 먼저 한다.
2. `3_meterial`은 흐름 보기와 graft 실험을 위한 허브다.
3. 복사본이 많아질수록 `manifest`, `symlink`, `SOURCE_OF_TRUTH` 안내가 우선된다.

---

## 3. Admission Rule

새 원소 foundation을 추가할 때는 아래 순서를 따른다.

1. [ELEMENT_REGISTRY.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/ELEMENT_REGISTRY.md)에 등록
2. 해당 원소가 foundation 후보인지 판단
3. [ELEMENT_FOUNDATION_TEMPLATE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/ELEMENT_FOUNDATION_TEMPLATE.md) 기준으로 scaffold 생성
4. README에 root/applied link를 명시

즉 **폴더 생성보다 registry 등록이 먼저**다.

---

## 4. Naming Rule

원소 foundation 이름은 다음을 따른다.

- `<Element>_Foundation`

예:

- `Hydrogen_Foundation`
- `Helium_Foundation`
- `Lithium_Foundation`

응용 엔진은 원소명이 아니라 도메인명을 따른다.

- `Battery_Dynamics_Engine`
- `Carbon_Composite_Stack`
- `Cooking_Process_Foundation`

---

## 5. Bridge Rule

모든 element foundation은 최소 하나의 root link와 하나의 applied link를 가져야 한다.

- root link:
  - `Chemical_Reaction_Foundation`
- applied link:
  - 배터리, 포집, 추진, 재료, 요리, 생명유지 중 하나 이상

원소 foundation이 완전히 고립돼 있으면, 허브에 들어올 이유가 약하다.

---

## 6. Hygiene Rule

정본 수준으로 관리하려면 최소한 아래를 갖춘다.

- tests
- signature
- README / README_EN
- version / changelog

가능하면 추가:

- `release_check.py`
- `cleanup_generated.py`
- package identity test

---

## 7. Long-Term Direction

`3_meterial`은 장기적으로 다음 흐름을 중심으로 확장한다.

```text
Chemical_Reaction_Foundation
  -> element foundations (H, He, Li, N, O, P, Si, ...)
  -> applied chemistry engines
  -> life support / energy / materials / industry
```

즉 목표는 “주기율표를 전부 복사해 넣는 것”이 아니라,  
**화학 root -> 원소 foundation -> 응용 chemistry**의 흐름을 유지하는 것이다.

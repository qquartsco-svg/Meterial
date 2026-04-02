# Element Foundation Template

> `3_chemical` 안에 새 원소 foundation을 추가할 때 따라야 하는 최소 템플릿.

## 목적

주기율표처럼 쌓아가더라도, 원소 foundation이 제각각 생기면 나중에 연결이 끊긴다.  
이 템플릿은 모든 원소 엔진이 최소한 같은 문법으로 읽히게 하기 위한 기준이다.

---

## 최소 폴더 구조

```text
Element_X_Foundation/
├── README.md
├── README_EN.md
├── CHANGELOG.md
├── VERSION
├── pyproject.toml
├── SIGNATURE.sha256
├── scripts/
│   ├── generate_signature.py
│   └── verify_signature.py
├── tests/
│   ├── conftest.py
│   └── test_<element>_foundation.py
└── <element>/
    ├── __init__.py
    ├── constants.py
    ├── contracts.py
    ├── properties.py
    ├── foundation.py
    ├── screening.py
    └── extension_hooks.py
```

---

## Optional Modules

원소 성격에 따라 아래를 선택적으로 추가한다.

- `production.py`
- `sourcing.py`
- `extraction.py`
- `storage.py`
- `safety.py`
- `domain_space.py`
- `domain_grid.py`
- `domain_transport.py`
- `domain_battery.py`
- `domain_agriculture.py`

원소마다 이름은 달라도, 역할은 아래 중 하나로 읽혀야 한다.

- 조달/생산
- 저장/수송
- 안전/제약
- 도메인 응용

---

## Required Design Questions

새 원소 foundation은 최소한 아래 질문에 답해야 한다.

1. 이 원소의 **핵심 물성**은 무엇인가?
2. 이 원소는 **어떻게 얻는가**?
3. 이 원소는 **어떻게 저장/수송**되는가?
4. 이 원소의 **핵심 위험**은 무엇인가?
5. 어떤 주장이 들어왔을 때 **무엇을 과장으로 볼 것인가**?
6. 이 원소는 어떤 **형제 엔진과 직접 연결**되는가?

---

## Required Cross-Links

모든 element foundation은 README에 아래 링크를 적는 것을 권장한다.

- `Chemical_Reaction_Foundation`
- 관련 자원/응용 엔진 1개 이상

예:

- Hydrogen -> `Element_Capture_Foundation`, `Battery_Dynamics_Engine`, `Carbon_Composite_Stack`
- Oxygen -> `Hydrogen_Foundation`, `Element_Capture_Foundation`, `TerraCore_Stack`
- Lithium -> `Battery_Dynamics_Engine`
- Helium -> `FusionCore_Stack`, `Element_Capture_Foundation`

---

## Promotion Rule

모든 원소가 foundation이 되어야 하는 건 아니다.

- `foundation candidate`
  - 산업/우주/생명유지 연결이 강함
- `bridge-only candidate`
  - 별도 foundation보다 기존 엔진 hook이 더 적절
- `applied-only`
  - 원소 자체보다 공정/재료 쪽이 핵심

즉 `3_chemical`은 주기율표 전체를 무조건 엔진화하는 곳이 아니라,  
**foundation으로 세울 가치가 있는 원소를 선별해서 쌓는 허브**다.

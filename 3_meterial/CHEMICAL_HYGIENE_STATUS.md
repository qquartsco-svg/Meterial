# Chemical Hygiene Status

> `3_meterial` 허브 안에서 테스트/서명/복사본 위생 상태를 추적하는 문서.

## 현재 판정

`3_meterial`의 개념 흐름은 현재 다음 순서로 안정적이다.

```text
Chemical_Reaction_Foundation
  -> element foundations
  -> applied chemistry engines
```

즉 레이어 구조 자체보다,
현재 남은 리스크는 **복사본 위생과 드리프트 관리** 쪽에 더 가깝다.

---

## 테스트 상태

- `Chemical_Reaction_Foundation` + `Hydrogen_Foundation` + `Helium_Foundation`
  - `191 passed`
- `Lithium_Foundation` + `Nitrogen_Foundation` + `Oxygen_Foundation`
  - `32 passed`
- `Phosphorus_Foundation` + `Silicon_Foundation`
  - `14 passed`
- `Battery_Dynamics_Engine`
  - `252 passed`
- `Cooking_Process_Foundation`
  - `28 passed`
- `Element_Capture_Foundation`
  - `35 passed`

허브에서 직접 확인된 합산 테스트는 `664 passed`다.

---

## 서명 상태

### currently aligned

- `Chemical_Reaction_Foundation`
- `Hydrogen_Foundation`
- `Helium_Foundation`
- `Lithium_Foundation`
- `Nitrogen_Foundation`
- `Oxygen_Foundation`
- `Phosphorus_Foundation`
- `Silicon_Foundation`

### requires periodic refresh in hub copy

- `Element_Capture_Foundation`
- `Carbon_Composite_Stack`

이 둘은 허브 복사본에서 README/example가 보수될 때
정본과 무관하게 로컬 manifest를 다시 맞춰야 할 수 있다.

---

## 위생 부채

### cleaned in hub

- `.DS_Store`
  - `3_meterial/`
  - `Battery_Dynamics_Engine/`
  - `Chemical_Reaction_Foundation/`
  - `Cooking_Process_Foundation/`
  - `Hydrogen_Foundation/`
- `.pytest_cache`
  - `Cooking_Process_Foundation/`
- empty duplicate copy traces
  - `Element_Capture_Foundation/docs 2`
  - `Element_Capture_Foundation/element_capture 2`
  - `Element_Capture_Foundation/examples 2`
  - `Element_Capture_Foundation/scripts 2`
  - `Element_Capture_Foundation/tests 2`

위 항목들은 현재 허브 복사본에서 정리 완료 상태다.

### remaining hygiene attention

- 복사본 엔진의 서명은 정본과 분리되어 drift할 수 있다.
- `3_meterial` 전체에는 아직 공통 `release_check`가 없다.
- 일부 복사본은 허브 기준 import 보수에 의존하므로, 정본 갱신 시 재확인이 필요하다.

---

## 운영 원칙

1. 기능 수정은 정본에서 먼저 한다.
2. 허브 복사본은 연결 흐름을 읽기 위한 용도로 유지한다.
3. 서명 mismatch는 복사본 drift 신호로 보고, 허브 수준에서만 정리한다.
4. 중복 흔적 삭제는 정본 구조 확인 후에만 한다.

---

## 다음 정리 순서

1. 서명 mismatch가 난 허브 복사본 manifest를 먼저 재정렬
2. 새 복사본을 추가할 때는 `SOURCE_OF_TRUTH.md`를 함께 만든다
3. 허브 전체 smoke/release check 문서를 장기적으로 추가한다

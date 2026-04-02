# Folder Structure

> `3_meterial`의 실제 폴더 배치와, 사람이 읽어야 하는 개념 레이어를 분리해서 설명하는 문서.

## 왜 이 문서가 필요한가

`3_meterial`은 지금 **flat layout** 으로 유지되고 있다.
즉 폴더 이름만 보면

- root
- element
- applied

가 한 줄에 섞여 보인다.

이 배치는 기존 링크와 복사본 호환성에는 유리하지만,
처음 보는 사람에게는 흐름이 바로 드러나지 않는다.

그래서 실제 배치를 크게 옮기기 전에,
먼저 **읽는 규칙**을 고정한다.

---

## 현재 실제 배치

```text
3_meterial/
  Chemical_Reaction_Foundation
  Hydrogen_Foundation
  Helium_Foundation
  Lithium_Foundation
  Nitrogen_Foundation
  Oxygen_Foundation
  Phosphorus_Foundation
  Silicon_Foundation
  Element_Capture_Foundation
  Battery_Dynamics_Engine
  Carbon_Composite_Stack
  Cooking_Process_Foundation
```

---

## 개념 레이어로 읽는 법

```text
Chemical root
  -> Chemical_Reaction_Foundation

Element foundations
  -> Hydrogen_Foundation
  -> Helium_Foundation
  -> Lithium_Foundation
  -> Nitrogen_Foundation
  -> Oxygen_Foundation
  -> Phosphorus_Foundation
  -> Silicon_Foundation

Applied chemistry engines
  -> Element_Capture_Foundation
  -> Battery_Dynamics_Engine
  -> Carbon_Composite_Stack
  -> Cooking_Process_Foundation
```

즉 실제 폴더는 평평하지만,
읽는 흐름은 항상

`root -> element -> applied`

순서를 따른다.

---

## 수정 원칙

1. 실제 폴더를 바로 대이동하지 않는다.
2. 먼저 README, registry, governance, source-of-truth 표식을 고정한다.
3. 복사본 엔진은 정본 위치를 명시한다.
4. 새 원소는 flat layout에 바로 추가하지 않고 registry부터 갱신한다.

---

## 장기 방향

장기적으로는 다음 두 방식 중 하나로 더 명확하게 갈 수 있다.

1. `manifest` 기반
   - 실제 폴더는 유지
   - root/element/applied를 manifest가 설명
2. `symlink` 기반
   - 정본은 한 곳에 두고
   - `3_meterial`에는 연결만 둠

지금은 두 방식을 준비하는 과도기이며,
따라서 `3_meterial`은 **structure-readable hub** 로 유지하는 것이 맞다.

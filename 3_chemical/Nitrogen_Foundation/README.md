> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# Nitrogen_Foundation v0.1.0

**질소(N₂)** 는 대기의 주성분이지만 **반응적으로는 둔화**되어 있어, 공업적 **고정(Haber–Bosch)** 과 **공기 분리**가 핵심 축이다.

## 레이어

- `properties` — N₂ 물성  
- `air_separation` — 극저온 ASU (카툰)  
- `fixation` — Haber 평형 카툰 (정밀 반응기 아님)  
- `storage` — 액체 질소 끓어오름  
- `safety` — 질식·저온  
- `screening` — 무상 비료·대기 조성 오류  
- `extension_hooks` — H₂, Chemical, Capture, TerraCore  

## 빠른 시작

```python
from nitrogen import run_nitrogen_foundation, NitrogenClaimPayload

r = run_nitrogen_foundation()
print(r.fixation.nh3_equilibrium_mole_fraction)

r2 = run_nitrogen_foundation(NitrogenClaimPayload("", claimed_free_fertilizer=True))
print(r2.screening.flags)
```

## 한계

Haber 모듈은 **평형 카툰**이며 촉매·동역학·플랜트 물류는 포함하지 않는다.

`pytest tests/ -v`

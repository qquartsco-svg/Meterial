> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# Lithium_Foundation v0.1.0

리튬은 배터리 시대의 핵심 원소다. 이 엔진은 **채굴/정제 → 배터리 성능 → 열안전 → 재활용 필요성**을 기초 레이어로 본다.

## 레이어
- `properties` — Li 물성
- `extraction` — brine vs hard-rock
- `battery` — LFP/NMC 프로파일
- `screening` — 무한공급/무열화/무재활용 과장 필터
- `foundation` — 통합 건강도(5축)

## quick start
```python
from lithium import run_lithium_foundation
r = run_lithium_foundation()
print(r.health.composite_omega)
```

## 테스트
`pytest tests/ -v`

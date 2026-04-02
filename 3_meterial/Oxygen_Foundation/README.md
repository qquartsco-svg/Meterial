> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# Oxygen_Foundation v0.1.0

**산소(O₂)** 는 연소·생명유지·추진(LOX)의 중심이며, **강한 산화제**라서 안전·저장(끓어오름)이 핵심이다.

## 레이어

- `properties` — O₂ 물성  
- `production` — 극저온 공기분리, 전기분해와 H₂의 화학양론 연결  
- `storage` — LOX 끓어오름  
- `safety` — 산소 농도와 화재 심각도(카툰 지수)  
- `screening` — 순산소 안전 과장, MOXIE 무에너지 주장  
- `domain_space` — LOX 추진, ISRU 개념  

## 빠른 시작

```python
from oxygen import run_oxygen_foundation, OxygenClaimPayload

r = run_oxygen_foundation()
print(r.production.specific_energy_kwh_per_kg_o2)

r2 = run_oxygen_foundation(OxygenClaimPayload("", claimed_pure_o2_safe=True))
print(r2.screening.flags)
```

`pytest tests/ -v`

> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# Helium_Foundation v0.1.0

**헬륨(He)** 은 화학 반응보다 **조달·극저온·희소성·안전(질식)** 이 지배하는 원소다. 이 패키지는 그 흐름을 관찰할 환경을 제공한다.

## 레이어

| L | 모듈 | 내용 |
|---|------|------|
| L0 | `contracts` | 계약 |
| L1 | `properties` | 물성, 이상기체 밀도 |
| L2 | `sourcing` | 천연가스 추출·회수 (합성 아님) |
| L3 | `storage` | 액체 듀어, 끓어오름, 고압 압축 에너지 |
| L4 | `safety` | 질식, 저온 화상 |
| L5 | `screening` | ATHENA (무한 자원·저가·합성 과장) |
| L6 | `extension_hooks` | H₂, 융합, 포집, VectorSpace |
| — | `domain_space` | 기구 부력(이상기체) |

## 빠른 시작

```python
from helium import run_helium_foundation, HeliumClaimPayload

r = run_helium_foundation()
print(r.sourcing.method, r.storage.boiloff_percent_per_day)

r2 = run_helium_foundation(HeliumClaimPayload("무한 헬륨", claimed_abundance_unlimited=True))
print(r2.screening.flags)
```

## 한계

Tree-level 모델. MRI 크라이오스탯·He-3 스핀 극화 등은 `FUTURE_TAGS`.

## 테스트

`pytest tests/ -v`

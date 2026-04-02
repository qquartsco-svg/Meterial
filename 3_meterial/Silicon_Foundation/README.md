> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# Silicon_Foundation v0.1.0

실리콘은 계산기/반도체와 태양광(PV)을 잇는 물질 코어다. 이 엔진은 정제-결함-열예산-수율의 현실 제약을 본다.

**반도체 설계 축과의 관계:** `Fabless`·`foundry.implementation.tick` 은 **공정 물리 대체가 아님**. 웨이퍼·가스·도펀트·배선을 어느 원소 엔진에서 키울지는 [반도체 소재 브리지](../docs/SEMICONDUCTOR_MATERIALS_BRIDGE.md) 참고. 포토레지스트·CMP 소모품은 `Photolithography_CMP_Foundation` (EDA 비대체).

- `refining`: Siemens 정제 카툰
- `device`: PV vs logic 성능/결함/열 여유
- `screening`: 무결함/무한효율 과장 필터

```python
from silicon import run_silicon_foundation
print(run_silicon_foundation().health.composite_omega)
```

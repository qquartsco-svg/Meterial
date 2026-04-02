> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# Silicon_Foundation v0.1.0

실리콘은 계산기/반도체와 태양광(PV)을 잇는 물질 코어다. 이 엔진은 정제-결함-열예산-수율의 현실 제약을 본다.

- `refining`: Siemens 정제 카툰
- `device`: PV vs logic 성능/결함/열 여유
- `screening`: 무결함/무한효율 과장 필터

```python
from silicon import run_silicon_foundation
print(run_silicon_foundation().health.composite_omega)
```

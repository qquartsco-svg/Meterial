# BLOCKCHAIN_INFO

## 목적

`Carbon_Composite_Stack`의 핵심 파일 무결성과 변경 연속성을 추적한다.

이 저장소에서 "블록체인"은 분산 합의 네트워크가 아니라,
아래 운영 패턴을 의미한다.

- `SIGNATURE.sha256` 기반 파일 무결성 검증
- `PHAM_BLOCKCHAIN_LOG.md` 기반 변경 연속성 기록

## 검증

```bash
python3 scripts/generate_signature.py
python3 scripts/verify_signature.py
```


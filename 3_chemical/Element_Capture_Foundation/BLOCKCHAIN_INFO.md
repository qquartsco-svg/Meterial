# BLOCKCHAIN_INFO

`Element_Capture_Foundation` 에서 말하는 “블록체인 서명”은 합의 네트워크나 스마트 컨트랙트를 뜻하지 않는다.

여기서는 루트의 [SIGNATURE.sha256](/Users/jazzin/Desktop/00_BRAIN/_staging/Element_Capture_Foundation/SIGNATURE.sha256)에 담긴
**파일별 SHA-256 무결성 매니페스트**를 뜻한다.

보장하는 것:

- 공개/배포 시점의 소스 및 문서 표면이 바뀌지 않았는지 빠르게 확인
- 로컬 사본과 릴리스 기준선 비교

보장하지 않는 것:

- 비밀키 전자서명
- 온체인 영속성
- 합의 검증

검증:

```bash
python3 scripts/verify_signature.py
```

재생성:

```bash
python3 scripts/generate_signature.py
```

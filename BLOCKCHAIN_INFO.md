# BLOCKCHAIN_INFO

이 저장소 `Meterial` 은 `SIGNATURE.sha256` 를 통해 현재 공개 정본의 파일 해시를 기록한다.

목적:

- README, 코드, 테스트, 설계 문서의 무결성 추적
- 공개 이후 문서/코드 drift 감지
- 로컬 복사본과 공개 정본의 차이 확인

현재 방식은 SHA-256 manifest 기반의 **경량 무결성 레이어**다.
즉 실제 퍼블릭 체인 스마트컨트랙트를 사용하는 시스템은 아니며,
“블록체인 스타일의 연쇄 무결성 기록”을 지향하는 저장소 레벨 서명 체계로 읽는 것이 맞다.

핵심 파일:

- `SIGNATURE.sha256`
- `scripts/generate_signature.py`
- `scripts/verify_signature.py`
- `scripts/release_check.py`

권장 절차:

1. 테스트 통과
2. 캐시/생성물 정리
3. 서명 재생성
4. 서명 검증
5. release check 실행

이 문서는 “절대적 진위 보증”이 아니라, 현재 저장소 상태를 추적하기 위한 무결성 안내다.

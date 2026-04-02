# Changelog

## v0.1.0 — 2026-04-02

초기 릴리스.

### 구현

- **L0 contracts**: 전체 데이터 계약 (ProductionAssessment, StorageAssessment, FuelCellAssessment, SafetyAssessment, ScreeningReport, HealthReport)
- **L1 properties**: H₂ 물성 카드, 이상기체/Van der Waals 밀도, 압축인자
- **L2 production**: 전기분해 (PEM/Alkaline/SOEC), SMR, 색상 코드 분류
- **L3 storage**: 압축 가스 (350/700 bar), 액체 수소, 금속 수소화물
- **L4 fuel_cell**: Nernst OCV, PEMFC/SOFC/AFC 효율, 전력 밀도
- **L5 safety**: 가연 범위, 환기, 수소취성, 폭발 과압
- **L6 screening**: ATHENA 7플래그 4단 판정
- **L7 extension_hooks**: 형제 엔진 브리지 9개, 미래 확장 태그 13개
- **domain_space**: LOX/LH₂ Isp, ISRU 전력, 생명유지 전기분해
- **domain_grid**: P2G 왕복 효율, LCOH 간이 계산
- **domain_transport**: FCEV 주행거리, 충전 시간, 연료비
- **tests**: 80+ 테스트 (전 레이어 + 도메인 + 스크리닝 + 건강도 + 무결성)
- **README.md / README_EN.md**: 한국어 정본 + 영어 동반본

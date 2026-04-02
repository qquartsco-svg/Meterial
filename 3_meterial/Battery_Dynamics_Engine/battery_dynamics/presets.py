"""배터리 화학종·셀 공정 프리셋.

v0.3.0 확장
───────────
  - 화학종별 실측 OCV curve table 추가 (NMC / LFP / LCO)
  - Arrhenius 활성화 에너지 Ea_r_ev 추가 (저온 R0 급등 반영)
  - 2RC 파라미터 (r2_ohm, c2_farad) 추가 (선택적)
  - 기존 API 100% 하위 호환

프리셋 목록
───────────
  NMC_18650    — 원통형 NMC (모바일·노트북) + OCV table + Arrhenius
  LFP_POUCH    — LFP 파우치 대형 (EV·ESS) + 평탄 OCV table + Arrhenius
  LCO_PHONE    — LCO 스마트폰 + OCV table
  NMC_EV       — NMC 각형 EV + OCV table + 2RC + Arrhenius
  NMC_AGED     — NMC 노화 (SOH=0.78, R0 증가)
  LFP_COLD     — LFP 저온 (−10°C, Arrhenius 자동 반영)

OCV 테이블 출처
──────────────
  대표적인 문헌/데이터시트 기반 근사값.
  실제 셀 특성은 제조사·lot·온도에 따라 다릅니다.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List

from .schema import ECMParams


# ══════════════════════════════════════════════════════════════════════════════
# OCV curve tables
# ══════════════════════════════════════════════════════════════════════════════

# NMC (NCM) 계열 대표 OCV curve — 비선형 S-curve
# SOC 0~1, OCV 3.0~4.2V
_NMC_OCV_TABLE = [
    (0.00, 3.00), (0.03, 3.40), (0.05, 3.50), (0.08, 3.57),
    (0.10, 3.60), (0.15, 3.65), (0.20, 3.68), (0.25, 3.71),
    (0.30, 3.73), (0.35, 3.76), (0.40, 3.79), (0.45, 3.82),
    (0.50, 3.86), (0.55, 3.89), (0.60, 3.92), (0.65, 3.95),
    (0.70, 3.98), (0.75, 4.01), (0.80, 4.05), (0.85, 4.09),
    (0.90, 4.13), (0.93, 4.16), (0.96, 4.18), (1.00, 4.20),
]

# LFP (LiFePO4) 대표 OCV curve — 3.2~3.35V 평탄 구간 특성
# 선형 근사와 가장 큰 차이: 20~85% SOC 구간이 거의 평탄
_LFP_OCV_TABLE = [
    (0.00, 2.50), (0.02, 2.80), (0.04, 3.00), (0.06, 3.08),
    (0.08, 3.13), (0.10, 3.18), (0.13, 3.21), (0.15, 3.22),
    (0.20, 3.24), (0.25, 3.25), (0.30, 3.26), (0.35, 3.27),
    (0.40, 3.27), (0.45, 3.28), (0.50, 3.28), (0.55, 3.28),
    (0.60, 3.29), (0.65, 3.29), (0.70, 3.30), (0.75, 3.31),
    (0.80, 3.32), (0.83, 3.33), (0.85, 3.35), (0.88, 3.38),
    (0.90, 3.42), (0.92, 3.48), (0.94, 3.54), (0.96, 3.58),
    (0.98, 3.62), (1.00, 3.65),
]

# LCO (LiCoO2) 스마트폰 OCV curve — 고전압, 급격한 S-curve
_LCO_OCV_TABLE = [
    (0.00, 3.00), (0.03, 3.48), (0.05, 3.57), (0.08, 3.63),
    (0.10, 3.67), (0.15, 3.72), (0.20, 3.76), (0.25, 3.80),
    (0.30, 3.83), (0.35, 3.86), (0.40, 3.89), (0.45, 3.92),
    (0.50, 3.95), (0.55, 3.98), (0.60, 4.02), (0.65, 4.06),
    (0.70, 4.10), (0.75, 4.14), (0.80, 4.18), (0.85, 4.23),
    (0.90, 4.27), (0.93, 4.30), (0.96, 4.33), (1.00, 4.35),
]

# NMC EV 각형 — NMC 계열과 유사하나 플랫 구간 더 넓음
_NMC_EV_OCV_TABLE = [
    (0.00, 2.80), (0.03, 3.30), (0.05, 3.45), (0.08, 3.55),
    (0.10, 3.60), (0.15, 3.64), (0.20, 3.67), (0.25, 3.70),
    (0.30, 3.72), (0.35, 3.74), (0.40, 3.77), (0.45, 3.80),
    (0.50, 3.83), (0.55, 3.86), (0.60, 3.89), (0.65, 3.92),
    (0.70, 3.96), (0.75, 3.99), (0.80, 4.03), (0.85, 4.07),
    (0.90, 4.11), (0.93, 4.14), (0.96, 4.17), (1.00, 4.20),
]


# ══════════════════════════════════════════════════════════════════════════════
# 프리셋 정의
# ══════════════════════════════════════════════════════════════════════════════

# NMC 18650 원통형 — 3.4Ah, 4.2V / 2.8V
# Ea_r_ev=0.35eV → 0°C에서 R0 약 2.3배 증가 (대표 NMC 특성)
NMC_18650 = ECMParams(
    q_ah               = 3.4,
    r0_ohm             = 0.022,
    r1_ohm             = 0.012,
    c1_farad           = 1800.0,
    soc_ocv_v_per_unit = 1.20,   # 선형 OCV fallback용 (table이 우선)
    soc_v0             = 3.00,
    thermal_c_j_per_k  = 120.0,
    thermal_h_w_per_k  = 0.8,
    t_amb_k            = 298.15,
    soh                = 1.0,
    t_cutoff_v         = 2.80,
    v_charge_max_v     = 4.20,
    label              = "NMC_18650",
    ocv_table          = _NMC_OCV_TABLE,
    r2_ohm             = 0.0,      # 1RC 모드
    c2_farad           = 0.0,
    Ea_r_ev            = 0.35,
    T_ref_k            = 298.15,
)

# LFP 파우치 대형 — 100Ah, 3.65V / 2.5V
# Ea_r_ev=0.55eV → LFP는 저온에서 R0 더 크게 증가
LFP_POUCH = ECMParams(
    q_ah               = 100.0,
    r0_ohm             = 0.0018,
    r1_ohm             = 0.0009,
    c1_farad           = 50000.0,
    soc_ocv_v_per_unit = 0.40,
    soc_v0             = 3.00,
    thermal_c_j_per_k  = 5000.0,
    thermal_h_w_per_k  = 5.0,
    t_amb_k            = 298.15,
    soh                = 1.0,
    t_cutoff_v         = 2.50,
    v_charge_max_v     = 3.65,
    label              = "LFP_POUCH",
    ocv_table          = _LFP_OCV_TABLE,
    Ea_r_ev            = 0.55,     # LFP: 저온 임피던스 민감
    T_ref_k            = 298.15,
)

# LCO 파우치 스마트폰 — 4.0Ah, 4.35V / 3.0V
LCO_PHONE = ECMParams(
    q_ah               = 4.0,
    r0_ohm             = 0.028,
    r1_ohm             = 0.016,
    c1_farad           = 1500.0,
    soc_ocv_v_per_unit = 1.35,
    soc_v0             = 3.00,
    thermal_c_j_per_k  = 80.0,
    thermal_h_w_per_k  = 0.30,
    t_amb_k            = 298.15,
    soh                = 1.0,
    t_cutoff_v         = 3.00,
    v_charge_max_v     = 4.35,
    label              = "LCO_PHONE",
    ocv_table          = _LCO_OCV_TABLE,
    Ea_r_ev            = 0.30,
    T_ref_k            = 298.15,
)

# NMC 각형 EV 대용량 — 230Ah, 4.2V / 2.8V
# 2RC 모델: 단기(RC1) + 장기(RC2) 분극 포함
NMC_EV = ECMParams(
    q_ah               = 230.0,
    r0_ohm             = 0.0014,
    r1_ohm             = 0.0007,
    c1_farad           = 80000.0,
    r2_ohm             = 0.0003,   # 2RC: 장기 분극
    c2_farad           = 500000.0,
    soc_ocv_v_per_unit = 1.20,
    soc_v0             = 3.00,
    thermal_c_j_per_k  = 30000.0,
    thermal_h_w_per_k  = 20.0,
    t_amb_k            = 298.15,
    soh                = 1.0,
    t_cutoff_v         = 2.80,
    v_charge_max_v     = 4.20,
    label              = "NMC_EV",
    ocv_table          = _NMC_EV_OCV_TABLE,
    Ea_r_ev            = 0.35,
    T_ref_k            = 298.15,
)

# NMC 18650 노화 셀 — SOH=0.78, R0 증가
NMC_AGED = ECMParams(
    q_ah               = 3.4,
    r0_ohm             = 0.048,
    r1_ohm             = 0.024,
    c1_farad           = 1800.0,
    soc_ocv_v_per_unit = 1.20,
    soc_v0             = 3.00,
    thermal_c_j_per_k  = 120.0,
    thermal_h_w_per_k  = 0.8,
    t_amb_k            = 298.15,
    soh                = 0.78,
    t_cutoff_v         = 2.80,
    v_charge_max_v     = 4.20,
    label              = "NMC_AGED",
    ocv_table          = _NMC_OCV_TABLE,
    Ea_r_ev            = 0.35,
    T_ref_k            = 298.15,
)

# LFP 저온 환경 — T_amb=−10°C, Arrhenius 자동 반영
LFP_COLD = ECMParams(
    q_ah               = 100.0,
    r0_ohm             = 0.0018,   # 기준값 — Arrhenius가 저온 상승 자동 처리
    r1_ohm             = 0.0009,
    c1_farad           = 50000.0,
    soc_ocv_v_per_unit = 0.40,
    soc_v0             = 3.00,
    thermal_c_j_per_k  = 5000.0,
    thermal_h_w_per_k  = 5.0,
    t_amb_k            = 263.15,   # −10°C
    soh                = 1.0,
    t_cutoff_v         = 2.50,
    v_charge_max_v     = 3.65,
    label              = "LFP_COLD",
    ocv_table          = _LFP_OCV_TABLE,
    Ea_r_ev            = 0.55,
    T_ref_k            = 298.15,
)


# ══════════════════════════════════════════════════════════════════════════════
# 레지스트리 & 유틸리티
# ══════════════════════════════════════════════════════════════════════════════

_REGISTRY: Dict[str, ECMParams] = {
    "nmc_18650": NMC_18650,
    "lfp_pouch": LFP_POUCH,
    "lco_phone": LCO_PHONE,
    "nmc_ev":    NMC_EV,
    "nmc_aged":  NMC_AGED,
    "lfp_cold":  LFP_COLD,
}


def get_preset(name: str, **overrides: Any) -> ECMParams:
    """프리셋 이름으로 ECMParams 반환. 키워드 파라미터로 오버라이드 가능.

    Examples
    --------
    >>> hot = get_preset("nmc_18650", t_amb_k=318.15)
    >>> no_table = get_preset("lfp_pouch", ocv_table=None)   # 선형 OCV fallback
    """
    key = name.lower().strip()
    if key not in _REGISTRY:
        raise KeyError(
            f"알 수 없는 프리셋: '{name}'. 사용 가능: {list_presets()}"
        )
    base = _REGISTRY[key]
    return dataclasses.replace(base, **overrides) if overrides else base


def list_presets() -> List[str]:
    """사용 가능한 프리셋 이름 목록 (정렬)."""
    return sorted(_REGISTRY.keys())

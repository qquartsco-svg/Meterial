from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Tuple


@dataclass(frozen=True)
class ArbiterConfig:
    """Thresholds for mission vs reflex arbitration (robot safety v0)."""

    gut_risk_pause: float = 0.75
    gut_risk_cap_heat: float = 0.45
    heat_cap_when_elevated_gut: float = 0.25


def arbiter_config_from_payload(raw: Optional[Mapping[str, Any]]) -> ArbiterConfig:
    if not raw:
        return ArbiterConfig()
    if not isinstance(raw, Mapping):
        raise TypeError("arbiter_config must be an object")
    return ArbiterConfig(
        gut_risk_pause=float(raw.get("gut_risk_pause", 0.75)),
        gut_risk_cap_heat=float(raw.get("gut_risk_cap_heat", 0.45)),
        heat_cap_when_elevated_gut=float(raw.get("heat_cap_when_elevated_gut", 0.25)),
    )


@dataclass(frozen=True)
class ArbiterVerdict:
    """How the cooking mission tick should respect SIK / safety."""

    pause_mission: bool
    heat_cap_0_1: float  # multiply heat proxy (0 = no intentional heating)
    reasons: Tuple[str, ...]

    @staticmethod
    def allow_all() -> "ArbiterVerdict":
        return ArbiterVerdict(pause_mission=False, heat_cap_0_1=1.0, reasons=())


def arbiter_verdict_from_dict(d: Mapping[str, Any]) -> ArbiterVerdict:
    if not isinstance(d, Mapping):
        raise TypeError("arbiter must be an object")
    pause = bool(d.get("pause_mission", False))
    cap = d.get("heat_cap_0_1", 1.0)
    if isinstance(cap, bool) or not isinstance(cap, (int, float)):
        raise TypeError("arbiter.heat_cap_0_1 must be a number")
    cap_f = max(0.0, min(1.0, float(cap)))
    reasons = d.get("reasons")
    if reasons is None:
        rt: Tuple[str, ...] = ()
    elif isinstance(reasons, (list, tuple)):
        rt = tuple(str(x) for x in reasons)
    else:
        raise TypeError("arbiter.reasons must be an array when present")
    return ArbiterVerdict(pause_mission=pause, heat_cap_0_1=cap_f, reasons=rt)


def arbiter_verdict_to_dict(v: ArbiterVerdict) -> Dict[str, Any]:
    return {
        "pause_mission": v.pause_mission,
        "heat_cap_0_1": v.heat_cap_0_1,
        "reasons": list(v.reasons),
    }


def _get_attr(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def arbiter_from_sik_tick_result(
    sik_result: Mapping[str, Any],
    *,
    cfg: Optional[ArbiterConfig] = None,
) -> ArbiterVerdict:
    """
    Build an ArbiterVerdict from `SensoryInputKernel.process_tick` return dict.

    Expects keys `reflex` (ReflexDecision or dict) and `felt_sense` (FeltSenseState or dict).
    """
    cfg = cfg or ArbiterConfig()
    reflex = sik_result.get("reflex")
    felt = sik_result.get("felt_sense")
    reasons: list[str] = []

    triggered = bool(_get_attr(reflex, "triggered"))
    threat_bias = float(_get_attr(reflex, "threat_bias") or 0.0)
    gut = float(_get_attr(felt, "gut_risk") or 0.0)
    tag = _get_attr(felt, "felt_tag")
    tag_s = str(tag) if tag is not None else ""

    if triggered:
        reasons.append("reflex_triggered")
        if threat_bias > 0:
            reasons.append(f"threat_bias={threat_bias:.2f}")
        return ArbiterVerdict(pause_mission=True, heat_cap_0_1=0.0, reasons=tuple(reasons))

    if gut >= cfg.gut_risk_pause:
        reasons.append(f"gut_risk>={cfg.gut_risk_pause}")
        if tag_s:
            reasons.append(f"felt_tag={tag_s}")
        return ArbiterVerdict(pause_mission=True, heat_cap_0_1=0.0, reasons=tuple(reasons))

    if gut >= cfg.gut_risk_cap_heat:
        reasons.append(f"gut_risk>={cfg.gut_risk_cap_heat}")
        return ArbiterVerdict(
            pause_mission=False,
            heat_cap_0_1=cfg.heat_cap_when_elevated_gut,
            reasons=tuple(reasons),
        )

    if tag_s and "warning" in tag_s:
        reasons.append("felt_tag_warning")
        return ArbiterVerdict(
            pause_mission=False,
            heat_cap_0_1=min(cfg.heat_cap_when_elevated_gut, 0.5),
            reasons=tuple(reasons),
        )

    return ArbiterVerdict.allow_all()

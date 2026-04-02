from __future__ import annotations

from dataclasses import replace
from typing import Any, Dict, Iterable, List, Mapping

from .contracts import KitchenObservation

try:
    from sensory_input_kernel.contracts.schemas import SensoryStimulus
    from sensory_input_kernel.sensory_kernel import SensoryInputKernel

    _SIK_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    SensoryStimulus = None  # type: ignore[misc, assignment]
    SensoryInputKernel = None  # type: ignore[misc, assignment]
    _SIK_AVAILABLE = False


def sik_available() -> bool:
    return bool(_SIK_AVAILABLE)


def stimuli_from_dicts(items: Iterable[Mapping[str, Any]]) -> List[Any]:
    """Build SIK `SensoryStimulus` list from JSON-like rows. Requires SIK on path."""
    if not _SIK_AVAILABLE:
        raise RuntimeError(
            "Sensory_Input_Kernel not importable; add _staging/Sensory_Input_Kernel to PYTHONPATH"
        )
    out: List[Any] = []
    for i, row in enumerate(items):
        if not isinstance(row, Mapping):
            raise TypeError(f"stimuli[{i}] must be an object")
        ch = row.get("channel")
        if ch not in ("vision", "hearing", "touch", "smell", "taste"):
            raise ValueError(f"stimuli[{i}].channel invalid {ch!r}")
        intensity = row.get("intensity", 0.0)
        if isinstance(intensity, bool) or not isinstance(intensity, (int, float)):
            raise TypeError(f"stimuli[{i}].intensity must be a number")
        sig = str(row.get("signal", ""))
        ts = float(row.get("timestamp", 0.0))
        ctx = row.get("context") or {}
        if ctx is not None and not isinstance(ctx, dict):
            raise TypeError(f"stimuli[{i}].context must be an object")
        out.append(
            SensoryStimulus(
                channel=ch,
                intensity=float(intensity),
                signal=sig,
                context=dict(ctx or {}),
                timestamp=ts,
            )
        )
    return out


def run_sik_process_tick(stimuli: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    """Run one SIK tick from JSON-like stimuli; returns same shape as `process_tick`."""
    kernel = SensoryInputKernel()
    st = stimuli_from_dicts(stimuli)
    return kernel.process_tick(st)


def merge_kitchen_observation_with_sik(
    base: KitchenObservation,
    *,
    wall_clock_s: float,
    sik_result: Mapping[str, Any],
    felt_tag_prefix: str = "sik",
) -> KitchenObservation:
    """
    Attach SIK summary into `KitchenObservation.tags` for recipe branching / logging.

    Does not overwrite temperature fields; optional vision fusion could be added later.
    """
    felt = sik_result.get("felt_sense")
    reflex = sik_result.get("reflex")

    tags = list(base.tags)
    ft = _attr(felt, "felt_tag")
    if ft:
        tags.append(f"{felt_tag_prefix}.felt:{ft}")
    gut = _attr(felt, "gut_risk")
    if gut is not None:
        tags.append(f"{felt_tag_prefix}.gut_risk:{float(gut):.3f}")
    if reflex is not None and bool(_attr(reflex, "triggered")):
        tags.append(f"{felt_tag_prefix}.reflex:triggered")
        act = _attr(reflex, "action")
        if act:
            tags.append(f"{felt_tag_prefix}.reflex_action:{act}")

    frame = sik_result.get("frame")
    if frame is not None:
        vis = _attr(frame, "vision")
        if vis is not None:
            motion = _attr(vis, "motion")
            if motion is not None and float(motion) > 0.5:
                tags.append(f"{felt_tag_prefix}.vision_motion_high")

    return replace(
        base,
        wall_clock_s=float(wall_clock_s),
        tags=tuple(dict.fromkeys(tags)),
    )


def _attr(obj: Any, name: str) -> Any:
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)

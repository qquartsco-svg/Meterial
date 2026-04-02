from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional

from .contracts import KitchenObservation

if TYPE_CHECKING:
    from anomalous_observation_foundation.contracts import ObservationFrame


_TAG_PATTERN = re.compile(r"cooking_tag:(\S+)")


def _parse_cooking_tags_from_notes(notes: str) -> List[str]:
    if not notes:
        return []
    return _TAG_PATTERN.findall(notes)


def kitchen_observation_from_aof(
    frame: "ObservationFrame",
    *,
    overlay: Optional[Mapping[str, Any]] = None,
) -> KitchenObservation:
    """
    Build a KitchenObservation from an AOF ObservationFrame.

    Convention (optional):
    - Any `raw_channels[].notes` may contain `cooking_tag:branch_id` (repeatable).
    - `overlay` (e.g. from L4 payload) can set wall_clock_s, temperatures, tags, vision_brownness,
      `reported_mass_g`, `reported_volume_ml`, `motion_ok` (same names as `KitchenObservation`).

    `signal_intensity` (0..1) is optionally mapped to vision brownness when overlay omits it.
    """
    tags: List[str] = []
    for ch in frame.raw_channels:
        tags.extend(_parse_cooking_tags_from_notes(ch.notes or ""))

    wall = float(frame.duration_s or 0.0)
    surf: Optional[float] = None
    core: Optional[float] = None
    vision: Optional[float] = None
    human_ok: Optional[bool] = None
    mass_g: Optional[float] = None
    vol_ml: Optional[float] = None
    motion_ok: Optional[bool] = None

    if overlay:
        if not isinstance(overlay, Mapping):
            raise TypeError("overlay must be an object when present")
        if "wall_clock_s" in overlay and overlay["wall_clock_s"] is not None:
            w = overlay["wall_clock_s"]
            if isinstance(w, bool) or not isinstance(w, (int, float)):
                raise TypeError("overlay.wall_clock_s must be a number")
            wall = float(w)
        surf = _opt_num(overlay, "reported_surface_temp_c")
        core = _opt_num(overlay, "reported_core_temp_c")
        vision = _opt_num(overlay, "vision_brownness_0_1")
        hg = overlay.get("human_gate_ok")
        if hg is not None:
            if not isinstance(hg, bool):
                raise TypeError("overlay.human_gate_ok must be boolean or null")
            human_ok = hg
        mass_g = _opt_num(overlay, "reported_mass_g")
        vol_ml = _opt_num(overlay, "reported_volume_ml")
        mo = overlay.get("motion_ok")
        if mo is not None:
            if not isinstance(mo, bool):
                raise TypeError("overlay.motion_ok must be boolean or null")
            motion_ok = mo
        ot = overlay.get("tags")
        if ot is not None:
            if not isinstance(ot, list):
                raise TypeError("overlay.tags must be an array")
            tags = list(tags) + [str(x) for x in ot]

    if vision is None and frame.signal_intensity is not None:
        vision = max(0.0, min(1.0, float(frame.signal_intensity)))

    return KitchenObservation(
        wall_clock_s=wall,
        reported_surface_temp_c=surf,
        reported_core_temp_c=core,
        vision_brownness_0_1=vision,
        human_gate_ok=human_ok,
        reported_mass_g=mass_g,
        reported_volume_ml=vol_ml,
        motion_ok=motion_ok,
        tags=tuple(dict.fromkeys(tags)),
    )


def _opt_num(d: Mapping[str, Any], key: str) -> Optional[float]:
    v = d.get(key)
    if v is None:
        return None
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise TypeError(f"overlay.{key} must be a number or null")
    return float(v)


def observation_frame_from_aof_min(d: Mapping[str, Any]) -> "ObservationFrame":
    """
    Minimal `ObservationFrame` from an L4-shaped `aof_min` object (no full AOF parser).
    Requires `anomalous_observation_foundation` importable (caller adds to sys.path).
    """
    from anomalous_observation_foundation.contracts import (
        VALID_SENSOR_CHANNELS,
        ObservationFrame,
        RawChannelSample,
    )

    if not isinstance(d, Mapping):
        raise TypeError("aof_min must be an object")
    case_id = str(d.get("case_id") or "cooking-aof-min").strip() or "cooking-aof-min"
    raw = d.get("raw_channels")
    if raw is None:
        raw_list: List[Mapping[str, Any]] = []
    elif not isinstance(raw, list):
        raise TypeError("aof_min.raw_channels must be an array")
    else:
        raw_list = raw
    out_ch = []
    for i, item in enumerate(raw_list):
        if not isinstance(item, dict):
            raise TypeError(f"aof_min.raw_channels[{i}] must be an object")
        ch = item.get("channel", "other")
        if not isinstance(ch, str) or ch not in VALID_SENSOR_CHANNELS:
            raise ValueError(f"aof_min.raw_channels[{i}].channel invalid {ch!r}")
        mu = item.get("media_uri")
        pr = item.get("payload_ref")
        if mu is not None and not isinstance(mu, str):
            raise TypeError("media_uri must be string or null")
        if pr is not None and not isinstance(pr, str):
            raise TypeError("payload_ref must be string or null")
        out_ch.append(
            RawChannelSample(
                channel=ch,
                media_uri=mu,
                payload_ref=pr,
                notes=str(item.get("notes") or ""),
            )
        )
    dur = d.get("duration_s")
    if dur is not None and (isinstance(dur, bool) or not isinstance(dur, (int, float))):
        raise TypeError("aof_min.duration_s must be a number or null")
    sig = d.get("signal_intensity")
    if sig is not None and (isinstance(sig, bool) or not isinstance(sig, (int, float))):
        raise TypeError("aof_min.signal_intensity must be a number or null")
    return ObservationFrame(
        case_id=case_id,
        raw_channels=tuple(out_ch),
        duration_s=float(dur) if dur is not None else None,
        signal_intensity=float(sig) if sig is not None else None,
    )

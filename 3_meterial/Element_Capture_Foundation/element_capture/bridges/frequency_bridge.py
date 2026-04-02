from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional

from ..adapter import apply_external_health_modifier
from ..contracts import CaptureAssessment
from ._resolver import import_sibling_package

CaptureSignalField = Literal["pump_rpm", "membrane_dp", "compressor_vibration"]
_FIELDS: List[str] = ["pump_rpm", "membrane_dp", "compressor_vibration"]


@dataclass
class CaptureFrequencyBridge:
    sample_rate_hz: float
    window_size: int = 128
    _buffers: Dict[str, List[float]] = field(default_factory=dict, init=False)

    def push(self, snapshot: object) -> None:
        for name in _FIELDS:
            if name not in self._buffers:
                self._buffers[name] = []
            value = float(getattr(snapshot, name, 0.0))
            if value != value or value in (float("inf"), float("-inf")):
                continue
            self._buffers[name].append(value)
            if len(self._buffers[name]) > self.window_size:
                self._buffers[name].pop(0)

    def ready(self, field: CaptureSignalField = "compressor_vibration", min_samples: int = 16) -> bool:
        return len(self._buffers.get(field, [])) >= min_samples

    def health(self, field: CaptureSignalField = "compressor_vibration"):
        if not self.ready(field, min_samples=8):
            return None
        freq = import_sibling_package("frequency_core", "FrequencyCore_Engine")
        adapter = freq.FrequencyAdapter(self.sample_rate_hz)
        return adapter.health(self._buffers[field])


def apply_frequency_health_to_capture(
    assessment: CaptureAssessment,
    *,
    machinery_health,
) -> CaptureAssessment:
    if machinery_health is None:
        return assessment
    notes: list[str] = []
    if getattr(machinery_health, "anomaly_detected", False):
        notes.extend(getattr(machinery_health, "anomaly_notes", []))
    return apply_external_health_modifier(
        assessment,
        machinery_health_0_1=float(getattr(machinery_health, "omega_freq", 1.0)),
        extra_notes=tuple(notes),
        evidence={
            "machinery_omega_freq": float(getattr(machinery_health, "omega_freq", 1.0)),
            "machinery_dominant_freq_hz": float(getattr(machinery_health, "dominant_freq_hz", 0.0)),
        },
    )

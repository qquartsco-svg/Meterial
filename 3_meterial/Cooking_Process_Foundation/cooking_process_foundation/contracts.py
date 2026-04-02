from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class SkillRef:
    """Culinary skill as a layered ID (tradition · technique · variant)."""

    tradition: str  # e.g. "fr", "jp", "mx"
    technique: str  # e.g. "saute", "braise", "emulsion"
    variant: str = ""  # e.g. "wet", "dry"


@dataclass
class FlowStep:
    """One node in the recipe *process* graph (not a text line)."""

    step_id: str
    skill: SkillRef
    # Advance when elapsed >= min_duration_s AND optional observation gates pass
    min_duration_s: float = 0.0
    target_surface_temp_c: Optional[float] = None
    min_brownness_0_1: Optional[float] = None
    # Metrology (scale / flowmeter adapters report via KitchenObservation)
    target_mass_g: Optional[float] = None
    mass_tolerance_g: Optional[float] = None
    target_volume_ml: Optional[float] = None
    volume_tolerance_ml: Optional[float] = None
    # When True, exit/branch requires obs.motion_ok is True (AMR / planner fuse)
    require_motion_ok: bool = False
    notes: str = ""
    next_on_success: str = ""
    next_on_branch: Dict[str, str] = field(default_factory=dict)  # key from observation tag -> step_id


@dataclass
class RecipeFlow:
    """Directed process: entry_step_id + steps. Linear if each next_on_success only."""

    flow_id: str
    title: str
    entry_step_id: str
    steps: Tuple[FlowStep, ...]


@dataclass
class KitchenState:
    """Mutable process state (what the 'dynamics program' owns)."""

    current_step_id: str
    time_in_step_s: float
    vessel_surface_temp_c: float
    core_temp_c: Optional[float]
    brownness_0_1: float
    phase_tags: Tuple[str, ...] = ()  # e.g. ("aqueous", "fat_emulsion")
    extras: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KitchenObservation:
    """Sensor / human input at a tick (AOF-style multimodal hook later)."""

    wall_clock_s: float
    reported_surface_temp_c: Optional[float] = None
    reported_core_temp_c: Optional[float] = None
    vision_brownness_0_1: Optional[float] = None
    human_gate_ok: Optional[bool] = None  # e.g. "mise en place done"
    reported_mass_g: Optional[float] = None
    reported_volume_ml: Optional[float] = None
    motion_ok: Optional[bool] = None  # from motion / AMR layer when fused
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class StepOutcome:
    completed_step_id: str
    next_step_id: str
    reason: str

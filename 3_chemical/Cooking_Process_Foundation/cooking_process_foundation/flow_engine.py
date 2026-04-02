from __future__ import annotations

from typing import Dict, Optional

from .contracts import FlowStep, KitchenObservation, KitchenState, RecipeFlow, StepOutcome
from .gates import (
    METROLOGY_FAIL_BRANCH_KEY,
    metrology_failure_branch_eligible,
    metrology_gates_satisfied,
    motion_gate_satisfied,
)
from .physics_proxy import integrate_heat, suggested_heat_proxy_for_skill


class FlowEngine:
    """
    Runs a RecipeFlow: each tick updates physics proxy, then evaluates step exit rules.
    This is the 'program' — not printing a recipe, but advancing process state.
    """

    def __init__(self, flow: RecipeFlow, initial: KitchenState) -> None:
        self._flow = flow
        self._by_id: Dict[str, FlowStep] = {s.step_id: s for s in flow.steps}
        if initial.current_step_id not in self._by_id:
            raise ValueError(f"current_step_id {initial.current_step_id!r} not in flow")
        self.state = initial
        self._terminal_outcome: Optional[StepOutcome] = None

    def is_finished(self) -> bool:
        return self._terminal_outcome is not None

    def current_step(self) -> FlowStep:
        return self._by_id[self.state.current_step_id]

    def tick(
        self,
        obs: KitchenObservation,
        dt_s: float,
        *,
        heat_cap_0_1: float = 1.0,
        mission_pause: bool = False,
    ) -> Optional[StepOutcome]:
        if self._terminal_outcome is not None:
            return self._terminal_outcome

        if mission_pause:
            return None

        step = self.current_step()
        cap = max(0.0, min(1.0, float(heat_cap_0_1)))
        q = suggested_heat_proxy_for_skill(step.target_surface_temp_c, self.state.vessel_surface_temp_c) * cap
        integrate_heat(self.state, obs, dt_s, heat_input_w_proxy=q)

        # Branch keys from observation tags (e.g. "doneness:rare")
        for tag in obs.tags:
            if tag in step.next_on_branch:
                if not motion_gate_satisfied(step, obs):
                    return None
                if not metrology_gates_satisfied(step, obs):
                    return None
                nxt = step.next_on_branch[tag]
                return self._complete(step.step_id, nxt, f"branch:{tag}")

        if METROLOGY_FAIL_BRANCH_KEY in step.next_on_branch:
            if motion_gate_satisfied(step, obs) and metrology_failure_branch_eligible(step, obs):
                nxt = step.next_on_branch[METROLOGY_FAIL_BRANCH_KEY]
                return self._complete(
                    step.step_id, nxt, f"branch:{METROLOGY_FAIL_BRANCH_KEY}"
                )

        if step.min_duration_s > 0 and self.state.time_in_step_s < step.min_duration_s:
            return None

        if step.target_surface_temp_c is not None:
            if self.state.vessel_surface_temp_c + 1.0 < step.target_surface_temp_c:
                return None

        if step.min_brownness_0_1 is not None:
            if self.state.brownness_0_1 < step.min_brownness_0_1:
                return None

        if not motion_gate_satisfied(step, obs):
            return None
        if not metrology_gates_satisfied(step, obs):
            return None

        nxt = step.next_on_success
        if not nxt:
            out = StepOutcome(
                completed_step_id=step.step_id,
                next_step_id="",
                reason="flow_complete",
            )
            self._terminal_outcome = out
            return out
        return self._complete(step.step_id, nxt, "conditions_met")

    def _complete(self, completed: str, nxt: str, reason: str) -> StepOutcome:
        if nxt not in self._by_id:
            raise ValueError(f"next step {nxt!r} not in flow")
        self.state.current_step_id = nxt
        self.state.time_in_step_s = 0.0
        return StepOutcome(completed_step_id=completed, next_step_id=nxt, reason=reason)

from __future__ import annotations

from typing import Optional

from .contracts import KitchenObservation, KitchenState


def integrate_heat(
    state: KitchenState,
    obs: KitchenObservation,
    dt_s: float,
    *,
    ambient_c: float = 22.0,
    heat_input_w_proxy: float = 0.0,
    tau_surface_s: float = 12.0,
    brownning_rate_per_s_at_180c: float = 0.02,
) -> None:
    """
    Minimal first-order proxy: surface temp relaxes toward a drive from heat_input;
    brownness grows faster above ~140 °C (Maillard-ish heuristic, not chemistry).
    Mutates `state` in place.
    """
    if dt_s <= 0:
        return

    t = state.vessel_surface_temp_c
    if obs.reported_surface_temp_c is not None:
        t = float(obs.reported_surface_temp_c)
    else:
        # crude: heat drives toward max; cool toward ambient when no heat
        target = ambient_c + min(200.0, heat_input_w_proxy * 0.15)
        alpha = min(1.0, dt_s / tau_surface_s)
        t = t + alpha * (target - t)

    state.vessel_surface_temp_c = t

    if obs.reported_core_temp_c is not None:
        state.core_temp_c = float(obs.reported_core_temp_c)

    # Brownness accumulation (toy)
    if t >= 140.0:
        rate = brownning_rate_per_s_at_180c * max(0.0, (t - 140.0) / 40.0)
        state.brownness_0_1 = min(1.0, state.brownness_0_1 + rate * dt_s)

    if obs.vision_brownness_0_1 is not None:
        # fuse toward vision (simple)
        v = float(obs.vision_brownness_0_1)
        state.brownness_0_1 = min(1.0, max(state.brownness_0_1, v * 0.3 + state.brownness_0_1 * 0.7))

    state.time_in_step_s += dt_s


def suggested_heat_proxy_for_skill(surface_target_c: Optional[float], current_c: float) -> float:
    """Map skill target to a 0..~1500 W proxy (dimensionless scale)."""
    if surface_target_c is None:
        return 400.0
    err = surface_target_c - current_c
    return max(0.0, min(1200.0, 300.0 + err * 8.0))

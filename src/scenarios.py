from __future__ import annotations

import pandas as pd


SCENARIOS = ["baseline", "with_events", "optimistic", "pessimistic"]


def scenario_scale_factor(scenario: str, signed_effect: float) -> float:
    """
    Returns a multiplier for a signed effect.
    optimistic:
      - positives * 1.2
      - negatives * 0.8  (less harmful)
    pessimistic:
      - positives * 0.8  (less beneficial)
      - negatives * 1.2  (more harmful)
    baseline/with_events:
      - no scaling
    """
    s = scenario.strip().lower()
    if s in {"baseline", "with_events"}:
        return 1.0

    if s == "optimistic":
        return 1.2 if signed_effect >= 0 else 0.8

    if s == "pessimistic":
        return 0.8 if signed_effect >= 0 else 1.2

    raise ValueError(f"Unknown scenario: {scenario!r}")


def apply_scenario_to_links(impact_links: pd.DataFrame, scenario: str) -> pd.DataFrame:
    """
    Returns a copy with an extra column scenario_multiplier to apply per link.
    """
    out = impact_links.copy()

    direction = out["direction"].str.lower().str.strip()
    signed = out["impact_estimate"].astype(float)
    signed = signed.where(direction == "increase", -signed)

    out["scenario_multiplier"] = [scenario_scale_factor(scenario, v) for v in signed.tolist()]
    return out

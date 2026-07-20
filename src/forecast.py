from __future__ import annotations

from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd


def _fit_linear_trend(years: np.ndarray, values: np.ndarray) -> Tuple[float, float]:
    """
    Fit y = a*x + b. Requires at least 2 points; otherwise returns flat line.
    """
    years = years.astype(float)
    values = values.astype(float)
    if len(years) < 2:
        a = 0.0
        b = float(values[-1]) if len(values) else 0.0
        return a, b
    a, b = np.polyfit(years, values, deg=1)
    return float(a), float(b)


def baseline_forecast(
    observations: pd.DataFrame,
    forecast_years: Iterable[int],
) -> pd.DataFrame:
    """
    Per indicator linear trend baseline forecast.
    Returns DataFrame with columns: year, indicator_code, baseline
    """
    forecast_years = np.array(list(forecast_years), dtype=int)

    rows = []
    for ind, grp in observations.groupby("indicator_code"):
        x = grp["date"].to_numpy(dtype=float)
        y = grp["value"].to_numpy(dtype=float)
        a, b = _fit_linear_trend(x, y)

        for yr in forecast_years:
            rows.append(
                {
                    "year": int(yr),
                    "indicator_code": ind,
                    "baseline": a * float(yr) + b,
                }
            )

    return pd.DataFrame(rows).sort_values(["indicator_code", "year"]).reset_index(drop=True)


def _distribute_total_over_duration(total: float, duration_years: int) -> Dict[int, float]:
    """
    Returns a map {offset_year: effect} over duration, linear equal split.
    For duration=1, offset 0 gets full total.
    """
    d = int(duration_years)
    if d <= 0:
        raise ValueError("duration_years must be >= 1")
    per_year = float(total) / float(d)
    return {i: per_year for i in range(d)}


def compute_event_effects_by_year(
    events: pd.DataFrame,
    impact_links: pd.DataFrame,
    years: Iterable[int],
    enabled_event_ids: set[str],
) -> pd.DataFrame:
    """
    Computes yearly event effects per indicator, already respecting lag + duration.
    Returns: year, indicator_code, effect, event_id
    """
    years = list(map(int, years))
    year_set = set(years)

    event_year = dict(zip(events["event_id"], events["event_date"]))

    rows = []
    for _, link in impact_links.iterrows():
        eid = str(link["event_id"])
        if eid not in enabled_event_ids:
            continue

        ind = str(link["indicator_code"])
        lag = int(link["lag_years"])
        dur = int(link["duration_years"])

        total = float(link["impact_estimate"]) * float(link.get("scenario_multiplier", 1.0))
        direction = str(link["direction"]).strip().lower()
        signed_total = total if direction == "increase" else -total

        start_year = int(event_year[eid]) + lag

        split = _distribute_total_over_duration(signed_total, dur)
        for offset, per_year_effect in split.items():
            y = start_year + int(offset)
            if y in year_set:
                rows.append({"year": y, "indicator_code": ind, "effect": float(per_year_effect), "event_id": eid})

    if not rows:
        return pd.DataFrame(columns=["year", "indicator_code", "effect", "event_id"])

    out = pd.DataFrame(rows)
    return out


def event_aware_forecast(
    observations: pd.DataFrame,
    events: pd.DataFrame,
    impact_links: pd.DataFrame,
    forecast_years: Iterable[int],
    enabled_event_ids: set[str],
) -> pd.DataFrame:
    """
    Returns: year, indicator_code, baseline, event_effect, forecast
    """
    base = baseline_forecast(observations, forecast_years)

    effects_long = compute_event_effects_by_year(
        events=events,
        impact_links=impact_links,
        years=forecast_years,
        enabled_event_ids=enabled_event_ids,
    )

    if effects_long.empty:
        merged = base.copy()
        merged["event_effect"] = 0.0
        merged["forecast"] = merged["baseline"]
        return merged
      effects = (
        effects_long.groupby(["year", "indicator_code"], as_index=False)["effect"]
        .sum()
        .rename(columns={"effect": "event_effect"})
    )

    merged = base.merge(effects, on=["year", "indicator_code"], how="left")
    merged["event_effect"] = merged["event_effect"].fillna(0.0)
    merged["forecast"] = merged["baseline"] + merged["event_effect"]
    return merged.sort_values(["indicator_code", "year"]).reset_index(drop=True)

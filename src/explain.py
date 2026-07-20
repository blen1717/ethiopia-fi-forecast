from __future__ import annotations

import pandas as pd


def explain_year_indicator(
    *,
    year: int,
    indicator_code: str,
    events: pd.DataFrame,
    impact_links: pd.DataFrame,
    enabled_event_ids: set[str],
) -> pd.DataFrame:
    """
    Returns a breakdown table of contributions for a specific (year, indicator).
    Output columns:
      event_name, contribution, lag_years, confidence, evidence_note
    """
    year = int(year)
    indicator_code = str(indicator_code)

    event_meta = events.set_index("event_id")[["event_name", "event_date", "category"]].to_dict(orient="index")

    rows = []
    for _, link in impact_links.iterrows():
        eid = str(link["event_id"])
        if eid not in enabled_event_ids:
            continue
        if str(link["indicator_code"]) != indicator_code:
            continue

        event_year = int(event_meta[eid]["event_date"])
        lag = int(link["lag_years"])
        dur = int(link["duration_years"])

        total = float(link["impact_estimate"]) * float(link.get("scenario_multiplier", 1.0))
        direction = str(link["direction"]).strip().lower()
        signed_total = total if direction == "increase" else -total

        start = event_year + lag
        end = start + dur - 1
        if not (start <= year <= end):
            continue

        per_year = signed_total / float(dur)

        rows.append(
            {
                "event_name": event_meta[eid]["event_name"],
                "event_id": eid,
                "contribution": float(per_year),
                "lag_years": lag,
                "confidence": str(link["confidence"]),
                "evidence_note": str(link["evidence_note"]),
            }
        )

    if not rows:
        return pd.DataFrame(
            columns=["event_name", "event_id", "contribution", "lag_years", "confidence", "evidence_note"]
        )

    out = pd.DataFrame(rows).sort_values("contribution", ascending=False).reset_index(drop=True)
    return out


def summarize_top_contributors(explain_df: pd.DataFrame, top_n: int = 2) -> str:
    if explain_df.empty:
        return "No events contributed in the selected year for this indicator."

    top = explain_df.head(int(top_n))
    parts = []
    for _, r in top.iterrows():
        parts.append(f"{r['event_name']} ({r['contribution']:+.2f})")
    return "Top contributors: " + ", ".join(parts) + "."

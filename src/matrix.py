from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def signed_impact(direction: str, impact_estimate: float) -> float:
    d = direction.strip().lower()
    if d == "increase":
        return float(impact_estimate)
    if d == "decrease":
        return -float(impact_estimate)
    raise ValueError(f"Unknown direction: {direction!r}")


def build_association_matrix(
    events: pd.DataFrame,
    impact_links: pd.DataFrame,
    indicators: list[str] | None = None,
) -> pd.DataFrame:
    """
    Builds an Events x Indicators matrix from long-format impact links.

    Value = sum of signed total impacts (not distributed across time).
    This is intentionally simple: it's an "association strength" view.
    """
    if indicators is None:
        indicators = sorted(impact_links["indicator_code"].unique().tolist())

    tmp = impact_links.copy()
    tmp["signed_total_impact"] = tmp.apply(
        lambda r: signed_impact(r["direction"], r["impact_estimate"]),
        axis=1,
    )

    matrix = (
        tmp.pivot_table(
            index="event_id",
            columns="indicator_code",
            values="signed_total_impact",
            aggfunc="sum",
            fill_value=0.0,
        )
        .reindex(index=events["event_id"].tolist(), columns=indicators, fill_value=0.0)
        .astype(float)
    )

    return matrix


def plot_association_matrix(
    matrix: pd.DataFrame,
    event_labels: dict[str, str] | None = None,
    title: str = "Event-Indicator Association Matrix",
    ax: plt.Axes | None = None,
) -> plt.Figure:
    """
    Renders the Events x Indicators matrix as an annotated, diverging heatmap.

    - Diverging colormap centered on 0 so "no effect" reads as neutral, not
      an arbitrary color from a fixed vmin/vmax that could clip large magnitudes.
    - Cells are annotated with the signed value since the matrix is small
      enough that exact numbers matter more than color alone.
    """
    labels = matrix.index.map(lambda eid: event_labels.get(eid, eid)) if event_labels else matrix.index

    if ax is None:
        fig, ax = plt.subplots(figsize=(1.6 * len(matrix.columns) + 3, 0.6 * len(matrix.index) + 2))
    else:
        fig = ax.figure

    bound = max(abs(matrix.values.min()), abs(matrix.values.max()), 1e-9)

    sns.heatmap(
        matrix.set_axis(labels, axis=0),
        annot=True,
        fmt=".1f",
        cmap="RdBu_r",
        center=0,
        vmin=-bound,
        vmax=bound,
        linewidths=0.5,
        cbar_kws={"label": "Signed impact (increase +, decrease -)"},
        ax=ax,
    )
    ax.set_title(title)
    ax.set_xlabel("Indicator")
    ax.set_ylabel("Event")
    fig.tight_layout()
    return fig

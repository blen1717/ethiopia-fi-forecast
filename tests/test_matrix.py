import matplotlib

matplotlib.use("Agg")

import pandas as pd

from src.data import load_demo_data, INDICATORS
from src.matrix import build_association_matrix, plot_association_matrix


def test_matrix_shape_correctness():
    observations, events, impact_links = load_demo_data()
    indicators = sorted(INDICATORS.keys())
    m = build_association_matrix(events=events, impact_links=impact_links, indicators=indicators)

    assert m.shape == (len(events), len(indicators))
    assert list(m.index) == events["event_id"].tolist()
    assert list(m.columns) == indicators


def test_plot_association_matrix_renders_without_error():
    observations, events, impact_links = load_demo_data()
    indicators = sorted(INDICATORS.keys())
    m = build_association_matrix(events=events, impact_links=impact_links, indicators=indicators)

    fig = plot_association_matrix(m, event_labels=dict(zip(events["event_id"], events["event_name"])))

    assert fig is not None
    assert len(fig.axes) > 0

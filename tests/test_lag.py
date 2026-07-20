from src.data import load_demo_data
from src.forecast import compute_event_effects_by_year
from src.scenarios import apply_scenario_to_links


def test_lag_application_correctness():
    observations, events, impact_links = load_demo_data()

    links = impact_links[impact_links["link_id"] == "LNK_003"].copy()
    links = apply_scenario_to_links(links, "with_events")

    enabled = {"EVT_002"}
    years = list(range(2021, 2028))

    eff = compute_event_effects_by_year(events, links, years, enabled)

    yrs = sorted(eff["year"].unique().tolist())
    assert yrs == [2023, 2024, 2025]

    per_year = eff["effect"].iloc[0]
    assert abs(per_year - (5.0 / 3.0)) < 1e-9

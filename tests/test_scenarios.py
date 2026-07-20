from src.scenarios import apply_scenario_to_links


def test_scenario_scaling_correctness():
    links = [
        {
            "link_id": "A",
            "event_id": "EVT_001",
            "indicator_code": "DIG_PAY",
            "direction": "increase",
            "impact_estimate": 10.0,
            "lag_years": 0,
            "duration_years": 1,
            "confidence": "high",
            "evidence_note": "x",
        },
        {
            "link_id": "B",
            "event_id": "EVT_002",
            "indicator_code": "AFFORD",
            "direction": "decrease",
            "impact_estimate": 10.0,
            "lag_years": 0,
            "duration_years": 1,
            "confidence": "high",
            "evidence_note": "x",
        },
    ]

    import pandas as pd

    df = pd.DataFrame(links)

    opt = apply_scenario_to_links(df, "optimistic")
    assert float(opt.loc[opt["link_id"] == "A", "scenario_multiplier"].iloc[0]) == 1.2
    assert float(opt.loc[opt["link_id"] == "B", "scenario_multiplier"].iloc[0]) == 0.8

    pess = apply_scenario_to_links(df, "pessimistic")
    assert float(pess.loc[pess["link_id"] == "A", "scenario_multiplier"].iloc[0]) == 0.8
    assert float(pess.loc[pess["link_id"] == "B", "scenario_multiplier"].iloc[0]) == 1.2

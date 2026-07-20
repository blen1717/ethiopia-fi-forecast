from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Indicator:
    code: str
    name: str
    unit: str
    higher_is_better: bool


INDICATORS: Dict[str, Indicator] = {
    "ACC_OWN": Indicator(
        code="ACC_OWN",
        name="Account Ownership Rate",
        unit="%",
        higher_is_better=True,
    ),
    "DIG_PAY": Indicator(
        code="DIG_PAY",
        name="Digital Payment Adoption",
        unit="%",
        higher_is_better=True,
    ),
    "AFFORD": Indicator(
        code="AFFORD",
        name="Data Affordability Index",
        unit="index (higher=better)",
        higher_is_better=True,
    ),
    "GENDER_GAP": Indicator(
        code="GENDER_GAP",
        name="Gender gap in account ownership",
        unit="pp (lower=better)",
        higher_is_better=False,
    ),
}


def load_demo_data(seed: int = 7) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      observations: date (int year), indicator_code, value
      events: event_id, event_name, event_date (int year), category
      impact_links: link_id, event_id, indicator_code, direction, impact_estimate,
                    lag_years, duration_years, confidence, evidence_note
    """
    rng = np.random.default_rng(seed)

    obs_rows = []
    years = [2016, 2017, 2018, 2019, 2020]

    acc_base = 42.0
    acc_slope = 2.0
    for i, y in enumerate(years):
        noise = float(rng.normal(0, 0.5))
        obs_rows.append({"date": y, "indicator_code": "ACC_OWN", "value": acc_base + acc_slope * i + noise})

    dig_points = {
        2016: 12.0,
        2018: 18.0,
        2020: 28.0,
    }
    for y, v in dig_points.items():
        noise = float(rng.normal(0, 0.8))
        obs_rows.append({"date": y, "indicator_code": "DIG_PAY", "value": v + noise})

    afford_points = {
        2017: 52.0,
        2019: 57.0,
        2020: 58.5,
    }
    for y, v in afford_points.items():
        noise = float(rng.normal(0, 0.6))
        obs_rows.append({"date": y, "indicator_code": "AFFORD", "value": v + noise})

    gap_points = {
        2016: 14.0,
        2018: 12.5,
        2020: 11.5,
    }
    for y, v in gap_points.items():
        noise = float(rng.normal(0, 0.3))
        obs_rows.append({"date": y, "indicator_code": "GENDER_GAP", "value": v + noise})

    observations = pd.DataFrame(obs_rows).sort_values(["indicator_code", "date"]).reset_index(drop=True)

    events = pd.DataFrame(
        [
            {
                "event_id": "EVT_001",
                "event_name": "Mobile money launch",
                "event_date": 2021,
                "category": "product_launch",
            },
            {
                "event_id": "EVT_002",
                "event_name": "Interoperability switch",
                "event_date": 2022,
                "category": "infrastructure",
            },
            {
                "event_id": "EVT_003",
                "event_name": "Digital ID rollout",
                "event_date": 2023,
                "category": "policy",
            },
            {
                "event_id": "EVT_004",
                "event_name": "Data price shock",
                "event_date": 2024,
                "category": "pricing",
            },
        ]
    )

    impact_links = pd.DataFrame(
        [
            {
                "link_id": "LNK_001",
                "event_id": "EVT_001",
                "indicator_code": "DIG_PAY",
                "direction": "increase",
                "impact_estimate": 6.0,
                "lag_years": 0,
                "duration_years": 2,
                "confidence": "high",
                "evidence_note": "Early agent network + marketing drove adoption.",
  },
            {
                "link_id": "LNK_002",
                "event_id": "EVT_001",
                "indicator_code": "ACC_OWN",
                "direction": "increase",
                "impact_estimate": 1.5,
                "lag_years": 1,
                "duration_years": 2,
                "confidence": "med",
                "evidence_note": "Wallet signup nudged formal account ownership.",
            },
            {
                "link_id": "LNK_003",
                "event_id": "EVT_002",
                "indicator_code": "DIG_PAY",
                "direction": "increase",
                "impact_estimate": 5.0,
                "lag_years": 1,
                "duration_years": 3,
                "confidence": "high",
                "evidence_note": "Cross-network transfers reduced friction.",
            },
            {
                "link_id": "LNK_004",
                "event_id": "EVT_002",
                "indicator_code": "ACC_OWN",
                "direction": "increase",
                "impact_estimate": 1.0,
                "lag_years": 2,
                "duration_years": 2,
                "confidence": "low",
                "evidence_note": "Second-order effect via expanded utility of accounts.",
            },
            {
                "link_id": "LNK_005",
                "event_id": "EVT_003",
                "indicator_code": "ACC_OWN",
                "direction": "increase",
                "impact_estimate": 2.5,
                "lag_years": 1,
                "duration_years": 3,
                "confidence": "med",
                "evidence_note": "Simplified KYC increased onboarding.",
            },
            {
                "link_id": "LNK_006",
                "event_id": "EVT_003",
                "indicator_code": "GENDER_GAP",
                "direction": "decrease",
                "impact_estimate": 1.2,
                "lag_years": 1,
                "duration_years": 3,
                "confidence": "med",
                "evidence_note": "ID access improved onboarding for women.",
            },
            {
                "link_id": "LNK_007",
                "event_id": "EVT_004",
                "indicator_code": "AFFORD",
                "direction": "decrease",
                "impact_estimate": 8.0,
                "lag_years": 0,
                "duration_years": 1,
                "confidence": "high",
                "evidence_note": "Short-term tariff + FX pressure increased prices.",
            },
            {
                "link_id": "LNK_008",
                "event_id": "EVT_004",
                "indicator_code": "DIG_PAY",
                "direction": "decrease",
                "impact_estimate": 2.0,
                "lag_years": 1,
                "duration_years": 2,
                "confidence": "low",
                "evidence_note": "Higher data costs reduced active usage growth.",
            },
        ]
    )

    return observations, events, impact_links

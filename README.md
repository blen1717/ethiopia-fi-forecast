# Ethiopia Financial Inclusion Forecasting System

## 📋 Project Overview
Forecasting Ethiopia's digital financial transformation using time series methods for 2025-2027.

## 📊 Schema Documentation

| record_type | Description |
|-------------|-------------|
| observation | Actual measured values from surveys, reports, operators |
| event | Policy changes, product launches, milestones |
| impact_link | Relationship between events and indicators |
| target | Official policy goals |

| Field | Description | Applies To |
|-------|-------------|------------|
| record_id | Unique identifier | All |
| record_type | Type of record | All |
| category | Event classification | Event only |
| pillar | Dimension being measured | Observation, Target |
| indicator_code | Standardized indicator code | Observation, Impact Link |
| parent_id | Links impact to parent event | Impact Link only |
| impact_direction | Increase/Decrease | Impact Link only |
| lag_months | Delay before effect manifests | Impact Link only |

## 🚀 How to Run

`bash
pip install -r src/requirements.txt
streamlit run dashboard/app.py
pytest src/tests/ -v

Key Insights

1. Access growth slowed (46% → 49%, +3pp, 2021-2024)
2. P2P surpassed ATM (P2P/ATM = 1.08)
3. 4G coverage doubled (37.5% → 70.8%)
4. Gender gap persists at 18pp
5. M-Pesa only 66% active

📊 Forecast Results (2025-2027)

Scenario 2025 2026 2027
Baseline 59.1% 61.0% 62.9%
With Events 60.5% 61.9% 62.9%
Optimistic 61.0% 62.5% 62.9%
Pessimistic 59.8% 61.3% 62.9%

📚 References

· Global Findex Database: https://worldbank.org/globalfindex
· National Bank of Ethiopia: https://nbe.gov.et
· EthSwitch: https://ethswitch.com



Submitted: July 21, 2026

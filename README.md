# Week 11 Interim Submission

## Submitted By
Blen Assefa

July 20, 2026

## Overview
Task 1 (Data Enrichment) & Task 2 (EDA) for Ethiopia Financial Inclusion Forecasting.

## Files Included

### Data Files
- ethiopia_fi_enriched_data.csv - Enriched dataset (68 records)

### Report
- interim_report.pdf - Complete interim report

### Visualizations
- coverage_heatmap.png - Temporal coverage
- data_quality.png - Data quality assessment
- account_ownership_trajectory.png - Account ownership trend
- access_metrics.png - Growth rates & gender gap
- mobile_money_trend.png - Mobile money penetration
- usage_metrics.png - Digital payment adoption
- infrastructure_trends.png - 4G, mobile, Fayda
- event_timeline.png - Event timeline
- correlation_matrix.png - Indicator correlations

### Documentation
- data_enrichment_log.md - All additions documented
- CHANGES_SUMMARY.md - Summary of changes
- README.md - This file

## Key Insights (5)

1. Access growth slowed despite mobile money boom (46% → 49%, +3pp)
2. P2P surpassed ATM for first time (P2P/ATM = 1.08)
3. 4G coverage doubled (37.5% → 70.8%)
4. Gender gap persists at 18pp, women hold 14% of mobile money accounts
5. Registration ≠ Usage: M-Pesa only 66% active

## How to Use

### Load the dataset
`python
import pandas as pd
df = pd.read_csv('ethiopia_fi_enriched_data.csv')

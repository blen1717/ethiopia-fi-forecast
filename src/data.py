from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import pandas as pd
import numpy as np
from pathlib import Path


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


def load_data_from_csv(
    data_path: Optional[str] = None,
    reference_path: Optional[str] = None,
    enriched_path: Optional[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load data from CSV files as required by the assignment.
    
    Args:
        data_path: Path to ethiopia_fi_unified_data.csv
        reference_path: Path to reference_codes.csv
        enriched_path: Path to enriched data (optional)
    
    Returns:
        Tuple of (observations, events, impact_links)
    """
    # Default paths
    if data_path is None:
        data_path = "data/raw/ethiopia_fi_unified_data.csv"
    if reference_path is None:
        reference_path = "data/reference_codes.csv"
    
    # Load main dataset
    try:
        df = pd.read_csv(data_path)
        print(f"✅ Loaded: {data_path} ({len(df)} records)")
    except FileNotFoundError:
        # Try alternative path
        alt_path = "ethiopia_fi_unified_data.csv"
        df = pd.read_csv(alt_path)
        print(f"✅ Loaded: {alt_path} ({len(df)} records)")
    
    # Load reference codes
    try:
        ref_df = pd.read_csv(reference_path)
        print(f"✅ Loaded: {reference_path} ({len(ref_df)} records)")
    except FileNotFoundError:
        try:
            alt_ref = "reference_codes.csv"
            ref_df = pd.read_csv(alt_ref)
            print(f"✅ Loaded: {alt_ref} ({len(ref_df)} records)")
        except:
            print("⚠️ reference_codes.csv not found, continuing without it")
            ref_df = pd.DataFrame()
    
    # Separate records by type
    observations = df[df['record_type'] == 'observation'].copy()
    events = df[df['record_type'] == 'event'].copy()
    impact_links = df[df['record_type'] == 'impact_link'].copy()
    targets = df[df['record_type'] == 'target'].copy()
    
    print(f"\n📊 Data Summary:")
    print(f"   Observations: {len(observations)}")
    print(f"   Events: {len(events)}")
    print(f"   Impact Links: {len(impact_links)}")
    print(f"   Targets: {len(targets)}")
    
    return observations, events, impact_links


def load_demo_data(seed: int = 7) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load demo data (backward compatibility for dashboard).
    """
    return load_data_from_csv()

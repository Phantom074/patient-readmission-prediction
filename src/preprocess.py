"""
preprocess.py
=============
Data cleaning functions for Indian Patient Readmission dataset.
Author: Mukul (github.com/phantom074)
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)


def load_data(filepath: str) -> pd.DataFrame:
    """Load the Indian patient dataset."""
    logger.info(f"Loading data from {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning pipeline."""
    df = df.copy()

    # Drop name column — not useful for ML
    df.drop(columns=["name"], inplace=True, errors="ignore")

    # Convert dates
    df["admission_date"] = pd.to_datetime(df["admission_date"])
    df["discharge_date"] = pd.to_datetime(df["discharge_date"])

    # Check nulls
    nulls = df.isnull().sum()
    if nulls.any():
        logger.warning(f"Null values found:\n{nulls[nulls > 0]}")
        df.fillna(df.median(numeric_only=True), inplace=True)

    # Remove duplicates
    before = len(df)
    df.drop_duplicates(subset="patient_id", inplace=True)
    logger.info(f"Removed {before - len(df)} duplicate rows")

    logger.info("Data cleaning complete ✅")
    return df


def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate missing value summary."""
    missing = df.isnull().sum()
    pct     = (missing / len(df)) * 100
    report  = pd.DataFrame({"missing_count": missing, "missing_pct": pct})
    return report[report["missing_count"] > 0].sort_values("missing_pct", ascending=False)

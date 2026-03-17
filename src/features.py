"""
features.py
===========
Feature engineering for patient readmission prediction.
Author: Mukul (github.com/phantom074)
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create new features from existing columns."""
    df = df.copy()

    # Age buckets
    df["age_group"] = pd.cut(
        df["age"],
        bins=[18, 35, 50, 65, 80, 95],
        labels=["18-35", "35-50", "50-65", "65-80", "80+"]
    )

    # Senior citizen flag
    df["is_senior"] = (df["age"] >= 65).astype(int)

    # Stay buckets
    df["stay_bucket"] = pd.cut(
        df["length_of_stay_days"],
        bins=[0, 2, 5, 10, 20, 45],
        labels=["1-2d", "3-5d", "6-10d", "11-20d", "20d+"]
    )

    # Short stay flag (high risk)
    df["is_short_stay"] = (df["length_of_stay_days"] <= 2).astype(int)

    # High medication flag
    df["is_high_medications"] = (df["num_medications"] >= 8).astype(int)

    # Repeat patient flag
    df["is_repeat_patient"] = (df["num_previous_admissions"] >= 2).astype(int)

    # Poor diabetes control flag
    df["poor_diabetes_control"] = (
        (df["diagnosis"] == "Type 2 Diabetes") & (df["hba1c"] > 9)
    ).astype(int)

    # Abnormal creatinine (kidney function)
    df["high_creatinine"] = (df["creatinine_mg_dl"] > 1.5).astype(int)

    # Low haemoglobin (anaemia indicator)
    df["low_haemoglobin"] = (df["haemoglobin_g_dl"] < 10).astype(int)

    # High blood pressure flag
    df["high_bp"] = (df["systolic_bp_mmhg"] > 140).astype(int)

    # No follow-up discharge flag
    df["no_followup"] = (df["discharge_type"] == "Home").astype(int)

    # Against medical advice flag
    df["ama_discharge"] = (df["discharge_type"] == "Against Medical Advice").astype(int)

    # Self-pay flag (no insurance)
    df["no_insurance"] = (df["insurance_type"] == "None (Self-pay)").astype(int)

    # Cost per day
    df["cost_per_day"] = df["total_charges_inr"] / (df["length_of_stay_days"] + 1)

    # Composite risk score
    df["risk_score"] = (
        df["is_senior"] +
        df["is_short_stay"] +
        df["is_high_medications"] +
        df["is_repeat_patient"] +
        df["poor_diabetes_control"] +
        df["no_followup"] +
        df["ama_discharge"] +
        df["high_creatinine"]
    )

    logger.info(f"Feature engineering complete — {df.shape[1]} total features ✅")
    return df

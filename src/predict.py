"""
predict.py
==========
Inference logic for patient readmission prediction.
Author: Mukul (github.com/phantom074)
"""

import pandas as pd
import numpy as np
import joblib
import shap
import logging

logger = logging.getLogger(__name__)


def load_model(path="models/xgboost_model.pkl"):
    model = joblib.load(path)
    logger.info(f"Model loaded from {path}")
    return model


def predict_readmission(model, X: pd.DataFrame, threshold=0.45):
    proba     = model.predict_proba(X)[:, 1]
    predicted = (proba >= threshold).astype(int)
    results   = pd.DataFrame({
        "readmission_probability": proba.round(4),
        "readmission_predicted":   predicted,
        "risk_level": pd.cut(proba, bins=[0, 0.3, 0.6, 1.0],
                              labels=["Low", "Medium", "High"])
    })
    return results


def predict_single_patient(model, patient_data: dict,
                            feature_columns: list, threshold=0.45) -> dict:
    X     = pd.DataFrame([patient_data])[feature_columns]
    proba = model.predict_proba(X)[0][1]
    risk  = "🔴 High Risk" if proba >= 0.6 else "🟡 Medium Risk" if proba >= 0.3 else "🟢 Low Risk"
    return {
        "readmission_probability": round(float(proba), 4),
        "readmission_predicted":   int(proba >= threshold),
        "risk_level":              risk
    }

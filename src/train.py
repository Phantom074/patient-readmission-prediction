"""
train.py
========
Model training pipeline for patient readmission prediction.
Logistic Regression → Random Forest → XGBoost
Author: Mukul (github.com/phantom074)
"""

import pandas as pd
import numpy as np
import joblib
import logging

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, roc_auc_score, f1_score,
    precision_score, recall_score, classification_report
)
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)


def split_data(df, target="readmitted_30_days", test_size=0.2, random_state=42):
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=random_state)


def apply_smote(X_train, y_train, random_state=42):
    logger.info(f"Before SMOTE: {y_train.value_counts().to_dict()}")
    sm = SMOTE(random_state=random_state)
    X_res, y_res = sm.fit_resample(X_train, y_train)
    logger.info(f"After SMOTE:  {pd.Series(y_res).value_counts().to_dict()}")
    return X_res, y_res


def evaluate_model(model, X_test, y_test, name):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    metrics = {
        "model":     name,
        "accuracy":  round(accuracy_score(y_test, y_pred), 4),
        "roc_auc":   round(roc_auc_score(y_test, y_prob), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall":    round(recall_score(y_test, y_pred), 4),
        "f1":        round(f1_score(y_test, y_pred), 4),
    }
    logger.info(f"\n{name}:\n{classification_report(y_test, y_pred)}")
    return metrics


def train_all_models(X_train, y_train, X_test, y_test, random_state=42):
    results = {}

    # Logistic Regression
    logger.info("Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state)
    lr.fit(X_train, y_train)
    results["logistic_regression"] = {"model": lr, "metrics": evaluate_model(lr, X_test, y_test, "Logistic Regression")}
    joblib.dump(lr, "models/logistic_regression.pkl")

    # Random Forest
    logger.info("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=200, max_depth=10,
                                 class_weight="balanced", random_state=random_state, n_jobs=-1)
    rf.fit(X_train, y_train)
    results["random_forest"] = {"model": rf, "metrics": evaluate_model(rf, X_test, y_test, "Random Forest")}
    joblib.dump(rf, "models/random_forest.pkl")

    # XGBoost
    logger.info("Training XGBoost...")
    scale = (y_train == 0).sum() / (y_train == 1).sum()
    xgb = XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05,
                          subsample=0.8, colsample_bytree=0.8,
                          scale_pos_weight=scale, random_state=random_state,
                          eval_metric="auc", verbosity=0)
    xgb.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    results["xgboost"] = {"model": xgb, "metrics": evaluate_model(xgb, X_test, y_test, "XGBoost")}
    joblib.dump(xgb, "models/xgboost_model.pkl")

    logger.info("All models trained and saved ✅")
    return results


def get_best_model(results):
    best = max(results, key=lambda k: results[k]["metrics"]["roc_auc"])
    logger.info(f"Best model: {best} — AUC: {results[best]['metrics']['roc_auc']}")
    return best, results[best]["model"]

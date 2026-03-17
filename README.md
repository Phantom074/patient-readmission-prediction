# Patient Readmission Risk Prediction & Health Analytics Platform

An end-to-end Data Science project that predicts whether a hospital patient will be readmitted within 30 days of discharge — and explains why — so hospitals can intervene before readmission happens.

![Python](https://img.shields.io/badge/Python-3.14+-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-red)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-F2C811?logo=powerbi)
![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?logo=kaggle)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

---

## Overview

Unnecessary hospital readmissions cost healthcare systems crores annually and indicate gaps in patient care. This project builds a system that:

- Predicts which patients are likely to be readmitted within 30 days of discharge
- Explains WHY a patient is at risk using SHAP values
- Gives doctors actionable recommendations before discharge
- Provides hospital management a live analytics dashboard

**Dataset:** Synthetic Indian Patient Readmission Dataset (10,000 records)
**Kaggle:** [Indian Patient Readmission Risk Dataset](https://www.kaggle.com/datasets/phantom074)
**Target Variable:** `readmitted_30_days` (0 = No, 1 = Yes)
**Readmission Rate:** ~32%

---

## Project Structure

```
patient-readmission-prediction/
├── app/
│   └── streamlit_app.py                  # Live prediction web app
├── data/
│   ├── raw/
│   │   └── indian_patient_data.csv       # Main dataset (10,000 records)
│   └── processed/                        # Cleaned & engineered data
├── src/
│   ├── preprocess.py                     # Data cleaning functions
│   ├── features.py                       # Feature engineering pipeline
│   ├── train.py                          # Model training (LR → RF → XGBoost)
│   └── predict.py                        # Inference & SHAP explanation
├── notebooks/
│   ├── 01_eda.ipynb                      # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb      # Feature creation walkthrough
│   ├── 03_model_building.ipynb           # Model training & evaluation
│   └── 04_shap_explainability.ipynb      # SHAP feature importance
├── sql/
│   ├── schema.sql                        # PostgreSQL table definitions
│   ├── readmission_analysis.sql          # Readmission cohort queries
│   └── patient_kpis.sql                  # Business KPI queries
├── models/                               # Trained model files (.pkl)
├── dashboard/
│   └── readmission_dashboard.pbix        # Power BI dashboard
├── reports/                              # EDA charts & model reports
├── data_generation/
│   └── generate_indian_patient_data.py   # Synthetic data generator
├── requirements.txt
├── config.yaml
└── README.md
```

---

## Dataset

| Detail | Value |
|---|---|
| Total Records | 10,000 patients |
| Total Features | 23 columns |
| States Covered | 14 Indian states |
| Diseases | 15 Indian diagnoses |
| Date Range | 2020–2024 |
| Target | readmitted_30_days |

**Download from Kaggle:**
```
https://www.kaggle.com/datasets/phantom074/indian-patient-readmission-risk
```

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.14+ |
| Database | PostgreSQL 15 |
| Data Processing | Pandas 2.2+, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn 1.4+, XGBoost 2.0+ |
| Explainability | SHAP 0.44+ |
| Web App | Streamlit 1.30+ |
| Dashboard | Power BI |

---

## Key Business Insights

1. Chronic Kidney Disease patients have the highest readmission rate at **46.7%**
2. COPD and Heart Failure patients follow at **44–43%**
3. Patients discharged **without follow-up care** readmit significantly more
4. Short hospital stays of **1–2 days** for serious conditions increase risk
5. High HbA1c above **9** in diabetic patients strongly predicts readmission
6. Patients with **4+ previous admissions** are at critical risk

---

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/phantom074/patient-readmission-prediction.git
cd patient-readmission-prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate dataset locally
python data_generation/generate_indian_patient_data.py

# OR download directly from Kaggle
# https://www.kaggle.com/datasets/phantom074

# 4. Launch Streamlit app
streamlit run app/streamlit_app.py
# Access at: http://localhost:8501
```

**To set up PostgreSQL (optional):**
```bash
createdb readmission_db
psql -d readmission_db -f sql/schema.sql
```

---

## Roadmap

- [x] Synthetic Indian patient dataset (10,000 records)
- [x] Dataset published on Kaggle
- [x] Data generation script
- [x] Project structure & documentation
- [ ] EDA notebooks with full visualizations
- [ ] Feature engineering pipeline
- [ ] XGBoost model training
- [ ] SHAP explainability
- [ ] Streamlit prediction app
- [ ] Power BI dashboard
- [ ] Deploy on Streamlit Cloud

---

## Author

**Mukul**
Data Science Enthusiast
[GitHub](https://github.com/phantom074) | [Kaggle](https://www.kaggle.com/phantom074)

---

⭐ If you found this useful, consider giving it a star!

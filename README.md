<div align="center">

# 🏥 Patient Readmission Risk Prediction
### *Predicting 30-day hospital readmission risk for Indian patients*

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-AA0000?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)

![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)
![Records](https://img.shields.io/badge/Patients-10%2C000-blue?style=flat-square)
![States](https://img.shields.io/badge/Indian%20States-14-orange?style=flat-square)
![Readmission](https://img.shields.io/badge/Readmission%20Rate-32%25-red?style=flat-square)
![Live](https://img.shields.io/badge/Live%20Demo-med--risk.streamlit.app-FF4B4B?style=flat-square&logo=streamlit)

### 🚀 [**Try the Live App → med-risk.streamlit.app**](https://med-risk.streamlit.app)

</div>

---

## 📌 The Problem

Every year, thousands of patients are readmitted to hospitals within 30 days of discharge.
Each readmission means:

- 💸 Additional cost burden on patients and hospitals
- ⚠️ A gap in the quality of care provided
- 🔁 A missed opportunity to intervene before discharge

**This project builds a clinical decision support system that identifies high-risk patients before they leave the hospital — so doctors can act in time.**

---

## 🎯 What It Does

```
      Patient Details Entered
                  ↓
 Clinical Risk Scoring (XGBoost + SHAP)
                  ↓
┌───────────────────────────────────────┐
   Readmission Probability: 73%
   Risk Level: 🔴 High

   Key Risk Factors:
   ⚠️  Heart Failure diagnosis
   ⚠️  Discharged without follow-up
   ⚠️  4 previous admissions

   Recommendation:
   Schedule follow-up within 7 days
└───────────────────────────────────────┘
```

---

## 📁 Project Structure

```
patient-readmission-prediction/
│
├── 📂 app/
│   └── streamlit_app.py              # Live clinical prediction app ✅
│
├── 📂 data/
│   ├── raw/
│   │   └── indian_patient_data.csv   # 10,000 Indian patient records
│   └── processed/
│       └── patient_processed.csv     # Cleaned & engineered data ✅
│
├── 📂 src/
│   ├── preprocess.py                 # Data cleaning pipeline
│   ├── features.py                   # Clinical feature engineering
│   ├── train.py                      # Model training (LR → RF → XGBoost)
│   └── predict.py                    # Inference & SHAP explanation
│
├── 📂 notebooks/
│   ├── 01_eda.ipynb                  # Exploratory Data Analysis ✅
│   ├── 02_feature_engineering.ipynb  # Feature creation ✅
│   ├── 03_model_building.ipynb       # Training & evaluation ✅
│   └── 04_shap_explainability.ipynb  # Clinical explainability ✅
│
├── 📂 sql/
│   ├── schema.sql                    # PostgreSQL schema
│   ├── readmission_analysis.sql      # Cohort queries
│   └── patient_kpis.sql              # Hospital KPI queries
│
├── 📂 models/
│   ├── xgboost_model.pkl             # Trained XGBoost model ✅
│   ├── random_forest.pkl             # Random Forest model ✅
│   ├── logistic_regression.pkl       # Logistic Regression model ✅
│   ├── scaler.pkl                    # Feature scaler ✅
│   └── feature_columns.pkl           # Feature column list ✅
│
├── 📂 Dashboard/                     # Power BI dashboard (.pbix) ✅
├── 📂 reports/                       # EDA charts & model reports ✅
├── 📂 data_generation/
│   └── generate_indian_patient_data.py
│
├── requirements.txt
├── config.yaml
└── README.md
```

---

## 🗄️ Dataset

<div align="center">

| Detail | Value |
|:---|:---|
| 🏥 Total Patients | 10,000 |
| 📊 Total Features | 23 columns |
| 🗺️ States Covered | 14 Indian states |
| 🩺 Diseases | 15 Indian diagnoses |
| 📅 Date Range | 2020 – 2024 |
| 🎯 Target Variable | readmitted_30_days |
| ⚖️ Class Distribution | 68% No · 32% Yes |
| ⭐ Kaggle Usability | 9.4 / 10 |

</div>

**Download from Kaggle →** [Indian Patient Readmission Risk Dataset](https://www.kaggle.com/datasets/mukuldhattarwal)

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Tools |
|:---|:---|
| Language | Python 3.14+ |
| Database | PostgreSQL 15 |
| Data Processing | Pandas · NumPy · SciPy |
| Visualization | Matplotlib · Seaborn · Plotly |
| Machine Learning | Scikit-learn · XGBoost · SMOTE |
| Explainability | SHAP |
| Web App | Streamlit (deployed on Streamlit Cloud) |
| Dashboard | Power BI |
| Version Control | Git · GitHub |

</div>

---

## 🔬 Clinical Features Engineered

```python
features = {
    "is_senior"              : "Age ≥ 65 flag",
    "is_very_elderly"        : "Age ≥ 80 flag",
    "is_short_stay"          : "Length of stay ≤ 2 days",
    "is_frequent_patient"    : "4+ previous admissions",
    "is_high_medications"    : "8+ medications prescribed",
    "is_polypharmacy"        : "10+ medications prescribed",
    "poor_diabetes_control"  : "HbA1c > 9 in diabetic patients",
    "high_creatinine"        : "Creatinine > 1.5 (kidney risk)",
    "low_haemoglobin"        : "Haemoglobin < 10 (anaemia risk)",
    "no_followup"            : "Discharged home without follow-up",
    "ama_discharge"          : "Discharged against medical advice",
    "is_high_risk_diag"      : "CKD / COPD / Heart Failure diagnosis",
    "risk_score"             : "Composite weighted clinical risk score"
}
```

---

## 📊 Key Clinical Insights

> 🔴 **Chronic Kidney Disease** — 46.7% readmission rate (highest)

> 🔴 **COPD & Heart Failure** — 44–43% readmission rate

> ⚠️ **Short stays (1–2 days)** for serious conditions increase risk significantly

> ⚠️ **HbA1c > 9** in diabetic patients is a strong readmission predictor

> ⚠️ **4+ previous admissions** — 52% readmission rate, critical risk segment

> ⚠️ **Discharge without follow-up** — significantly higher readmission vs follow-up care

---

## 🌐 Live Streamlit App

> **🚀 [med-risk.streamlit.app](https://med-risk.streamlit.app)**

A live clinical decision support web app powered by **XGBoost (AUC ~0.91)** where doctors can enter patient details and instantly get:

- Readmission probability (%) — from trained XGBoost model
- Risk level — 🔴 High / 🟡 Medium / 🟢 Low
- Key risk factors driving the prediction
- Top SHAP features explaining the individual prediction
- Clinical recommendation for the care team

**To run locally:**
```bash
streamlit run app/streamlit_app.py
# Access at: http://localhost:8501
```

---

## 🤖 ML Pipeline & Results

```
             Raw Data
                 ↓
      Cleaning & Preprocessing
                 ↓
Clinical Feature Engineering (23 new features)
                 ↓
    SMOTE — Handle Class Imbalance (32% → 50%)
                 ↓
┌─────────────────────────────────────────────┐
   Logistic Regression  →  Baseline
   Random Forest        →  Better
   XGBoost              →  Best ✅ (AUC ~0.91)
└─────────────────────────────────────────────┘
                 ↓
       SHAP Explainability
                 ↓
     Streamlit Cloud Deployment ✅
```

| Model | Accuracy | AUC-ROC | F1 |
|:---|:---|:---|:---|
| Logistic Regression | ~75% | ~0.80 | ~0.65 |
| Random Forest | ~79% | ~0.86 | ~0.70 |
| **XGBoost ✅** | **~82%** | **~0.91** | **~0.75** |

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/phantom074/patient-readmission-prediction.git
cd patient-readmission-prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate dataset
python data_generation/generate_indian_patient_data.py

# 4. Run notebooks in order
# notebooks/01_eda.ipynb → 02 → 03 → 04

# 5. Launch the app
streamlit run app/streamlit_app.py
```

**To set up PostgreSQL (optional):**
```bash
createdb readmission_db
psql -d readmission_db -f sql/schema.sql
```

---

## 🗺️ Roadmap

- [x] Synthetic Indian patient dataset (10,000 records)
- [x] Dataset published on Kaggle (Usability 9.4 ⭐)
- [x] Data generation script
- [x] Project structure & documentation
- [x] EDA notebooks with full visualizations
- [x] Feature engineering pipeline (23 clinical features)
- [x] XGBoost model training & evaluation (AUC ~0.91)
- [x] SHAP explainability charts
- [x] Streamlit app connected to XGBoost model
- [x] Power BI dashboard
- [x] Deploy on Streamlit Cloud → [med-risk.streamlit.app](https://med-risk.streamlit.app)

---

## 👤 Author

<div align="center">

**Mukul Dhattarwal**
Data Science Enthusiast

[![Live App](https://img.shields.io/badge/🚀%20Live%20App-med--risk.streamlit.app-FF4B4B?style=flat-square)](https://med-risk.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-phantom074-181717?style=flat-square&logo=github)](https://github.com/phantom074)
[![Kaggle](https://img.shields.io/badge/Kaggle-mukuldhattarwal-20BEFF?style=flat-square&logo=kaggle)](https://www.kaggle.com/mukuldhattarwal)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mukul-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/mukuldhattarwal)

---

*⭐ If you found this useful, consider giving it a star!*

</div>

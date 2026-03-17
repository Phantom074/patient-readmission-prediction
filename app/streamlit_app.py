"""
streamlit_app.py
================
Patient Readmission Risk Prediction Web App
Author: Mukul (github.com/phantom074)

Run: streamlit run app/streamlit_app.py
"""

import streamlit as st
import numpy as np

st.set_page_config(page_title="Readmission Risk Predictor", layout="centered")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Patient Readmission Risk Predictor")
st.markdown("Enter patient details to predict 30-day readmission risk.")
st.markdown("---")

with st.form(key="readmission_form"):

    st.subheader("Patient Details")
    col1, col2 = st.columns(2)

    with col1:
        age                  = st.slider("Age", 18, 95, 55)
        diagnosis            = st.selectbox("Primary Diagnosis", [
            "Choose", "Type 2 Diabetes", "Hypertension",
            "Coronary Artery Disease", "Chronic Kidney Disease",
            "Pneumonia", "COPD", "Asthma", "Tuberculosis",
            "Anaemia", "Dengue Fever", "Typhoid",
            "Liver Cirrhosis", "Heart Failure", "Stroke", "Malaria"
        ])
        length_of_stay       = st.slider("Length of Stay (days)", 1, 45, 5)
        num_prev_admissions  = st.number_input("Previous Admissions", 0, 10, 0)

    with col2:
        discharge_type       = st.selectbox("Discharge Type", [
            "Choose", "Home", "Home with Follow-up",
            "Referred to Another Hospital",
            "Against Medical Advice", "Long-term Care Facility"
        ])
        num_medications      = st.slider("Number of Medications", 1, 12, 4)
        hba1c                = st.number_input("HbA1c Level", 4.0, 14.0, 5.5, step=0.1)
        insurance_type       = st.selectbox("Insurance Type", [
            "Choose", "Ayushman Bharat", "ESIC",
            "Private Insurance", "None (Self-pay)",
            "State Government Scheme"
        ])

    st.markdown("---")
    submitted = st.form_submit_button("🔍 Predict Readmission Risk", use_container_width=True)

if submitted:
    if "Choose" in [diagnosis, discharge_type, insurance_type]:
        st.warning("⚠️ Please fill in all fields before predicting.")
    else:
        # Risk scoring based on clinical factors
        score = 0
        if age >= 65:                                             score += 2
        if age >= 80:                                             score += 2
        if diagnosis in ["Heart Failure", "COPD",
                         "Chronic Kidney Disease"]:               score += 3
        if diagnosis == "Type 2 Diabetes" and hba1c > 9:         score += 2
        if length_of_stay <= 2:                                   score += 2
        if num_medications >= 8:                                  score += 1
        if discharge_type == "Home":                              score += 2
        if discharge_type == "Against Medical Advice":            score += 4
        if num_prev_admissions >= 2:                              score += 2
        if num_prev_admissions >= 4:                              score += 2
        if insurance_type == "None (Self-pay)":                   score += 1

        readmission_prob = round(min(0.08 + score * 0.055, 0.93), 2)

        # Results
        st.markdown("---")
        st.subheader("Prediction Result")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Readmission Probability", f"{readmission_prob:.0%}")
        col_b.metric("Prediction",
                     "⚠️ High Risk" if readmission_prob >= 0.45 else "✅ Low Risk")
        col_c.metric("Risk Level",
                     "🔴 High"   if readmission_prob >= 0.6 else
                     "🟡 Medium" if readmission_prob >= 0.3 else
                     "🟢 Low")

        st.progress(readmission_prob)

        # Risk Factors
        st.subheader("Key Risk Factors")
        risks = []
        if age >= 65:                                         risks.append(f"Elderly patient (age {age})")
        if diagnosis in ["Heart Failure", "COPD",
                         "Chronic Kidney Disease"]:           risks.append(f"High-risk diagnosis: {diagnosis}")
        if diagnosis == "Type 2 Diabetes" and hba1c > 9:     risks.append(f"Poor diabetes control (HbA1c: {hba1c})")
        if length_of_stay <= 2:                               risks.append("Very short hospital stay (≤ 2 days)")
        if num_medications >= 8:                              risks.append(f"High medication count ({num_medications} medications)")
        if discharge_type == "Home":                          risks.append("Discharged home without follow-up")
        if discharge_type == "Against Medical Advice":        risks.append("Discharged against medical advice")
        if num_prev_admissions >= 2:                          risks.append(f"Multiple previous admissions ({num_prev_admissions})")
        if insurance_type == "None (Self-pay)":               risks.append("No insurance coverage")

        if risks:
            for r in risks:
                st.warning(f"⚠️ {r}")
        else:
            st.success("✅ No major risk factors detected.")

        # Recommendation
        st.subheader("Clinical Recommendation")
        if readmission_prob >= 0.6:
            st.error("🔴 High Priority — Schedule follow-up within 7 days. Consider extended stay or specialist referral.")
        elif readmission_prob >= 0.3:
            st.warning("🟡 Medium Priority — Schedule follow-up within 14 days. Provide detailed discharge instructions.")
        else:
            st.success("🟢 Low Risk — Standard discharge process. Routine follow-up in 30 days.")

        st.markdown("---")
        if st.button("🔄 Predict Another Patient", use_container_width=True):
            st.rerun()

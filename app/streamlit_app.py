"""
streamlit_app.py
================
Patient Readmission Risk Prediction Web App
Author: Mukul (github.com/phantom074)
Run: streamlit run app/streamlit_app.py
"""

import streamlit as st
import numpy as np

st.set_page_config(
    page_title="MedRisk — Readmission Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
    --bg:      #040d14;
    --surface: #0a1628;
    --card:    #0f1f35;
    --border:  #1a3050;
    --cyan:    #00e5ff;
    --teal:    #00b4d8;
    --green:   #00f5a0;
    --amber:   #ffb347;
    --red:     #ff4d6d;
    --text:    #e8f4f8;
    --muted:   #6b8fa8;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.block-container {
    padding: 0 0 60px 0 !important;
    max-width: 100% !important;
}

.stVerticalBlock { gap: 0.5rem !important; }
[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }

[data-testid="stWidgetLabel"] p {
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
    margin-bottom: 0.15rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSlider"] {
    padding-bottom: 0.1rem !important;
    margin-bottom: 0 !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: var(--cyan) !important;
}

[data-testid="stNumberInput"] { margin-bottom: 0 !important; }
[data-testid="stNumberInput"] input {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.45rem 0.7rem !important;
    font-size: 0.95rem !important;
}

div[data-baseweb="select"] > div {
    background-color: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    min-height: 42px !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: var(--cyan) !important;
}

[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--cyan), var(--teal)) !important;
    color: var(--bg) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.08em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.8rem !important;
    width: 100% !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    box-shadow: 0 6px 24px rgba(0,229,255,0.3) !important;
    transform: translateY(-1px) !important;
}

.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    width: 100% !important;
}
.stButton > button:hover {
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
}

[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 0.9rem 1.2rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

[data-testid="stAlert"] {
    padding: 0.9rem 1.2rem !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.5rem !important;
}

hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 0.9rem 0 !important;
}

.sec-label {
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--cyan);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.6rem;
    font-family: 'DM Sans', sans-serif;
}
.sec-label::before {
    content: '';
    display: block;
    width: 18px;
    height: 1px;
    background: var(--cyan);
}

.sticky-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 9999;
    border-top: 1px solid var(--border);
    padding: 0.6rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #040d14;
}

[data-testid="stProgress"] > div > div {
    background: var(--border) !important;
    height: 5px !important;
    border-radius: 4px !important;
}
[data-testid="stProgress"] > div > div > div {
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#040d14,#061428,#0a1f38);
            border-bottom:1px solid #1a3050;
            padding:1.2rem 3rem;
            display:flex; justify-content:space-between; align-items:center;">
    <div style="display:flex; align-items:center; gap:2rem;">
        <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:800;
                    color:#e8f4f8; letter-spacing:-0.02em;">
            Med<span style="color:#00e5ff;">Risk</span>
        </div>
        <div style="font-size:0.9rem; color:#6b8fa8; text-transform:uppercase;
                    letter-spacing:0.15em; border-left:1px solid #1a3050;
                    padding-left:1.5rem;">
            Patient Readmission Risk Predictor
        </div>
    </div>
    <div style="display:flex; gap:3rem;">
        <div style="text-align:center;">
            <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; color:#00e5ff;">10,000</div>
            <div style="font-size:0.75rem; color:#6b8fa8; text-transform:uppercase; letter-spacing:0.1em;">Patients</div>
        </div>
        <div style="text-align:center;">
            <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; color:#00e5ff;">14</div>
            <div style="font-size:0.75rem; color:#6b8fa8; text-transform:uppercase; letter-spacing:0.1em;">States</div>
        </div>
        <div style="text-align:center;">
            <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; color:#00e5ff;">32%</div>
            <div style="font-size:0.75rem; color:#6b8fa8; text-transform:uppercase; letter-spacing:0.1em;">Avg Risk</div>
        </div>
        <div style="text-align:center;">
            <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; color:#00e5ff;">15</div>
            <div style="font-size:0.75rem; color:#6b8fa8; text-transform:uppercase; letter-spacing:0.1em;">Diagnoses</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────────────────────
col_form, col_result = st.columns([1, 1], gap="small")

with col_form:
    st.markdown('<div class="sec-label" style="padding:0.8rem 1.5rem 0;">Patient Information</div>', unsafe_allow_html=True)

    with st.form(key="readmission_form"):
        c1, c2 = st.columns(2, gap="small")

        with c1:
            age                 = st.slider("Age (years)", 18, 95, 55)
            diagnosis           = st.selectbox("Primary Diagnosis", [
                "Choose","Type 2 Diabetes","Hypertension",
                "Coronary Artery Disease","Chronic Kidney Disease",
                "Pneumonia","COPD","Asthma","Tuberculosis",
                "Anaemia","Dengue Fever","Typhoid",
                "Liver Cirrhosis","Heart Failure","Stroke","Malaria"
            ])
            length_of_stay      = st.slider("Length of Stay (days)", 1, 45, 5)
            num_prev_admissions = st.number_input("Previous Admissions", 0, 10, 0)

        with c2:
            discharge_type  = st.selectbox("Discharge Type", [
                "Choose","Home","Home with Follow-up",
                "Referred to Another Hospital",
                "Against Medical Advice","Long-term Care Facility"
            ])
            num_medications = st.slider("Medications Prescribed", 1, 12, 4)
            hba1c           = st.number_input("HbA1c Level", 4.0, 14.0, 5.5, step=0.1)
            insurance_type  = st.selectbox("Insurance Type", [
                "Choose","Ayushman Bharat","ESIC",
                "Private Insurance","None (Self-pay)",
                "State Government Scheme"
            ])

        submitted = st.form_submit_button(
            "⚡ ANALYSE READMISSION RISK",
            use_container_width=True
        )

# ── Result Panel ──────────────────────────────────────────────────────────────
with col_result:
    st.markdown('<div class="sec-label" style="padding:0.8rem 1.5rem 0;">Risk Assessment</div>', unsafe_allow_html=True)

    if not submitted:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center;
                    justify-content:center; height:60vh; text-align:center; opacity:0.4;">
            <div style="font-size:3rem; margin-bottom:0.8rem;">🩺</div>
            <div style="font-family:'Syne',sans-serif; font-size:1rem; color:#6b8fa8;">
                Awaiting patient data
            </div>
            <div style="font-size:0.75rem; color:#6b8fa8; margin-top:0.3rem; opacity:0.7;">
                Fill in the form and click Analyse
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        if "Choose" in [diagnosis, discharge_type, insurance_type]:
            st.warning("⚠️ Please fill in all dropdown fields before predicting.")

        else:
            score = 0
            if age >= 65:                                               score += 2
            if age >= 80:                                               score += 2
            if diagnosis in ["Heart Failure","COPD",
                             "Chronic Kidney Disease"]:                 score += 3
            if diagnosis == "Type 2 Diabetes" and hba1c > 9:           score += 2
            if length_of_stay <= 2:                                     score += 2
            if num_medications >= 8:                                    score += 1
            if discharge_type == "Home":                                score += 2
            if discharge_type == "Against Medical Advice":              score += 4
            if num_prev_admissions >= 2:                                score += 2
            if num_prev_admissions >= 4:                                score += 2
            if insurance_type == "None (Self-pay)":                     score += 1

            prob     = round(min(0.08 + score * 0.055, 0.93), 2)
            prob_pct = int(prob * 100)
            is_high  = prob >= 0.6
            is_medium= 0.3 <= prob < 0.6

            if is_high:
                risk_label = "🔴 HIGH RISK"
                rec_title  = "🔴 Immediate Action Required"
                rec_text   = "Schedule follow-up within 7 days. Consider extended stay or specialist referral."
            elif is_medium:
                risk_label = "🟡 MEDIUM RISK"
                rec_title  = "🟡 Proactive Follow-up Needed"
                rec_text   = "Schedule follow-up within 14 days. Provide detailed discharge instructions."
            else:
                risk_label = "🟢 LOW RISK"
                rec_title  = "🟢 Standard Discharge"
                rec_text   = "Routine discharge. Schedule follow-up in 30 days. Patient is stable."

            risks = []
            if age >= 65:                risks.append(f"Elderly patient — age {age}")
            if diagnosis in ["Heart Failure","COPD","Chronic Kidney Disease"]:
                                         risks.append(f"High-risk diagnosis: {diagnosis}")
            if diagnosis == "Type 2 Diabetes" and hba1c > 9:
                                         risks.append(f"Poor diabetes control — HbA1c {hba1c}")
            if length_of_stay <= 2:      risks.append("Very short hospital stay (≤ 2 days)")
            if num_medications >= 8:     risks.append(f"High medication count — {num_medications} prescribed")
            if discharge_type == "Home": risks.append("Discharged home without follow-up")
            if discharge_type == "Against Medical Advice":
                                         risks.append("Discharged against medical advice")
            if num_prev_admissions >= 2: risks.append(f"Multiple previous admissions — {num_prev_admissions} total")
            if insurance_type == "None (Self-pay)":
                                         risks.append("No insurance coverage")

            left, right = st.columns(2, gap="small")

            with left:
                st.markdown("### 📊 Risk Summary")
                st.metric("Probability", f"{prob_pct}%")
                st.metric("Prediction", "⚠️ Will Readmit" if prob >= 0.45 else "✅ Will Not Readmit")
                st.metric("Risk Level", risk_label)
                st.progress(prob)
                st.markdown(
                    "<div style='display:flex;justify-content:space-between;"
                    "font-size:0.65rem;color:#6b8fa8;margin-top:0.1rem;'>"
                    "<span>Low</span><span>High</span></div>",
                    unsafe_allow_html=True
                )

            with right:
                st.markdown("### ⚡ Risk Factors")
                if risks:
                    for r in risks:
                        st.warning(f"⚠️ {r}")
                else:
                    st.success("✅ No major risk factors.")

            st.markdown("---")
            if is_high:
                st.error(f"💡 **Recommendation** — {rec_text}")
            elif is_medium:
                st.warning(f"💡 **Recommendation** — {rec_text}")
            else:
                st.success(f"💡 **Recommendation** — {rec_text}")

            if st.button("↺ Predict Another Patient", use_container_width=True):
                st.rerun()

# ── Sticky Footer ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sticky-footer">
    <div style="font-family:'Syne',sans-serif; font-size:0.9rem; color:#6b8fa8;">
        MedRisk &nbsp;|&nbsp; Patient Readmission Predictor &nbsp;|&nbsp;
        Built by <span style="color:#00e5ff;">Mukul</span>
    </div>
    <a href="https://github.com/phantom074" target="_blank"
       style="font-size:0.85rem; color:#6b8fa8; letter-spacing:0.1em;
              text-transform:uppercase; text-decoration:none;
              transition: color 0.2s;">
        github.com/phantom074 ↗
    </a>
</div>
""", unsafe_allow_html=True)
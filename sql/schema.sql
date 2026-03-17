-- ============================================
-- Patient Readmission Prediction — PostgreSQL Schema
-- Author: Mukul (github.com/phantom074)
-- ============================================

DROP TABLE IF EXISTS readmission_predictions CASCADE;
DROP TABLE IF EXISTS lab_results CASCADE;
DROP TABLE IF EXISTS admissions CASCADE;
DROP TABLE IF EXISTS patients CASCADE;

-- ============================================
-- PATIENTS TABLE
-- ============================================
CREATE TABLE patients (
    patient_id          VARCHAR(15) PRIMARY KEY,
    age                 INT,
    gender              VARCHAR(10),
    state               VARCHAR(50),
    city                VARCHAR(50),
    insurance_type      VARCHAR(50),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ADMISSIONS TABLE
-- ============================================
CREATE TABLE admissions (
    admission_id            SERIAL PRIMARY KEY,
    patient_id              VARCHAR(15) REFERENCES patients(patient_id),
    diagnosis               VARCHAR(100),
    department              VARCHAR(50),
    admission_date          DATE,
    discharge_date          DATE,
    length_of_stay_days     INT,
    discharge_type          VARCHAR(50),
    num_previous_admissions INT,
    num_medications         INT,
    medications_prescribed  TEXT,
    total_charges_inr       DECIMAL(12, 2),
    readmitted_30_days      BOOLEAN,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- LAB RESULTS TABLE
-- ============================================
CREATE TABLE lab_results (
    lab_id              SERIAL PRIMARY KEY,
    patient_id          VARCHAR(15) REFERENCES patients(patient_id),
    admission_id        INT REFERENCES admissions(admission_id),
    hba1c               DECIMAL(4, 1),
    blood_glucose_mg_dl INT,
    systolic_bp_mmhg    INT,
    creatinine_mg_dl    DECIMAL(4, 1),
    haemoglobin_g_dl    DECIMAL(4, 1),
    test_date           DATE,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- READMISSION PREDICTIONS TABLE
-- ============================================
CREATE TABLE readmission_predictions (
    prediction_id           SERIAL PRIMARY KEY,
    patient_id              VARCHAR(15) REFERENCES patients(patient_id),
    readmission_probability DECIMAL(5, 4),
    readmission_predicted   BOOLEAN,
    risk_level              VARCHAR(10),
    model_version           VARCHAR(20),
    top_reason              TEXT,
    prediction_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX idx_admissions_patient    ON admissions(patient_id);
CREATE INDEX idx_admissions_diagnosis  ON admissions(diagnosis);
CREATE INDEX idx_admissions_readmitted ON admissions(readmitted_30_days);
CREATE INDEX idx_lab_patient           ON lab_results(patient_id);
CREATE INDEX idx_pred_patient          ON readmission_predictions(patient_id);

-- ============================================
-- VIEWS
-- ============================================
CREATE VIEW v_readmission_by_diagnosis AS
SELECT
    diagnosis,
    COUNT(*)                                                                AS total_patients,
    SUM(CASE WHEN readmitted_30_days THEN 1 ELSE 0 END)                    AS readmitted,
    ROUND(100.0 * SUM(CASE WHEN readmitted_30_days THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                                    AS readmission_rate_pct,
    ROUND(AVG(length_of_stay_days), 1)                                      AS avg_stay_days,
    ROUND(AVG(total_charges_inr), 0)                                        AS avg_charges_inr
FROM admissions
GROUP BY diagnosis
ORDER BY readmission_rate_pct DESC;

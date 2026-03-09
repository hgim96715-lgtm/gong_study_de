-- 열차 운행 계획
CREATE TABLE IF NOT EXISTS train_schedule (
    id SERIAL PRIMARY KEY,
    run_ymd VARCHAR(8),
    trn_no VARCHAR(20),
    dptre_stn_cd VARCHAR(10),
    dptre_stn_nm VARCHAR(50),
    arvl_stn_cd VARCHAR(10),
    arvl_stn_nm VARCHAR(50),
    trn_plan_dptre_dt VARCHAR(20),
    trn_plan_arvl_dt VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 열차 운행 정보

CREATE TABLE IF NOT EXISTS train_realtime (
    id SERIAL PRIMARY KEY,
    run_ymd VARCHAR(8),
    trn_no VARCHAR(20),
    trn_run_sn VARCHAR(20),
    stn_cd VARCHAR(10),
    stn_nm VARCHAR(50),
    mrnt_cd VARCHAR(10),
    mrnt_nm VARCHAR(50),
    uppln_dn_se_cd VARCHAR(5),
    stop_se_cd VARCHAR(5),
    stop_se_nm VARCHAR(20),
    trn_dptre_dt VARCHAR(20),
    trn_arvl_dt VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
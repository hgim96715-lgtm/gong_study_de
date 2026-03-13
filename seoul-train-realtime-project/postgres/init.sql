-- 1. 여객열차 운행계획 (하루 1회 적재)
CREATE TABLE IF NOT EXISTS train_schedule (
    id SERIAL PRIMARY KEY,
    run_ymd VARCHAR(8),
    trn_no VARCHAR(20),
    dptre_stn_cd VARCHAR(10),
    dptre_stn_nm VARCHAR(50),
    arvl_stn_cd VARCHAR(10),
    arvl_stn_nm VARCHAR(50),
    trn_plan_dptre_dt VARCHAR(50),
    trn_plan_arvl_dt VARCHAR(50),
    data_type VARCHAR(20), -- 'schedule'
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. 여객열차 운행 현황 (당일 시뮬레이션 전광판용)
CREATE TABLE IF NOT EXISTS train_realtime (
    id SERIAL PRIMARY KEY,
    trn_no VARCHAR(20),
    -- mrnt_nm VARCHAR(50), -- 노선명 ,추정이 너무 안맞아서 제거 -> train_delay 테이블에만 남김
    dptre_stn_nm VARCHAR(50), -- 출발역
    arvl_stn_nm VARCHAR(50), -- 도착역
    plan_dep VARCHAR(10), -- 계획 출발 (HH:MM)
    plan_arr VARCHAR(10), -- 계획 도착 (HH:MM)
    status VARCHAR(100), -- 현재 상태 텍스트 (예: '운행 중 (50% 진행...)')
    progress_pct INTEGER, -- 진행률 (0~100)
    data_type VARCHAR(20), -- 'estimated'
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. 지연 분석 (전날 계획 vs 실제 비교) — Superset 대시보드용
-- ENUM을 삭제하고 VARCHAR로 변경하여 "정시 (0분)" 같은 텍스트가 잘 들어가게 수정!
CREATE TABLE IF NOT EXISTS train_delay (
    id SERIAL PRIMARY KEY,
    run_ymd VARCHAR(8), -- 운행 날짜 (전날)
    trn_no VARCHAR(20), -- 열차 번호
    mrnt_nm VARCHAR(50), -- 노선명 (경부선 등)
    dptre_stn_nm VARCHAR(50), -- 출발역
    arvl_stn_nm VARCHAR(50), -- 도착역
    plan_dep VARCHAR(10), -- 계획 출발 HH:MM
    plan_arr VARCHAR(10), -- 계획 도착 HH:MM
    real_dep VARCHAR(10), -- 실제 출발 HH:MM
    real_arr VARCHAR(10), -- 실제 도착 HH:MM
    dep_delay INTEGER, -- 출발 지연 분 (양수=지연, 음수=조기)
    arr_delay INTEGER, -- 도착 지연 분
    dep_status VARCHAR(50), -- 상태 텍스트 (예: '정시 (0분)', '대폭지연 (+45분)')
    arr_status VARCHAR(50), -- 상태 텍스트
    data_type VARCHAR(20), -- 'delay_analysis'
    created_at TIMESTAMP DEFAULT NOW()
);
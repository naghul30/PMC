
import re
import os
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from sqlalchemy import create_engine, text


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PMC Smart Mill Monitoring",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# DARK INDUSTRIAL UI
# ============================================================
st.markdown(
    """
<style>
    .stApp {
        background: #07090d;
        color: #e5e7eb;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    section[data-testid="stSidebar"] {
        background: #0b0e13;
        border-right: 1px solid #242a34;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    /* Top navigation - replaces the Streamlit sidebar */
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="stAppViewContainer"] { margin-left: 0 !important; }
    .top-nav-wrap {
        background: #111a22;
        border: 1px solid #31424e;
        border-radius: 2px;
        padding: 0 8px;
        margin: 0 0 16px 0;
        box-shadow: 0 2px 12px rgba(0,0,0,.25);
    }
    .topnav-btn button {
        background: transparent !important;
        border: 0 !important;
        border-radius: 0 !important;
        color: #e9a43a !important;
        font-size: 13px !important;
        font-weight: 650 !important;
        padding: 8px 9px !important;
        min-height: 34px !important;
        box-shadow: none !important;
    }
    .topnav-btn button:hover {
        background: #1d2a34 !important;
        color: #ffd38a !important;
    }
    .settings-panel {
        background: #0d151c;
        border: 1px solid #30414d;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 14px;
        color: #cbd5e1;
        font-size: 12px;
    }
    .secondary-card {
        background: #0b151d;
        border: 1px solid #29414e;
        border-radius: 14px;
        padding: 16px;
        min-height: 112px;
    }
    .secondary-card-label { color:#8fa5b3; font-size:10px; text-transform:uppercase; letter-spacing:.5px; font-weight:800; }
    .secondary-card-value { color:#f8fafc; font-size:27px; font-weight:900; margin-top:6px; }
    .secondary-card-sub { color:#6ee7b7; font-size:11px; margin-top:4px; }
    .secondary-insight { background:#0b1720; border-left:4px solid #38bdf8; border-radius:9px; padding:12px 14px; color:#cbd5e1; font-size:12px; margin:12px 0; }
    .secondary-alert { background:#1b110c; border-left:4px solid #f97316; border-radius:9px; padding:12px 14px; color:#fdba74; font-size:12px; margin:12px 0; }

    .main-header {
        padding: 20px 22px;
        border: 1px solid #2a303a;
        border-radius: 14px;
        background: #10141b;
        margin-bottom: 16px;
    }

    .main-header-title {
        font-size: 29px;
        font-weight: 750;
        color: #f8fafc;
    }

    .main-header-sub {
        font-size: 13px;
        color: #8b96a6;
        margin-top: 4px;
    }

    .section-heading {
        font-size: 19px;
        font-weight: 750;
        color: #f1f5f9;
        margin: 20px 0 10px 0;
    }

    .kpi {
        background: #10141b;
        border: 1px solid #2a303a;
        border-radius: 12px;
        padding: 15px 17px;
        min-height: 100px;
    }

    .kpi-label {
        font-size: 11px;
        color: #8b96a6;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: .4px;
    }

    .kpi-value {
        font-size: 27px;
        font-weight: 750;
        color: #f8fafc;
        margin-top: 7px;
    }

    .alert-panel {
        background: #21130c;
        border: 1px solid #7c3514;
        border-left: 5px solid #f97316;
        border-radius: 12px;
        padding: 13px 16px;
        margin: 14px 0 18px 0;
    }

    .alert-title {
        color: #fb923c;
        font-size: 15px;
        font-weight: 750;
    }

    .alert-text {
        color: #fdba74;
        font-size: 13px;
        margin-top: 4px;
    }

    .recommendation {
        background: #0e141c;
        border: 1px solid #334155;
        border-left: 4px solid #60a5fa;
        border-radius: 10px;
        padding: 12px 14px;
        margin: 8px 0;
    }

    .recommendation-title {
        color: #f8fafc;
        font-weight: 750;
        font-size: 13px;
    }

    .recommendation-text {
        color: #cbd5e1;
        font-size: 12px;
        margin-top: 4px;
        line-height: 1.5;
    }

    .point-box {
        margin-top: 10px;
        padding: 10px;
        border: 1px solid #303744;
        border-radius: 10px;
        background: #090c11;
    }

    .point-box-header {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        color: #8b96a6;
        font-size: 11px;
        border-bottom: 1px solid #242a34;
        padding-bottom: 7px;
        margin-bottom: 7px;
    }

    .point-box-empty {
        min-height: 55px;
    }

    .point-value {
        color: #e5e7eb;
        font-size: 13px;
        margin-bottom: 7px;
    }

    .point-alert {
        border: 1px solid #6b2b18;
        border-left: 4px solid #f97316;
        border-radius: 8px;
        background: #1b100b;
        padding: 9px 10px;
        margin-top: 7px;
    }

    .point-alert.low {
        border-color: #6b4a14;
        border-left-color: #f59e0b;
        background: #181309;
    }

    .point-alert-title {
        color: #fb923c;
        font-size: 12px;
        font-weight: 750;
    }

    .point-alert.low .point-alert-title {
        color: #fbbf24;
    }

    .point-alert-detail {
        color: #cbd5e1;
        font-size: 11px;
        margin-top: 4px;
    }

    .point-alert-recommendation {
        color: #d1d5db;
        font-size: 11px;
        line-height: 1.45;
        margin-top: 5px;
    }

    .point-good {
        border: 1px solid #1f5138;
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        background: #0b1711;
        padding: 9px 10px;
        margin-top: 7px;
    }

    .point-good-title {
        color: #4ade80;
        font-size: 12px;
        font-weight: 750;
    }

    .point-good-detail {
        color: #9ca3af;
        font-size: 11px;
        margin-top: 4px;
    }

    .clicked-panel {
        background: #111827;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 14px 16px;
        margin: 12px 0 18px 0;
    }

    .clicked-title {
        color: #f8fafc;
        font-size: 16px;
        font-weight: 750;
    }

    .clicked-text {
        color: #9ca3af;
        font-size: 12px;
        margin-top: 3px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #10141b;
        border-color: #2a303a !important;
        border-radius: 14px !important;
    }

    div[data-testid="stPlotlyChart"] {
        background: #05070a;
        border: 1px solid #222833;
        border-radius: 10px;
        overflow: hidden;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #2a303a;
        border-radius: 10px;
        overflow: hidden;
    }

    .small-note {
        color: #8b96a6;
        font-size: 12px;
    }

    .ster-card { background:#08131c; border:1px solid #174b66; border-radius:18px; padding:14px; margin-bottom:8px; box-shadow:0 8px 22px rgba(0,0,0,.20); }
    .ster-card-top { display:flex; justify-content:space-between; align-items:center; gap:8px; }
    .ster-name { color:#f8fafc; font-weight:800; font-size:18px; white-space:nowrap; }
    .ster-normal { color:#8be28b; font-size:12px; margin-right:8px; }
    .ster-alert { color:#ff8d72; font-size:12px; margin-right:8px; }
    .ster-cycle { min-width:105px; text-align:center; padding:9px 10px; border-radius:5px; font-weight:800; color:#fff; }
    .ster-cooking { background:#087208; border:1px solid #62d362; }
    .ster-done { background:#2110a9; border:1px solid #9a8cff; }
    .ster-idle { background:#730000; border:1px solid #ff8b8b; }
    .ster-updated { color:#dbeafe; font-size:11px; margin-top:10px; }
    .ster-divider { height:1px; background:#3a4a55; margin:11px 0; }
    .ster-grid { display:grid; grid-template-columns:1fr 1fr; }
    .ster-grid > div { min-height:78px; padding:8px 10px; text-align:center; border-bottom:1px solid #31404a; }
    .ster-grid > div:nth-child(odd) { border-right:1px solid #31404a; }
    .ster-label { color:#f1f5f9; font-weight:800; font-size:12px; margin-bottom:8px; }
    .ster-value { background:#f4f5f7; color:#111827; border-radius:18px; padding:7px 6px; font-weight:800; font-size:13px; }
    .mode-value { color:#087208; }
    .ster-extra { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; color:#aebdca; font-size:10px; }
    .ster-extra span { background:#101e29; border:1px solid #243b49; border-radius:8px; padding:5px 7px; }
    .ster-analysis { margin:8px 0 9px; padding:8px 10px; border-radius:9px; font-size:11px; display:flex; flex-direction:column; gap:2px; }
    .ster-analysis-good { background:#08180e; border:1px solid #1c5a34; color:#69e08a; }
    .ster-analysis-good span { color:#9aa8b5; }
    .ster-analysis-alert { background:#1a0d0b; border:1px solid #71321f; color:#ff996f; }
    .ster-step-focus { margin-top:10px; padding:10px 12px; border-radius:10px; background:#101b24; border:1px solid #315164; display:flex; justify-content:space-between; align-items:center; gap:10px; }
    .ster-step-number { color:#f8fafc; font-size:17px; font-weight:900; letter-spacing:.3px; }
    .ster-step-total { color:#8fd8ff; font-size:15px; font-weight:850; }
    .ster-step-guide { color:#b9c8d3; font-size:10px; margin-top:3px; }
    .press-card { background:#08131c; border:1px solid #174b66; border-radius:18px; padding:15px; margin-bottom:12px; }
    .press-card-top { display:flex; justify-content:space-between; align-items:center; gap:8px; }
    .press-name { color:#f8fafc; font-weight:900; font-size:18px; }
    .press-status { padding:6px 10px; border-radius:7px; font-size:11px; font-weight:850; }
    .press-running { background:#0b4f2d; border:1px solid #4ade80; color:#86efac; }
    .press-stopped { background:#3b1414; border:1px solid #ef4444; color:#fca5a5; }
    .press-auto { color:#67e8f9; font-weight:850; }
    .press-manual { color:#fbbf24; font-weight:850; }
    .press-time { color:#91a5b4; font-size:10px; margin-top:7px; }
    .press-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:7px; margin-top:10px; }
    .press-metric { background:#0d1a23; border:1px solid #223b4a; border-radius:9px; padding:9px; min-height:58px; }
    .press-label { color:#91a5b4; font-size:9px; text-transform:uppercase; font-weight:800; }
    .press-value { color:#f1f5f9; font-size:15px; font-weight:850; margin-top:4px; }
    .press-analysis { margin-top:10px; padding:9px 11px; border-radius:9px; background:#0b1720; border:1px solid #28495c; color:#cbd5e1; font-size:10px; }
    .press-analysis b { color:#f8fafc; }
    .press-level-status { margin-top:8px; padding:7px 10px; border-radius:8px; text-align:center; font-size:11px; font-weight:850; }
    .press-level-high { background:#21160a; border:1px solid #8a5a14; color:#fbbf24; }
    .press-level-low { background:#0b1720; border:1px solid #28516a; color:#7dd3fc; }
    .press-level-at { background:#111827; border:1px solid #475569; color:#cbd5e1; }
    .valve-grid { display:grid; grid-template-columns:1.45fr repeat(8,1fr); background:#08131c; border:1px solid #174b66; border-bottom:0; min-height:44px; align-items:center; }
    .valve-head, .valve-label, .valve-cell { padding:9px 8px; border-right:1px solid #223744; color:#e5edf4; font-size:12px; font-weight:700; }
    .valve-head { color:#fff; text-transform:uppercase; }
    .valve-head.center, .valve-cell { text-align:center; }
    .valve-cell { display:flex; justify-content:center; align-items:center; gap:5px; font-size:9px; }
    .valve-dot { width:13px; height:13px; border-radius:50%; display:inline-block; }
    .valve-dot.open { background:#9bea59; box-shadow:0 0 0 3px rgba(155,234,89,.14); }
    .valve-dot.close { background:#ff4d55; box-shadow:0 0 0 3px rgba(255,77,85,.14); }
    .run-card { background:#0d151c; border:1px solid #243746; border-radius:14px; padding:14px 16px; min-height:150px; }
    .run-card-title { color:#dce7ef; font-size:13px; font-weight:800; text-transform:uppercase; letter-spacing:.5px; }
    .run-big { color:#f8fafc; font-size:30px; font-weight:850; margin-top:5px; }
    .run-sub { color:#8fa2b1; font-size:11px; margin-top:3px; }
    .run-day { margin-top:12px; padding-top:10px; border-top:1px solid #263945; display:flex; justify-content:space-between; }
    .run-day-label { color:#8fa2b1; font-size:10px; text-transform:uppercase; }
    .run-day-value { color:#6ee7b7; font-size:17px; font-weight:800; }
    .health-grid { display:grid; grid-template-columns:1.4fr repeat(5,1fr); border:1px solid #253744; border-radius:12px; overflow:hidden; background:#0b1218; }
    .health-cell { padding:10px 8px; border-right:1px solid #253744; border-bottom:1px solid #253744; text-align:center; color:#dbe5ec; font-size:11px; }
    .health-label { text-align:left; font-weight:800; color:#f8fafc; }
    .health-good { color:#6ee7b7; font-weight:800; }
    .health-warn { color:#fb923c; font-weight:800; }
    .health-na { color:#71808d; }
    .analysis-card { background:#0b1218; border:1px solid #243746; border-radius:14px; padding:14px; min-height:175px; }
    .analysis-title { color:#f8fafc; font-size:14px; font-weight:800; margin-bottom:10px; }
    .analysis-row { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #1c2a34; color:#9fb0bd; font-size:11px; }
    .analysis-row b { color:#e7eef3; }
    .insight { border-left:4px solid #38bdf8; background:#0b1720; border-radius:8px; padding:10px 12px; color:#cbd5e1; font-size:12px; margin-top:8px; }

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# CONFIGURATION
# ============================================================
DEFAULT_FILE = "production_usage_report (34).xls"
PRESS_COLS = [f"Press {i}" for i in range(1, 9)]

# ============================================================
# MYSQL DATA SOURCE – STERILIZER / PRESS
# ============================================================
DB_CONFIG = {
    "host": st.secrets["DB_HOST"],
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
    "database": st.secrets["DB_NAME"],
}

# Running-hours data is stored in the Smart Perak Motor database,
# separately from the MQTT sterilizer/press database.
RUNNING_HOURS_DB_CONFIG = {
    "host": st.secrets["RUNNING_HOURS_DB_HOST"],
    "user": st.secrets["RUNNING_HOURS_DB_USER"],
    "password": st.secrets["RUNNING_HOURS_DB_PASSWORD"],
    "database": st.secrets["RUNNING_HOURS_DB_NAME"],
}


@st.cache_resource(show_spinner=False)
def get_db_engine():
    try:
        import pymysql  # noqa: F401
    except ImportError as exc:
        raise RuntimeError("MySQL driver is missing. Install it with: pip install pymysql") from exc
    url = (
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    )
    return create_engine(url, pool_pre_ping=True, pool_recycle=1800, connect_args={"connect_timeout": 3, "read_timeout": 8, "write_timeout": 8})


@st.cache_data(ttl=5, show_spinner=False)
def load_sterilizer_db(start_dt, end_dt):
    engine = get_db_engine()
    sql = text('''
        SELECT id, sterilizer_no, device, ts, insdt, pressure, temperature,
               inlet_modulating_percent, auto_manual, cooking_status, state,
               inlet_cmd, exhaust_cmd, condense_cmd, queue_no, recipe_no,
               total_recipe_time, step_countdown, elapsed_time, last_step,
               raw_payload, created_at
        FROM (
            SELECT x.*, ROW_NUMBER() OVER (PARTITION BY sterilizer_no ORDER BY insdt DESC) AS rn
            FROM pmc_sterilizer_data x
            WHERE insdt >= :start_dt AND insdt <= :end_dt
        ) latest_rows
        WHERE rn <= 5
        ORDER BY sterilizer_no, insdt
    ''')
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={"start_dt": start_dt, "end_dt": end_dt})
    if not df.empty:
        df["insdt"] = pd.to_datetime(df["insdt"], errors="coerce")
        for c in ["pressure", "temperature", "inlet_modulating_percent"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


@st.cache_resource(show_spinner=False)
def get_running_hours_db_engine():
    try:
        import pymysql  # noqa: F401
    except ImportError as exc:
        raise RuntimeError("MySQL driver is missing. Install it with: pip install pymysql") from exc
    url = (
        f"mysql+pymysql://{RUNNING_HOURS_DB_CONFIG['user']}:{RUNNING_HOURS_DB_CONFIG['password']}"
        f"@{RUNNING_HOURS_DB_CONFIG['host']}/{RUNNING_HOURS_DB_CONFIG['database']}"
    )
    return create_engine(url, pool_pre_ping=True, pool_recycle=1800, connect_args={"connect_timeout": 3, "read_timeout": 8, "write_timeout": 8})


@st.cache_data(ttl=300, show_spinner=False)
def load_running_hours_db():
    # IMPORTANT: machine_running_hours comes from the Smart Perak Motor DB.
    # This is intentionally separate from pmc_mqtt_pmc used for live process data.
    engine = get_running_hours_db_engine()
    sql = text("""
        SELECT
            i.item_station_id AS id,
            s.station_name,
            i.station_id,
            l.location_name,
            i.location_id,
            p.parts_name,
            i.item_id AS part_id,
            i.machine_running_hours
        FROM item_station_location i
        JOIN stations s ON i.station_id = s.station_id
        JOIN locations l ON i.location_id = l.location_id
        JOIN parts p ON i.item_id = p.parts_id
        ORDER BY s.station_name, p.parts_name
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    if not df.empty:
        df["machine_running_hours"] = pd.to_numeric(df["machine_running_hours"], errors="coerce")
    return df


@st.cache_data(ttl=60, show_spinner=False)
def load_sterilizer_performance_window(start_dt, end_dt):
    """Load ALL sterilizer_performance records for the selected calendar dates.

    IMPORTANT: the sterilizer_performance table has separate ``date`` and
    ``time`` columns.  The selected-date filter is therefore applied to the
    table's ``date`` column itself, not to a derived cycle/door timestamp.
    This prevents valid records from disappearing when cooking/door timestamps
    are missing or fall on a different day.
    """
    engine = get_running_hours_db_engine()
    start_date = pd.Timestamp(start_dt).date()
    end_date = pd.Timestamp(end_dt).date()
    sql = text("""
        SELECT
            id,
            date,
            time,
            sterilizer,
            status,
            cycle_no,
            old_cycle_no,
            back_pressure_receiver,
            p1,
            p2,
            p3,
            cooking_start_time,
            cooking_stop_time,
            door_shut_time,
            door_open_time,
            initial_steam,
            final_blow,
            checked_flag,
            insdt
        FROM sterilizer_performance
        WHERE date >= :start_date
          AND date <= :end_date
          AND sterilizer IN (6, 7, 8, 9, 10)
        ORDER BY date, time, sterilizer, cycle_no, id
    """)
    with engine.connect() as conn:
        df = pd.read_sql(
            sql,
            conn,
            params={"start_date": start_date, "end_date": end_date},
        )

    if df.empty:
        return df

    # Keep the source date/time exactly as the performance-record reference.
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["time"] = df["time"].astype(str).replace({"NaT": "", "nan": ""})

    # Build a plotting/reference timestamp from date + time first.
    # Fall back to insdt / cooking-stop / door-open when necessary.
    date_text = df["date"].dt.strftime("%Y-%m-%d")
    df["record_time"] = pd.to_datetime(
        date_text + " " + df["time"], errors="coerce"
    )

    for c in ["cooking_start_time", "cooking_stop_time", "door_shut_time", "door_open_time", "insdt"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    for c in ["cooking_stop_time", "door_open_time", "insdt"]:
        if c in df.columns:
            df["record_time"] = df["record_time"].fillna(df[c])

    # Keep the old name too because the process-confirmation code uses it.
    df["cycle_ref_time"] = df["record_time"]

    for c in ["sterilizer", "cycle_no", "p1", "p2", "p3", "back_pressure_receiver"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


@st.cache_data(ttl=30, show_spinner=False)
def load_press_confirmation_near_sample(sample_dt, press_no, window_minutes=30):
    """Load the nearest press/digester record around a selected NIR sample.

    The NIR sample is not itself a press sensor record, so confirmation uses the
    nearest timestamp from pmc_press_station_log within a bounded window.
    """
    engine = get_db_engine()
    i = int(press_no)
    start_dt = pd.Timestamp(sample_dt) - pd.Timedelta(minutes=window_minutes)
    end_dt = pd.Timestamp(sample_dt) + pd.Timedelta(minutes=window_minutes)
    sql = text(f"""
        SELECT
            ts_local,
            d{i}_amp AS digester_amp,
            d{i}_temp AS digester_temp,
            d{i}_level AS digester_level,
            sp{i}_amp AS press_motor_amp,
            sp{i}_setpoint AS press_setpoint,
            sp{i}_hpu_pressure AS hydraulic_pressure,
            sp{i}_auto_manual AS auto_manual,
            sp{i}_cone_pct AS cone_pct
        FROM pmc_press_station_log
        WHERE ts_local >= :start_dt
          AND ts_local <= :end_dt
        ORDER BY ts_local ASC
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={"start_dt": start_dt.to_pydatetime(), "end_dt": end_dt.to_pydatetime()})
    if df.empty:
        return df
    df["ts_local"] = pd.to_datetime(df["ts_local"], errors="coerce")
    df = df.dropna(subset=["ts_local"]).copy()
    df["_distance_sec"] = (df["ts_local"] - pd.Timestamp(sample_dt)).abs().dt.total_seconds()
    row = df.sort_values("_distance_sec").iloc[[0]].copy()
    return row


def _format_value(value, decimals=1, suffix=""):
    v = pd.to_numeric(value, errors="coerce")
    if pd.isna(v):
        return "--"
    return f"{float(v):.{decimals}f}{suffix}"


def _level_status(value):
    raw = str(value).strip().lower()
    if raw in {"full", "high", "above 75", "above 75%"}:
        return "Above 75%"
    if raw in {"not-full", "not full", "low", "below 75", "below 75%"}:
        return "Below 75%"
    n = pd.to_numeric(value, errors="coerce")
    if pd.notna(n):
        if n > 75:
            return "Above 75%"
        if n < 75:
            return "Below 75%"
        return "At 75%"
    return "Unknown"



@st.cache_data(ttl=30, show_spinner=False)
def load_press_confirmation_hour(sample_dt, press_no):
    """Load all Press/Digester records from the NIR sample's clock hour.

    Example: NIR at 00:42 -> use Press records from 00:00:00 through
    00:59:59 of the same date. This deliberately avoids the old +/- window
    matching because the user's process confirmation is hour-based.
    """
    engine = get_db_engine()
    sample_dt = pd.Timestamp(sample_dt)
    hour_start = sample_dt.floor("h")
    hour_end = hour_start + pd.Timedelta(hours=1)
    i = int(press_no)
    sql = text(f"""
        SELECT
            ts_local,
            d{i}_amp AS digester_amp,
            d{i}_temp AS digester_temp,
            d{i}_level AS digester_level,
            sp{i}_amp AS press_motor_amp,
            sp{i}_setpoint AS press_setpoint,
            sp{i}_hpu_pressure AS hydraulic_pressure,
            sp{i}_auto_manual AS auto_manual,
            sp{i}_cone_pct AS cone_pct
        FROM pmc_press_station_log
        WHERE ts_local >= :start_dt
          AND ts_local < :end_dt
        ORDER BY ts_local ASC
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={
            "start_dt": hour_start.to_pydatetime(),
            "end_dt": hour_end.to_pydatetime(),
        })
    if df.empty:
        return df
    df["ts_local"] = pd.to_datetime(df["ts_local"], errors="coerce")
    return df.dropna(subset=["ts_local"]).copy()


@st.cache_data(ttl=60, show_spinner=False)
@st.cache_data(ttl=30, show_spinner=False)
def load_press_confirmation_all_hour(sample_dt):
    """Load all Press/Digester records for the exact clock hour containing the NIR sample."""
    engine = get_db_engine()
    sample_dt = pd.Timestamp(sample_dt)
    hour_start = sample_dt.floor("h")
    hour_end = hour_start + pd.Timedelta(hours=1)

    cols = ["ts_local"]
    for i in range(1, 9):
        cols += [
            f"d{i}_amp AS d{i}_amp", f"d{i}_temp AS d{i}_temp", f"d{i}_level AS d{i}_level",
            f"sp{i}_amp AS sp{i}_amp", f"sp{i}_setpoint AS sp{i}_setpoint",
            f"sp{i}_hpu_pressure AS sp{i}_hpu_pressure", f"sp{i}_auto_manual AS sp{i}_auto_manual",
        ]
    sql = text(f"""
        SELECT {', '.join(cols)}
        FROM pmc_press_station_log
        WHERE ts_local >= :start_dt AND ts_local < :end_dt
        ORDER BY ts_local ASC
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={
            "start_dt": hour_start.to_pydatetime(),
            "end_dt": hour_end.to_pydatetime(),
        })
    if df.empty:
        return df
    df["ts_local"] = pd.to_datetime(df["ts_local"], errors="coerce")
    for i in range(1, 9):
        for c in [f"d{i}_amp", f"d{i}_temp", f"sp{i}_amp", f"sp{i}_setpoint", f"sp{i}_hpu_pressure"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna(subset=["ts_local"]).sort_values("ts_local")


def load_sterilizer_confirmation_previous_hour(sample_dt):
    """Load Sterilizer 6-10 records from the hour immediately before the NIR hour.

    Example: NIR at 00:42 on 24-Sep-2026 -> Sterilizer window is
    23:00:00-23:59:59 on 23-Sep-2026. Matching is based on the actual
    sterilizer `date + time` record, not `insdt`, because the process event
    happened at the recorded cycle time.
    """
    engine = get_running_hours_db_engine()
    sample_dt = pd.Timestamp(sample_dt)
    nir_hour_start = sample_dt.floor("h")
    ster_start = nir_hour_start - pd.Timedelta(hours=1)
    ster_end = nir_hour_start

    sql = text("""
        SELECT
            id,
            date,
            time,
            sterilizer,
            status,
            cycle_no,
            old_cycle_no,
            p1,
            p2,
            p3,
            back_pressure_receiver,
            cooking_start_time,
            cooking_stop_time,
            door_shut_time,
            door_open_time,
            insdt
        FROM sterilizer_performance
        WHERE sterilizer IN (6, 7, 8, 9, 10)
          AND date >= :start_date
          AND date <= :end_date
        ORDER BY sterilizer, date, time, id
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={
            "start_date": ster_start.date(),
            "end_date": (ster_end - pd.Timedelta(seconds=1)).date(),
        })

    if df.empty:
        return df

    # The actual event timestamp is date + time.
    df["event_dt"] = pd.to_datetime(
        df["date"].astype(str).str[:10] + " " + df["time"].astype(str),
        errors="coerce",
    )
    df = df[df["event_dt"].notna()].copy()
    df = df[(df["event_dt"] >= ster_start) & (df["event_dt"] < ster_end)].copy()

    for c in ["sterilizer", "cycle_no", "p1", "p2", "p3", "back_pressure_receiver"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df.sort_values(["sterilizer", "event_dt", "id"])

def render_high_nir_process_confirmation(selected, press_name, high_limit=4.7):
    """Complete process confirmation for a high NIR point.

    It combines the selected Press's nearest process record with the actual
    sterilizer cycle records for Sterilizers 6-10. Values are displayed as
    observations; the dashboard does not claim causation from one sample.
    """
    if selected is None or float(selected.get("value", 0)) <= high_limit:
        return
    sample_dt = pd.to_datetime(selected.get("datetime"), errors="coerce")
    if pd.isna(sample_dt):
        return

    press_no = int(str(press_name).split()[-1])
    st.markdown('<div class="section-heading">High Oil Loss – Complete Process Confirmation</div>', unsafe_allow_html=True)
    st.caption(
        f"NIR {float(selected['value']):.2f}% at {sample_dt.strftime('%d %b %Y %H:%M')} · "
        f"high limit {high_limit:.2f}%. Process values below are the nearest available records around the NIR sample."
    )

    # ------------------------------------------------------------
    # 1) PRESS + DIGESTER CONFIRMATION
    # ------------------------------------------------------------
    try:
        p = load_press_confirmation_near_sample(sample_dt, press_no)
    except Exception as exc:
        p = pd.DataFrame()
        st.warning(f"Press/digester confirmation could not be loaded: {exc}")

    st.markdown("**Press & Digester Performance**")
    if p.empty:
        st.info(f"No Press {press_no} process record was found within ±30 minutes of the NIR sample.")
    else:
        r = p.iloc[0]
        record_dt = pd.to_datetime(r.get("ts_local"), errors="coerce")
        dist_min = abs((record_dt - sample_dt).total_seconds()) / 60 if pd.notna(record_dt) else None
        level = _level_status(r.get("digester_level"))
        motor = pd.to_numeric(r.get("press_motor_amp"), errors="coerce")
        setpoint = pd.to_numeric(r.get("press_setpoint"), errors="coerce")
        hydraulic = pd.to_numeric(r.get("hydraulic_pressure"), errors="coerce")
        temp = pd.to_numeric(r.get("digester_temp"), errors="coerce")
        damp = pd.to_numeric(r.get("digester_amp"), errors="coerce")
        amp_status = "RUNNING" if pd.notna(motor) and motor > 5 else "STOPPED"
        amp_colour = "#4ade80" if amp_status == "RUNNING" else "#fbbf24"
        temp_status = "Normal" if pd.notna(temp) and 80 <= temp <= 95 else ("Low" if pd.notna(temp) and temp < 80 else ("High" if pd.notna(temp) else "--"))
        level_status = "Normal" if level in {"Above 75%", "At 75%"} else ("Low" if level == "Below 75%" else "--")
        hydraulic_status = "Normal" if pd.notna(hydraulic) and hydraulic >= 70 else ("Low" if pd.notna(hydraulic) else "--")
        motor_status = "Normal" if pd.notna(motor) and 29 <= motor <= 56 else ("Low" if pd.notna(motor) and motor < 29 else ("High" if pd.notna(motor) else "--"))
        setpoint_status = "Within motor target" if pd.notna(setpoint) and pd.notna(motor) and abs(motor-setpoint) <= 5 else "Review" if pd.notna(setpoint) and pd.notna(motor) else "--"

        cols = st.columns(8)
        metrics = [
            ("Record time", record_dt.strftime('%d %b %H:%M') if pd.notna(record_dt) else "--"),
            ("Time from NIR", f"{dist_min:.0f} min" if dist_min is not None else "--"),
            ("Digester level", level),
            ("Digester temp", _format_value(temp, 1, " °C")),
            ("Digester amps", _format_value(damp, 1, " A")),
            ("Press setpoint", _format_value(setpoint, 1, " A")),
            ("Press motor", _format_value(motor, 1, " A")),
            ("Hydraulic", _format_value(hydraulic, 1, " bar")),
        ]
        for c, (label, value) in zip(cols, metrics):
            with c:
                st.metric(label, value)
        st.markdown(
            f"**Press {press_no}:** <span style='color:{amp_colour};font-weight:700'>{amp_status}</span> · "
            f"Auto/Manual: **{str(r.get('auto_manual') or '--')}** · "
            f"Level: **{level} ({level_status})** · Temperature: **{temp_status}** · "
            f"Motor: **{motor_status}** · Hydraulic: **{hydraulic_status}** · Setpoint relation: **{setpoint_status}**",
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------
    # 2) STERILIZER 1-5 / CYCLE CONFIRMATION
    # ------------------------------------------------------------
    try:
        start_dt = sample_dt - pd.Timedelta(hours=24)
        end_dt = sample_dt + pd.Timedelta(hours=24)
        perf = load_sterilizer_performance_window(start_dt.to_pydatetime(), end_dt.to_pydatetime())
    except Exception as exc:
        perf = pd.DataFrame()
        st.warning(f"Sterilizer cycle confirmation could not be loaded: {exc}")

    st.markdown("**Sterilizer Cycle Confirmation — Sterilizer 6 to 10**")
    if perf.empty:
        st.info("No sterilizer performance records were found around the selected NIR sample.")
        return

    perf = perf[perf["sterilizer"].isin([6, 7, 8, 9, 10])].copy()
    if perf.empty:
        st.info("No Sterilizer 6–10 records were found around the selected NIR sample.")
        return

    cards = []
    for ster_no in [6, 7, 8, 9, 10]:
        g = perf[perf["sterilizer"] == ster_no].copy()
        if g.empty:
            cards.append((ster_no, None))
            continue
        g = g.dropna(subset=["cycle_ref_time"])
        if g.empty:
            cards.append((ster_no, None))
            continue

        # Prefer a cycle whose operating window contains the NIR timestamp.
        start_candidates = [c for c in ["cooking_start_time", "door_shut_time"] if c in g.columns]
        end_candidates = [c for c in ["cooking_stop_time", "door_open_time"] if c in g.columns]
        containing = pd.Series(False, index=g.index)
        if start_candidates and end_candidates:
            starts = pd.NaT
            ends = pd.NaT
            for c in start_candidates:
                starts = g[c] if isinstance(starts, type(pd.NaT)) else starts.fillna(g[c])
            for c in end_candidates:
                ends = g[c] if isinstance(ends, type(pd.NaT)) else ends.fillna(g[c])
            containing = starts.notna() & ends.notna() & (starts <= sample_dt) & (ends >= sample_dt)
        if containing.any():
            row = g[containing].sort_values("cycle_ref_time").iloc[-1].copy()
            relation = "NIR falls inside cycle"
        else:
            completed = g[g["cycle_ref_time"] <= sample_dt]
            if not completed.empty:
                row = completed.sort_values("cycle_ref_time").iloc[-1].copy()
                relation = "Latest completed cycle before NIR"
            else:
                g["_dist"] = (g["cycle_ref_time"] - sample_dt).abs()
                row = g.sort_values("_dist").iloc[0].copy()
                relation = "Nearest cycle after NIR"
        row["_relation"] = relation
        row["_distance_min"] = abs((pd.Timestamp(row["cycle_ref_time"]) - sample_dt).total_seconds()) / 60
        cards.append((ster_no, row))

    for ster_no, r in cards:
        if r is None:
            st.markdown(f"**Sterilizer {ster_no}** — No matching cycle found")
            continue
        cycle = pd.to_numeric(r.get("cycle_no"), errors="coerce")
        p1 = pd.to_numeric(r.get("p1"), errors="coerce")
        p2 = pd.to_numeric(r.get("p2"), errors="coerce")
        p3 = pd.to_numeric(r.get("p3"), errors="coerce")
        bpv = pd.to_numeric(r.get("back_pressure_receiver"), errors="coerce")
        ref = pd.to_datetime(r.get("cycle_ref_time"), errors="coerce")
        st.markdown(f"**Sterilizer {ster_no} · Cycle {int(cycle) if pd.notna(cycle) else '--'}**")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        for c, label, val in [
            (c1, "P1", _format_value(p1, 1, " PSI")),
            (c2, "P2", _format_value(p2, 1, " PSI")),
            (c3, "P3", _format_value(p3, 1, " PSI")),
            (c4, "BPV", _format_value(bpv, 1, " PSI")),
            (c5, "Cycle time", ref.strftime('%d %b %H:%M') if pd.notna(ref) else '--'),
            (c6, "Relation", str(r.get('_relation', '--'))),
        ]:
            with c:
                st.metric(label, val)

    st.caption("This confirmation uses the actual sterilizer_performance values. It is a process correlation check around the selected high-NIR sample, not proof that any single parameter caused the oil loss.")

def render_high_nir_sterilizer_confirmation(selected, high_limit=4.7):
    """Show separate sterilizer-cycle confirmation for a selected high NIR point."""
    if selected is None or float(selected.get("value", 0)) <= high_limit:
        return

    sample_dt = pd.to_datetime(selected.get("datetime"), errors="coerce")
    if pd.isna(sample_dt):
        return

    # Search around the NIR sample. The matching cycle is then selected per
    # sterilizer, so Sterilizer 6/8/9/10 etc. are never mixed together.
    start_dt = sample_dt - pd.Timedelta(hours=24)
    end_dt = sample_dt + pd.Timedelta(hours=24)

    try:
        perf = load_sterilizer_performance_window(start_dt.to_pydatetime(), end_dt.to_pydatetime())
    except Exception as exc:
        st.warning(f"Sterilizer confirmation could not be loaded: {exc}")
        return

    st.markdown(
        '<div class="section-heading">High Oil Loss – Sterilizer Cycle Confirmation</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        f"NIR {float(selected['value']):.2f}% at {sample_dt.strftime('%d %b %Y %H:%M')} "
        f"(high limit {high_limit:.2f}%). Showing the nearest completed sterilizer cycle separately for each sterilizer."
    )

    if perf.empty:
        st.info("No sterilizer performance cycle was found within ±24 hours of this NIR sample.")
        return

    candidates = []
    for sterilizer_no, group in perf.groupby("sterilizer", dropna=True):
        g = group.dropna(subset=["cycle_ref_time"]).copy()
        if g.empty:
            continue

        completed = g[g["cycle_ref_time"] <= sample_dt]
        if not completed.empty:
            # Latest completed cycle before the NIR sample.
            row = completed.sort_values("cycle_ref_time").iloc[-1].copy()
            relation = "Completed before NIR"
        else:
            # If there is no completed cycle before the sample, use the nearest
            # cycle after it so the user can see that the match is prospective.
            g["_distance"] = (g["cycle_ref_time"] - sample_dt).abs()
            row = g.sort_values("_distance").iloc[0].copy()
            relation = "Nearest cycle after NIR"

        row["_relation"] = relation
        row["_distance_min"] = abs((pd.Timestamp(row["cycle_ref_time"]) - sample_dt).total_seconds()) / 60.0
        candidates.append(row)

    if not candidates:
        st.info("No valid sterilizer cycle timestamps were available for confirmation.")
        return

    confirm_df = pd.DataFrame(candidates).sort_values("sterilizer")

    for _, r in confirm_df.iterrows():
        ster = r.get("sterilizer")
        ster_text = str(int(ster)) if pd.notna(ster) else "--"
        cycle = r.get("cycle_no")
        cycle_text = str(int(cycle)) if pd.notna(cycle) else "--"

        vals = {}
        for label, col in [("P1", "p1"), ("P2", "p2"), ("P3", "p3"), ("BPV", "back_pressure_receiver")]:
            value = pd.to_numeric(r.get(col), errors="coerce")
            vals[label] = f"{value:.1f} PSI" if pd.notna(value) else "--"

        ref = pd.to_datetime(r.get("cycle_ref_time"), errors="coerce")
        ref_text = ref.strftime("%d %b %Y %H:%M") if pd.notna(ref) else "--"
        distance = r.get("_distance_min")
        distance_text = f"{float(distance):.0f} min from NIR" if pd.notna(distance) else "--"
        relation = str(r.get("_relation", ""))

        st.markdown(
            f"""
            <div class="analysis-card" style="margin:8px 0;">
                <div class="analysis-title">Sterilizer {ster_text} &nbsp; | &nbsp; Cycle {cycle_text}</div>
                <div class="analysis-row"><span>Cycle reference</span><b>{ref_text}</b></div>
                <div class="analysis-row"><span>Relation to NIR</span><b>{relation} ({distance_text})</b></div>
                <div class="analysis-row"><span>P1</span><b>{vals['P1']}</b></div>
                <div class="analysis-row"><span>P2</span><b>{vals['P2']}</b></div>
                <div class="analysis-row"><span>P3</span><b>{vals['P3']}</b></div>
                <div class="analysis-row"><span>BPV</span><b>{vals['BPV']}</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("P1/P2/P3/BPV are read directly from sterilizer_performance. No pressure values are inferred from the live sterilizer table.")


def render_process_confirmation_page():
    """Dedicated full process confirmation page for a selected high-NIR sample."""
    selected = st.session_state.get("selected_nir_point")
    high_limit = 4.7

    st.markdown(
        '<div class="main-header"><div class="main-header-title">High Oil Loss – Complete Process Analysis</div>'
        '<div class="main-header-sub">NIR → Press & Digester → Sterilizer cycle confirmation</div></div>',
        unsafe_allow_html=True,
    )

    if not selected:
        st.info("Select a NIR data point from the NIR Trend page first.")
        if st.button("← Back to NIR Trend", key="back_nir_no_sample"):
            st.session_state.pmc_page = "Lab Oil Loss – NIR Data Trend"
            st.rerun()
        return

    value = float(selected.get("value", 0))
    sample_dt = pd.to_datetime(selected.get("datetime"), errors="coerce")
    press_name = str(selected.get("press", "Press 1"))
    if pd.isna(sample_dt):
        st.error("The selected NIR point does not have a valid timestamp.")
        return

    if value <= high_limit:
        st.info(f"Selected NIR value is {value:.2f}%, which is not above the high limit of {high_limit:.2f}%.")
        if st.button("← Back to NIR Trend", key="back_nir_normal"):
            st.session_state.pmc_page = "Lab Oil Loss – NIR Data Trend"
            st.rerun()
        return

    st.markdown(
        f"**{press_name}** · NIR **{value:.2f}%** · Sample time **{sample_dt.strftime('%d %b %Y %H:%M')}** · High limit **{high_limit:.2f}%**",
    )

    if st.button("← Back to NIR Trend", key="back_nir_detail"):
        st.session_state.pmc_page = "Lab Oil Loss – NIR Data Trend"
        st.rerun()

    # PRESS / DIGESTER -------------------------------------------------
    st.markdown('<div class="section-heading">1. Press & Digester Confirmation</div>', unsafe_allow_html=True)
    press_no = int(re.findall(r"\d+", press_name)[-1])
    try:
        p = load_press_confirmation_hour(sample_dt, press_no)
    except Exception as exc:
        p = pd.DataFrame()
        st.warning(f"Press/digester data could not be loaded: {exc}")

    hour_start = sample_dt.floor("h")
    hour_end = hour_start + pd.Timedelta(hours=1)
    st.caption(
        f"Press analysis window: {hour_start.strftime('%d %b %Y %H:%M')}–{(hour_end - pd.Timedelta(seconds=1)).strftime('%H:%M:%S')} "
        f"(the complete clock hour containing the NIR sample)."
    )

    if p.empty:
        st.warning(f"No Press {press_no} process records were found in the NIR hour.")
    else:
        # Use the latest record in the NIR hour as the primary snapshot, while
        # also showing how many records were actually available in that hour.
        r = p.sort_values("ts_local").iloc[-1]
        record_dt = pd.to_datetime(r.get("ts_local"), errors="coerce")
        distance = abs((record_dt - sample_dt).total_seconds()) / 60 if pd.notna(record_dt) else None
        level = _level_status(r.get("digester_level"))
        temp = pd.to_numeric(r.get("digester_temp"), errors="coerce")
        damp = pd.to_numeric(r.get("digester_amp"), errors="coerce")
        motor = pd.to_numeric(r.get("press_motor_amp"), errors="coerce")
        setpoint = pd.to_numeric(r.get("press_setpoint"), errors="coerce")
        hydraulic = pd.to_numeric(r.get("hydraulic_pressure"), errors="coerce")
        mode = str(r.get("auto_manual") or "--")

        def check(label, ok):
            return "✓ NORMAL" if ok else "⚠ CHECK"

        level_ok = level in {"Above 75%", "At 75%"}
        temp_ok = pd.notna(temp) and 80 <= float(temp) <= 95
        damp_ok = pd.notna(damp) and float(damp) >= 24
        motor_ok = pd.notna(motor) and 29 <= float(motor) <= 56
        hydraulic_ok = pd.notna(hydraulic) and float(hydraulic) >= 70
        setpoint_ok = pd.notna(motor) and pd.notna(setpoint) and abs(float(motor)-float(setpoint)) <= 5

        metrics = [
            ("Record time", record_dt.strftime("%d %b %H:%M:%S") if pd.notna(record_dt) else "--"),
            ("Time from NIR", f"{distance:.0f} min" if distance is not None else "--"),
            ("Digester level", level),
            ("Digester temperature", _format_value(temp, 1, " °C")),
            ("Digester motor", _format_value(damp, 1, " A")),
            ("Press setpoint", _format_value(setpoint, 1, " A")),
            ("Press motor", _format_value(motor, 1, " A")),
            ("Hydraulic pressure", _format_value(hydraulic, 1, " bar")),
            ("Mode", mode),
        ]
        cols = st.columns(3)
        for i, (label, val) in enumerate(metrics):
            with cols[i % 3]:
                st.metric(label, val)
        st.caption(f"Press {press_no}: {len(p)} process record(s) found in this NIR hour. The latest record in that hour is used for the primary confirmation snapshot.")

        status_rows = pd.DataFrame([
            {"Parameter": "Digester level", "Observed": level, "Check": check("", level_ok), "Rule": "Above 75% preferred"},
            {"Parameter": "Digester temperature", "Observed": _format_value(temp,1," °C"), "Check": check("", temp_ok), "Rule": "80–95 °C"},
            {"Parameter": "Digester motor amps", "Observed": _format_value(damp,1," A"), "Check": check("", damp_ok), "Rule": "≥ 24 A"},
            {"Parameter": "Press motor amps", "Observed": _format_value(motor,1," A"), "Check": check("", motor_ok), "Rule": "29–56 A"},
            {"Parameter": "Press setpoint relation", "Observed": f"{_format_value(motor,1)} vs {_format_value(setpoint,1)}", "Check": check("", setpoint_ok), "Rule": "Within ±5 A"},
            {"Parameter": "Hydraulic pressure", "Observed": _format_value(hydraulic,1," bar"), "Check": check("", hydraulic_ok), "Rule": "≥ 70 bar"},
        ])
        st.dataframe(status_rows, use_container_width=True, hide_index=True)

    # STERILIZER -------------------------------------------------------
    st.markdown('<div class="section-heading">2. Sterilizer Cycle Confirmation — Sterilizer 1 to 5</div>', unsafe_allow_html=True)
    nir_hour_start = sample_dt.floor("h")
    ster_start = nir_hour_start - pd.Timedelta(hours=1)
    ster_end = nir_hour_start
    st.caption(
        f"Sterilizer analysis window: {ster_start.strftime('%d %b %Y %H:%M')}–{(ster_end - pd.Timedelta(seconds=1)).strftime('%H:%M:%S')} "
        f"(the complete hour immediately before the NIR/Press hour)."
    )
    try:
        perf = load_sterilizer_confirmation_previous_hour(sample_dt)
    except Exception as exc:
        perf = pd.DataFrame()
        st.warning(f"Sterilizer performance data could not be loaded: {exc}")

    if perf.empty:
        st.warning(
            "No Sterilizer 6–10 performance records were found in the previous hour "
            f"({ster_start.strftime('%d %b %Y %H:%M')}–{(ster_end - pd.Timedelta(seconds=1)).strftime('%H:%M:%S')})."
        )
    else:
        # Keep each sterilizer separate. If more than one record/cycle exists in
        # the hour, show the latest cycle for the confirmation card and expose
        # the complete records below it.
        for ster_no in [6, 7, 8, 9, 10]:
            g = perf[perf["sterilizer"] == ster_no].copy()
            st.markdown(f"### Sterilizer {ster_no}")
            if g.empty:
                st.info(f"No Sterilizer {ster_no} record in the previous hour.")
                continue

            row = g.sort_values(["event_dt", "id"]).iloc[-1]
            cycle = pd.to_numeric(row.get("cycle_no"), errors="coerce")
            p1 = pd.to_numeric(row.get("p1"), errors="coerce")
            p2 = pd.to_numeric(row.get("p2"), errors="coerce")
            p3 = pd.to_numeric(row.get("p3"), errors="coerce")
            bpv = pd.to_numeric(row.get("back_pressure_receiver"), errors="coerce")
            event_dt = pd.to_datetime(row.get("event_dt"), errors="coerce")

            cols = st.columns(6)
            vals = [
                ("Cycle", int(cycle) if pd.notna(cycle) else "--"),
                ("P1", _format_value(p1, 1, " PSI")),
                ("P2", _format_value(p2, 1, " PSI")),
                ("P3", _format_value(p3, 1, " PSI")),
                ("BPV", _format_value(bpv, 1, " PSI")),
                ("Record time", event_dt.strftime("%d %b %H:%M:%S") if pd.notna(event_dt) else "--"),
            ]
            for col, (label, val) in zip(cols, vals):
                with col:
                    st.metric(label, val)

            st.caption(f"{len(g)} Sterilizer {ster_no} record(s) found in the previous hour. Latest cycle in that hour is shown above.")
            detail = g[["event_dt", "cycle_no", "p1", "p2", "p3", "back_pressure_receiver", "status"]].copy()
            detail = detail.rename(columns={
                "event_dt": "Record Time",
                "cycle_no": "Cycle",
                "p1": "P1",
                "p2": "P2",
                "p3": "P3",
                "back_pressure_receiver": "BPV",
                "status": "Status",
            })
            detail["Record Time"] = pd.to_datetime(detail["Record Time"], errors="coerce").dt.strftime("%d %b %Y %H:%M:%S")
            st.dataframe(detail, use_container_width=True, hide_index=True)

    st.caption("This analysis uses the NIR clock hour for Press/Digester data and the immediately preceding clock hour for Sterilizer 6–10 cycle data. It is a process correlation check, not a causal determination.")


# ============================================================
# SECONDARY OIL LOSS – NIR SLUDGE / POND DATA
# ============================================================
SECONDARY_SETLINE = 1.6

@st.cache_data(ttl=20, show_spinner=False)
@st.cache_data(ttl=1200, show_spinner=False)
def load_grading_average_data(start_date, end_date):
    """Load daily average grading data from mypalmcom_smartperakmotor."""
    engine = get_running_hours_db_engine()
    sql = text("""
        SELECT
            `date`,
            `underripe_pct`,
            `ripe_pct`,
            `overripe_pct`,
            `hard_pct`,
            `empty_pct`,
            `longstalk_pct`,
            `unripe_pct`
        FROM `grading_average_data`
        WHERE `date` BETWEEN :start_date AND :end_date
        ORDER BY `date`
    """)
    with engine.connect() as conn:
        df = pd.read_sql(
            sql,
            conn,
            params={"start_date": start_date, "end_date": end_date},
        )

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    grading_cols = [
        "underripe_pct",
        "ripe_pct",
        "overripe_pct",
        "hard_pct",
        "empty_pct",
        "longstalk_pct",
        "unripe_pct",
    ]
    for col in grading_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.sort_values("date").reset_index(drop=True)
def load_secondary_oil_loss(start_dt, end_dt):
    engine = get_running_hours_db_engine()
    sql = text("""
        SELECT
            id,
            timestamp,
            sample_id,
            val2
        FROM nir_sludge
        WHERE sample_id LIKE '%pond%'
          AND timestamp >= :start_dt
          AND timestamp <= :end_dt
        ORDER BY timestamp DESC
        LIMIT 5000
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={"start_dt": start_dt, "end_dt": end_dt})
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["val2"] = pd.to_numeric(df["val2"], errors="coerce")
        df = df.dropna(subset=["timestamp", "val2"]).sort_values("timestamp")
    return df


def secondary_trend_label(values):
    vals = pd.to_numeric(values, errors="coerce").dropna()
    if len(vals) < 2:
        return "Insufficient data for trend"
    n = min(20, len(vals))
    recent = vals.tail(n)
    slope = float(recent.iloc[-1] - recent.iloc[0]) / max(len(recent)-1, 1)
    if slope > 0.01:
        return "Rising"
    if slope < -0.01:
        return "Falling"
    return "Stable"


def calculate_daily_running_hours(df, no, selected_day):
    if df.empty or "day_hours" not in df.columns:
        return 0.0
    x = df[pd.to_numeric(df["sterilizer_no"], errors="coerce") == int(no)]
    if x.empty:
        return 0.0
    value = pd.to_numeric(x.iloc[0]["day_hours"], errors="coerce")
    return float(value) if pd.notna(value) else 0.0


@st.cache_data(ttl=10, show_spinner=False)
def load_sterilizer_running_history(start_dt, end_dt):
    engine = get_db_engine()
    sql = text("""
        SELECT sterilizer_no,
               ROUND(SUM(
                   CASE WHEN LOWER(COALESCE(cooking_status,'')) IN ('cooking','running','active','1','true','on')
                   THEN LEAST(TIMESTAMPDIFF(SECOND, insdt, next_insdt), 300) ELSE 0 END
               ) / 3600, 2) AS day_hours
        FROM (
            SELECT sterilizer_no, insdt, cooking_status,
                   LEAD(insdt) OVER (PARTITION BY sterilizer_no ORDER BY insdt) AS next_insdt
            FROM pmc_sterilizer_data
            WHERE insdt >= :start_dt AND insdt <= :end_dt
        ) q
        WHERE next_insdt IS NOT NULL
        GROUP BY sterilizer_no
    """)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn, params={"start_dt": start_dt, "end_dt": end_dt})


@st.cache_data(ttl=5, show_spinner=False)
def load_press_db(start_dt, end_dt):
    engine = get_db_engine()
    cols = ["id", "ts", "ts_local", "device"]
    for i in range(1, 9):
        cols += [
            f"d{i}_amp", f"d{i}_temp", f"d{i}_level",
            f"sp{i}_amp", f"sp{i}_setpoint", f"sp{i}_cone_pct",
            f"sp{i}_auto_manual", f"sp{i}_hpu_amp", f"sp{i}_hpu_pressure",
            f"sp{i}_cone_activated", f"sp{i}_cone_deactivated",
        ]
    cols += ["tfc1_amp", "tfc2_amp", "tfc3_amp", "tfc4_amp", "tfc5_amp",
             "cbc1_amp", "cbc2_amp", "cross1_amp", "cross2_amp", "raw_data"]
    select_cols = ",\n            ".join(cols)
    sql = text(f'''
        SELECT
            {select_cols}
        FROM pmc_press_station_log
        WHERE ts_local >= :start_dt
          AND ts_local <= :end_dt
        ORDER BY ts_local DESC
        LIMIT 1
    ''')
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={"start_dt": start_dt, "end_dt": end_dt})
    if not df.empty:
        df["ts_local"] = pd.to_datetime(df["ts_local"], errors="coerce")
        # Only convert numeric process fields. IMPORTANT: keep spX_auto_manual
        # as text because the database stores values such as "Auto" / "Manual".
        for i in range(1, 9):
            for c in [
                f"d{i}_amp", f"d{i}_temp",
                f"sp{i}_amp", f"sp{i}_setpoint", f"sp{i}_cone_pct",
                f"sp{i}_hpu_amp", f"sp{i}_hpu_pressure"
            ]:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


@st.cache_data(ttl=10, show_spinner=False)
def load_press_trend_db(start_dt, end_dt, press_no):
    """Load the complete selected-period digester temperature/level history for one press.

    This is intentionally separate from load_press_db(), which only loads the latest
    row for the live press cards. The trend graph must use every timestamp from the
    selected start through end date.
    """
    engine = get_db_engine()
    i = int(press_no)
    sql = text(f"""
        SELECT ts_local,
               d{i}_temp AS temperature,
               d{i}_level AS level_raw
        FROM pmc_press_station_log
        WHERE ts_local >= :start_dt
          AND ts_local <= :end_dt
        ORDER BY ts_local ASC
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={"start_dt": start_dt, "end_dt": end_dt})

    if df.empty:
        return df

    df["ts_local"] = pd.to_datetime(df["ts_local"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    raw = df["level_raw"].astype(str).str.strip().str.lower()
    numeric_level = pd.to_numeric(df["level_raw"], errors="coerce")

    df["level_state"] = "Unknown"
    df.loc[raw.isin(["full", "high", "above 75", "above 75%"]), "level_state"] = "Above 75%"
    df.loc[raw.isin(["not-full", "not full", "low", "below 75", "below 75%"]), "level_state"] = "Below 75%"
    df.loc[numeric_level > 75, "level_state"] = "Above 75%"
    df.loc[numeric_level < 75, "level_state"] = "Below 75%"
    df.loc[numeric_level == 75, "level_state"] = "At 75%"

    # Numeric representation for the secondary level axis.
    # 100 = Above 75%, 0 = Below 75%, 50 = exactly 75%.
    df["level_value"] = df["level_state"].map({
        "Above 75%": 100,
        "At 75%": 50,
        "Below 75%": 0,
    })

    return df.dropna(subset=["ts_local"]).sort_values("ts_local")


def process_alerts_for_press(row, press_no):
    findings = []
    i = int(press_no)
    checks = [
        (f"d{i}_level", "Digester Level", "< 75%", lambda v: v < 75,
         "Check digester feed level. Low digester level may affect pressing stability."),
        (f"d{i}_temp", "Digester Temperature", "< 80°C or > 95°C", lambda v: v < 80 or v > 95,
         "Check digester temperature control and steam input."),
        (f"d{i}_amp", "Digester Motor Amps", "< 24 A", lambda v: v < 24,
         "Check digester motor loading and feed condition."),
        (f"sp{i}_hpu_pressure", "Press Hydraulic Pressure", "< 70 bar", lambda v: v < 70,
         "Check press hydraulic pressure and hydraulic system condition."),
        (f"sp{i}_amp", "Press Motor Amps", "< 29 A or > 56 A", lambda v: v < 29 or v > 56,
         "Check press motor loading, feed condition and press operation."),
    ]
    for col, name, limit, bad, recommendation in checks:
        if col in row.index and pd.notna(row[col]):
            value = float(row[col])
            if bad(value):
                findings.append({"parameter": name, "actual": value, "limit": limit,
                                 "recommendation": recommendation, "column": col})
    return findings


def process_alerts_for_sterilizer(row):
    findings = []
    if row is None or row.empty:
        return findings
    no = pd.to_numeric(row.get("sterilizer_no"), errors="coerce")
    pressure = pd.to_numeric(row.get("pressure"), errors="coerce")
    if pd.isna(no) or pd.isna(pressure):
        return findings
    ranges = {1: (14, 26), 2: (23, 36), 3: (34, 43)}
    if int(no) in ranges:
        low, high = ranges[int(no)]
        if pressure < low or pressure > high:
            findings.append({"parameter": f"P{int(no)} Pressure", "actual": float(pressure),
                             "limit": f"{low}–{high} psi",
                             "recommendation": "Check sterilizer pressure and steam control."})
    return findings


def render_db_alerts(findings):
    if not findings:
        st.markdown(
            '<div class="point-good"><div class="point-good-title">✓ All running good</div>'
            '<div class="point-good-detail">No configured Sterilizer/Press alert was triggered.</div></div>',
            unsafe_allow_html=True,
        )
        return
    for f in findings:
        st.markdown(
            f'''<div class="point-alert">
                <div class="point-alert-title">⚠ ALERT: {f["parameter"]}</div>
                <div class="point-alert-detail">Actual: <b>{f["actual"]:.2f}</b> &nbsp; | &nbsp; Limit: <b>{f["limit"]}</b></div>
                <div class="point-alert-recommendation">Recommendation: {f["recommendation"]}</div>
            </div>''',
            unsafe_allow_html=True,
        )


# The rules below are the alert limits supplied for the mill.
# They are used only when the corresponding parameter exists in
# the uploaded Excel/report row.
PROCESS_ALERT_STATIONS = {"Sterilizer", "Press"}

ALERT_RULES = [
    # Ramp
    {
        "station": "Ramp",
        "parameter": "Hard Bunches",
        "aliases": ["Hard Bunches", "Hard Bunch"],
        "condition": "high",
        "limit": 45,
        "unit": "units",
        "recommendation": "Check bunch quality at the ramp and investigate hard/underripe incoming fruit.",
    },
    {
        "station": "Ramp",
        "parameter": "Under Ripe Bunches",
        "aliases": ["Under Ripe Bunches", "Under Ripe", "Underripe"],
        "condition": "high",
        "limit": 20,
        "unit": "%",
        "recommendation": "Review incoming FFB ripeness and ramp grading. High underripe fruit can contribute to process oil-loss variation.",
    },
    {
        "station": "Ramp",
        "parameter": "Loose Fruits",
        "aliases": ["Loose Fruits", "Loose Fruit"],
        "condition": "low",
        "limit": 5,
        "unit": "%",
        "recommendation": "Check loose-fruit recovery and ramp collection condition.",
    },
    {
        "station": "Ramp",
        "parameter": "Overall Ripeness",
        "aliases": ["Overall Ripeness", "Ripeness"],
        "condition": "low",
        "limit": 50,
        "unit": "%",
        "recommendation": "Review incoming fruit ripeness distribution and grading condition.",
    },
    {
        "station": "Ramp",
        "parameter": "Overdue",
        "aliases": ["Overdue"],
        "condition": "high",
        "limit": 5,
        "unit": "units",
        "recommendation": "Check overdue FFB handling and fruit residence time.",
    },
    {
        "station": "Ramp",
        "parameter": "Loose Fruits",
        "aliases": ["Loose Fruits", "Loose Fruit"],
        "condition": "high",
        "limit": 10,
        "unit": "%",
        "recommendation": "Check loose-fruit recovery and ramp handling. High loose fruit should be investigated.",
    },

    # Sterilizer
    {
        "station": "Sterilizer",
        "parameter": "P1 Pressure",
        "aliases": ["P1 Pressure", "P1"],
        "condition": "range",
        "low": 14,
        "high": 26,
        "unit": "psi",
        "recommendation": "Check sterilizer P1 pressure and steam control.",
    },
    {
        "station": "Sterilizer",
        "parameter": "P2 Pressure",
        "aliases": ["P2 Pressure", "P2"],
        "condition": "range",
        "low": 23,
        "high": 36,
        "unit": "psi",
        "recommendation": "Check sterilizer P2 pressure and steam control.",
    },
    {
        "station": "Sterilizer",
        "parameter": "P3 Pressure",
        "aliases": ["P3 Pressure", "P3"],
        "condition": "range",
        "low": 34,
        "high": 43,
        "unit": "psi",
        "recommendation": "Check sterilizer P3 pressure and steam control.",
    },
    {
        "station": "Sterilizer",
        "parameter": "BPV",
        "aliases": ["BPV"],
        "condition": "range",
        "low": 36,
        "high": 48,
        "unit": "",
        "recommendation": "Check BPV operating range and sterilizer steam conditions.",
    },
    {
        "station": "Sterilizer",
        "parameter": "Holding Time",
        "aliases": ["Holding Time", "Hold Time"],
        "condition": "range",
        "low": 40,
        "high": 60,
        "unit": "min",
        "recommendation": "Check sterilizer holding time and cycle sequence.",
    },

    # Press
    {
        "station": "Press",
        "parameter": "Digester Level",
        "aliases": ["Digester Level"],
        "condition": "low",
        "limit": 75,
        "unit": "%",
        "recommendation": "Check digester feed level. Low digester level may affect pressing stability.",
    },
    {
        "station": "Press",
        "parameter": "Digester Temperature",
        "aliases": ["Digester Temperature", "Digester Temp"],
        "condition": "low",
        "limit": 80,
        "unit": "°C",
        "recommendation": "Check digester temperature and steam/heat supply.",
    },
    {
        "station": "Press",
        "parameter": "Digester Temperature",
        "aliases": ["Digester Temperature", "Digester Temp"],
        "condition": "high",
        "limit": 95,
        "unit": "°C",
        "recommendation": "Check digester temperature control and steam input.",
    },
    {
        "station": "Press",
        "parameter": "Digester Drainage Flow",
        "aliases": ["Digester Drainage Flow", "Drainage Flow"],
        "condition": "text_low",
        "limit": None,
        "unit": "",
        "recommendation": "Check digester drainage flow and blockage/flow restriction.",
    },
    {
        "station": "Press",
        "parameter": "Digester Motor Amps",
        "aliases": ["Digester Motor Amps", "Digester Motor Amp", "Digester Amps"],
        "condition": "low",
        "limit": 24,
        "unit": "A",
        "recommendation": "Check digester motor loading and feed condition.",
    },
    {
        "station": "Press",
        "parameter": "Press Hydraulic Pressure",
        "aliases": ["Press Hydraulic Pressure", "Hydraulic Pressure"],
        "condition": "low",
        "limit": 70,
        "unit": "bar",
        "recommendation": "Check press hydraulic pressure and hydraulic system condition.",
    },
    {
        "station": "Press",
        "parameter": "Press Motor Amps",
        "aliases": ["Press Motor Amps", "Press Motor Amp"],
        "condition": "low",
        "limit": 29,
        "unit": "A",
        "recommendation": "Check press motor loading and operating condition.",
    },
    {
        "station": "Press",
        "parameter": "Press Motor Amps",
        "aliases": ["Press Motor Amps", "Press Motor Amp"],
        "condition": "high",
        "limit": 56,
        "unit": "A",
        "recommendation": "Check press motor load, feed condition and possible overload.",
    },
    {
        "station": "Press",
        "parameter": "Press Fibre Flow",
        "aliases": ["Press Fibre Flow", "Fibre Flow", "Fiber Flow"],
        "condition": "text_low",
        "limit": None,
        "unit": "",
        "recommendation": "Check fibre flow and press discharge condition.",
    },
]


# ============================================================
# HELPERS
# ============================================================
def clean_name(value):
    value = str(value)
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip().lower()


def flatten_columns(df):
    out = df.copy()

    if isinstance(out.columns, pd.MultiIndex):
        flat = []
        for col in out.columns:
            parts = []
            for item in col:
                if pd.notna(item):
                    item = str(item).strip()
                    if item and item.lower() != "nan":
                        parts.append(item)
            flat.append(" | ".join(parts))
        out.columns = flat
    else:
        out.columns = [str(c).strip() for c in out.columns]

    return out


def find_matching_columns(columns, aliases):
    matches = []
    normalized_columns = [(col, clean_name(col)) for col in columns]

    for alias in aliases:
        a = clean_name(alias)
        for col, norm in normalized_columns:
            if a == norm or a in norm or norm in a:
                if col not in matches:
                    matches.append(col)

    return matches


def value_is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def evaluate_rule(value, rule):
    """Return (violated, direction_text)."""
    if pd.isna(value):
        return False, ""

    condition = rule["condition"]

    if condition == "high":
        if value_is_number(value) and float(value) > rule["limit"]:
            return True, f">{rule['limit']}{rule['unit']}"
        return False, ""

    if condition == "low":
        if value_is_number(value) and float(value) < rule["limit"]:
            return True, f"<{rule['limit']}{rule['unit']}"
        return False, ""

    if condition == "range":
        if value_is_number(value):
            number = float(value)
            if number < rule["low"] or number > rule["high"]:
                return True, f"{rule['low']}–{rule['high']}{rule['unit']}"
        return False, ""

    if condition == "text_low":
        text_value = clean_name(value)
        low_words = ["low", "low flow", "very low", "no flow"]
        if any(word in text_value for word in low_words):
            return True, "LOW"
        return False, ""

    return False, ""


def analyze_associated_row(row, press_name):
    """
    Compare every available associated Excel parameter at the clicked
    timestamp against the configured mill alert rules.
    """
    findings = []

    for rule in ALERT_RULES:
        if rule["station"] not in PROCESS_ALERT_STATIONS:
            continue

        matches = find_matching_columns(row.index, rule["aliases"])

        # Prefer a column that contains the same press number when available.
        press_number = press_name.split()[-1]
        press_specific = [
            c for c in matches
            if f"press {press_number}" in clean_name(c)
            or f"p{press_number}" in clean_name(c)
        ]

        candidate_columns = press_specific or matches

        for column in candidate_columns:
            value = row[column]
            violated, limit_text = evaluate_rule(value, rule)

            if violated:
                findings.append(
                    {
                        "Station": rule["station"],
                        "Parameter": rule["parameter"],
                        "Excel Column": column,
                        "Actual Value": value,
                        "Alert Condition": limit_text,
                        "Recommendation": rule["recommendation"],
                    }
                )
                break

    return findings


@st.cache_data(ttl=300, show_spinner=False)
def load_nir_pressedfiber_db(start_date, end_date):
    """Load NIR pressed-fiber samples from Smart Perak Motor DB.

    Each sample_id contains the press number after the text 'press'.
    Example: 21-9-26-press12060921-05519 -> Press 1.
    The raw DB rows are kept so a selected graph point can still be
    traced back to its original sample_id/timestamp.
    """
    engine = get_running_hours_db_engine()

    start_dt = pd.Timestamp(start_date)
    end_dt = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)

    sql = text("""
        SELECT
            `sample_id`,
            `val2`,
            `timestamp`
        FROM `nir_pressedfiber`
        WHERE `timestamp` BETWEEN :start_dt AND :end_dt
        ORDER BY `timestamp`
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            sql,
            conn,
            params={
                "start_dt": start_dt.to_pydatetime(),
                "end_dt": end_dt.to_pydatetime(),
            },
        )

    if df.empty:
        return df, df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["val2"] = pd.to_numeric(df["val2"], errors="coerce")
    df["sample_id"] = df["sample_id"].astype("string")

    # Extract the press number immediately after 'press'.
    # For example:
    #   press120... -> Press 1
    #   press220... -> Press 2
    #   press720... -> Press 7
    df["press_no"] = pd.to_numeric(
        df["sample_id"].str.extract(r"press\s*([1-8])", expand=False),
        errors="coerce",
    )

    df = df.dropna(subset=["timestamp", "val2", "press_no"]).copy()
    df["press_no"] = df["press_no"].astype(int)

    # Keep only Press 1–8 for the eight NIR cards.
    df = df[df["press_no"].between(1, 8)].copy()

    # Preserve the DB row identity for point selection.
    df["_SourceRow"] = range(len(df))

    df["Date"] = df["timestamp"].dt.normalize()
    df["Sampling Time"] = df["timestamp"].dt.strftime("%H:%M:%S")
    df["DateTime"] = df["timestamp"]

    # Convert the row-oriented DB data into the same Press 1–8 structure
    # expected by the existing NIR trend cards.
    for press_no in range(1, 9):
        col = f"Press {press_no}"
        df[col] = pd.NA
        mask = df["press_no"].eq(press_no)
        df.loc[mask, col] = df.loc[mask, "val2"]

    for col in PRESS_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("DateTime").reset_index(drop=True)
    df["_SourceRow"] = range(len(df))

    # source_flat is the DB-row lookup used by the existing point-analysis
    # section. It now contains sample_id/val2/timestamp instead of Excel data.
    source_flat = df.set_index("_SourceRow", drop=False).copy()

    return df, source_flat


@st.cache_data
def load_data(uploaded_file=None):
    source = uploaded_file if uploaded_file is not None else Path(DEFAULT_FILE)

    tables = pd.read_html(source)
    if not tables:
        return None

    raw = tables[0]

    if not isinstance(raw.columns, pd.MultiIndex):
        raise ValueError(
            "Expected the report to contain grouped headers."
        )

    # NIR table used for the trend.
    nir = raw["NIR"].copy()

    nir["Date"] = pd.to_datetime(
        nir["Date"].replace("-", pd.NA),
        format="%d-%m-%Y",
        errors="coerce",
    )

    nir["Sampling Time"] = (
        nir["Sampling Time"]
        .replace("-", pd.NA)
        .astype("string")
    )

    for press in PRESS_COLS:
        if press in nir.columns:
            nir[press] = pd.to_numeric(
                nir[press],
                errors="coerce",
            )

    nir["DateTime"] = pd.to_datetime(
        nir["Date"].dt.strftime("%Y-%m-%d")
        + " "
        + nir["Sampling Time"].fillna("00:00"),
        errors="coerce",
    )

    # Keep original row position so a clicked NIR point can retrieve
    # the corresponding row from the complete Excel table.
    nir["_SourceRow"] = nir.index

    nir = nir.dropna(
        subset=["DateTime"]
    ).sort_values("DateTime")

    source_flat = flatten_columns(raw)

    return raw, nir, source_flat


# ============================================================
# CLARIFICATION STATION
# ============================================================
# The clarification sensor records use the same MQTT monitoring database as
# the Press station. The table name can be overridden if the deployment uses
# a different name.
CLARIFICATION_TABLE = os.getenv(
    "PMC_CLARIFICATION_TABLE",
    "pmc_clarification_data_log",
)


def _safe_table_name(name):
    """Allow only a normal MySQL identifier before interpolating a table name."""
    if not re.fullmatch(r"[A-Za-z0-9_]+", str(name or "")):
        raise ValueError("Invalid clarification table name")
    return str(name)


@st.cache_data(ttl=300, show_spinner=False)
def find_clarification_table():
    """Find the clarification table when the configured name is unavailable."""
    engine = get_db_engine()
    configured = _safe_table_name(CLARIFICATION_TABLE)
    candidates = []
    sql = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
          AND LOWER(table_name) LIKE '%clarification%'
        ORDER BY table_name
    """)
    with engine.connect() as conn:
        try:
            found = pd.read_sql(sql, conn)
            candidates = found["table_name"].astype(str).tolist()
        except Exception:
            pass

    # Prefer the configured table only when it actually exists.
    for name in candidates:
        if name.lower() == configured.lower():
            return name
    for name in candidates:
        if "clarification" in name.lower() and "log" in name.lower():
            return name
    for name in candidates:
        if "clarification" in name.lower():
            return name
    return configured


@st.cache_data(ttl=30, show_spinner=False)
def load_clarification_db(start_dt, end_dt):
    """Load clarification-station history for the selected period."""
    engine = get_db_engine()
    table = _safe_table_name(find_clarification_table())
    sql = text(f"""
        SELECT
            id, ts, ts_local, station,
            sludge_tank_1_level, sludge_tank_1_temp,
            sludge_tank_2_level, sludge_tank_2_temp,
            pure_oil_tank_1_level, pure_oil_tank_1_temp,
            pure_oil_tank_2_level, pure_oil_tank_2_temp,
            crude_oil_tank_1_1_level, crude_oil_tank_1_1_temp,
            crude_oil_tank_1_2_level, crude_oil_tank_1_2_temp,
            vertical_clarifier_1_level, vertical_clarifier_1_temp,
            vertical_clarifier_2_level, vertical_clarifier_2_temp,
            vacuum_dryer_1_pressure, vacuum_dryer_2_pressure,
            vibrating_screen_1_amp, vibrating_screen_2_amp,
            vibrating_screen_3_amp,
            decanter_1_amp, decanter_2_amp,
            created_at, quality_overall, quality_source
        FROM `{table}`
        WHERE station = 'clarification_station'
          AND ts_local >= :start_dt
          AND ts_local <= :end_dt
        ORDER BY ts_local
    """)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={
            "start_dt": pd.Timestamp(start_dt).to_pydatetime(),
            "end_dt": pd.Timestamp(end_dt).to_pydatetime(),
        })
    if df.empty:
        return df

    for c in [
        "ts_local", "created_at", "sludge_tank_1_level", "sludge_tank_1_temp",
        "sludge_tank_2_level", "sludge_tank_2_temp", "pure_oil_tank_1_level",
        "pure_oil_tank_1_temp", "pure_oil_tank_2_level", "pure_oil_tank_2_temp",
        "crude_oil_tank_1_1_level", "crude_oil_tank_1_1_temp",
        "crude_oil_tank_1_2_level", "crude_oil_tank_1_2_temp",
        "vertical_clarifier_1_level", "vertical_clarifier_1_temp",
        "vertical_clarifier_2_level", "vertical_clarifier_2_temp",
        "vacuum_dryer_1_pressure", "vacuum_dryer_2_pressure",
        "vibrating_screen_1_amp", "vibrating_screen_2_amp",
        "vibrating_screen_3_amp", "decanter_1_amp", "decanter_2_amp",
    ]:
        if c in df.columns:
            if c in {"ts_local", "created_at"}:
                df[c] = pd.to_datetime(df[c], errors="coerce")
            else:
                df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna(subset=["ts_local"]).sort_values("ts_local").reset_index(drop=True)


def _clarification_duration_above_threshold(df, column, threshold, window_start, window_end, max_gap_minutes=15):
    """Estimate hours above a threshold from consecutive clarification readings.

    Only consecutive readings with a gap of <= max_gap_minutes are counted so a
    missing-data gap is not incorrectly treated as continuous operation.
    """
    if df.empty or column not in df.columns:
        return 0.0

    work = df[["ts_local", column]].copy()
    work["ts_local"] = pd.to_datetime(work["ts_local"], errors="coerce")
    work[column] = pd.to_numeric(work[column], errors="coerce")
    work = work.dropna(subset=["ts_local", column]).sort_values("ts_local")
    if work.empty:
        return 0.0

    start = pd.Timestamp(window_start)
    end = pd.Timestamp(window_end)
    work = work[(work["ts_local"] >= start) & (work["ts_local"] <= end)].copy()
    if work.empty:
        return 0.0

    work["next_time"] = work["ts_local"].shift(-1).fillna(end)
    work["next_time"] = work["next_time"].clip(upper=end)
    work["duration_hours"] = (
        work["next_time"] - work["ts_local"]
    ).dt.total_seconds() / 3600.0

    valid_gap = work["duration_hours"].between(0, max_gap_minutes / 60.0)
    above = work[column] > threshold
    return float(work.loc[valid_gap & above, "duration_hours"].sum())


def _clarification_running_status(df, column, window_start, window_end, amp_threshold=5.0):
    """Return latest running state and estimated running hours for a motor-current column."""
    latest_value = None
    if not df.empty and column in df.columns:
        valid = df[["ts_local", column]].copy()
        valid[column] = pd.to_numeric(valid[column], errors="coerce")
        valid = valid.dropna(subset=[column]).sort_values("ts_local")
        if not valid.empty:
            latest_value = float(valid.iloc[-1][column])

    hours = _clarification_duration_above_threshold(
        df, column, amp_threshold, window_start, window_end
    )
    running = latest_value is not None and latest_value > amp_threshold
    return running, latest_value, hours


def _trend_word(df, column):
    s = pd.to_numeric(df[column], errors="coerce").dropna()
    if len(s) < 2:
        return "Insufficient data"
    first, last = float(s.iloc[0]), float(s.iloc[-1])
    scale = max(abs(first), abs(last), 1.0)
    delta = last - first
    if abs(delta) <= 0.02 * scale:
        return "Stable"
    return "Rising" if delta > 0 else "Falling"


def _clarification_kpi_rows(df, specs):
    rows = []
    for label, col, unit in specs:
        if col not in df.columns:
            continue
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if s.empty:
            latest = avg = minimum = maximum = None
        else:
            latest, avg, minimum, maximum = float(s.iloc[-1]), float(s.mean()), float(s.min()), float(s.max())
        rows.append({
            "Parameter": label,
            "Latest": f"{latest:.1f} {unit}" if latest is not None else "--",
            "Average": f"{avg:.1f} {unit}" if avg is not None else "--",
            "Minimum": f"{minimum:.1f} {unit}" if minimum is not None else "--",
            "Maximum": f"{maximum:.1f} {unit}" if maximum is not None else "--",
            "Trend": _trend_word(df, col),
            "Samples": int(s.size),
        })
    return pd.DataFrame(rows)


def _add_clarification_chart(df, title, series, y_title, height=360):
    fig = go.Figure()
    added = False
    for label, col in series:
        if col not in df.columns:
            continue
        y = pd.to_numeric(df[col], errors="coerce")
        if not y.notna().any():
            continue
        fig.add_trace(go.Scatter(
            x=df["ts_local"], y=y, mode="lines", name=label,
            connectgaps=False,
            hovertemplate=f"%{{x|%d %b %Y %H:%M:%S}}<br>{label}: %{{y:.2f}}<extra></extra>",
        ))
        added = True
    if not added:
        st.info(f"No data available for {title}.")
        return
    fig.update_layout(
        height=height,
        margin=dict(l=55, r=25, t=45, b=55),
        title=title,
        paper_bgcolor="#0b151d",
        plot_bgcolor="#0b151d",
        font=dict(color="#dbe5ec"),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0),
        xaxis=dict(title="Time", type="date", gridcolor="#293a46", rangeslider_visible=True),
        yaxis=dict(title=y_title, gridcolor="#293a46", zeroline=False),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "scrollZoom": True})


# ============================================================
# TOP NAVIGATION
# ============================================================


# ============================================================
# TOP NAVIGATION
# ============================================================
NAV_ITEMS = [
    ("NIR Trend", "Lab Oil Loss – NIR Data Trend"),
    ("Overall Grading", "Overall Grading"),
    ("Sterilizer", "Sterilizer Running Hours"),
    ("Press", "Press Running Hours"),
    ("Clarification", "Clarification Monitoring"),
    ("Secondary Oil Loss", "Secondary Oil Loss Prediction"),
]

if "pmc_page" not in st.session_state:
    st.session_state.pmc_page = "Lab Oil Loss – NIR Data Trend"
if "pmc_settings" not in st.session_state:
    st.session_state.pmc_settings = False

st.markdown('<div class="top-nav-wrap">', unsafe_allow_html=True)
nav_cols = st.columns([1.05, 1.2, 1.0, 0.9, 1.05, 1.35, 0.5])
for idx, (label, target) in enumerate(NAV_ITEMS):
    with nav_cols[idx]:
        st.markdown('<div class="topnav-btn">', unsafe_allow_html=True)
        if st.button(label, key=f"topnav_{idx}", use_container_width=True):
            st.session_state.pmc_page = target
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
with nav_cols[-1]:
    st.markdown('<div class="topnav-btn">', unsafe_allow_html=True)
    if st.button("⚙", key="topnav_settings", use_container_width=True, help="Dashboard settings"):
        st.session_state.pmc_settings = not st.session_state.pmc_settings
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

page = st.session_state.pmc_page

if st.session_state.pmc_settings:
    st.markdown(
        '<div class="settings-panel"><b>Dashboard Settings</b><br>'
        'Live database monitoring is enabled. Sterilizer, Press and Clarification pages auto-refresh every 20 minutes. '
        'Secondary Oil Loss uses a fixed analysis line of <b>1.60</b> and has its own Refresh Now button.'
        '</div>',
        unsafe_allow_html=True,
    )




def render_high_nir_inline_process_confirmation(selected, press_name, high_limit=4.7):
    """Show process data inline when a selected NIR point is above 4.7%."""
    if selected is None:
        return

    try:
        nir_value = float(selected.get("value", 0))
    except (TypeError, ValueError):
        return

    if nir_value <= high_limit:
        return

    sample_dt = pd.to_datetime(selected.get("datetime"), errors="coerce")
    if pd.isna(sample_dt):
        return

    press_no_match = re.findall(r"\d+", str(press_name))
    if not press_no_match:
        return
    press_no = int(press_no_match[-1])

    st.markdown(
        '<div class="section-heading" style="font-size:15px;margin-top:12px;">'
        'High NIR Process Check</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        f"NIR {nir_value:.2f}% is above the fixed 4.70% limit. "
        f"Press/Digester data uses the NIR clock hour "
        f"({sample_dt.floor('h').strftime('%d %b %Y %H:%M')}–"
        f"{(sample_dt.floor('h') + pd.Timedelta(hours=1) - pd.Timedelta(seconds=1)).strftime('%H:%M:%S')}); "
        f"Sterilizer data uses the immediately preceding clock hour."
    )

    # ------------------------------------------------------------
    # OVERALL GRADING: selected NIR sample date
    # ------------------------------------------------------------
    # The grading report is matched to the calendar date of the selected
    # NIR sample. It is read from grading_average_data in the same
    # mypalmcom_smartperakmotor database.
    grading_date = sample_dt.date()
    st.markdown(
        '<div class="section-heading">Overall Grading Report</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        f"Overall grading for the selected NIR sample date: "
        f"{sample_dt.strftime('%d %b %Y')}"
    )

    try:
        grading_selected = load_grading_average_data(grading_date, grading_date)
    except Exception as exc:
        grading_selected = pd.DataFrame()
        st.warning(f"Overall grading data could not be loaded: {exc}")

    if grading_selected.empty:
        st.info(
            f"No Overall Grading record was found for "
            f"{sample_dt.strftime('%d %b %Y')}."
        )
    else:
        # Normally there is one daily-average row. If the database contains
        # more than one row for the same date, show all of them in the table.
        grading_row = grading_selected.iloc[-1]
        grading_categories = [
            ("Underripe", "underripe_pct"),
            ("Ripe", "ripe_pct"),
            ("Overripe", "overripe_pct"),
            ("Hard", "hard_pct"),
            ("Empty", "empty_pct"),
            ("Longstalk", "longstalk_pct"),
            ("Unripe", "unripe_pct"),
        ]

        grading_cols = st.columns(7)
        for col, (label, field) in zip(grading_cols, grading_categories):
            value = pd.to_numeric(grading_row.get(field), errors="coerce")
            value_text = f"{float(value):.2f}%" if pd.notna(value) else "--"
            with col:
                st.metric(label, value_text)

        grading_display = grading_selected.copy()
        grading_display["date"] = pd.to_datetime(
            grading_display["date"], errors="coerce"
        ).dt.strftime("%d-%m-%Y")
        grading_display = grading_display.rename(
            columns={
                "date": "Date",
                "underripe_pct": "Underripe (%)",
                "ripe_pct": "Ripe (%)",
                "overripe_pct": "Overripe (%)",
                "hard_pct": "Hard (%)",
                "empty_pct": "Empty (%)",
                "longstalk_pct": "Longstalk (%)",
                "unripe_pct": "Unripe (%)",
            }
        )
        st.dataframe(
            grading_display.round(2),
            use_container_width=True,
            hide_index=True,
        )

        # Show the selected-date grading distribution as a compact chart.
        grading_chart = go.Figure()
        for label, field in grading_categories:
            chart_value = pd.to_numeric(grading_row.get(field), errors="coerce")
            if pd.notna(chart_value):
                grading_chart.add_trace(
                    go.Bar(
                        x=[label],
                        y=[float(chart_value)],
                        name=label,
                        hovertemplate=f"{label}: %{{y:.2f}}%<extra></extra>",
                    )
                )
        grading_chart.update_layout(
            height=330,
            margin=dict(l=45, r=20, t=25, b=55),
            paper_bgcolor="#0b151d",
            plot_bgcolor="#0b151d",
            font=dict(color="#dbe5ec"),
            showlegend=False,
            xaxis=dict(title="Grading Category", gridcolor="#293a46"),
            yaxis=dict(title="Percentage (%)", gridcolor="#293a46", zeroline=False),
        )
        st.plotly_chart(
            grading_chart,
            use_container_width=True,
            config={"displaylogo": False},
        )

    st.caption(
        "The values shown are the actual database readings associated with the "
        "selected high-NIR sample. This is a process correlation check; it does "
        "not by itself establish causation."
    )

    # ------------------------------------------------------------
    # STERILIZER: previous-hour cycle data
    # ------------------------------------------------------------
    try:
        ster_df = load_sterilizer_confirmation_previous_hour(sample_dt)
    except Exception as exc:
        ster_df = pd.DataFrame()
        st.warning(f"Sterilizer performance data could not be loaded: {exc}")

    st.markdown("**Sterilizer Cycle Performance**")

    if ster_df.empty:
        ster_hour_start = sample_dt.floor("h") - pd.Timedelta(hours=1)
        ster_hour_end = sample_dt.floor("h")
        st.info(
            "No Sterilizer 6–10 performance records were found in the previous hour "
            f"({ster_hour_start.strftime('%d %b %Y %H:%M')}–"
            f"{(ster_hour_end - pd.Timedelta(seconds=1)).strftime('%H:%M:%S')})."
        )
    else:
        # Latest cycle for each sterilizer, while keeping the complete record
        # table below so no cycle data is hidden.
        latest_rows = []
        for ster_no in [6, 7, 8, 9, 10]:
            g = ster_df[ster_df["sterilizer"] == ster_no].sort_values(
                ["event_dt", "id"]
            )
            if not g.empty:
                latest_rows.append(g.iloc[-1])

        if latest_rows:
            st.markdown("**Latest cycle in the previous hour**")
            for row in latest_rows:
                cycle = pd.to_numeric(row.get("cycle_no"), errors="coerce")
                ster_no = pd.to_numeric(row.get("sterilizer"), errors="coerce")
                event_dt = pd.to_datetime(row.get("event_dt"), errors="coerce")

                cols = st.columns(6)
                values = [
                    ("Sterilizer", int(ster_no) if pd.notna(ster_no) else "--"),
                    ("Cycle", int(cycle) if pd.notna(cycle) else "--"),
                    ("P1", _format_value(row.get("p1"), 1, " PSI")),
                    ("P2", _format_value(row.get("p2"), 1, " PSI")),
                    ("P3", _format_value(row.get("p3"), 1, " PSI")),
                    ("BPV", _format_value(row.get("back_pressure_receiver"), 1, " PSI")),
                ]
                for c, (label, value) in zip(cols, values):
                    with c:
                        st.metric(label, value)

                if pd.notna(event_dt):
                    st.caption(
                        f"Sterilizer {int(ster_no)} record time: "
                        f"{event_dt.strftime('%d %b %Y %H:%M:%S')}"
                    )

        ster_detail = ster_df[
            [
                "event_dt",
                "sterilizer",
                "cycle_no",
                "p1",
                "p2",
                "p3",
                "back_pressure_receiver",
                "status",
            ]
        ].copy()
        ster_detail = ster_detail.rename(
            columns={
                "event_dt": "Record Time",
                "sterilizer": "Sterilizer",
                "cycle_no": "Cycle",
                "p1": "P1 (PSI)",
                "p2": "P2 (PSI)",
                "p3": "P3 (PSI)",
                "back_pressure_receiver": "BPV (PSI)",
                "status": "Status",
            }
        )
        ster_detail["Record Time"] = pd.to_datetime(
            ster_detail["Record Time"], errors="coerce"
        ).dt.strftime("%d %b %Y %H:%M:%S")

        st.markdown("**All Sterilizer cycle records in the previous hour**")
        st.dataframe(
            ster_detail,
            use_container_width=True,
            hide_index=True,
        )


    # ------------------------------------------------------------
    # PRESS
    # ------------------------------------------------------------
    try:
        press_df = load_press_confirmation_hour(sample_dt, press_no)
    except Exception as exc:
        press_df = pd.DataFrame()
        st.warning(f"Press/Digester data could not be loaded: {exc}")

    st.markdown("**Press Performance**")

    if press_df.empty:
        st.info(f"No Press {press_no} / Digester records were found in the NIR hour.")
    else:
        press_df = press_df.sort_values("ts_local").copy()
        latest = press_df.iloc[-1]

        latest_dt = pd.to_datetime(latest.get("ts_local"), errors="coerce")
        press_values = [
            ("Record time", latest_dt.strftime("%d %b %H:%M:%S") if pd.notna(latest_dt) else "--"),
            ("Press setpoint", _format_value(latest.get("press_setpoint"), 1, " A")),
            ("Press motor amps", _format_value(latest.get("press_motor_amp"), 1, " A")),
            ("Hydraulic pressure", _format_value(latest.get("hydraulic_pressure"), 1, " bar")),
            ("Auto / Manual", str(latest.get("auto_manual") or "--")),
        ]
        metric_cols = st.columns(5)
        for col, (label, value) in zip(metric_cols, press_values):
            with col:
                st.metric(label, value)

        press_detail = press_df[
            ["ts_local", "press_setpoint", "press_motor_amp", "hydraulic_pressure", "auto_manual"]
        ].copy().rename(
            columns={
                "ts_local": "Record Time",
                "press_setpoint": "Press Setpoint (A)",
                "press_motor_amp": "Press Motor Amps (A)",
                "hydraulic_pressure": "Hydraulic Pressure (bar)",
                "auto_manual": "Auto / Manual",
            }
        )
        press_detail["Record Time"] = pd.to_datetime(
            press_detail["Record Time"], errors="coerce"
        ).dt.strftime("%d %b %Y %H:%M:%S")
        st.dataframe(press_detail, use_container_width=True, hide_index=True)

    # ------------------------------------------------------------
    # DIGESTER
    # ------------------------------------------------------------
    st.markdown("**Digester Performance**")

    if press_df.empty:
        st.info(f"No Digester records were found for Press {press_no} in the NIR hour.")
    else:
        latest = press_df.iloc[-1]
        latest_dt = pd.to_datetime(latest.get("ts_local"), errors="coerce")
        digester_values = [
            ("Record time", latest_dt.strftime("%d %b %H:%M:%S") if pd.notna(latest_dt) else "--"),
            ("Digester level", _level_status(latest.get("digester_level"))),
            ("Digester temperature", _format_value(latest.get("digester_temp"), 1, " °C")),
            ("Digester amps", _format_value(latest.get("digester_amp"), 1, " A")),
        ]
        metric_cols = st.columns(4)
        for col, (label, value) in zip(metric_cols, digester_values):
            with col:
                st.metric(label, value)

        digester_detail = press_df[
            ["ts_local", "digester_level", "digester_temp", "digester_amp"]
        ].copy().rename(
            columns={
                "ts_local": "Record Time",
                "digester_level": "Digester Level",
                "digester_temp": "Digester Temperature (°C)",
                "digester_amp": "Digester Amps (A)",
            }
        )
        digester_detail["Record Time"] = pd.to_datetime(
            digester_detail["Record Time"], errors="coerce"
        ).dt.strftime("%d %b %Y %H:%M:%S")
        st.dataframe(digester_detail, use_container_width=True, hide_index=True)



def render_point_recommendation(
    press,
    selected,
    clicked_row,
    findings,
    high_limit,
    enable_alert,
):
    """Render the recommendation directly inside the selected press card."""
    selected_value = selected["value"]
    selected_dt = selected["datetime"]

    # NIR alert uses one fixed limit only.
    nir_status = "HIGH" if selected_value > high_limit else "NORMAL"

    st.markdown(
        f"""
        <div class="point-box">
            <div class="point-box-header">
                <span>📊 Sample Analysis</span>
                <span>{selected_dt.strftime("%d %b %Y  %H:%M")}</span>
            </div>
            <div class="point-value">
                NIR OIL LOSS: <b>{selected_value:.2f}%</b>
            </div>
        """,
        unsafe_allow_html=True,
    )

    if findings:
        # Show the most important alert(s) directly in the box.
        for finding in findings:
            actual = finding["Actual Value"]
            actual_text = (
                f"{float(actual):.2f}"
                if value_is_number(actual)
                else str(actual)
            )

            parameter = finding["Parameter"]
            condition = finding["Alert Condition"]

            if condition.startswith(">"):
                message = f"{parameter} is too high"
            elif condition.startswith("<"):
                message = f"{parameter} is too low"
            elif condition == "LOW":
                message = f"{parameter} is too low"
            else:
                message = f"{parameter} is outside the alert range"

            st.markdown(
                f"""
                <div class="point-alert">
                    <div class="point-alert-title">
                        ⚠ ALERT: {message}
                    </div>
                    <div class="point-alert-detail">
                        Actual: <b>{actual_text}</b>
                        &nbsp; | &nbsp;
                        Limit: <b>{condition}</b>
                    </div>
                    <div class="point-alert-recommendation">
                        Recommendation: {finding["Recommendation"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif nir_status == "HIGH":
        st.markdown(
            f"""
            <div class="point-alert">
                <div class="point-alert-title">
                    ⚠ ALERT: NIR oil loss is high
                </div>
                <div class="point-alert-detail">
                    NIR: <b>{selected_value:.2f}%</b>
                    &nbsp; | &nbsp;
                    High limit: <b>{high_limit:.2f}%</b>
                </div>
                <div class="point-alert-recommendation">
                    Recommendation: Review the associated process readings.
                    No configured Sterilizer or Press parameter alert
                    was triggered for this sample.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="point-good">
                <div class="point-good-title">
                    ✓ All running good
                </div>
                <div class="point-good-detail">
                    No configured alert was triggered for this sample.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PAGE 1
# ============================================================
if page == "Lab Oil Loss – NIR Data Trend":

    st.markdown(
        """
        <div class="main-header">
            <div class="main-header-title">
                Lab Oil Loss Data Report
            </div>
            <div class="main-header-sub">
                NIR trend analysis with Sterilizer and Press alert analysis
                for Press 1–8
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-heading">NIR Data Source</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Live NIR data source: mypalmcom_smartperakmotor → nir_pressedfiber. "
        "Press number is extracted from sample_id after 'press'."
    )

    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------
    st.markdown(
        '<div class="section-heading">Monitoring Period</div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns([1, 1, 2])

    with f1:
        start_date = st.date_input(
            "From Date",
            value=date(2026, 9, 21),
            key="nir_start_date",
        )

    with f2:
        end_date = st.date_input(
            "To Date",
            value=date(2026, 9, 25),
            key="nir_end_date",
        )

    with f3:
        st.markdown("**Selected period**")
        st.markdown(
            f"""
            <div class="small-note">
                {start_date.strftime("%d %b %Y")}
                → {end_date.strftime("%d %b %Y")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    if start_date > end_date:
        st.error("From Date cannot be later than To Date.")
        st.stop()

    try:
        nir, source_flat = load_nir_pressedfiber_db(start_date, end_date)
    except Exception as e:
        st.error(f"Unable to read NIR data from nir_pressedfiber: {e}")
        st.stop()

    # The old Excel version used a dataframe named `filtered` after applying
    # the selected date range. The DB loader already applies the From/To date
    # filter in SQL, so use the returned DB dataframe as `filtered` for the
    # existing NIR trend code below.
    filtered = nir.copy()

    if nir.empty:
        st.warning(
            f"No NIR data found in nir_pressedfiber for "
            f"{start_date.strftime("%d %b %Y")} to {end_date.strftime("%d %b %Y")}."
        )
        st.stop()


    # ALERT SETTINGS
    # --------------------------------------------------------
    st.markdown(
        '<div class="section-heading">Alert Settings</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        a1, a2, a3 = st.columns([1, 1, 3])

        enable_alert = True
        high_limit = 4.7

        with a1:
            st.metric("NIR High Setpoint", "4.70%")

        with a2:
            st.metric("Low Limit", "Not used")

        with a3:
            st.caption(
                "The 4.70% high-loss alert is always active. Select any NIR point above 4.70% "
                "to open the full process check using the NIR timestamp: Press/Digester = same clock hour; "
                "Sterilizer = immediately preceding clock hour."
            )

    # --------------------------------------------------------
    # PRESS STATUS
    # --------------------------------------------------------
    press_info = {}

    for press in PRESS_COLS:
        # The report can contain duplicate NIR rows for the same press,
        # timestamp and value. Count each actual NIR sample only once.
        # Example: Press 1 on 23–24 Sep has 13 raw rows but only 7
        # unique timestamp/value samples, which is what the chart shows.
        press_samples = filtered[["DateTime", press, "_SourceRow"]].dropna(
            subset=[press]
        ).copy()
        press_samples = (
            press_samples
            .drop_duplicates(subset=["DateTime", press], keep="first")
            .sort_values("DateTime")
        )
        values = press_samples[press]

        if values.empty:
            press_info[press] = {
                "latest": None,
                "average": None,
                "maximum": None,
                "samples": 0,
                "status": "NO DATA",
            }
        else:
            latest = float(values.iloc[-1])

            if latest > high_limit:
                status = "HIGH"
            else:
                status = "NORMAL"

            press_info[press] = {
                "latest": latest,
                "average": float(values.mean()),
                "maximum": float(values.max()),
                "samples": int(values.count()),
                "status": status,
            }

    # --------------------------------------------------------
    # NIR HIGH-LOSS ALERT SUMMARY
    # --------------------------------------------------------
    # The 4.70% limit is always active. The alert is based on the actual
    # NIR samples in the selected date range, not only the latest sample.
    high_sample_frames = []
    for press in PRESS_COLS:
        h = (
            filtered[["DateTime", press]]
            .dropna(subset=[press])
            .drop_duplicates(subset=["DateTime", press], keep="first")
            .copy()
        )
        h = h[h[press] > high_limit]
        if not h.empty:
            h["Press"] = press
            h["NIR Oil Loss (%)"] = pd.to_numeric(h[press], errors="coerce")
            high_sample_frames.append(h[["DateTime", "Press", "NIR Oil Loss (%)"]])

    high_samples = (
        pd.concat(high_sample_frames, ignore_index=True).sort_values("DateTime")
        if high_sample_frames else pd.DataFrame(columns=["DateTime", "Press", "NIR Oil Loss (%)"])
    )
    high_count = len(high_samples)
    affected_presses = sorted(high_samples["Press"].unique().tolist()) if high_count else []
    latest_high = high_samples.iloc[-1] if high_count else None

    if high_count:
        affected_text = ", ".join(affected_presses)
        latest_text = (
            f"Latest high sample: <b>{latest_high['Press']}</b> · "
            f"<b>{float(latest_high['NIR Oil Loss (%)']):.2f}%</b> · "
            f"{pd.Timestamp(latest_high['DateTime']).strftime('%d %b %Y %H:%M:%S')}"
        )
        st.markdown(
            f"""<div class=\"alert-panel\">
                <div class=\"alert-title\">⚠ NIR HIGH OIL LOSS ALERT</div>
                <div class=\"alert-text\">
                    NIR samples above the fixed <b>4.70%</b> setpoint: <b>{high_count}</b>
                    &nbsp; | &nbsp; Affected: <b>{affected_text}</b>
                </div>
                <div class=\"alert-text\" style=\"margin-top:6px;\">{latest_text}</div>
                <div class=\"point-alert-recommendation\" style=\"margin-top:8px;\">
                    Select any NIR point above 4.70% to open the full High NIR Process Check.
                    Process timing: Press/Digester = NIR clock hour; Sterilizer = immediately preceding clock hour.
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
        with st.expander("View High NIR Samples", expanded=False):
            high_display = high_samples.copy()
            high_display["DateTime"] = pd.to_datetime(high_display["DateTime"]).dt.strftime("%d %b %Y %H:%M:%S")
            st.dataframe(high_display, use_container_width=True, hide_index=True)
    else:
        st.markdown(
            """<div class=\"point-good\">
                <div class=\"point-good-title\">✓ NIR Within Setpoint</div>
                <div class=\"point-good-detail\">
                    No NIR sample is above the fixed 4.70% high-loss setpoint in the selected period.
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------
    all_values = filtered[PRESS_COLS].stack().dropna()

    latest_value = (
        float(all_values.iloc[-1])
        if len(all_values)
        else None
    )

    avg_value = (
        float(all_values.mean())
        if len(all_values)
        else None
    )

    max_value = (
        float(all_values.max())
        if len(all_values)
        else None
    )

    k1, k2, k3, k4 = st.columns(4)

    kpi_data = [
        (
            "Latest NIR Oil Loss",
            f"{latest_value:.2f}%"
            if latest_value is not None
            else "--",
        ),
        (
            "Average Oil Loss",
            f"{avg_value:.2f}%"
            if avg_value is not None
            else "--",
        ),
        (
            "Maximum Oil Loss",
            f"{max_value:.2f}%"
            if max_value is not None
            else "--",
        ),
        (
            "NIR Samples",
            str(int(len(all_values))),
        ),
    ]

    for col, (label, value) in zip(
        [k1, k2, k3, k4],
        kpi_data,
    ):
        with col:
            st.markdown(
                f"""
                <div class="kpi">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # EIGHT BLACK NIR GRAPHS
    # --------------------------------------------------------
    st.markdown(
        '<div class="section-heading">Individual Press NIR Trends</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Select a point to show its NIR value and the Sterilizer/Press alert "
        "recommendation directly inside the same Press card."
    )

    for row_start in range(0, 8, 2):

        left_press = PRESS_COLS[row_start]
        right_press = PRESS_COLS[row_start + 1]

        left_col, right_col = st.columns(2)

        for col, press in [
            (left_col, left_press),
            (right_col, right_press),
        ]:
            with col:
                info = press_info[press]

                with st.container(border=True):

                    h1, h2 = st.columns([3, 1])

                    with h1:
                        st.markdown(
                            f"### 🔹 {press}"
                        )

                    with h2:
                        if info["samples"] == 0:
                            st.warning("NO DATA")
                        elif info["status"] == "HIGH":
                            st.error("⚠ HIGH")
                        else:
                            st.success("✓ NORMAL")

                    m1, m2, m3, m4 = st.columns(4)

                    with m1:
                        st.caption("Latest")
                        st.markdown(
                            f"**{info['latest']:.2f}%**"
                            if info["latest"] is not None
                            else "**--**"
                        )

                    with m2:
                        st.caption("Average")
                        st.markdown(
                            f"**{info['average']:.2f}%**"
                            if info["average"] is not None
                            else "**--**"
                        )

                    with m3:
                        st.caption("Maximum")
                        st.markdown(
                            f"**{info['maximum']:.2f}%**"
                            if info["maximum"] is not None
                            else "**--**"
                        )

                    with m4:
                        st.caption("Samples")
                        st.markdown(
                            f"**{info['samples']}**"
                        )

                    # Use the same unique samples for the chart as for the
                    # Samples KPI. This prevents duplicate report rows from
                    # being counted or plotted twice.
                    plot_df = (
                        filtered[["DateTime", press, "_SourceRow"]]
                        .dropna(subset=[press])
                        .drop_duplicates(
                            subset=["DateTime", press],
                            keep="first",
                        )
                        .sort_values("DateTime")
                        .copy()
                    )

                    fig = go.Figure()

                    if not plot_df.empty:
                        customdata = []

                        for _, r in plot_df.iterrows():
                            customdata.append(
                                [
                                    press,
                                    int(r["_SourceRow"]),
                                    float(r[press]),
                                    pd.Timestamp(r["DateTime"]).strftime(
                                        "%d %b %Y %H:%M"
                                    ),
                                ]
                            )

                        fig.add_trace(
                            go.Scatter(
                                x=plot_df["DateTime"],
                                y=plot_df[press],
                                mode="lines+markers",
                                name=press,
                                line=dict(
                                    color="#38bdf8",
                                    width=2.5,
                                ),
                                marker=dict(
                                    color="#e5e7eb",
                                    size=6,
                                    line=dict(
                                        color="#38bdf8",
                                        width=1,
                                    ),
                                ),
                                customdata=customdata,
                                hovertemplate=(
                                    "<b>%{customdata[0]}</b><br>"
                                    "%{customdata[3]}<br>"
                                    "NIR Oil Loss: "
                                    "%{customdata[2]:.2f}%"
                                    "<br><br>"
                                    "<b></b>"
                                    "<extra></extra>"
                                ),
                            )
                        )

                    # Fixed NIR reference line: always visible on every Press graph.
                    fig.add_hline(
                        y=4.7,
                        line_dash="dash",
                        line_color="#ef4444",
                        line_width=1.5,
                        annotation_text="NIR LIMIT 4.7%",
                        annotation_font_color="#f87171",
                        annotation_position="top right",
                    )


                    fig.update_layout(
                        height=360,
                        margin=dict(
                            l=55,
                            r=20,
                            t=18,
                            b=50,
                        ),
                        paper_bgcolor="#05070a",
                        plot_bgcolor="#05070a",
                        font=dict(
                            color="#d1d5db",
                            size=11,
                        ),
                        xaxis=dict(
                            title="Date / Time",
                            color="#9ca3af",
                            gridcolor="#202631",
                            zerolinecolor="#202631",
                            linecolor="#343b48",
                        ),
                        yaxis=dict(
                            title="NIR Oil Loss (%)",
                            color="#9ca3af",
                            gridcolor="#202631",
                            zerolinecolor="#202631",
                            linecolor="#343b48",
                        ),
                        hovermode="closest",
                        showlegend=False,
                    )

                    event = st.plotly_chart(
                        fig,
                        use_container_width=True,
                        key=f"nir_chart_{press}",
                        on_select="rerun",
                        selection_mode=("points",),
                    )

                    # Streamlit Plotly selection payload.
                    if event and hasattr(event, "selection"):
                        points = event.selection.get("points", [])

                        if points:
                            point = points[0]
                            cd = point.get("customdata")

                            if cd:
                                selected_point = {
                                    "press": str(cd[0]),
                                    "source_row": int(cd[1]),
                                    "value": float(cd[2]),
                                    "datetime": pd.to_datetime(cd[3]),
                                }
                                st.session_state.selected_nir_point = selected_point

                                # High-NIR points open the detailed process check
                                # on a separate full-width page so the process
                                # tables and Sterilizer cycle data are readable.
                                if float(selected_point["value"]) > 4.7:
                                    st.session_state.pmc_page = "High NIR Process Check"
                                    st.rerun()

                    # ------------------------------------------------
                    # POINT RECOMMENDATION INSIDE THIS PRESS CARD
                    # ------------------------------------------------
                    selected = st.session_state.get("selected_nir_point")

                    if selected and selected["press"] == press:
                        source_row = selected["source_row"]

                        matching_rows = source_flat[
                            source_flat.index == source_row
                        ]

                        if not matching_rows.empty:
                            clicked_row = matching_rows.iloc[0]
                            findings = analyze_associated_row(
                                clicked_row,
                                press,
                            )
                        else:
                            clicked_row = pd.Series(dtype=object)
                            findings = []

                        render_point_recommendation(
                            press=press,
                            selected=selected,
                            clicked_row=clicked_row,
                            findings=findings,
                            high_limit=high_limit,
                            enable_alert=enable_alert,
                        )

                    else:
                        # Keep the recommendation area permanently inside
                        # every Press card. It must never look like a separate
                        # investigation page/section.
                        st.markdown(
                            """
                            <div class="point-box point-box-empty">
                                <div class="point-box-header">
                                    <span>📊 Sample Analysis</span>
                                    <span>Press point status</span>
                                </div>
                                <div class="point-good-detail">
                                    Select a data point to display the exact NIR value
                                    and Sterilizer/Press alert recommendation here.
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------
    st.markdown(
        '<div class="section-heading">Press-wise Summary</div>',
        unsafe_allow_html=True,
    )

    rows = []

    for press in PRESS_COLS:
        info = press_info[press]

        rows.append(
            {
                "Press": press,
                "Latest (%)": (
                    round(info["latest"], 2)
                    if info["latest"] is not None
                    else None
                ),
                "Average (%)": (
                    round(info["average"], 2)
                    if info["average"] is not None
                    else None
                ),
                "Maximum (%)": (
                    round(info["maximum"], 2)
                    if info["maximum"] is not None
                    else None
                ),
                "Samples": info["samples"],
                "Status": info["status"],
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # RAW NIR DATA
    # --------------------------------------------------------
    with st.expander("View NIR Sample Data"):
        display_cols = [
            "sample_id",
            "Date",
            "Sampling Time",
            "val2",
            "press_no",
        ] + PRESS_COLS

        display_df = filtered[
            [c for c in display_cols if c in filtered.columns]
        ].copy()

        if "Date" in display_df.columns:
            display_df["Date"] = display_df["Date"].dt.strftime(
                "%d-%m-%Y"
            )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# DEDICATED HIGH NIR PROCESS CHECK
# ============================================================
elif page in {"High NIR Process Check", "Process Confirmation"}:
    selected = st.session_state.get("selected_nir_point")

    st.markdown(
        '<div class="main-header">'
        '<div class="main-header-title">High NIR Process Check</div>'
        '<div class="main-header-sub">Selected NIR sample → Press & Digester → Sterilizer previous-hour cycle data</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not selected:
        st.info("Select an NIR data point above 4.7% from the NIR Trend page.")
        if st.button("← Back to NIR Trend", key="back_high_nir_empty"):
            st.session_state.pmc_page = "Lab Oil Loss – NIR Data Trend"
            st.rerun()
    else:
        selected_value = float(selected.get("value", 0))
        if selected_value <= 4.7:
            st.info(f"Selected NIR value is {selected_value:.2f}%, so the high-NIR process check is only shown for values above 4.70%.")
            if st.button("← Back to NIR Trend", key="back_high_nir_normal"):
                st.session_state.pmc_page = "Lab Oil Loss – NIR Data Trend"
                st.rerun()
        else:
            press_name = str(selected.get("press", "Press 1"))
            sample_dt = pd.to_datetime(selected.get("datetime"), errors="coerce")

            b1, b2, b3 = st.columns([1, 1, 4])
            with b1:
                if st.button("← Back to NIR Trend", key="back_high_nir"):
                    st.session_state.pmc_page = "Lab Oil Loss – NIR Data Trend"
                    st.rerun()
            with b2:
                st.metric("NIR Oil Loss", f"{selected_value:.2f}%")
            with b3:
                st.markdown(
                    f"**{press_name}** · Sample time: **{sample_dt.strftime('%d %b %Y %H:%M:%S') if pd.notna(sample_dt) else '--'}** · "
                    "High limit: **4.70%**",
                )

            # Render the same complete process data at full page width.
            render_high_nir_inline_process_confirmation(
                selected=selected,
                press_name=press_name,
                high_limit=4.7,
            )


# ============================================================
# ============================================================
# PAGE 2 – OVERALL GRADING REPORT
# ============================================================
elif page == "Overall Grading":

    @st.fragment(run_every="1200s")
    def render_overall_grading_page():
        st.markdown(
            '<div class="main-header">'
            '<div class="main-header-title">Overall Grading Report</div>'
            '<div class="main-header-sub">Daily average fruit grading from grading_average_data</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        # Date range requested for the daily average grading report.
        f1, f2, f3 = st.columns([1, 1, 2])
        with f1:
            grading_start = st.date_input(
                "From Date",
                value=date(2026, 9, 21),
                key="grading_start_date",
            )
        with f2:
            grading_end = st.date_input(
                "To Date",
                value=date(2026, 9, 25),
                key="grading_end_date",
            )
        with f3:
            if st.button("↻ Refresh Now", key="grading_refresh", use_container_width=True):
                load_grading_average_data.clear()
                st.rerun()
            st.caption(
                f"Selected period: {grading_start.strftime('%d %b %Y')} → "
                f"{grading_end.strftime('%d %b %Y')} • Auto-refresh: 20 minutes"
            )

        if grading_start > grading_end:
            st.warning("From Date must be on or before To Date.")
            return

        try:
            grading = load_grading_average_data(grading_start, grading_end)
        except Exception as exc:
            st.error(f"Overall grading database connection failed: {exc}")
            return

        if grading.empty:
            st.info(
                f"No grading data found in grading_average_data for "
                f"{grading_start.strftime('%d %b %Y')} to {grading_end.strftime('%d %b %Y')}."
            )
            return

        categories = [
            ("Underripe", "underripe_pct"),
            ("Ripe", "ripe_pct"),
            ("Overripe", "overripe_pct"),
            ("Hard", "hard_pct"),
            ("Empty", "empty_pct"),
            ("Longstalk", "longstalk_pct"),
            ("Unripe", "unripe_pct"),
        ]

        latest = grading.iloc[-1]

        st.markdown(
            '<div class="section-heading">Latest Daily Average</div>',
            unsafe_allow_html=True,
        )
        card_cols = st.columns(7)
        for col, (label, field) in zip(card_cols, categories):
            value = pd.to_numeric(latest[field], errors="coerce")
            value_text = f"{float(value):.2f}%" if pd.notna(value) else "--"
            with col:
                st.markdown(
                    f'<div class="kpi">'
                    f'<div class="kpi-label">{label}</div>'
                    f'<div class="kpi-value">{value_text}</div>'
                    f'<div class="small-note">{pd.Timestamp(latest["date"]).strftime("%d %b %Y")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        # Daily average table.
        st.markdown(
            '<div class="section-heading">Daily Average Grading</div>',
            unsafe_allow_html=True,
        )
        display = grading.copy()
        display["date"] = display["date"].dt.strftime("%d-%m-%Y")
        display.columns = [
            "Date",
            "Underripe (%)",
            "Ripe (%)",
            "Overripe (%)",
            "Hard (%)",
            "Empty (%)",
            "Longstalk (%)",
            "Unripe (%)",
        ]
        st.dataframe(
            display.round(2),
            use_container_width=True,
            hide_index=True,
        )

        # Stacked distribution chart.
        st.markdown(
            '<div class="section-heading">Daily Grading Distribution</div>',
            unsafe_allow_html=True,
        )
        fig = go.Figure()
        for label, field in categories:
            fig.add_trace(
                go.Bar(
                    x=grading["date"],
                    y=grading[field],
                    name=label,
                    hovertemplate=(
                        f"{label}: %{{y:.2f}}%<br>"
                        "%{x|%d %b %Y}<extra></extra>"
                    ),
                )
            )
        fig.update_layout(
            barmode="stack",
            height=430,
            margin=dict(l=55, r=25, t=45, b=55),
            paper_bgcolor="#0b151d",
            plot_bgcolor="#0b151d",
            font=dict(color="#dbe5ec"),
            xaxis=dict(title="Date", type="date", gridcolor="#293a46"),
            yaxis=dict(title="Percentage (%)", gridcolor="#293a46", zeroline=False),
            legend=dict(orientation="h", y=1.08, x=0),
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displaylogo": False},
        )

        # Individual category trends.
        st.markdown(
            '<div class="section-heading">Grading Category Trends</div>',
            unsafe_allow_html=True,
        )
        trend_fig = go.Figure()
        for label, field in categories:
            trend_fig.add_trace(
                go.Scatter(
                    x=grading["date"],
                    y=grading[field],
                    mode="lines+markers",
                    name=label,
                    hovertemplate=(
                        f"{label}: %{{y:.2f}}%<br>"
                        "%{x|%d %b %Y}<extra></extra>"
                    ),
                )
            )
        trend_fig.update_layout(
            height=430,
            margin=dict(l=55, r=25, t=45, b=55),
            paper_bgcolor="#0b151d",
            plot_bgcolor="#0b151d",
            font=dict(color="#dbe5ec"),
            hovermode="x unified",
            xaxis=dict(title="Date", type="date", gridcolor="#293a46"),
            yaxis=dict(title="Percentage (%)", gridcolor="#293a46", zeroline=False),
            legend=dict(orientation="h", y=1.08, x=0),
        )
        st.plotly_chart(
            trend_fig,
            use_container_width=True,
            config={"displaylogo": False},
        )

        with st.expander("View Overall Grading DB Data"):
            st.dataframe(grading, use_container_width=True, hide_index=True)

    render_overall_grading_page()
# PAGE 3 – STERILIZER MONITORING
# ============================================================
elif page == "Sterilizer Running Hours":

    @st.fragment(run_every="1200s")
    def render_sterilizer_page():
        st.markdown(
            '<div class="main-header"><div class="main-header-title">Sterilizer Monitoring</div>'
            '<div class="main-header-sub">Live cooking-step pressure direction and running hours</div></div>',
            unsafe_allow_html=True,
        )

        f1, f2 = st.columns([1, 1])
        with f1:
            s_date = st.date_input("Monitoring date", value=date.today(), key="ster_start")
        with f2:
            e_date = st.date_input("End date", value=date.today(), key="ster_end")

        start_dt = datetime.combine(s_date, datetime.min.time())
        end_dt = datetime.combine(e_date, datetime.max.time())

        refresh_col, info_col = st.columns([1, 4])
        with refresh_col:
            if st.button("↻ Refresh Now", key="sterilizer_refresh", use_container_width=True):
                load_sterilizer_db.clear()
                load_sterilizer_running_history.clear()
                load_sterilizer_performance_window.clear()
                load_running_hours_db.clear()
                st.rerun()
        with info_col:
            st.caption("Auto-refresh: every 20 minutes • Use Refresh Now for immediate latest data")

        try:
            ster = load_sterilizer_db(start_dt, end_dt)
            run_hours = load_running_hours_db()
            run_hist = load_sterilizer_running_history(start_dt, end_dt)
            # The performance table contains the actual cycle-level P1/P2/P3/BPV
            # values. Include the previous day because a cycle feeding the selected
            # day's process can have been completed during the preceding hour.
            perf_start = start_dt - timedelta(days=1)
            ster_perf = load_sterilizer_performance_window(perf_start, end_dt)
        except Exception as exc:
            st.error(f"Sterilizer database connection failed: {exc}")
            ster, run_hours, run_hist, ster_perf = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        STEP_GUIDANCE = {
            1: ("Steps 1–2", "RAISE", 25.0),
            2: ("Steps 1–2", "RAISE", 25.0),
            3: ("Steps 3–4", "DROP", 15.0),
            4: ("Steps 3–4", "DROP", 15.0),
            5: ("Step 5", "RAISE", 35.0),
            6: ("Steps 6–7", "DROP", 25.0),
            7: ("Steps 6–7", "DROP", 25.0),
            8: ("Step 8", "RAISE", 40.0),
            9: ("Step 9", "MAINTAIN", 40.0),
            10: ("Steps 10–11", "DONE", None),
            11: ("Steps 10–11", "DONE", None),
        }

        def parse_step(value):
            if pd.isna(value):
                return None
            m = re.search(r"\d+", str(value))
            return int(m.group()) if m else None

        def pressure_analysis(df_no, row):
            step = parse_step(row.get("last_step"))
            group, action, target = STEP_GUIDANCE.get(step, ("Unknown step", "CHECK", None))
            current = pd.to_numeric(row.get("pressure"), errors="coerce")
            if pd.isna(current):
                return action, target, "NO DATA", "Pressure data unavailable."

            recent = pd.to_numeric(df_no["pressure"], errors="coerce").dropna().tail(5)
            slope = 0.0
            if len(recent) >= 2:
                slope = float(recent.iloc[-1] - recent.iloc[0]) / max(len(recent) - 1, 1)

            if action == "RAISE":
                if target is not None and current > target + 1.0:
                    return action, target, "ALERT", f"Pressure is above the {target:.0f} PSI target."
                if target is not None and current < target - 1.0 and slope <= 0:
                    return action, target, "ALERT", f"Pressure is not raising toward {target:.0f} PSI."
                return action, target, "OK", f"Pressure is raising toward {target:.0f} PSI."

            if action == "DROP":
                if target is not None and current < target - 1.0:
                    return action, target, "ALERT", f"Pressure has gone below the {target:.0f} PSI target."
                if target is not None and current > target + 1.0 and slope >= 0:
                    return action, target, "ALERT", f"Pressure is not dropping toward {target:.0f} PSI."
                return action, target, "OK", f"Pressure is dropping toward {target:.0f} PSI."

            if action == "MAINTAIN":
                if target is not None and abs(float(current) - target) > 2.0:
                    return action, target, "ALERT", f"Pressure is away from the {target:.0f} PSI holding target."
                return action, target, "OK", f"Pressure is maintaining around {target:.0f} PSI."

            if action == "DONE":
                return action, target, "OK", "Cooking over — Done."

            return action, target, "OK", "No pressure movement rule is configured for this step."

        def running_total(no):
            if run_hours.empty:
                return None
            text_no = rf"(?:steril(?:izer|iser)|st)[ _-]*0*{no}\b"
            mask = (
                run_hours["station_name"].astype(str).str.contains(text_no, case=False, regex=True, na=False)
                | run_hours["parts_name"].astype(str).str.contains(text_no, case=False, regex=True, na=False)
            )
            matches = run_hours.loc[mask]
            if matches.empty:
                base = run_hours[
                    run_hours["station_name"].astype(str).str.contains("steril", case=False, na=False)
                    | run_hours["parts_name"].astype(str).str.contains("steril", case=False, na=False)
                ]
                matches = base[base.apply(lambda r: str(no) in f"{r.get('station_name','')} {r.get('parts_name','')}", axis=1)]
            if matches.empty or matches["machine_running_hours"].dropna().empty:
                return None
            return float(matches["machine_running_hours"].max())

        if ster.empty:
            st.info("No sterilizer data found for the selected period.")
            return

        numbers = [1, 2, 3, 4, 5]
        latest_all = ster.sort_values("insdt").groupby("sterilizer_no", dropna=True).tail(1).copy()
        latest_all["sterilizer_no"] = pd.to_numeric(latest_all["sterilizer_no"], errors="coerce")
        latest_all = latest_all[latest_all["sterilizer_no"].isin(numbers)]

        card_rows = [[1, 2, 3], [4, 5]]
        for row_numbers in card_rows:
            cols = st.columns(len(row_numbers))
            for idx, no in enumerate(row_numbers):
                with cols[idx]:
                    df_no = ster[pd.to_numeric(ster["sterilizer_no"], errors="coerce") == no].sort_values("insdt")
                    rr = latest_all[latest_all["sterilizer_no"] == no]
                    r = rr.iloc[-1] if not rr.empty else None
                    if r is None or df_no.empty:
                        st.markdown(
                            f'<div class="ster-card"><div class="ster-card-top"><div class="ster-name">STERILIZER NO. {no}</div>'
                            '<div class="ster-cycle ster-idle">No Data</div></div></div>',
                            unsafe_allow_html=True,
                        )
                        continue

                    cooking = str(r.get("cooking_status", "--")).strip().lower()
                    if cooking in {"cooking", "running", "active", "1", "true", "on"}:
                        cycle_text, cycle_class = "Cooking", "ster-cooking"
                    elif cooking in {"done", "complete", "completed", "finished"}:
                        cycle_text, cycle_class = "Done", "ster-done"
                    else:
                        cycle_text, cycle_class = "Not Cooking", "ster-idle"

                    auto = str(r.get("auto_manual", "--")).strip().upper()
                    pressure = pd.to_numeric(r.get("pressure"), errors="coerce")
                    temperature = pd.to_numeric(r.get("temperature"), errors="coerce")
                    step = parse_step(r.get("last_step"))
                    group, action, target = STEP_GUIDANCE.get(step, ("Step --", "CHECK", None))
                    _, target_value, alert_kind, alert_text = pressure_analysis(df_no, r)
                    total = running_total(no)
                    day_hours = calculate_daily_running_hours(run_hist, no, s_date)

                    # Actual cycle-level performance values from sterilizer_performance.
                    # Keep only Sterilizers 1-5 and use the latest performance record
                    # available up to the selected end time for this card.
                    perf_no = pd.DataFrame()
                    if not ster_perf.empty and "sterilizer" in ster_perf.columns:
                        perf_no = ster_perf[
                            pd.to_numeric(ster_perf["sterilizer"], errors="coerce") == no
                        ].copy()
                    if not perf_no.empty:
                        perf_time_col = "cycle_ref_time" if "cycle_ref_time" in perf_no.columns else "insdt"
                        perf_no["_perf_time"] = pd.to_datetime(perf_no[perf_time_col], errors="coerce")
                        perf_no = perf_no[perf_no["_perf_time"].notna()]
                        perf_no = perf_no[perf_no["_perf_time"] <= pd.Timestamp(end_dt)]
                        perf_row = perf_no.sort_values("_perf_time").iloc[-1] if not perf_no.empty else None
                    else:
                        perf_row = None

                    if perf_row is not None:
                        perf_cycle = pd.to_numeric(perf_row.get("cycle_no"), errors="coerce")
                        perf_p1 = pd.to_numeric(perf_row.get("p1"), errors="coerce")
                        perf_p2 = pd.to_numeric(perf_row.get("p2"), errors="coerce")
                        perf_p3 = pd.to_numeric(perf_row.get("p3"), errors="coerce")
                        perf_bpv = pd.to_numeric(perf_row.get("back_pressure_receiver"), errors="coerce")
                        perf_time = perf_row.get("_perf_time")
                        # Number of distinct cycles recorded on the selected monitoring day.
                        day_perf = perf_no[pd.to_datetime(perf_no["_perf_time"], errors="coerce").dt.date == s_date]
                        cycle_count_day = day_perf["cycle_no"].dropna().nunique() if not day_perf.empty else 0
                    else:
                        perf_cycle = perf_p1 = perf_p2 = perf_p3 = perf_bpv = float("nan")
                        perf_time = pd.NaT
                        cycle_count_day = 0

                    analysis_html = (
                        '<div class="ster-analysis ster-analysis-alert">' if alert_kind == "ALERT"
                        else '<div class="ster-analysis ster-analysis-good">'
                    )
                    analysis_html += f'<b>{"⚠" if alert_kind == "ALERT" else "✓"} {alert_text}</b>'
                    if pd.notna(pressure):
                        analysis_html += f'<span>Current: {pressure:.1f} PSI'
                        if target_value is not None:
                            analysis_html += f' &nbsp;|&nbsp; Target: {target_value:.0f} PSI'
                        analysis_html += '</span>'
                    analysis_html += '</div>'

                    updated = pd.to_datetime(r.get("insdt"), errors="coerce")
                    updated_text = updated.strftime("%d/%m/%Y %I:%M %p") if pd.notna(updated) else "--"
                    active_time = r.get("elapsed_time", "--")
                    if pd.notna(active_time) if not isinstance(active_time, str) else False:
                        try:
                            active_time = f"{float(active_time):.0f} min"
                        except Exception:
                            pass

                    header_status = '<span class="ster-alert">⚠ PRESSURE</span>' if alert_kind == "ALERT" else '<span class="ster-normal">● NORMAL</span>'
                    total_html = f'{total:.1f} h' if total is not None else '--'
                    extra_html = (
                        f'<span>Target: {target:.0f} PSI</span>' if target is not None else ''
                    ) + f'<span>Recipe: {r.get("recipe_no", "--")}</span><span>Queue: {r.get("queue_no", "--")}</span><span>Total: {total_html}</span><span>Day: {day_hours:.1f} h</span>'

                    # Cycle-level confirmation values from sterilizer_performance.
                    perf_cycle_text = _format_value(perf_cycle, 0)
                    perf_p1_text = _format_value(perf_p1, 2, " PSI")
                    perf_p2_text = _format_value(perf_p2, 2, " PSI")
                    perf_p3_text = _format_value(perf_p3, 2, " PSI")
                    perf_bpv_text = _format_value(perf_bpv, 2, " PSI")
                    perf_time_text = perf_time.strftime("%d/%m/%Y %H:%M") if pd.notna(perf_time) else "--"
                    perf_html = (
                        '<div class="ster-extra" style="margin-top:10px;">'
                        f'<span><b>CYCLE COUNT:</b> {perf_cycle_text}</span>'
                        f'<span><b>P1:</b> {perf_p1_text}</span>'
                        f'<span><b>P2:</b> {perf_p2_text}</span>'
                        f'<span><b>P3:</b> {perf_p3_text}</span>'
                        f'<span><b>BPV:</b> {perf_bpv_text}</span>'
                        f'<span><b>CYCLES TODAY:</b> {cycle_count_day}</span>'
                        f'<span><b>PERFORMANCE TIME:</b> {perf_time_text}</span>'
                        '</div>'
                    )

                    step_focus = (
                        f'<div class="ster-step-focus">'
                        f'<div><div class="ster-step-number">STEP {step if step is not None else "--"}</div>'
                        f'<div class="ster-step-guide">{group} • {alert_text}</div></div>'
                        f'<div class="ster-step-total">TOTAL: 11</div></div>'
                    )

                    st.markdown(
                        f'<div class="ster-card"><div class="ster-card-top">'
                        f'<div>{header_status}<span class="ster-name">STERILIZER NO. {no}</span></div>'
                        f'<div class="ster-cycle {cycle_class}">{cycle_text}</div></div>'
                        f'<div class="ster-updated">◷ Last Updated: {updated_text}</div><div class="ster-divider"></div>'
                        f'<div class="ster-grid">'
                        f'<div><div class="ster-label">MODE</div><div class="ster-value mode-value">{auto}</div></div>'
                        f'<div><div class="ster-label">ACTIVE COOKING TIME</div><div class="ster-value">{active_time}</div></div>'
                        f'<div><div class="ster-label">OPERATING PRESSURE</div><div class="ster-value">{pressure:.2f} PSI</div></div>'
                        f'<div><div class="ster-label">TEMPERATURE</div><div class="ster-value">{temperature:.2f} °C</div></div>'
                        f'</div>{step_focus}{analysis_html}'
                        f'<div class="ster-extra">{extra_html}</div>{perf_html}</div>',
                        unsafe_allow_html=True,
                    )

        # ============================================================
        # STERILIZER PERFORMANCE — SEPARATE P1 / P2 / P3 / BPV TRENDS
        # ============================================================
        st.markdown('<div class="section-heading">Sterilizer Pressure Trends</div>', unsafe_allow_html=True)
        st.caption(
            "P1, P2, P3 and BPV are shown as separate trends. "
            "Each trend includes all Sterilizer 6–10 records found in the "
            "sterilizer_performance table for the selected calendar dates. "
            "Duplicate cycle records are retained."
        )

        if ster_perf.empty:
            st.info(
                f"No sterilizer performance records were found in sterilizer_performance "
                f"for {s_date.strftime('%d %b %Y')} to {e_date.strftime('%d %b %Y')}."
            )
        else:
            perf_graph = ster_perf.copy()
            perf_graph["sterilizer"] = pd.to_numeric(perf_graph["sterilizer"], errors="coerce")
            perf_graph["cycle_no"] = pd.to_numeric(perf_graph["cycle_no"], errors="coerce")
            perf_graph = perf_graph[perf_graph["sterilizer"].isin([6, 7, 8, 9, 10])].copy()

            # IMPORTANT: filter by the actual table date, not cycle_ref_time.
            # A performance row is considered part of the selected date because
            # its `date` column belongs to that date.
            perf_graph["_record_date"] = pd.to_datetime(perf_graph["date"], errors="coerce").dt.date
            perf_graph = perf_graph[
                perf_graph["_record_date"].notna()
                & (perf_graph["_record_date"] >= s_date)
                & (perf_graph["_record_date"] <= e_date)
            ].copy()

            if perf_graph.empty:
                st.info(
                    f"No Sterilizer 6–10 performance rows match the selected dates "
                    f"{s_date.strftime('%d %b %Y')} to {e_date.strftime('%d %b %Y')}."
                )
            else:
                # Cycle selector is placed before the four pressure graphs.
                # Selecting a cycle changes the graphs to show that cycle across
                # Sterilizers 6–10. This makes it easy to inspect one complete
                # sterilizer cycle at a time.
                cycle_values = sorted(
                    pd.to_numeric(perf_graph["cycle_no"], errors="coerce")
                    .dropna()
                    .astype(int)
                    .unique()
                    .tolist()
                )
                cycle_values = [c for c in cycle_values if 1 <= c <= 30]
                if not cycle_values:
                    cycle_values = list(range(1, 31))

                stored_cycle = st.session_state.get("sterilizer_selected_cycle")
                default_index = cycle_values.index(int(stored_cycle)) if stored_cycle in cycle_values else 0
                selected_cycle = st.selectbox(
                    "Select Cycle",
                    cycle_values,
                    index=default_index,
                    key="sterilizer_cycle_dropdown",
                    help="Select a cycle to compare P1, P2, P3 and BPV across Sterilizers 6–10.",
                )
                st.session_state["sterilizer_selected_cycle"] = int(selected_cycle)
                st.session_state["sterilizer_selected_sterilizer"] = None

                selected_cycle_df = perf_graph[perf_graph["cycle_no"] == float(selected_cycle)].copy()

                pressure_series = [
                    ("P1", "p1"),
                    ("P2", "p2"),
                    ("P3", "p3"),
                    ("BPV", "back_pressure_receiver"),
                ]

                # One graph for each pressure parameter. The selected cycle is
                # shown across Sterilizers 6–10. Duplicate records are retained.
                selected_sterilizer = None

                marker_symbols = {
                    6: "circle",
                    7: "square",
                    8: "diamond",
                    9: "triangle-up",
                    10: "x",
                }

                for label, column in pressure_series:
                    st.markdown(
                        f"<div style=\"margin:18px 0 8px 0; font-size:20px; font-weight:700; color:#e8f0f5;\">"
                        f"{label} <span style=\"color:#718392; font-size:14px; font-weight:500;\">PRESSURE PROFILE · CYCLE 1–30</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    fig_cycle = go.Figure()
                    plotted_any = False

                    for ster_no in [6, 7, 8, 9, 10]:
                        g = selected_cycle_df[selected_cycle_df["sterilizer"] == ster_no].copy()
                        y = pd.to_numeric(g[column], errors="coerce")
                        valid = y.notna()
                        g = g.loc[valid].copy()
                        y = y.loc[valid]
                        if g.empty:
                            continue

                        g = g.assign(_value=y.values).sort_values(
                            ["record_time", "id"],
                            kind="stable",
                        )
                        # Keep every duplicate record. Multiple points for one
                        # sterilizer/cycle are displayed at the same X position.
                        fig_cycle.add_trace(
                            go.Scatter(
                                x=[f"Sterilizer {ster_no}"] * len(g),
                                y=g["_value"],
                                mode="markers",
                                name=f"Sterilizer {ster_no}",
                                marker=dict(
                                    symbol=marker_symbols[ster_no],
                                    size=11,
                                    line=dict(width=1),
                                ),
                                customdata=g[["sterilizer", "id", "cycle_no", "record_time", "date", "time"]].astype(str).values,
                                hovertemplate=(
                                    f"<b>Cycle {int(selected_cycle)} · Sterilizer {ster_no}</b><br>"
                                    f"{label}: %{{y:.2f}} PSI<br>"
                                    "Record ID: %{customdata[1]}<br>"
                                    "Record Time: %{customdata[3]}<extra></extra>"
                                ),
                                showlegend=False,
                            )
                        )
                        plotted_any = True

                    if not plotted_any:
                        st.info(f"No {label} values are available for Sterilizers 6–10 in the selected dates.")
                        continue

                    fig_cycle.update_layout(
                        height=405,
                        margin=dict(l=62, r=28, t=48, b=58),
                        paper_bgcolor="#071018",
                        plot_bgcolor="#0b151d",
                        font=dict(color="#dbe5ec", family="Arial"),
                        hovermode="closest",
                        hoverlabel=dict(
                            bgcolor="#111e28",
                            bordercolor="#415565",
                            font=dict(color="#eef5f8", size=13),
                        ),
                        legend=dict(
                            orientation="h",
                            y=1.10,
                            x=0,
                            bgcolor="rgba(0,0,0,0)",
                            font=dict(size=12),
                        ),
                        xaxis=dict(
                            title=dict(text="Sterilizer", font=dict(size=12)),
                            type="category",
                            categoryorder="array",
                            categoryarray=["Sterilizer 6", "Sterilizer 7", "Sterilizer 8", "Sterilizer 9", "Sterilizer 10"],
                            tickfont=dict(size=10),
                            gridcolor="#223541",
                            zeroline=False,
                            showline=True,
                            linecolor="#314654",
                            mirror=False,
                        ),
                        yaxis=dict(
                            title=dict(text=f"{label} Pressure (PSI)", font=dict(size=12)),
                            gridcolor="#223541",
                            zeroline=False,
                            showline=True,
                            linecolor="#314654",
                            tickfont=dict(size=10),
                        ),
                        shapes=[],
                    )
                    chart_event = st.plotly_chart(
                        fig_cycle,
                        use_container_width=True,
                        config={"displaylogo": False},
                        key=f"sterilizer_pressure_chart_{label}",
                        on_select="rerun",
                        selection_mode=("points",),
                    )

                    # Clicking any point selects its cycle. The selected cycle is
                    # then used below to show P1 + P2 + P3 + BPV together.
                    try:
                        selected_points = chart_event.selection.points if chart_event is not None else []
                    except Exception:
                        selected_points = []
                    if selected_points:
                        point = selected_points[0]
                        try:
                            custom = point.get("customdata") or []
                            clicked_cycle = int(float(custom[2])) if len(custom) > 2 else int(selected_cycle)
                            clicked_ster = int(float(custom[0])) if custom else None
                        except Exception:
                            clicked_cycle = int(selected_cycle)
                            clicked_ster = None
                        st.session_state["sterilizer_selected_cycle"] = clicked_cycle
                        if clicked_ster is not None:
                            st.session_state["sterilizer_selected_sterilizer"] = clicked_ster

                # When an operator clicks Cycle 1 (or any cycle), show ALL four
                # pressure values for that exact sterilizer/cycle. No deduplication
                # is performed; if multiple rows exist for the same cycle, every
                # matching row is displayed.
                selected_cycle = st.session_state.get("sterilizer_selected_cycle")
                selected_sterilizer = st.session_state.get("sterilizer_selected_sterilizer")
                if selected_sterilizer is not None and selected_sterilizer not in [6, 7, 8, 9, 10]:
                    selected_sterilizer = None
                    st.session_state["sterilizer_selected_sterilizer"] = None
                if selected_cycle is not None:
                    detail = perf_graph[perf_graph["cycle_no"] == float(selected_cycle)].copy()
                    if selected_sterilizer is not None:
                        detail_ster = detail[detail["sterilizer"] == float(selected_sterilizer)].copy()
                        if not detail_ster.empty:
                            detail = detail_ster

                    st.markdown(
                        f"### Selected Cycle {int(selected_cycle)}" +
                        (f" — Sterilizer {int(selected_sterilizer)}" if selected_sterilizer is not None else "" )
                    )
                    if detail.empty:
                        st.info(f"No performance record exists for Cycle {int(selected_cycle)} in the selected date range.")
                    else:
                        detail = detail.sort_values(["date", "record_time", "sterilizer", "id"], kind="stable")
                        for _, row in detail.iterrows():
                            st.markdown(
                                f"**Sterilizer {int(row['sterilizer'])} · Cycle {int(row['cycle_no'])}** "
                                f"| P1: **{_format_value(row['p1'], 2, ' PSI')}** "
                                f"| P2: **{_format_value(row['p2'], 2, ' PSI')}** "
                                f"| P3: **{_format_value(row['p3'], 2, ' PSI')}** "
                                f"| BPV: **{_format_value(row['back_pressure_receiver'], 2, ' PSI')}** "
                                f"| Record ID: **{row['id']}**"
                            )

                # Complete underlying performance data — no cycle deduplication.
                st.markdown("### Sterilizer Performance Records")
                table_df = perf_graph.copy().sort_values(
                    ["date", "record_time", "sterilizer", "cycle_no", "id"],
                    kind="stable",
                )
                display_cols = [
                    "id", "date", "time", "sterilizer", "status", "cycle_no",
                    "p1", "p2", "p3", "back_pressure_receiver",
                    "cooking_start_time", "cooking_stop_time",
                    "door_shut_time", "door_open_time", "insdt"
                ]
                display_cols = [c for c in display_cols if c in table_df.columns]
                display_df = table_df[display_cols].copy()
                display_df = display_df.rename(columns={
                    "id": "ID",
                    "date": "Date",
                    "time": "Time",
                    "sterilizer": "Sterilizer",
                    "status": "Status",
                    "cycle_no": "Cycle",
                    "p1": "P1 (PSI)",
                    "p2": "P2 (PSI)",
                    "p3": "P3 (PSI)",
                    "back_pressure_receiver": "BPV (PSI)",
                    "cooking_start_time": "Cooking Start",
                    "cooking_stop_time": "Cooking Stop",
                    "door_shut_time": "Door Shut",
                    "door_open_time": "Door Open",
                    "insdt": "Inserted At",
                })
                for c in ["Date", "Cooking Start", "Cooking Stop", "Door Shut", "Door Open", "Inserted At"]:
                    if c in display_df.columns:
                        display_df[c] = pd.to_datetime(display_df[c], errors="coerce").dt.strftime("%d %b %Y %H:%M:%S")
                for c in ["P1 (PSI)", "P2 (PSI)", "P3 (PSI)", "BPV (PSI)"]:
                    if c in display_df.columns:
                        display_df[c] = pd.to_numeric(display_df[c], errors="coerce").round(2)
                st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown('<div class="section-heading">Valve Status</div>', unsafe_allow_html=True)
        header = '<div class="valve-grid"><div class="valve-head">STERILIZER</div>' + ''.join(f'<div class="valve-head center">{n}</div>' for n in numbers) + '</div>'
        rows_html = ''
        def valve_state(v):
            ss = str(v).strip().lower()
            return "open" if ss in {"1", "true", "open", "on", "opened", "100", "100.0"} else "close"
        for label, col in [("Condensate", "condense_cmd"), ("Inlet Valve", "inlet_cmd"), ("Exhaust Valve", "exhaust_cmd")]:
            cells = []
            for no in numbers:
                rr = latest_all[latest_all["sterilizer_no"] == no]
                r = rr.iloc[-1] if not rr.empty else None
                state = valve_state(r.get(col)) if r is not None else "close"
                cells.append(f'<div class="valve-cell"><span class="valve-dot {state}"></span>{state.upper()}</div>')
            rows_html += f'<div class="valve-grid"><div class="valve-label">{label}</div>{"".join(cells)}</div>'
        st.markdown(header + rows_html, unsafe_allow_html=True)
        st.caption(f"{len(ster):,} records loaded • Running hours: Smart Perak Motor DB")

    render_sterilizer_page()


# ============================================================
# PAGE 4 – PRESS MONITORING
# ============================================================
elif page == "Press Running Hours":

    @st.fragment(run_every="1200s")
    def render_press_page():
        st.markdown(
            """<div class="main-header"><div class="main-header-title">Press Monitoring</div>
            <div class="main-header-sub">8-press live status, operating mode and process condition</div></div>""",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            p_date = st.date_input("Start date", value=date.today(), key="press_start")
        with c2:
            q_date = st.date_input("End date", value=date.today(), key="press_end")
        start_dt = datetime.combine(p_date, datetime.min.time())
        end_dt = datetime.combine(q_date, datetime.max.time())

        refresh_col, info_col = st.columns([1, 4])
        with refresh_col:
            if st.button("↻ Refresh Now", key="press_refresh", use_container_width=True):
                load_press_db.clear()
                st.rerun()
        with info_col:
            st.caption("Auto-refresh: every 20 minutes • Use Refresh Now for immediate latest data")

        try:
            press_df = load_press_db(start_dt, end_dt)
        except Exception as exc:
            st.error(f"Press database connection failed: {exc}")
            press_df = pd.DataFrame()

        if press_df.empty:
            st.info("No press data found for the selected period.")
            return

        latest = press_df.sort_values("ts_local").iloc[-1]
        latest_time = pd.to_datetime(latest.get("ts_local"), errors="coerce")
        st.caption(f"Latest DB sample: {latest_time.strftime('%d/%m/%Y %I:%M:%S %p') if pd.notna(latest_time) else '--'}")

        # A press is considered running from its main press motor current.
        # 5 A avoids treating tiny/noise current as a running press.
        RUNNING_AMP_THRESHOLD = 5.0

        running_count = 0
        auto_count = 0
        manual_count = 0
        for i in range(1, 9):
            amp = pd.to_numeric(latest.get(f"sp{i}_amp"), errors="coerce")
            mode_raw = latest.get(f"sp{i}_auto_manual", "--")
            mode_text = str(mode_raw).strip().upper()
            if mode_text in {"1", "1.0", "AUTO", "AUTOMATIC", "A"}:
                mode = "AUTO"
            elif mode_text in {"0", "0.0", "MANUAL", "M", "HAND"}:
                mode = "MANUAL"
            else:
                mode = mode_text if mode_text not in {"", "NAN", "NONE"} else "--"
            if pd.notna(amp) and amp > RUNNING_AMP_THRESHOLD:
                running_count += 1
                if mode == "AUTO":
                    auto_count += 1
                elif mode == "MANUAL":
                    manual_count += 1

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Presses Running", f"{running_count} / 8")
        k2.metric("Auto Running", str(auto_count))
        k3.metric("Manual Running", str(manual_count))
        k4.metric("Stopped", str(8 - running_count))

        # 4 x 2 press cards.
        for row_numbers in ([1,2], [3,4], [5,6], [7,8]):
            cols = st.columns(2)
            for idx, i in enumerate(row_numbers):
                with cols[idx]:
                    amp = pd.to_numeric(latest.get(f"sp{i}_amp"), errors="coerce")
                    setpoint = pd.to_numeric(latest.get(f"sp{i}_setpoint"), errors="coerce")
                    dtemp = pd.to_numeric(latest.get(f"d{i}_temp"), errors="coerce")
                    damp = pd.to_numeric(latest.get(f"d{i}_amp"), errors="coerce")
                    level_raw = latest.get(f"d{i}_level")
                    level_numeric = pd.to_numeric(level_raw, errors="coerce")
                    hpu = pd.to_numeric(latest.get(f"sp{i}_hpu_pressure"), errors="coerce")

                    # Read the AUTO/MANUAL value directly from this press's own DB column.
                    mode_raw = latest.get(f"sp{i}_auto_manual")
                    mode_text = str(mode_raw).strip().upper() if pd.notna(mode_raw) else ""
                    if mode_text in {"1", "1.0", "AUTO", "AUTOMATIC", "A"}:
                        mode = "AUTO"
                    elif mode_text in {"0", "0.0", "MANUAL", "M", "HAND"}:
                        mode = "MANUAL"
                    else:
                        mode = mode_text if mode_text and mode_text not in {"NAN", "NONE", "NULL"} else "UNKNOWN"

                    is_running = pd.notna(amp) and amp > RUNNING_AMP_THRESHOLD
                    status_text = "RUNNING" if is_running else "STOPPED"
                    status_class = "press-running" if is_running else "press-stopped"
                    mode_class = "press-auto" if mode == "AUTO" else "press-manual" if mode == "MANUAL" else ""

                    # Digester level analysis: explicitly show whether it is above or below 75%.
                    # Digester level can be stored either as a numeric percentage
                    # or as the MQTT text values "full" / "not-full".
                    level_text = str(level_raw).strip().lower() if pd.notna(level_raw) else ""
                    if pd.notna(level_numeric):
                        if level_numeric > 75:
                            level_state = "LEVEL ABOVE 75%"
                            level_class = "press-level-high"
                        elif level_numeric < 75:
                            level_state = "LEVEL BELOW 75%"
                            level_class = "press-level-low"
                        else:
                            level_state = "LEVEL AT 75%"
                            level_class = "press-level-at"
                    elif level_text in {"full", "high", "above 75", "above 75%"}:
                        level_state = "LEVEL ABOVE 75%"
                        level_class = "press-level-high"
                    elif level_text in {"not-full", "not full", "low", "below 75", "below 75%"}:
                        level_state = "LEVEL BELOW 75%"
                        level_class = "press-level-low"
                    else:
                        level_state = "LEVEL: --"
                        level_class = ""

                    if not is_running:
                        analysis = "Press is stopped based on motor current."
                    else:
                        analysis = f"Press is running in {mode} mode. Digester level is {level_state.replace('LEVEL ', '').lower()}."

                    ts_text = latest_time.strftime("%d %b %Y %H:%M:%S") if pd.notna(latest_time) else "--"

                    def fmt(v, unit):
                        return f"{v:.1f} {unit}" if pd.notna(v) else "--"

                    metrics = [
                        ("MODE", mode),
                        ("SETPOINT", fmt(setpoint, "")),
                        ("MOTOR AMPS", fmt(amp, "A")),
                        ("DIGESTER TEMP", fmt(dtemp, "°C")),
                        ("DIGESTER AMPS", fmt(damp, "A")),
                        ("HYDRAULIC", fmt(hpu, "bar")),
                    ]
                    metric_html = "".join(
                        f'<div class="press-metric"><div class="press-label">{lab}</div><div class="press-value">{val}</div></div>'
                        for lab, val in metrics
                    )

                    st.markdown(
                        f'<div class="press-card">'
                        f'<div class="press-card-top"><div class="press-name">PRESS {i}</div>'
                        f'<div class="press-status {status_class}">{status_text}</div></div>'
                        f'<div class="press-time">◷ {ts_text} &nbsp; • &nbsp; MODE: <span class="{mode_class}">{mode}</span></div>'
                        f'<div class="press-grid">{metric_html}</div>'
                        f'<div class="press-level-status {level_class}">{level_state}</div>'
                        f'<div class="press-analysis"><b>Current Analysis</b><br>{analysis}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        # ========================================================
        # DIGESTER PERFORMANCE TREND – COMPLETE START-TO-END HISTORY
        # ========================================================
        st.markdown(
            '<div class="section-heading">Digester Performance Trend</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Complete selected-period history for digester temperature and level. "
            "The graph includes every available DB timestamp from the selected start to end date."
        )

        trend_press = st.selectbox(
            "Select Press for Digester Trend",
            [f"Press {i}" for i in range(1, 9)],
            key="digester_trend_press",
        )
        ti = int(trend_press.split()[-1])

        try:
            trend_df = load_press_trend_db(start_dt, end_dt, ti)
        except Exception as exc:
            st.error(f"Could not load the complete digester trend for Press {ti}: {exc}")
            trend_df = pd.DataFrame()

        if trend_df.empty:
            st.info(f"No digester temperature/level data available for Press {ti} in the selected period.")
        else:
            valid_temp = trend_df[trend_df["temperature"].notna()].copy()
            above = valid_temp[valid_temp["level_state"] == "Above 75%"]
            below = valid_temp[valid_temp["level_state"] == "Below 75%"]
            at75 = valid_temp[valid_temp["level_state"] == "At 75%"]

            a1, a2, a3, a4 = st.columns(4)
            a1.metric("Total Readings", f"{len(valid_temp):,}")
            a2.metric("Above 75%", f"{len(above):,}")
            a3.metric("Below 75%", f"{len(below):,}")
            a4.metric("Temperature Range", (
                f"{valid_temp['temperature'].min():.1f}–{valid_temp['temperature'].max():.1f} °C"
                if not valid_temp.empty else "--"
            ))

            # Temperature uses the left axis. Digester level is shown on the right
            # axis as a state line: 100 = Above 75%, 0 = Below 75%.
            fig_dt = make_subplots(specs=[[{"secondary_y": True}]])
            fig_dt.add_trace(
                go.Scatter(
                    x=valid_temp["ts_local"],
                    y=valid_temp["temperature"],
                    mode="lines",
                    name="Temperature",
                    line=dict(width=2.5),
                    connectgaps=False,
                    hovertemplate="%{x|%H:%M:%S}<br>Temperature: %{y:.1f} °C<extra></extra>",
                ),
                secondary_y=False,
            )

            level_df = trend_df[trend_df["level_value"].notna()].copy()
            if not level_df.empty:
                fig_dt.add_trace(
                    go.Scatter(
                        x=level_df["ts_local"],
                        y=level_df["level_value"],
                        mode="lines",
                        name="Level",
                        line=dict(width=2.5, shape="hv"),
                        connectgaps=False,
                        hovertemplate=(
                            "%{x|%H:%M:%S}<br>Level: "
                            "%{customdata}<extra></extra>"
                        ),
                        customdata=level_df["level_state"],
                    ),
                    secondary_y=True,
                )

            # Fixed 90°C process reference line, matching the requested style.
            fig_dt.add_hline(
                y=90,
                line_dash="dash",
                line_width=1.5,
                annotation_text="Baseline (90°C)",
                annotation_position="top right",
                secondary_y=False,
            )

            # Keep the level state readable on the right side.
            fig_dt.update_yaxes(
                title_text="Temperature",
                rangemode="tozero",
                secondary_y=False,
            )
            fig_dt.update_yaxes(
                title_text="Level",
                range=[-5, 105],
                tickmode="array",
                tickvals=[0, 50, 100],
                ticktext=["Less than 75", "75%", "Above 75"],
                secondary_y=True,
            )
            fig_dt.update_xaxes(
                title_text="Time",
                showgrid=False,
                rangeslider_visible=True,
            )
            fig_dt.update_layout(
                height=470,
                margin=dict(l=55, r=65, t=45, b=55),
                paper_bgcolor="#071018",
                plot_bgcolor="#071018",
                font=dict(color="#e5e7eb"),
                hovermode="x unified",
                legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
                xaxis=dict(type="date"),
            )
            st.plotly_chart(fig_dt, use_container_width=True, config={"displayModeBar": True, "scrollZoom": True})

            st.caption(
                f"Press {ti}: {len(valid_temp):,} temperature readings from "
                f"{valid_temp['ts_local'].min():%d/%m/%Y %H:%M:%S} to "
                f"{valid_temp['ts_local'].max():%d/%m/%Y %H:%M:%S}."
            )

            # Compact level/temperature summary for the same complete dataset.
            summary_rows = []
            for state, group in (("Above 75%", above), ("Below 75%", below), ("At 75%", at75)):
                summary_rows.append({
                    "Level Condition": state,
                    "Samples": len(group),
                    "Avg Temperature (°C)": round(group["temperature"].mean(), 2) if not group.empty else None,
                    "Min Temperature (°C)": round(group["temperature"].min(), 2) if not group.empty else None,
                    "Max Temperature (°C)": round(group["temperature"].max(), 2) if not group.empty else None,
                })
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

        with st.expander("View Press DB Data"):
            st.dataframe(press_df, use_container_width=True, hide_index=True)

    render_press_page()


# ============================================================
# PAGE 5 – CLARIFICATION MONITORING
# ============================================================
elif page == "Clarification Monitoring":

    @st.fragment(run_every="1200s")
    def render_clarification_page():
        st.markdown(
            '<div class="main-header">'
            '<div class="main-header-title">Clarification Monitoring</div>'
            '<div class="main-header-sub">Clarification station levels, temperatures, pressures and equipment load</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        f1, f2, rf = st.columns([1, 1, 1])
        with f1:
            c_start = st.date_input("From", value=date.today(), key="clar_start")
        with f2:
            c_end = st.date_input("To", value=date.today(), key="clar_end")
        with rf:
            st.write("")
            if st.button("↻ Refresh Now", key="clar_refresh", use_container_width=True):
                load_clarification_db.clear()
                find_clarification_table.clear()
                st.rerun()

        start_dt = datetime.combine(c_start, datetime.min.time())
        end_dt = datetime.combine(c_end, datetime.max.time())

        try:
            clar = load_clarification_db(start_dt, end_dt)
        except Exception as exc:
            st.error(f"Clarification database could not be loaded: {exc}")
            clar = pd.DataFrame()

        if clar.empty:
            st.info("No clarification-station records were found for the selected period.")
        else:
            latest = clar.iloc[-1]
            st.caption(
                f"{len(clar):,} records • {clar['ts_local'].min():%d %b %Y %H:%M:%S} "
                f"to {clar['ts_local'].max():%d %b %Y %H:%M:%S}"
            )

            # Latest process snapshot
            st.markdown('<div class="section-heading">Latest Clarification Status</div>', unsafe_allow_html=True)
            latest_specs = [
                ("Sludge Tank 1 Level", "sludge_tank_1_level", "%"),
                ("Sludge Tank 1 Temp", "sludge_tank_1_temp", "°C"),
                ("Sludge Tank 2 Level", "sludge_tank_2_level", "%"),
                ("Sludge Tank 2 Temp", "sludge_tank_2_temp", "°C"),
                ("Pure Oil Tank 1 Level", "pure_oil_tank_1_level", "%"),
                ("Pure Oil Tank 2 Level", "pure_oil_tank_2_level", "%"),
                ("Crude Oil Tank 1-1 Level", "crude_oil_tank_1_1_level", "%"),
                ("Crude Oil Tank 1-2 Level", "crude_oil_tank_1_2_level", "%"),
            ]
            cols = st.columns(4)
            for idx, (label, col, unit) in enumerate(latest_specs):
                value = pd.to_numeric(latest.get(col), errors="coerce")
                text_value = f"{value:.1f} {unit}" if pd.notna(value) else "--"
                cols[idx % 4].metric(label, text_value)

            # Clarifier and equipment snapshot
            st.markdown('<div class="section-heading">Clarifier & Equipment Status</div>', unsafe_allow_html=True)
            eq_specs = [
                ("Vertical Clarifier 1 Level", "vertical_clarifier_1_level", "%"),
                ("Vertical Clarifier 1 Temp", "vertical_clarifier_1_temp", "°C"),
                ("Vertical Clarifier 2 Level", "vertical_clarifier_2_level", "%"),
                ("Vertical Clarifier 2 Temp", "vertical_clarifier_2_temp", "°C"),
                ("Vacuum Dryer 1", "vacuum_dryer_1_pressure", ""),
                ("Vacuum Dryer 2", "vacuum_dryer_2_pressure", ""),
                ("Vibrating Screen 1", "vibrating_screen_1_amp", "A"),
                ("Vibrating Screen 2", "vibrating_screen_2_amp", "A"),
                ("Vibrating Screen 3", "vibrating_screen_3_amp", "A"),
                ("Decanter 1", "decanter_1_amp", "A"),
                ("Decanter 2", "decanter_2_amp", "A"),
            ]
            cols = st.columns(4)
            for idx, (label, col, unit) in enumerate(eq_specs):
                value = pd.to_numeric(latest.get(col), errors="coerce")
                text_value = f"{value:.1f} {unit}" if pd.notna(value) else "--"
                cols[idx % 4].metric(label, text_value)

            # Trend graphs grouped by process function.
            st.markdown('<div class="section-heading">Clarification Trends</div>', unsafe_allow_html=True)

            # ------------------------------------------------------------
            # INDIVIDUAL TANK LEVEL TRENDS
            # Each tank gets its own graph so the level movement can be
            # monitored independently without overlapping the other tanks.
            # ------------------------------------------------------------
            st.markdown("### Tank Level Trends")
            tank_level_specs = [
                ("Sludge Tank 1 Level", "sludge_tank_1_level"),
                ("Sludge Tank 2 Level", "sludge_tank_2_level"),
                ("Pure Oil Tank 1 Level", "pure_oil_tank_1_level"),
                ("Pure Oil Tank 2 Level", "pure_oil_tank_2_level"),
                ("Crude Oil Tank 1-1 Level", "crude_oil_tank_1_1_level"),
                ("Crude Oil Tank 1-2 Level", "crude_oil_tank_1_2_level"),
            ]
            for tank_title, tank_col in tank_level_specs:
                _add_clarification_chart(
                    clar,
                    tank_title,
                    [(tank_title, tank_col)],
                    "Level (%)",
                    height=330,
                )

            # Vertical clarifier levels are also kept separate from the tank
            # graphs because they are a different process section.
            st.markdown("### Vertical Clarifier Level Trends")
            _add_clarification_chart(
                clar,
                "Vertical Clarifier 1 Level",
                [("Vertical Clarifier 1", "vertical_clarifier_1_level")],
                "Level (%)",
                height=330,
            )
            _add_clarification_chart(
                clar,
                "Vertical Clarifier 2 Level",
                [("Vertical Clarifier 2", "vertical_clarifier_2_level")],
                "Level (%)",
                height=330,
            )

            # ------------------------------------------------------------
            # INDIVIDUAL TANK / CLARIFIER TEMPERATURE TRENDS
            # Each temperature gets its own graph, matching the separate
            # level graphs above. This makes each process temperature easy
            # to inspect without overlapping multiple temperature series.
            # ------------------------------------------------------------
            st.markdown("### Tank & Clarifier Temperature Trends")
            tank_temperature_specs = [
                ("Sludge Tank 1 Temperature", "sludge_tank_1_temp"),
                ("Sludge Tank 2 Temperature", "sludge_tank_2_temp"),
                ("Pure Oil Tank 1 Temperature", "pure_oil_tank_1_temp"),
                ("Pure Oil Tank 2 Temperature", "pure_oil_tank_2_temp"),
                ("Crude Oil Tank 1-1 Temperature", "crude_oil_tank_1_1_temp"),
                ("Crude Oil Tank 1-2 Temperature", "crude_oil_tank_1_2_temp"),
            ]
            for temp_title, temp_col in tank_temperature_specs:
                _add_clarification_chart(
                    clar,
                    temp_title,
                    [(temp_title, temp_col)],
                    "Temperature (°C)",
                    height=330,
                )

            # Keep the two vertical clarifier temperatures separate as well.
            _add_clarification_chart(
                clar,
                "Vertical Clarifier 1 Temperature",
                [("Vertical Clarifier 1", "vertical_clarifier_1_temp")],
                "Temperature (°C)",
                height=330,
            )
            _add_clarification_chart(
                clar,
                "Vertical Clarifier 2 Temperature",
                [("Vertical Clarifier 2", "vertical_clarifier_2_temp")],
                "Temperature (°C)",
                height=330,
            )
            _add_clarification_chart(
                clar,
                "Vertical Clarifier Levels",
                [
                    ("Vertical Clarifier 1", "vertical_clarifier_1_level"),
                    ("Vertical Clarifier 2", "vertical_clarifier_2_level"),
                ],
                "Level (%)",
            )
            _add_clarification_chart(
                clar,
                "Vacuum Dryer Pressure",
                [
                    ("Vacuum Dryer 1", "vacuum_dryer_1_pressure"),
                    ("Vacuum Dryer 2", "vacuum_dryer_2_pressure"),
                ],
                "Pressure",
            )
            _add_clarification_chart(
                clar,
                "Vibrating Screen 1 Motor Load",
                [("Vibrating Screen 1", "vibrating_screen_1_amp")],
                "Current (A)",
                height=330,
            )
            _add_clarification_chart(
                clar,
                "Vibrating Screen 2 Motor Load",
                [("Vibrating Screen 2", "vibrating_screen_2_amp")],
                "Current (A)",
                height=330,
            )
            _add_clarification_chart(
                clar,
                "Vibrating Screen 3 Motor Load",
                [("Vibrating Screen 3", "vibrating_screen_3_amp")],
                "Current (A)",
                height=330,
            )
            _add_clarification_chart(
                clar,
                "Decanter 1 Motor Load",
                [("Decanter 1", "decanter_1_amp")],
                "Current (A)",
                height=330,
            )
            _add_clarification_chart(
                clar,
                "Decanter 2 Motor Load",
                [("Decanter 2", "decanter_2_amp")],
                "Current (A)",
                height=330,
            )

            # Statistical analysis without inventing alarm thresholds.
            st.markdown('<div class="section-heading">Parameter Analysis</div>', unsafe_allow_html=True)
            st.caption(
                "Latest, average, minimum, maximum and direction are calculated from the selected period. "
                "No Normal/High/Low process limit is invented here; configured limits can be added when provided."
            )
            analysis_specs = [
                ("Sludge Tank 1 Level", "sludge_tank_1_level", "%"),
                ("Sludge Tank 1 Temperature", "sludge_tank_1_temp", "°C"),
                ("Sludge Tank 2 Level", "sludge_tank_2_level", "%"),
                ("Sludge Tank 2 Temperature", "sludge_tank_2_temp", "°C"),
                ("Pure Oil Tank 1 Level", "pure_oil_tank_1_level", "%"),
                ("Pure Oil Tank 2 Level", "pure_oil_tank_2_level", "%"),
                ("Crude Oil Tank 1-1 Level", "crude_oil_tank_1_1_level", "%"),
                ("Crude Oil Tank 1-1 Temperature", "crude_oil_tank_1_1_temp", "°C"),
                ("Vertical Clarifier 1 Level", "vertical_clarifier_1_level", "%"),
                ("Vertical Clarifier 1 Temperature", "vertical_clarifier_1_temp", "°C"),
                ("Vertical Clarifier 2 Level", "vertical_clarifier_2_level", "%"),
                ("Vertical Clarifier 2 Temperature", "vertical_clarifier_2_temp", "°C"),
                ("Vacuum Dryer 1 Pressure", "vacuum_dryer_1_pressure", ""),
                ("Vacuum Dryer 2 Pressure", "vacuum_dryer_2_pressure", ""),
                ("Vibrating Screen 1", "vibrating_screen_1_amp", "A"),
                ("Vibrating Screen 2", "vibrating_screen_2_amp", "A"),
                ("Vibrating Screen 3", "vibrating_screen_3_amp", "A"),
                ("Decanter 1", "decanter_1_amp", "A"),
                ("Decanter 2", "decanter_2_amp", "A"),
            ]
            st.dataframe(
                _clarification_kpi_rows(clar, analysis_specs),
                use_container_width=True,
                hide_index=True,
            )

            with st.expander("View Clarification DB Data"):
                st.dataframe(clar, use_container_width=True, hide_index=True)

    render_clarification_page()


# ============================================================
# PAGE 6 – SECONDARY OIL LOSS PREDICTION
# ============================================================
elif page == "Secondary Oil Loss Prediction":

    @st.fragment(run_every="1200s")
    def render_secondary_page():
        st.markdown(
            '<div class="main-header">'
            '<div class="main-header-title">Secondary Oil Loss Prediction</div>'
            '<div class="main-header-sub">NIR sludge pond trend monitoring • fixed set line: 1.60</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("↻ Refresh Now", key="secondary_refresh", use_container_width=True):
                load_secondary_oil_loss.clear()
                st.rerun()
        with c2:
            st.caption("Auto-refresh: every 20 minutes • Set line: 1.60 • Source: nir_sludge / pond samples")

        # Date range for the secondary oil-loss trend.
        d1, d2 = st.columns(2)
        with d1:
            sec_start_date = st.date_input("Start date", value=date.today(), key="secondary_start_date")
        with d2:
            sec_end_date = st.date_input("End date", value=date.today(), key="secondary_end_date")
        sec_start_dt = datetime.combine(sec_start_date, datetime.min.time())
        sec_end_dt = datetime.combine(sec_end_date, datetime.max.time())

        if sec_start_dt > sec_end_dt:
            st.warning("Start date must be on or before the end date.")
            return

        try:
            sec = load_secondary_oil_loss(sec_start_dt, sec_end_dt)
        except Exception as exc:
            st.error(f"Secondary oil loss database connection failed: {exc}")
            return

        if sec.empty:
            st.info("No pond NIR data found in nir_sludge.")
            return

        latest = sec.iloc[-1]
        latest_val = float(latest["val2"])
        avg_val = float(sec["val2"].mean())
        min_val = float(sec["val2"].min())
        max_val = float(sec["val2"].max())
        above = int((sec["val2"] > SECONDARY_SETLINE).sum())
        below = int((sec["val2"] < SECONDARY_SETLINE).sum())
        trend = secondary_trend_label(sec["val2"])
        latest_time = latest["timestamp"]
        status = "ABOVE SET LINE" if latest_val > SECONDARY_SETLINE else "AT / BELOW SET LINE"
        status_class = "secondary-alert" if latest_val > SECONDARY_SETLINE else "secondary-insight"

        kcols = st.columns(5)
        cards = [
            ("Latest NIR", f"{latest_val:.2f}", status),
            ("Set Line", f"{SECONDARY_SETLINE:.2f}", "Fixed analysis line"),
            ("Average", f"{avg_val:.2f}", f"{len(sec):,} samples"),
            ("Range", f"{min_val:.2f} – {max_val:.2f}", "Observed period"),
            ("Trend", trend, "Recent samples"),
        ]
        for col, (label, value, sub) in zip(kcols, cards):
            with col:
                st.markdown(
                    f'<div class="secondary-card"><div class="secondary-card-label">{label}</div>'
                    f'<div class="secondary-card-value">{value}</div><div class="secondary-card-sub">{sub}</div></div>',
                    unsafe_allow_html=True,
                )

        if latest_val > SECONDARY_SETLINE:
            st.markdown(
                f"""<div class=\"alert-panel\">
                    <div class=\"alert-title\">⚠ SECONDARY OIL LOSS HIGH ALERT</div>
                    <div class=\"alert-text\">
                        Latest NIR: <b>{latest_val:.2f}</b> &nbsp; | &nbsp; Setpoint: <b>{SECONDARY_SETLINE:.2f}</b>
                        &nbsp; | &nbsp; Difference: <b>{latest_val-SECONDARY_SETLINE:+.2f}</b>
                    </div>
                    <div class=\"point-alert-recommendation\" style=\"margin-top:8px;\">
                        Select an above-setpoint NIR sample to check Press/Digester readings in the same NIR clock hour
                        and Sterilizer 6–10 cycle readings in the immediately preceding hour.
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""<div class=\"point-good\">
                    <div class=\"point-good-title\">✓ Secondary Oil Loss Within Setpoint</div>
                    <div class=\"point-good-detail\">Latest NIR {latest_val:.2f} is at/below the fixed {SECONDARY_SETLINE:.2f} setpoint.</div>
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="{status_class}"><b>Current Analysis</b><br>'
            f'Latest sample: <b>{latest_val:.2f}</b> at {latest_time.strftime("%d %b %Y %H:%M:%S")}. '
            f'Set line is fixed at <b>{SECONDARY_SETLINE:.2f}</b>. '
            f'{above:,} samples are above the line and {below:,} are below the line. '
            f'Current trend: <b>{trend}</b>.</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-heading">Secondary Oil Loss Trend</div>', unsafe_allow_html=True)
        fig = go.Figure()
        sec_plot = sec.copy()
        sec_customdata = [
            [int(r["id"]) if pd.notna(r.get("id")) else -1, float(r["val2"]), pd.Timestamp(r["timestamp"]).strftime("%d %b %Y %H:%M:%S")]
            for _, r in sec_plot.iterrows()
        ]
        fig.add_trace(go.Scatter(
            x=sec_plot["timestamp"], y=sec_plot["val2"], mode="lines+markers",
            name="NIR Sludge / Pond", line=dict(color="#38bdf8", width=2),
            marker=dict(size=5), customdata=sec_customdata,
            hovertemplate="<b>%{x}</b><br>NIR: %{y:.2f}<br><extra></extra>",
        ))
        fig.add_hline(
            y=SECONDARY_SETLINE, line_dash="dash", line_color="#f97316",
            annotation_text="SET LINE 1.60", annotation_position="top left"
        )
        fig.update_layout(
            height=420, paper_bgcolor="#081017", plot_bgcolor="#081017",
            font=dict(color="#dbe5ec"), margin=dict(l=20,r=20,t=25,b=35),
            xaxis=dict(showgrid=True, gridcolor="#1d303c", title="Timestamp"),
            yaxis=dict(showgrid=True, gridcolor="#1d303c", title="NIR Value"),
            legend=dict(orientation="h", y=1.05, x=0),
            hovermode="x unified",
        )
        sec_event = st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False},
            key="secondary_nir_trend", on_select="rerun", selection_mode=("points",)
        )
        if sec_event and hasattr(sec_event, "selection"):
            sec_points = sec_event.selection.get("points", [])
            if sec_points:
                cd = sec_points[0].get("customdata")
                if cd and float(cd[1]) > SECONDARY_SETLINE:
                    st.session_state.selected_secondary_point = {
                        "id": int(cd[0]),
                        "value": float(cd[1]),
                        "datetime": pd.to_datetime(cd[2]),
                    }
                    st.session_state.pmc_page = "Secondary High Process Check"
                    st.rerun()

        st.markdown('<div class="section-heading">Trend Analysis</div>', unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            st.markdown(
                f'<div class="analysis-card"><div class="analysis-title">Set Line Position</div>'
                f'<div class="analysis-row"><span>Latest</span><b>{latest_val:.2f}</b></div>'
                f'<div class="analysis-row"><span>Set line</span><b>{SECONDARY_SETLINE:.2f}</b></div>'
                f'<div class="analysis-row"><span>Difference</span><b>{latest_val-SECONDARY_SETLINE:+.2f}</b></div></div>',
                unsafe_allow_html=True,
            )
        with b:
            st.markdown(
                f'<div class="analysis-card"><div class="analysis-title">Observed Samples</div>'
                f'<div class="analysis-row"><span>Above 1.60</span><b>{above:,}</b></div>'
                f'<div class="analysis-row"><span>Below 1.60</span><b>{below:,}</b></div>'
                f'<div class="analysis-row"><span>Maximum</span><b>{max_val:.2f}</b></div></div>',
                unsafe_allow_html=True,
            )
        with c:
            st.markdown(
                f'<div class="analysis-card"><div class="analysis-title">Trend Direction</div>'
                f'<div class="analysis-row"><span>Recent trend</span><b>{trend}</b></div>'
                f'<div class="analysis-row"><span>Minimum</span><b>{min_val:.2f}</b></div>'
                f'<div class="analysis-row"><span>Latest sample</span><b>{latest_time.strftime("%d %b %H:%M")}</b></div></div>',
                unsafe_allow_html=True,
            )

        with st.expander("View Pond NIR Data"):
            st.dataframe(sec, use_container_width=True, hide_index=True)

    render_secondary_page()


# ============================================================
# SECONDARY HIGH NIR PROCESS CHECK
# ============================================================
elif page == "Secondary High Process Check":
    selected = st.session_state.get("selected_secondary_point")
    st.markdown(
        '<div class="main-header"><div class="main-header-title">Secondary High NIR Process Check</div>'
        '<div class="main-header-sub">Selected pond NIR → Clarification process data from the same NIR clock hour</div></div>',
        unsafe_allow_html=True,
    )

    if not selected:
        st.info("Select an above-setpoint Secondary Oil Loss NIR point first.")
        if st.button("← Back to Secondary Oil Loss", key="back_secondary_empty"):
            st.session_state.pmc_page = "Secondary Oil Loss Prediction"
            st.rerun()
    else:
        value = float(selected.get("value", 0))
        sample_dt = pd.to_datetime(selected.get("datetime"), errors="coerce")

        if pd.isna(sample_dt):
            st.error("Selected Secondary NIR sample has no valid timestamp.")
        elif value <= SECONDARY_SETLINE:
            st.info(f"Selected value {value:.2f} is not above the {SECONDARY_SETLINE:.2f} setpoint.")
            if st.button("← Back to Secondary Oil Loss", key="back_secondary_not_high"):
                st.session_state.pmc_page = "Secondary Oil Loss Prediction"
                st.rerun()
        else:
            # ------------------------------------------------------------
            # Selected NIR summary
            # ------------------------------------------------------------
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                st.metric("NIR Oil Loss", f"{value:.2f}")
            with b2:
                st.metric("Setpoint", f"{SECONDARY_SETLINE:.2f}")
            with b3:
                st.metric("Above Setpoint", f"{value-SECONDARY_SETLINE:+.2f}")
            with b4:
                st.metric("Sample Time", sample_dt.strftime("%d %b %H:%M:%S"))

            if st.button("← Back to Secondary Oil Loss", key="back_secondary_process"):
                st.session_state.pmc_page = "Secondary Oil Loss Prediction"
                st.rerun()

            # ------------------------------------------------------------
            # CLARIFICATION ONLY
            # Use the full clarification-station history in the 5 hours
            # immediately preceding the selected Secondary NIR sample.
            # This gives enough process history around the NIR event instead
            # of limiting the analysis to one clock hour.
            # No Press, Digester or Sterilizer data is loaded here.
            # ------------------------------------------------------------
            st.markdown(
                '<div class="section-heading">Clarification Performance — Previous 5 Hours</div>',
                unsafe_allow_html=True,
            )
            window_end = sample_dt
            window_start = sample_dt - pd.Timedelta(hours=5)
            st.caption(
                f"Clarification analysis window: {window_start.strftime('%d %b %Y %H:%M:%S')}–"
                f"{window_end.strftime('%d %b %Y %H:%M:%S')} "
                f"(full clarification-station history in the 5 hours leading up to the selected Secondary NIR sample)."
            )

            try:
                clar_high = load_clarification_db(window_start, window_end)
            except Exception as exc:
                clar_high = pd.DataFrame()
                st.error(f"Clarification data could not be loaded: {exc}")

            if clar_high.empty:
                st.warning(
                    "No clarification-station records were found in the 5-hour window before the selected NIR sample."
                )
            else:
                clar_high = clar_high.sort_values("ts_local").reset_index(drop=True)
                latest = clar_high.iloc[-1]

                st.markdown(
                    '<div class="section-heading">Latest Clarification Snapshot</div>',
                    unsafe_allow_html=True,
                )

                snapshot_specs = [
                    ("Sludge Tank 1 Level", "sludge_tank_1_level", "%"),
                    ("Sludge Tank 1 Temp", "sludge_tank_1_temp", "°C"),
                    ("Sludge Tank 2 Level", "sludge_tank_2_level", "%"),
                    ("Sludge Tank 2 Temp", "sludge_tank_2_temp", "°C"),
                    ("Pure Oil Tank 1 Level", "pure_oil_tank_1_level", "%"),
                    ("Pure Oil Tank 1 Temp", "pure_oil_tank_1_temp", "°C"),
                    ("Pure Oil Tank 2 Level", "pure_oil_tank_2_level", "%"),
                    ("Pure Oil Tank 2 Temp", "pure_oil_tank_2_temp", "°C"),
                    ("Crude Oil Tank 1-1 Level", "crude_oil_tank_1_1_level", "%"),
                    ("Crude Oil Tank 1-1 Temp", "crude_oil_tank_1_1_temp", "°C"),
                    ("Crude Oil Tank 1-2 Level", "crude_oil_tank_1_2_level", "%"),
                    ("Crude Oil Tank 1-2 Temp", "crude_oil_tank_1_2_temp", "°C"),
                    ("Vertical Clarifier 1 Level", "vertical_clarifier_1_level", "%"),
                    ("Vertical Clarifier 1 Temp", "vertical_clarifier_1_temp", "°C"),
                    ("Vertical Clarifier 2 Level", "vertical_clarifier_2_level", "%"),
                    ("Vertical Clarifier 2 Temp", "vertical_clarifier_2_temp", "°C"),
                    ("Vacuum Dryer 1 Pressure", "vacuum_dryer_1_pressure", ""),
                    ("Vacuum Dryer 2 Pressure", "vacuum_dryer_2_pressure", ""),
                    ("Vibrating Screen 1", "vibrating_screen_1_amp", "A"),
                    ("Vibrating Screen 2", "vibrating_screen_2_amp", "A"),
                    ("Vibrating Screen 3", "vibrating_screen_3_amp", "A"),
                    ("Decanter 1", "decanter_1_amp", "A"),
                    ("Decanter 2", "decanter_2_amp", "A"),
                ]

                snap_cols = st.columns(4)
                for idx, (label, col_name, unit) in enumerate(snapshot_specs):
                    raw = latest.get(col_name)
                    num = pd.to_numeric(raw, errors="coerce")
                    if pd.notna(num):
                        value_text = f"{float(num):.1f}{unit}"
                    elif pd.notna(raw):
                        value_text = str(raw)
                    else:
                        value_text = "--"
                    with snap_cols[idx % 4]:
                        st.metric(label, value_text)

                st.caption(
                    f"{len(clar_high):,} clarification records found in the 5-hour NIR window. "
                    f"Latest clarification record: {latest['ts_local']:%d %b %Y %H:%M:%S}."
                )

                # ------------------------------------------------------------
                # THRESHOLD / EQUIPMENT CHECK
                # Level: count hours above 90%.
                # Temperature: count hours above 70°C.
                # Motor equipment: >5 A is treated as RUNNING, consistent with
                # the Press page running-current rule.
                # ------------------------------------------------------------
                st.markdown(
                    '<div class="section-heading">Clarification Threshold & Equipment Check</div>',
                    unsafe_allow_html=True,
                )
                st.caption(
                    "Analysis covers the same 5-hour window. Hours are estimated from consecutive DB readings; "
                    "gaps longer than 15 minutes are not counted as continuous condition. "
                    "Level threshold: >90%. Temperature threshold: >70°C. Motor running threshold: >5 A."
                )

                level_specs = [
                    ("Sludge Tank 1", "sludge_tank_1_level"),
                    ("Sludge Tank 2", "sludge_tank_2_level"),
                    ("Pure Oil Tank 1", "pure_oil_tank_1_level"),
                    ("Pure Oil Tank 2", "pure_oil_tank_2_level"),
                    ("Crude Oil Tank 1-1", "crude_oil_tank_1_1_level"),
                    ("Crude Oil Tank 1-2", "crude_oil_tank_1_2_level"),
                    ("Vertical Clarifier 1", "vertical_clarifier_1_level"),
                    ("Vertical Clarifier 2", "vertical_clarifier_2_level"),
                ]
                temp_specs = [
                    ("Sludge Tank 1", "sludge_tank_1_temp"),
                    ("Sludge Tank 2", "sludge_tank_2_temp"),
                    ("Pure Oil Tank 1", "pure_oil_tank_1_temp"),
                    ("Pure Oil Tank 2", "pure_oil_tank_2_temp"),
                    ("Crude Oil Tank 1-1", "crude_oil_tank_1_1_temp"),
                    ("Crude Oil Tank 1-2", "crude_oil_tank_1_2_temp"),
                    ("Vertical Clarifier 1", "vertical_clarifier_1_temp"),
                    ("Vertical Clarifier 2", "vertical_clarifier_2_temp"),
                ]
                motor_specs = [
                    ("Vibrating Screen 1", "vibrating_screen_1_amp"),
                    ("Vibrating Screen 2", "vibrating_screen_2_amp"),
                    ("Vibrating Screen 3", "vibrating_screen_3_amp"),
                    ("Decanter 1", "decanter_1_amp"),
                    ("Decanter 2", "decanter_2_amp"),
                ]

                level_rows = []
                for label, col_name in level_specs:
                    latest_value = pd.to_numeric(latest.get(col_name), errors="coerce")
                    hours = _clarification_duration_above_threshold(
                        clar_high, col_name, 90.0, window_start, window_end
                    )
                    level_rows.append({
                        "Equipment": label,
                        "Latest Level (%)": f"{float(latest_value):.1f}" if pd.notna(latest_value) else "--",
                        "Hours Above 90%": f"{hours:.2f}",
                    })

                st.markdown("**Level condition — above 90%**")
                st.dataframe(pd.DataFrame(level_rows), use_container_width=True, hide_index=True)

                temp_rows = []
                for label, col_name in temp_specs:
                    latest_value = pd.to_numeric(latest.get(col_name), errors="coerce")
                    hours = _clarification_duration_above_threshold(
                        clar_high, col_name, 70.0, window_start, window_end
                    )
                    temp_rows.append({
                        "Equipment": label,
                        "Latest Temperature (°C)": f"{float(latest_value):.1f}" if pd.notna(latest_value) else "--",
                        "Hours Above 70°C": f"{hours:.2f}",
                    })

                st.markdown("**Temperature condition — above 70°C**")
                st.dataframe(pd.DataFrame(temp_rows), use_container_width=True, hide_index=True)

                motor_rows = []
                for label, col_name in motor_specs:
                    running, amp_value, hours = _clarification_running_status(
                        clar_high, col_name, window_start, window_end, amp_threshold=5.0
                    )
                    motor_rows.append({
                        "Equipment": label,
                        "Latest Current (A)": f"{amp_value:.1f}" if amp_value is not None else "--",
                        "Current Status": "RUNNING" if running else "STOPPED",
                        "Running Hours (5h Window)": f"{hours:.2f}",
                    })

                st.markdown("**Vibrating Screen & Decanter Running Check**")
                st.dataframe(pd.DataFrame(motor_rows), use_container_width=True, hide_index=True)

                # Full record history is retained so the user can see exactly
                # what clarification readings existed around the high NIR sample.
                st.markdown(
                    '<div class="section-heading">All Clarification Records — Previous 5 Hours</div>',
                    unsafe_allow_html=True,
                )
                display_cols = [
                    "ts_local",
                    "sludge_tank_1_level", "sludge_tank_1_temp",
                    "sludge_tank_2_level", "sludge_tank_2_temp",
                    "pure_oil_tank_1_level", "pure_oil_tank_1_temp",
                    "pure_oil_tank_2_level", "pure_oil_tank_2_temp",
                    "crude_oil_tank_1_1_level", "crude_oil_tank_1_1_temp",
                    "crude_oil_tank_1_2_level", "crude_oil_tank_1_2_temp",
                    "vertical_clarifier_1_level", "vertical_clarifier_1_temp",
                    "vertical_clarifier_2_level", "vertical_clarifier_2_temp",
                    "vacuum_dryer_1_pressure", "vacuum_dryer_2_pressure",
                    "vibrating_screen_1_amp", "vibrating_screen_2_amp",
                    "vibrating_screen_3_amp", "decanter_1_amp", "decanter_2_amp",
                ]
                detail = clar_high[[c for c in display_cols if c in clar_high.columns]].copy()
                detail = detail.rename(columns={
                    "ts_local": "Record Time",
                    "sludge_tank_1_level": "Sludge T1 Level",
                    "sludge_tank_1_temp": "Sludge T1 Temp",
                    "sludge_tank_2_level": "Sludge T2 Level",
                    "sludge_tank_2_temp": "Sludge T2 Temp",
                    "pure_oil_tank_1_level": "Pure Oil T1 Level",
                    "pure_oil_tank_1_temp": "Pure Oil T1 Temp",
                    "pure_oil_tank_2_level": "Pure Oil T2 Level",
                    "pure_oil_tank_2_temp": "Pure Oil T2 Temp",
                    "crude_oil_tank_1_1_level": "Crude T1-1 Level",
                    "crude_oil_tank_1_1_temp": "Crude T1-1 Temp",
                    "crude_oil_tank_1_2_level": "Crude T1-2 Level",
                    "crude_oil_tank_1_2_temp": "Crude T1-2 Temp",
                    "vertical_clarifier_1_level": "Clarifier 1 Level",
                    "vertical_clarifier_1_temp": "Clarifier 1 Temp",
                    "vertical_clarifier_2_level": "Clarifier 2 Level",
                    "vertical_clarifier_2_temp": "Clarifier 2 Temp",
                    "vacuum_dryer_1_pressure": "Vacuum Dryer 1",
                    "vacuum_dryer_2_pressure": "Vacuum Dryer 2",
                    "vibrating_screen_1_amp": "Vib Screen 1",
                    "vibrating_screen_2_amp": "Vib Screen 2",
                    "vibrating_screen_3_amp": "Vib Screen 3",
                    "decanter_1_amp": "Decanter 1",
                    "decanter_2_amp": "Decanter 2",
                })
                detail["Record Time"] = pd.to_datetime(detail["Record Time"], errors="coerce").dt.strftime("%d %b %Y %H:%M:%S")
                st.dataframe(detail, use_container_width=True, hide_index=True, height=520)

                st.markdown(
                    '<div class="section-heading">Clarification Trend — Previous 5 Hours</div>',
                    unsafe_allow_html=True,
                )
                st.caption(
                    "The following trends use the complete clarification-station records from the 5-hour window before the selected NIR sample."
                )

                # Keep the high-NIR confirmation page readable: group related
                # clarification signals rather than mixing them with other stations.
                trend_groups = [
                    (
                        "Tank Levels",
                        [
                            ("Sludge Tank 1", "sludge_tank_1_level"),
                            ("Sludge Tank 2", "sludge_tank_2_level"),
                            ("Pure Oil Tank 1", "pure_oil_tank_1_level"),
                            ("Pure Oil Tank 2", "pure_oil_tank_2_level"),
                            ("Crude Oil Tank 1-1", "crude_oil_tank_1_1_level"),
                            ("Crude Oil Tank 1-2", "crude_oil_tank_1_2_level"),
                            ("Vertical Clarifier 1", "vertical_clarifier_1_level"),
                            ("Vertical Clarifier 2", "vertical_clarifier_2_level"),
                        ],
                        "%",
                    ),
                    (
                        "Tank Temperatures",
                        [
                            ("Sludge Tank 1", "sludge_tank_1_temp"),
                            ("Sludge Tank 2", "sludge_tank_2_temp"),
                            ("Pure Oil Tank 1", "pure_oil_tank_1_temp"),
                            ("Pure Oil Tank 2", "pure_oil_tank_2_temp"),
                            ("Crude Oil Tank 1-1", "crude_oil_tank_1_1_temp"),
                            ("Crude Oil Tank 1-2", "crude_oil_tank_1_2_temp"),
                            ("Vertical Clarifier 1", "vertical_clarifier_1_temp"),
                            ("Vertical Clarifier 2", "vertical_clarifier_2_temp"),
                        ],
                        "°C",
                    ),
                ]

                for group_title, specs, unit in trend_groups:
                    st.markdown(f"**{group_title}**")
                    for label, col_name in specs:
                        if col_name not in clar_high.columns:
                            continue
                        series = pd.to_numeric(clar_high[col_name], errors="coerce")
                        if series.notna().sum() == 0:
                            continue
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=clar_high["ts_local"],
                            y=series,
                            mode="lines+markers",
                            name=label,
                            line=dict(color="#38bdf8", width=2),
                            marker=dict(size=5),
                            hovertemplate=f"<b>{label}</b><br>%{{x}}<br>%{{y:.2f}} {unit}<extra></extra>",
                        ))
                        fig.update_layout(
                            height=250,
                            paper_bgcolor="#081017",
                            plot_bgcolor="#081017",
                            font=dict(color="#dbe5ec"),
                            margin=dict(l=20, r=20, t=28, b=35),
                            xaxis=dict(title="Time", showgrid=True, gridcolor="#1d303c"),
                            yaxis=dict(title=unit, showgrid=True, gridcolor="#1d303c"),
                            showlegend=False,
                        )
                        st.markdown(f"*{label}*")
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                equipment_specs = [
                    ("Vacuum Dryer 1 Pressure", "vacuum_dryer_1_pressure"),
                    ("Vacuum Dryer 2 Pressure", "vacuum_dryer_2_pressure"),
                    ("Vibrating Screen 1", "vibrating_screen_1_amp"),
                    ("Vibrating Screen 2", "vibrating_screen_2_amp"),
                    ("Vibrating Screen 3", "vibrating_screen_3_amp"),
                    ("Decanter 1", "decanter_1_amp"),
                    ("Decanter 2", "decanter_2_amp"),
                ]
                st.markdown("**Clarification Equipment Trends**")
                for label, col_name in equipment_specs:
                    if col_name not in clar_high.columns:
                        continue
                    series = pd.to_numeric(clar_high[col_name], errors="coerce")
                    if series.notna().sum() == 0:
                        continue
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=clar_high["ts_local"],
                        y=series,
                        mode="lines+markers",
                        name=label,
                        line=dict(color="#22c55e", width=2),
                        marker=dict(size=5),
                        hovertemplate=f"<b>{label}</b><br>%{{x}}<br>%{{y:.2f}}<extra></extra>",
                    ))
                    fig.update_layout(
                        height=250,
                        paper_bgcolor="#081017",
                        plot_bgcolor="#081017",
                        font=dict(color="#dbe5ec"),
                        margin=dict(l=20, r=20, t=28, b=35),
                        xaxis=dict(title="Time", showgrid=True, gridcolor="#1d303c"),
                        yaxis=dict(title="Value", showgrid=True, gridcolor="#1d303c"),
                        showlegend=False,
                    )
                    st.markdown(f"*{label}*")
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            st.caption(
                "This Secondary Oil Loss process check uses only Clarification-station readings from the same clock hour as the selected pond NIR sample. "
                "Press, Digester and Sterilizer data are intentionally not shown on this page."
            )

# ============================================================
# OTHER PAGES
# ============================================================
else:
    st.markdown(
        f"""
        <div class="main-header">
            <div class="main-header-title">{page}</div>
            <div class="main-header-sub">
                This monitoring report will be developed next.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info("This report page will be developed next.")

import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ThermoCardial AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

/* ── Global ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #fefce8;
    color: #1f2937;
}
.stApp {
    background: linear-gradient(135deg, #fefce8 0%, #fef9c3 50%, #fef3c7 100%);
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 1280px !important;
}

/* ── Hero ───────────────────────────────────────────── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ff4d6d, #c77dff, #4cc9f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #8a84a0;
    margin-top: 0.4rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}
.hero-bar {
    height: 3px;
    background: linear-gradient(90deg, #ff4d6d, #c77dff, #4cc9f0);
    border-radius: 2px;
    margin: 1.2rem 0 2rem 0;
}

/* ── Section titles ─────────────────────────────────── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #c77dff;
    letter-spacing: 0.02em;
    margin-bottom: 0.25rem;
}
.section-line {
    height: 2px;
    width: 40px;
    background: linear-gradient(90deg, #c77dff, #4cc9f0);
    border-radius: 2px;
    margin-bottom: 1.2rem;
}

/* ── Section cards ──────────────────────────────────── */
.section-card {
    background: rgba(28,21,48,0.6);
    border: 1px solid rgba(199,125,255,0.15);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

/* ── Input form card ────────────────────────────────── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.8rem 1.8rem 1.4rem 1.8rem;
    margin-bottom: 0.5rem;
}
.input-row-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8a84a0;
    margin: 0 0 0.6rem 0.1rem;
    font-weight: 600;
}

/* ── Field labels (the text above each input widget) ── */
label,
[data-testid="stWidgetLabel"] p,
.stSelectbox label,
.stNumberInput label {
    color: #6a6480 !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.3rem !important;
    line-height: 1.4 !important;
}

/* ── Tooltip / Help icon ────────────────────────────── */
[data-testid="tooltipHoverTarget"] {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 17px !important;
    height: 17px !important;
    border-radius: 50% !important;
    background: rgba(199,125,255,0.25) !important;
    border: 1.5px solid #c77dff !important;
    color: #e8e4f0 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    cursor: help !important;
    margin-left: 5px !important;
    vertical-align: middle !important;
    flex-shrink: 0 !important;
    transition: background 0.2s !important;
}
[data-testid="tooltipHoverTarget"]:hover {
    background: rgba(199,125,255,0.5) !important;
}
/* Tooltip popup bubble */
[data-testid="stTooltipContent"],
div[role="tooltip"] {
    background: #1c1530 !important;
    color: #e8e4f0 !important;
    border: 1px solid rgba(199,125,255,0.35) !important;
    border-radius: 10px !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.65rem 0.9rem !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6) !important;
    white-space: pre-line !important;
    max-width: 260px !important;
    line-height: 1.4 !important;
}

/* ── Number inputs ──────────────────────────────────── */
[data-baseweb="input"] {
    background: #ffffff !important;
    border: 1.5px solid #c8c0d8 !important;
    border-radius: 9px !important;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.06) !important;
    transition: border-color 0.2s !important;
}
[data-baseweb="input"]:focus-within {
    border-color: #c77dff !important;
    box-shadow: 0 0 0 3px rgba(199,125,255,0.18) !important;
}
[data-baseweb="input"] input {
    background: transparent !important;
    color: #111111 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    caret-color: #5a00cc !important;
}
[data-baseweb="input"] input::placeholder {
    color: #999999 !important;
    font-weight: 400 !important;
    opacity: 1 !important;
}

/* ── Selectbox ──────────────────────────────────────── */
[data-baseweb="select"] > div:first-child {
    background: #ffffff !important;
    border: 1.5px solid #c8c0d8 !important;
    border-radius: 9px !important;
    color: #111111 !important;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.06) !important;
    transition: border-color 0.2s !important;
    min-height: 42px !important;
}
[data-baseweb="select"] > div:first-child:focus-within {
    border-color: #c77dff !important;
    box-shadow: 0 0 0 3px rgba(199,125,255,0.18) !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] div[class*="singleValue"],
[data-baseweb="select"] div[class*="ValueContainer"] {
    color: #111111 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}
[data-baseweb="select"] svg {
    color: #7a6890 !important;
}

/* Dropdown menu */
[data-baseweb="menu"] {
    background: #ffffff !important;
    border: 1px solid #e0d8f0 !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.18) !important;
    margin-top: 4px !important;
}
[data-baseweb="menu"] li {
    color: #111111 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li[aria-selected="true"] {
    background: #f0eaff !important;
    color: #5a00cc !important;
}

/* ── Number input stepper buttons ───────────────────── */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: #f4f0ff !important;
    color: #5a00cc !important;
    border-color: #c8c0d8 !important;
    font-weight: 700 !important;
}
button[data-testid="stNumberInputStepDown"]:hover,
button[data-testid="stNumberInputStepUp"]:hover {
    background: #e4d8ff !important;
}

/* ── Submit button ──────────────────────────────────── */
.stButton > button {
    width: 100%;
    padding: 0.9rem 2rem;
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    background: linear-gradient(135deg, #ff4d6d, #c77dff);
    color: #ffffff !important;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 4px 24px rgba(199,125,255,0.35);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(199,125,255,0.5);
    background: linear-gradient(135deg, #ff3356, #b56df0);
}

/* ── Result cards ───────────────────────────────────── */
.result-positive {
    background: linear-gradient(135deg, rgba(255,77,109,0.15), rgba(255,77,109,0.05));
    border: 1px solid rgba(255,77,109,0.4);
    border-radius: 20px; padding: 2rem; text-align: center;
}
.result-medium {
    background: linear-gradient(135deg, rgba(255,190,11,0.15), rgba(255,190,11,0.05));
    border: 1px solid rgba(255,190,11,0.4);
    border-radius: 20px; padding: 2rem; text-align: center;
}
.result-negative {
    background: linear-gradient(135deg, rgba(76,201,240,0.15), rgba(76,201,240,0.05));
    border: 1px solid rgba(76,201,240,0.4);
    border-radius: 20px; padding: 2rem; text-align: center;
}
.result-label { font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:800; margin:0.5rem 0; }
.result-emoji { font-size: 3rem; margin-bottom: 0.5rem; }
.confidence-text { font-size: 0.85rem; color: #8a84a0; margin-top: 0.5rem; }
.confidence-val  { font-size: 2rem; font-family:'Syne',sans-serif; font-weight:700; }

/* ── Stat cards ─────────────────────────────────────── */
.stat-card-pos {
    background: linear-gradient(135deg,rgba(255,77,109,0.12),rgba(255,77,109,0.03));
    border: 1px solid rgba(255,77,109,0.3); border-radius:16px; padding:1.5rem; text-align:center;
}
.stat-card-neg {
    background: linear-gradient(135deg,rgba(76,201,240,0.12),rgba(76,201,240,0.03));
    border: 1px solid rgba(76,201,240,0.3); border-radius:16px; padding:1.5rem; text-align:center;
}
.card {
    background: rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
    border-radius:16px; padding:1.5rem; backdrop-filter:blur(10px); margin-bottom:1rem;
}
.stat-number { font-family:'Syne',sans-serif; font-size:3rem; font-weight:800; line-height:1; }
.stat-label  { font-size:0.85rem; color:#8a84a0; text-transform:uppercase; letter-spacing:0.1em; margin-top:0.4rem; }
.stat-pos-color { color:#ff4d6d; }
.stat-neg-color { color:#4cc9f0; }

/* ── Risk / protect badges ──────────────────────────── */
.risk-badge {
    display:inline-block; background:rgba(255,77,109,0.15);
    border:1px solid rgba(255,77,109,0.3); color:#ff4d6d;
    border-radius:20px; padding:0.3rem 0.8rem; font-size:0.82rem; margin:0.25rem;
}
.protect-badge {
    display:inline-block; background:rgba(76,201,240,0.12);
    border:1px solid rgba(76,201,240,0.3); color:#4cc9f0;
    border-radius:20px; padding:0.3rem 0.8rem; font-size:0.82rem; margin:0.25rem;
}

/* ── Dividers & misc ────────────────────────────────── */
.custom-divider {
    border:none; height:1px;
    background:linear-gradient(90deg,transparent,rgba(255,255,255,0.1),transparent);
    margin:2rem 0;
}
.stDataFrame { border-radius:12px; overflow:hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DB SETUP
# ─────────────────────────────────────────────
DB_PATH = "thermocardial.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            age INTEGER, sex INTEGER, cp INTEGER, trestbps INTEGER,
            chol INTEGER, fbs INTEGER, restecg INTEGER, thalach INTEGER,
            exang INTEGER, oldpeak REAL, slope INTEGER, ca INTEGER, thal INTEGER,
            probability REAL, risk_level TEXT, prediction INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(fields, prob, risk_level, prediction):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO predictions (
            timestamp, age, sex, cp, trestbps, chol, fbs, restecg,
            thalach, exang, oldpeak, slope, ca, thal,
            probability, risk_level, prediction
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        fields['age'], fields['sex'], fields['cp'], fields['trestbps'],
        fields['chol'], fields['fbs'], fields['restecg'], fields['thalach'],
        fields['exang'], fields['oldpeak'], fields['slope'], fields['ca'], fields['thal'],
        round(prob, 4), risk_level, prediction
    ))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM predictions WHERE prediction=1")
    pos = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM predictions WHERE prediction=0")
    neg = c.fetchone()[0]
    conn.close()
    return pos, neg

def get_all_records():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC LIMIT 50", conn
    )
    conn.close()
    return df

init_db()

# ─────────────────────────────────────────────
# CATEGORICAL FIELD MAPPINGS
# Format: { field_key: [ ("Medical Name (N)", N), ... ] }
# Dropdown shows "Medical Name (N)" — model receives only N.
# Source: heart.csv column unique values.
# ─────────────────────────────────────────────
FIELD_MAPS = {
    # sex: 0 = Female, 1 = Male
    "sex": [
        ("Female (0)",  0),
        ("Male (1)",    1),
    ],
    # cp: chest pain type — 4 types from dataset
    "cp": [
        ("Typical Angina (0)",    0),   # exertional, relieved by rest
        ("Atypical Angina (1)",   1),   # chest pain, unusual features
        ("Non-Anginal Pain (2)",  2),   # not cardiac in origin
        ("Asymptomatic (3)",      3),   # no chest pain at all
    ],
    # fbs: fasting blood sugar > 120 mg/dl
    "fbs": [
        ("No — ≤ 120 mg/dl (0)",  0),
        ("Yes — > 120 mg/dl (1)", 1),
    ],
    # restecg: resting ECG results
    "restecg": [
        ("Normal (0)",                          0),
        ("ST-T Wave Abnormality (1)",           1),   # T-wave inversion / ST elevation
        ("Left Ventricular Hypertrophy (2)",    2),   # by Estes' criteria
    ],
    # exang: exercise-induced angina
    "exang": [
        ("No (0)",   0),
        ("Yes (1)",  1),
    ],
    # slope: slope of peak exercise ST segment
    "slope": [
        ("Upsloping (0)",     0),   # relatively normal
        ("Flat (1)",          1),   # borderline abnormal
        ("Downsloping (2)",   2),   # sign of ischaemia
    ],
    # ca: major vessels coloured by fluoroscopy — CSV has 0,1,2,3,4
    "ca": [
        ("0 Vessels (0)",  0),
        ("1 Vessel (1)",   1),
        ("2 Vessels (2)",  2),
        ("3 Vessels (3)",  3),
        ("4 Vessels (4)",  4),
    ],
    # thal: thalassemia type
    "thal": [
        ("Normal (0)",              0),
        ("Fixed Defect (1)",        1),   # permanent reduced flow
        ("Reversible Defect (2)",   2),   # stress-induced, recoverable
        ("Unknown / Not Tested (3)",3),
    ],
}

# ── Helpers ────────────────────────────────────────────────────────────
def labels(field_key: str) -> list:
    """Return display strings shown in the dropdown."""
    return [lbl for lbl, _ in FIELD_MAPS[field_key]]

def map_val(field_key: str, label: str) -> int:
    """Given a display label, return the integer the model needs."""
    for lbl, val in FIELD_MAPS[field_key]:
        if lbl == label:
            return val
    raise ValueError(f"Label '{label}' not found in FIELD_MAPS['{field_key}']")

def strip_code(label: str) -> str:
    """'Typical Angina (0)' → 'Typical Angina'  (for display in badges)."""
    return label.rsplit("(", 1)[0].strip()

# ── Tooltips ───────────────────────────────────────────────────────────
TOOLTIPS = {
    "age":      "Patient age in years (valid range: 20–100).",
    "sex":      "Biological sex.\n  Female = 0 | Male = 1",
    "cp":       "Chest pain type (cp):\n  0 = Typical Angina\n  1 = Atypical Angina\n  2 = Non-Anginal Pain\n  3 = Asymptomatic",
    "trestbps": "Resting systolic blood pressure on admission (mmHg).\n  Normal < 120 | High ≥ 140",
    "chol":     "Serum cholesterol (mg/dl).\n  Desirable < 200 | Borderline 200–239 | High ≥ 240",
    "fbs":      "Fasting blood sugar > 120 mg/dl?\n  No = 0 | Yes = 1",
    "restecg":  "Resting ECG result (restecg):\n  0 = Normal\n  1 = ST-T Wave Abnormality\n  2 = Left Ventricular Hypertrophy",
    "thalach":  "Maximum heart rate achieved during exercise stress test (bpm).",
    "exang":    "Did exercise induce chest pain?\n  No = 0 | Yes = 1",
    "oldpeak":  "ST depression (mm) during exercise vs. rest.\n  Higher = more ischaemia. Range: 0.0–7.0",
    "slope":    "Slope of peak exercise ST segment:\n  0 = Upsloping\n  1 = Flat\n  2 = Downsloping",
    "ca":       "Major coronary vessels coloured by fluoroscopy (0–4).\n  More vessels = wider blockage.",
    "thal":     "Thalassemia type:\n  0 = Normal\n  1 = Fixed Defect\n  2 = Reversible Defect\n  3 = Unknown",
}

# ─────────────────────────────────────────────
# MODEL LOAD
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load("heart_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

model_loaded = os.path.exists("heart_model.pkl") and os.path.exists("scaler.pkl")

# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="padding: 1rem 0 0.5rem 0;">
    <p class="hero-title">ThermoCardial AI</p>
    <p class="hero-sub">🫀 Heart Disease Risk Assessment System — Thermodynamic Attention Regression</p>
    <div class="hero-bar"></div>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ `heart_model.pkl` or `scaler.pkl` not found. Please run `train_model.py` first to generate them.")
    st.stop()

model, scaler = load_model()

# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Patient Input Parameters</p><div class="section-line"></div>', unsafe_allow_html=True)

# st.markdown('<div class="input-card">', unsafe_allow_html=True)

# ══ GROUP 1: Demographics & Vitals ══════════════════════════════════════
st.markdown('<p class="input-row-label">📋 Demographics & Vitals</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="medium")
with c1:
    age = st.number_input(
        "Age (years)", min_value=20, max_value=100, value=50, step=1,
        help=TOOLTIPS["age"],
    )
with c2:
    _sex_lbl = st.selectbox("Sex", options=labels("sex"), help=TOOLTIPS["sex"])
    sex = map_val("sex", _sex_lbl)
with c3:
    trestbps = st.number_input(
        "Resting Blood Pressure (mmHg)", min_value=80, max_value=220, value=120, step=1,
        help=TOOLTIPS["trestbps"],
    )
with c4:
    thalach = st.number_input(
        "Max Heart Rate (bpm)", min_value=60, max_value=250, value=150, step=1,
        help=TOOLTIPS["thalach"],
    )

st.markdown('<div style="height:1.1rem"></div>', unsafe_allow_html=True)

# ══ GROUP 2: Lab Results & ECG ══════════════════════════════════════════
st.markdown('<p class="input-row-label">🧪 Lab Results & ECG</p>', unsafe_allow_html=True)

c5, c6, c7, c8 = st.columns(4, gap="medium")
with c5:
    chol = st.number_input(
        "Cholesterol (mg/dl)", min_value=100, max_value=600, value=200, step=1,
        help=TOOLTIPS["chol"],
    )
with c6:
    _fbs_lbl = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dl (fbs)", options=labels("fbs"),
        help=TOOLTIPS["fbs"],
    )
    fbs = map_val("fbs", _fbs_lbl)
with c7:
    _restecg_lbl = st.selectbox(
        "Resting ECG Result (restecg)", options=labels("restecg"),
        help=TOOLTIPS["restecg"],
    )
    restecg = map_val("restecg", _restecg_lbl)
with c8:
    _cp_lbl = st.selectbox("Chest Pain Type (cp)", options=labels("cp"), help=TOOLTIPS["cp"])
    cp = map_val("cp", _cp_lbl)

st.markdown('<div style="height:1.1rem"></div>', unsafe_allow_html=True)

# ══ GROUP 3: Exercise & Imaging ═════════════════════════════════════════
st.markdown('<p class="input-row-label">🏃 Exercise Test & Imaging</p>', unsafe_allow_html=True)

c9, c10, c11, c12, c13 = st.columns([1, 1, 1, 1, 1], gap="medium")
with c9:
    _exang_lbl = st.selectbox(
        "Exercise Angina (exang)", options=labels("exang"),
        help=TOOLTIPS["exang"],
    )
    exang = map_val("exang", _exang_lbl)
with c10:
    oldpeak = st.number_input(
        "ST Depression (oldpeak)", min_value=0.0, max_value=7.0,
        value=1.0, step=0.1, format="%.1f",
        help=TOOLTIPS["oldpeak"],
    )
with c11:
    _slope_lbl = st.selectbox(
        "ST Slope (slope)", options=labels("slope"),
        help=TOOLTIPS["slope"],
    )
    slope = map_val("slope", _slope_lbl)
with c12:
    _ca_lbl = st.selectbox(
        "Coronary Vessels (ca)", options=labels("ca"),
        help=TOOLTIPS["ca"],
    )
    ca = map_val("ca", _ca_lbl)
with c13:
    _thal_lbl = st.selectbox(
        "Thalassemia (thal)", options=labels("thal"),
        help=TOOLTIPS["thal"],
    )
    thal = map_val("thal", _thal_lbl)

st.markdown('</div>', unsafe_allow_html=True)  # close input-card

# ── Encoding strip ───────────────────────────────────────────────────────
st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#1f2937;font-size:0.72rem;text-transform:uppercase;'
    'letter-spacing:0.1em;margin-bottom:0.5rem;font-weight:600;">📋 Numeric encodings sent to model</p>',
    unsafe_allow_html=True,
)
enc_cols = st.columns(8, gap="small")
enc_items = [
    ("sex",     _sex_lbl,     sex),
    ("cp",      _cp_lbl,      cp),
    ("fbs",     _fbs_lbl,     fbs),
    ("restecg", _restecg_lbl, restecg),
    ("exang",   _exang_lbl,   exang),
    ("slope",   _slope_lbl,   slope),
    ("ca",      _ca_lbl,      ca),
    ("thal",    _thal_lbl,    thal),
]
for col, (fname, full_lbl, num) in zip(enc_cols, enc_items):
    with col:
        st.markdown(
            f'<div style="background:rgba(199,125,255,0.07);border:1px solid rgba(199,125,255,0.18);'
            f'border-radius:10px;padding:0.55rem 0.5rem;text-align:center;">'
            f'<div style="color:#1f2937;font-size:0.65rem;text-transform:uppercase;'
            f'letter-spacing:0.07em;margin-bottom:0.2rem;font-weight:600;">{fname}</div>'
            f'<div style="color:#1f2937;font-size:0.74rem;margin-bottom:0.15rem;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="{full_lbl}">'
            f'{strip_code(full_lbl)}</div>'
            f'<div style="color:#1f2937;font-weight:800;font-size:1.2rem;'
            f'font-family:Syne,sans-serif;line-height:1;">{num}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PREDICT BUTTON
# ─────────────────────────────────────────────
col_btn, _ = st.columns([2, 5])
with col_btn:
    predict_clicked = st.button("🔍 Analyse & Predict")

# ─────────────────────────────────────────────
# PREDICTION LOGIC
# ─────────────────────────────────────────────
if predict_clicked:
    fields = dict(
        age=age, sex=sex, cp=cp, trestbps=trestbps, chol=chol,
        fbs=fbs, restecg=restecg, thalach=thalach, exang=exang,
        oldpeak=oldpeak, slope=slope, ca=ca, thal=thal
    )

    input_arr = np.array([[age, sex, cp, trestbps, chol, fbs,
                           restecg, thalach, exang, oldpeak, slope, ca, thal]])
    input_scaled = scaler.transform(input_arr)
    prob = model.predict_proba(input_scaled)[0][1]
    prediction = 1 if prob > 0.4 else 0

    if prob > 0.7:
        risk_level = "High Risk"
        result_class = "result-positive"
        emoji = "⚠️"
        label_color = "#ff4d6d"
        label_text = "High Risk — Heart Disease Likely"
    elif prob > 0.4:
        risk_level = "Medium Risk"
        result_class = "result-medium"
        emoji = "🟡"
        label_color = "#ffbe0b"
        label_text = "Medium Risk — Borderline"
    else:
        risk_level = "Low Risk"
        result_class = "result-negative"
        emoji = "✅"
        label_color = "#4cc9f0"
        label_text = "Low Risk — No Heart Disease"

    save_to_db(fields, prob, risk_level, prediction)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Prediction Result</p><div class="section-line"></div>', unsafe_allow_html=True)

    # ── Result card + gauge side by side ──
    r1, r2 = st.columns([1, 1.6])

    with r1:
        st.markdown(f"""
        <div class="{result_class}">
            <div class="result-emoji">{emoji}</div>
            <div class="result-label" style="color:{label_color};">{label_text}</div>
            <div class="confidence-text">Confidence Score</div>
            <div class="confidence-val" style="color:{label_color};">{prob:.0%}</div>
        </div>
        """, unsafe_allow_html=True)

        # Risk / Protective factors
        risk_factors, protect_factors = [], []
        if age > 60: risk_factors.append("Age > 60")
        if trestbps > 140: risk_factors.append("High Blood Pressure")
        if chol > 240: risk_factors.append("High Cholesterol")
        if exang == 1: risk_factors.append("Exercise Angina")
        if oldpeak > 2: risk_factors.append("High ST Depression")
        if ca >= 2: risk_factors.append("Blocked Vessels")
        if thalach > 140: protect_factors.append("Good Max HR")
        if ca == 0: protect_factors.append("No Vessel Blockage")
        if exang == 0: protect_factors.append("No Exercise Pain")

        if risk_factors or protect_factors:
            st.markdown("<br>", unsafe_allow_html=True)
            if risk_factors:
                badges = "".join([f'<span class="risk-badge">⚠ {f}</span>' for f in risk_factors])
                st.markdown(f"**Risk Factors**<br>{badges}", unsafe_allow_html=True)
            if protect_factors:
                badges = "".join([f'<span class="protect-badge">✓ {f}</span>' for f in protect_factors])
                st.markdown(f"**Protective Factors**<br>{badges}", unsafe_allow_html=True)

    with r2:
        # Gauge chart
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(prob * 100, 1),
            number={"suffix": "%", "font": {"size": 40, "color": label_color, "family": "Syne"}},
            title={"text": "Risk Probability", "font": {"size": 14, "color": "#8a84a0", "family": "DM Sans"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#444", "tickfont": {"color": "#666"}},
                "bar": {"color": label_color, "thickness": 0.25},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40],  "color": "rgba(76,201,240,0.15)"},
                    {"range": [40, 70], "color": "rgba(255,190,11,0.15)"},
                    {"range": [70, 100],"color": "rgba(255,77,109,0.15)"},
                ],
                "threshold": {
                    "line": {"color": label_color, "width": 3},
                    "thickness": 0.75,
                    "value": round(prob * 100, 1),
                },
            }
        ))
        gauge_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#e8e4f0"},
            height=260,
            margin=dict(l=20, r=20, t=40, b=10),
        )
        st.plotly_chart(gauge_fig, use_container_width=True)

    # ─────────────────────────────────────────
    # GRAPHICAL REPRESENTATION OF INPUT PARAMS
    # ─────────────────────────────────────────
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Your Input Parameters — Visual Analysis</p><div class="section-line"></div>', unsafe_allow_html=True)

    param_labels = [
        "Age", "Sex", "Chest\nPain", "BP", "Chol",
        "FBS", "ECG", "Max HR", "Exang",
        "Oldpeak", "Slope", "Vessels", "Thal"
    ]
    param_values = [age, sex, cp, trestbps, chol, fbs, restecg,
                    thalach, exang, oldpeak, slope, ca, thal]

    # Radar + Bar tabs
    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "🕸 Radar Chart", "🌡 Normalised Heatmap"])

    with tab1:
        bar_fig = go.Figure()
        colors_bar = [
            "#ff4d6d" if v > np.percentile(param_values, 70)
            else "#4cc9f0" if v < np.percentile(param_values, 30)
            else "#c77dff"
            for v in param_values
        ]
        bar_fig.add_trace(go.Bar(
            x=param_labels,
            y=param_values,
            marker_color=colors_bar,
            marker_line_width=0,
            opacity=0.85,
            text=[str(v) for v in param_values],
            textposition="outside",
            textfont={"color": "#e8e4f0", "size": 11},
        ))
        bar_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.02)",
            font={"color": "#e8e4f0", "family": "DM Sans"},
            xaxis={"gridcolor": "rgba(255,255,255,0.05)", "tickfont": {"size": 11}},
            yaxis={"gridcolor": "rgba(255,255,255,0.05)"},
            height=380,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
        )
        st.plotly_chart(bar_fig, use_container_width=True)

    with tab2:
        # Normalise for radar
        max_vals = [100, 1, 3, 220, 600, 1, 2, 250, 1, 7, 2, 3, 3]
        norm = [v/m for v, m in zip(param_values, max_vals)]
        labels_r = param_labels + [param_labels[0]]
        values_r = norm + [norm[0]]

        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(
            r=values_r,
            theta=labels_r,
            fill="toself",
            fillcolor=f"rgba(199,125,255,0.15)",
            line={"color": "#c77dff", "width": 2},
            marker={"color": label_color, "size": 7},
            name="Your Values",
        ))
        radar_fig.update_layout(
            polar={
                "bgcolor": "rgba(255,255,255,0.03)",
                "radialaxis": {"visible": True, "range": [0, 1], "gridcolor": "rgba(255,255,255,0.1)", "tickfont": {"color": "#666"}},
                "angularaxis": {"gridcolor": "rgba(255,255,255,0.08)", "tickfont": {"color": "#b8b0d0"}},
            },
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "#e8e4f0"},
            height=400,
            margin=dict(l=40, r=40, t=30, b=30),
            showlegend=False,
        )
        st.plotly_chart(radar_fig, use_container_width=True)

    with tab3:
        # Single-row heatmap
        max_vals_h = [100, 1, 3, 220, 600, 1, 2, 250, 1, 7.0, 2, 3, 3]
        norm_h = [round(v/m, 3) for v, m in zip(param_values, max_vals_h)]
        hm_fig = go.Figure(go.Heatmap(
            z=[norm_h],
            x=param_labels,
            y=["Normalised"],
            colorscale=[[0, "#4cc9f0"], [0.5, "#c77dff"], [1, "#ff4d6d"]],
            showscale=True,
            text=[[f"{v:.2f}" for v in norm_h]],
            texttemplate="%{text}",
            textfont={"size": 12, "color": "white"},
        ))
        hm_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#e8e4f0"},
            height=160,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis={"tickfont": {"size": 11}},
        )
        st.plotly_chart(hm_fig, use_container_width=True)
        st.caption("Values normalised 0–1 against clinical maximum. Red = higher relative value.")

# ─────────────────────────────────────────────
# COMMUNITY STATISTICS SECTION
# ─────────────────────────────────────────────
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Community Statistics</p><div class="section-line"></div>', unsafe_allow_html=True)
st.markdown('<p style="color:#8a84a0; font-size:0.9rem; margin-top:-0.8rem; margin-bottom:1.2rem;">Aggregated results from all patients assessed so far</p>', unsafe_allow_html=True)

pos_count, neg_count = get_stats()
total = pos_count + neg_count

# ── Stat cards ──
sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown(f"""
    <div class="stat-card-pos">
        <div class="stat-number stat-pos-color">{pos_count}</div>
        <div class="stat-label">Heart Disease Positive</div>
        <div style="font-size:0.82rem; color:#8a84a0; margin-top:0.6rem;">
            {"—" if total == 0 else f"{pos_count/total:.0%} of total"}
        </div>
    </div>
    """, unsafe_allow_html=True)
with sc2:
    st.markdown(f"""
    <div class="stat-card-neg">
        <div class="stat-number stat-neg-color">{neg_count}</div>
        <div class="stat-label">Heart Disease Negative</div>
        <div style="font-size:0.82rem; color:#8a84a0; margin-top:0.6rem;">
            {"—" if total == 0 else f"{neg_count/total:.0%} of total"}
        </div>
    </div>
    """, unsafe_allow_html=True)
with sc3:
    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <div class="stat-number" style="color:#c77dff;">{total}</div>
        <div class="stat-label">Total Assessments</div>
        <div style="font-size:0.82rem; color:#8a84a0; margin-top:0.6rem;">Lifetime records</div>
    </div>
    """, unsafe_allow_html=True)

if total > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)

    with ch1:
        # Donut
        donut_fig = go.Figure(go.Pie(
            labels=["Heart Disease +", "Heart Disease −"],
            values=[pos_count, neg_count],
            hole=0.6,
            marker_colors=["#ff4d6d", "#4cc9f0"],
            textinfo="percent",
            textfont={"color": "white", "size": 13},
            pull=[0.04, 0],
        ))
        donut_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "#e8e4f0", "family": "DM Sans"},
            legend={"font": {"color": "#b8b0d0"}},
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            annotations=[dict(
                text=f"{total}<br><span style='font-size:10px'>Total</span>",
                x=0.5, y=0.5, font_size=22,
                font_color="#e8e4f0",
                showarrow=False,
            )],
        )
        st.plotly_chart(donut_fig, use_container_width=True)

    with ch2:
        # Fetch recent records for trend
        records = get_all_records()
        if len(records) >= 2:
            records["date"] = pd.to_datetime(records["timestamp"]).dt.date
            daily = records.groupby(["date", "prediction"]).size().reset_index(name="count")
            trend_fig = px.bar(
                daily, x="date", y="count", color="prediction",
                color_discrete_map={1: "#ff4d6d", 0: "#4cc9f0"},
                labels={"prediction": "Prediction", "count": "Count", "date": "Date"},
                title="Daily Assessment Trend",
            )
            trend_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.02)",
                font={"color": "#e8e4f0", "family": "DM Sans"},
                legend={"font": {"color": "#b8b0d0"}, "title_text": ""},
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis={"gridcolor": "rgba(255,255,255,0.05)"},
                yaxis={"gridcolor": "rgba(255,255,255,0.05)"},
                title_font={"size": 14, "color": "#8a84a0"},
            )
            new_names = {"0": "Negative", "1": "Positive"}
            def _rename_trace(t):
                clean = str(t.name).strip()
                return t.update(name=new_names.get(clean, clean or t.name))
            trend_fig.for_each_trace(_rename_trace)
            st.plotly_chart(trend_fig, use_container_width=True)

# ─────────────────────────────────────────────
# RECENT RECORDS TABLE
# ─────────────────────────────────────────────
if total > 0:
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    with st.expander("📋 Recent Assessment Records (Last 50)", expanded=False):
        records = get_all_records()
        records["prediction"] = records["prediction"].map({1: "🔴 Positive", 0: "🟢 Negative"})
        records = records.drop(columns=["id"])
        st.dataframe(
            records,
            use_container_width=True,
            hide_index=True,
        )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="custom-divider"></div>
<p style="text-align:center; color:#3d3854; font-size:0.78rem; letter-spacing:0.08em; text-transform:uppercase;">
    ThermoCardial AI — For Academic &amp; Research Use Only · Not a Substitute for Medical Diagnosis
</p>
""", unsafe_allow_html=True)
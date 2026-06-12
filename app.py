import pandas as pd
import streamlit as st
from datetime import date
import numpy as np
import plotly.express as px

# ================= CONFIG =================
st.set_page_config(page_title="Engineer Utilization", layout="wide")

# ================= UI =================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

header,#MainMenu,footer{
    visibility:hidden;
}
.stApp{
    background-color:#F5F7FB;

    background-image:
        radial-gradient(
            at 10% 10%,
            rgba(59,130,246,.10) 0,
            transparent 35%
        ),
        radial-gradient(
            at 90% 10%,
            rgba(239,68,68,.08) 0,
            transparent 35%
        ),
        radial-gradient(
            at 50% 90%,
            rgba(16,185,129,.08) 0,
            transparent 35%
        );
}
.stApp::before{
    content:"";
    position:fixed;

    width:400px;
    height:400px;

    background:#DBEAFE;

    border-radius:50%;

    filter:blur(120px);

    top:-150px;
    left:-150px;

    z-index:-1;
}

.stSelectbox{
    margin-bottom:8px;
}
div.stButton > button{

    width:52px !important;

    height:20px !important;
    min-height:20px !important;

    font-size:9px !important;

    font-weight:500 !important;

    padding:0 !important;

    border-radius:16px !important;
}
div.stButton > button p{
    font-size:11px !important;
}
div.stButton{
    text-align:right !important;
}
.block-container{
    padding-top:1rem;
    padding-left:1rem;
    padding-right:1rem;
    max-width:100%;
}
/* ===== KPI CARD ===== */

.kpi-card{

    background:white;

    border-radius:20px;

    padding:16px;

    height:125px;

    border:1px solid #EDF0F5;

    box-shadow:
    0 2px 10px rgba(0,0,0,0.03);

    transition:0.2s;
}

.kpi-card:hover{

    transform:translateY(-2px);

    box-shadow:
    0 12px 24px rgba(0,0,0,0.06);
}

.kpi-value{

    font-size:28px;

    font-weight:700;

    color:#111827;
}

.kpi-active{

    border-top:4px solid #D71920;
}

/* ===== SECTION CARD ===== */

.widget-card{

    background:white;

    border-radius:24px;

    border:1px solid #EDF0F5;

    padding:15px;

    box-shadow:
    0 2px 10px rgba(0,0,0,0.03);
}

/* ===== HEADER ===== */

.dashboard-header{

    background:white;

    border-radius:24px;

    padding:24px;

    border:1px solid #EDF0F5;

    box-shadow:
    0 2px 10px rgba(0,0,0,0.03);
}

.dashboard-title{

    font-size:40px;

    font-weight:700;

    color:#111827;
}

.dashboard-subtitle{

    color:#64748B;

    font-size:16px;
}

/* ===== SMALL INFO CARD ===== */

.info-card{

    background:white;

    border-radius:20px;

    padding:16px;

    height:100%;

    border:1px solid #EDF0F5;

    text-align:center;
}

.info-title{

    font-size:12px;

    color:#94A3B8;
}

.info-value{

    margin-top:8px;

    font-size:18px;

    font-weight:700;

    color:#111827;
}
/* ===== SECTION HEADERS ===== */

.section-header{

    font-size:18px;

    font-weight:650;

    color:#111827;

    margin-top:20px;

    margin-bottom:10px;

    letter-spacing:-0.3px;
}
/* CHART */

div[data-testid="stPlotlyChart"]{

    background:white;

    border:none !important;

    padding:0 !important;
}

section[data-testid="stFileUploaderDropzone"]{
    border:1px dashed #DCE3EF !important;
    border-radius:10px !important;
    background:#FAFBFD !important;

    min-height:42px !important;

    padding:4px !important;
}

section[data-testid="stFileUploaderDropzone"] div{
    font-size:12px !important;
}
[data-testid="stVerticalBlock"]{
    gap:0rem;
}
.stMultiSelect div[data-baseweb="select"]{
    min-height:26px !important;
    font-size:13px !important;
}
.stDateInput input{
    height:34px !important;
    font-size:14px !important;
}
.sidebar-card{
    background:white;
    border-radius:28px;
    border:1px solid #E9EDF5;
    box-shadow:0 8px 30px rgba(15,23,42,.06);
}
.sidebar-title{
    font-size:18px;
    font-weight:700;
    color:#111827;
    margin-bottom:12px;
}
.metric-card {
    background: white;
    border-radius: 20px;
    padding: 12px;
    border: 1px solid #EDF0F5;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
[data-testid="stMetric"]{
    background:white;
    border:1px solid #EDF0F5;
    border-radius:16px;
    padding:8px;
    box-shadow:0 2px 8px rgba(0,0,0,0.03);
    position:relative;
}

[data-testid="stMetricLabel"]{
    font-size:11px;
    margin-top:38px;
}
section[data-testid="stSidebar"]{
    border-bottom-left-radius:40px;
    border-bottom-right-radius:40px;
}
[data-testid="stMetricValue"]{
    font-size:18px;
}
[data-testid="stMetric"]{
    background:white;
    border-radius:18px;
    padding:10px;
    border:1px solid #E9EDF5;
    box-shadow:0 2px 8px rgba(15,23,42,0.04);
}
[data-testid="stMetric"]{
    background:#FFFFFF;
    border:1px solid #E9EDF5;
    border-radius:22px;
    padding:10px 10px;
    min-height:95px;
    box-shadow:0 4px 18px rgba(15,23,42,.05);
}

[data-testid="stMetricLabel"]{
    font-size:12px !important;
    color:#64748B !important;
    font-weight:500 !important;
}

[data-testid="stMetricValue"]{
    font-size:18px !important;
    color:#111827 !important;
    font-weight:700 !important;
}
[data-testid="stVerticalBlockBorderWrapper"]{
    background:white;
    border-radius:20px;
    border:1px solid #E9EDF5;
    box-shadow:0 4px 18px rgba(15,23,42,.05);
}
.sidebar-divider{
    width:1px;
    background:#CBD5E1;

    min-height:100vh;
    margin:0 6px;

    position:relative;
    z-index:9999;
}
.kpi-box{
    background:white;
    border:1px solid #E9EDF5;
    border-radius:16px;

    padding:4px 1px;
    margin-left:1px;
    margin-right:1px;
    min-height:105px;

    text-align:center;

    box-shadow:0 2px 8px rgba(15,23,42,.03);
}
.kpi-green{
    border-top:4px solid #10B981;
}

.kpi-orange{
    border-top:4px solid #F97316;
}

.kpi-icon{
    width:34px;
    height:34px;

    display:flex;
    align-items:center;
    justify-content:center;

    margin:auto;
    margin-bottom:3px;

    border-radius:12px;

    background:#FFF1F2;

    font-size:16px;
}
.red-bg{background:#FFF1F2;}
.blue-bg{background:#EEF4FF;}
.green-bg{background:#EEFDF3;}
.purple-bg{background:#F7EEFF;}
.orange-bg{background:#FFF7ED;}

.kpi-label{
    font-size:13px;
    color:#64748B;
    font-weight:500;
    line-height:1.2;
    min-height:30px;
    display:flex;
    align-items:center;
    justify-content:center;
}

.kpi-number{
    font-size:18px;
    font-weight:650;
    color:#111827;
    margin-top:3px;
    line-height:1;
}
label{
    font-size:13px !important;
    font-weight:600 !important;
    color:#111827 !important;
}
.stMultiSelect{
    margin-bottom:-4px !important;
}

.stDateInput{
    margin-bottom:-4px !important;
}
[data-testid="stSidebar"] .element-container{
    margin-bottom:4px !important;
}
[data-testid="stFileUploaderDropzone"] button{
    font-size:9px !important;

    min-height:22px !important;
    height:22px !important;

    width:75px !important;

    padding:0px 4px !important;

    border-radius:6px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"]{
    display:none !important;
}
[data-testid="stFileUploaderDropzone"] p{
    font-size:11px !important;
}
[data-testid="stFileUploaderFileName"]{
    font-size:8px !important;
    font-weight:500 !important;
}
[data-testid="stFileUploader"] small{
    font-size:9px !important;
}
[data-testid="stFileUploader"] svg{
    width:14px !important;
    height:14px !important;
}
[data-testid="stFileUploader"]{
    margin-bottom:-10px !important;
}

[data-testid="stFileUploader"] small{
    display:none !important;
}

/* Uploaded filename row */

[data-testid="stFileUploaderFileName"]{
    font-size:8px !important;
    line-height:1 !important;
}

/* Remove extra spacing */

[data-testid="stFileUploader"] section{
    min-height:50px !important;
}
/* Uploaded file row */

[data-testid="stFileUploaderFile"]{
    padding:2px 4px !important;
    min-height:24px !important;
    height:24px !important;
}

/* File name */

[data-testid="stFileUploaderFileName"]{
    font-size:7px !important;
    line-height:1 !important;
}

/* Delete button */

[data-testid="stFileUploaderDeleteBtn"]{
    width:16px !important;
    height:16px !important;
    min-height:16px !important;
    padding:0 !important;
}

/* Upload area */

section[data-testid="stFileUploaderDropzone"]{
    min-height:42px !important;
    padding:2px !important;
}
/* TABLE OUTER */

[data-testid="stDataEditor"]{
    border:1px solid #E9EDF5 !important;
    border-radius:18px !important;
    overflow:hidden !important;
    background:white !important;
}

/* HEADER */

[data-testid="stDataEditor"] [role="columnheader"]{
    background:#EEF2FF !important;
    color:#111827 !important;
    font-weight:700 !important;
    font-size:12px !important;
    border-bottom:1px solid #E5E7EB !important;
}

/* CELLS */

[data-testid="stDataEditor"] [role="gridcell"]{
    font-size:12px !important;
    color:#374151 !important;
    background:white !important;
    padding-top:4px !important;
    padding-bottom:4px !important;
}

/* HOVER */

[data-testid="stDataEditor"] [role="gridcell"]:hover{
    background:#F9FAFB !important;
}


</style>
""", unsafe_allow_html=True)

# ================= LOAD =================
@st.cache_data
def load_data(file):
    df = pd.read_excel(file, engine="openpyxl")
    df.columns = df.columns.str.strip()

    cols = df.columns.tolist()

    try:
        required_indices = [0,12,13,14,15,16,17,18,19,21,35,36]

        if max(required_indices) >= len(cols):
            st.error("Excel format incorrect (missing required columns).")
            st.stop()
    except:
        st.error("File format is incorrect or columns missing.")
        st.stop()

    # Rename safely
    df = df.rename(columns={
        cols[0]: "Company",
        cols[12]: "Start_Date",
        cols[13]: "Start_Hour",
        cols[14]: "Start_Min",
        cols[15]: "End_Date",
        cols[16]: "End_Hour",
        cols[17]: "End_Min",
        cols[18]: "Hours",
        cols[19]: "Engineer",
        cols[21]: "State",
        cols[35]: "Dealer",
        cols[36]: "Call_Ref"
    })

    df = df[[
        "Company","State","Dealer","Engineer",
        "Call_Ref",
        "Start_Date","Start_Hour","Start_Min",
        "End_Date","End_Hour","End_Min"
    ]]

    # Clean text
    df["Engineer"] = df["Engineer"].astype(str).str.strip().str.upper()
    df["Dealer"] = df["Dealer"].astype(str).str.strip()
    df["Dealer"] = df["Dealer"].replace("nan", np.nan)
    def safe_mode(x):
        x = x.dropna()
        if x.empty:
            return "UNKNOWN"
        return x.mode().iloc[0]

    dealer_map = df.groupby("Engineer")["Dealer"].agg(safe_mode)
    df["Dealer"] = df["Dealer"].fillna(df["Engineer"].map(dealer_map))
    df["Company"] = df["Company"].astype(str).str.strip()
    df["State"] = df["State"].astype(str).str.strip()

    # Dates
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")
    df["End_Date"] = pd.to_datetime(df["End_Date"], errors="coerce")

    # Time
    df["Start_Hour"] = pd.to_numeric(df["Start_Hour"], errors="coerce").fillna(0)
    df["Start_Min"] = pd.to_numeric(df["Start_Min"], errors="coerce").fillna(0)

    df["End_Hour"] = pd.to_numeric(df["End_Hour"], errors="coerce").fillna(0)
    df["End_Min"] = pd.to_numeric(df["End_Min"], errors="coerce").fillna(0)

    # Datetime
    df["Actual_Start"] = df["Start_Date"] + pd.to_timedelta(df["Start_Hour"], unit="h") + pd.to_timedelta(df["Start_Min"], unit="m")
    df["Actual_End"] = df["End_Date"] + pd.to_timedelta(df["End_Hour"], unit="h") + pd.to_timedelta(df["End_Min"], unit="m")

    # Duration calculation (FIXED)
    df["Hours"] = (df["Actual_End"] - df["Actual_Start"]).dt.total_seconds() / 3600
    df["Hours"] = df["Hours"].clip(lower=0).fillna(0)

    # Delayed closure (>48 hrs)
    df["Delayed Closure"] = df["Hours"] > 48

    # Low duration calls (<1 hrs)
    df["Below 1hr Calls"] = df["Hours"] < 1
    df["Call Status"] = np.select(
        [
            df["Hours"] < 1,
            df["Hours"] > 48
        ],
        [
            "Below 1 Hour",
            "Delayed Closure"
        ],
        default="1-48 Hours"
    )

    # Cap hours at 8
    df["Hours_Capped"] = df["Hours"].clip(upper=8)
    # Display Time
    df["Start Time"] = df["Start_Hour"].astype(int).astype(str).str.zfill(2) + ":" + df["Start_Min"].astype(int).astype(str).str.zfill(2)
    df["End Time"] = df["End_Hour"].astype(int).astype(str).str.zfill(2) + ":" + df["End_Min"].astype(int).astype(str).str.zfill(2)

    # Format duration
    def format_duration(h):
        h_int = int(h)
        m = int(round((h - h_int) * 60))
        return f"{h_int}h {m}m"

    df["Recorded Duration"] = df["Hours"].apply(format_duration)
    df["Actual Duration (Adjusted)"] = df["Hours_Capped"].apply(
    lambda h: f"{int(h)}h {int(round((h%1)*60))}m"
    )
    return df
    
# ================= FILE =================

sidebar, divider, main = st.columns([0.68, 0.02, 6.7])
with divider:
    st.markdown(
        "<div class='sidebar-divider'></div>",
        unsafe_allow_html=True
    )
with main:

    h1 = st.container()

    with h1:
        st.markdown("""
        <div style="
        background:white;
        border-radius:26px;
        padding:14px 20px;
        border:1px solid #E9EDF5;
        box-shadow:0 4px 18px rgba(15,23,42,.05);
        ">

        <div style="
        display:flex;
        align-items:center;
        gap:20px;
        ">

        <div style="
        width:8px;
        height:58px;
        background:#EF233C;
        border-radius:20px;
        "></div>

        <div>

        <div style="
        font-size:26px;
        font-weight:700;
        color:#111827;
        ">
        Service Engineer Utilization Dashboard
        </div>

        <div style="
        margin-top:5px;
        color:#64748B;
        font-size:14px;
        ">
        Track performance across locations, states, dealers and engineers
        </div>

        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # ================= FILTERS =================
with sidebar:

    st.image(
        "assets/chicago-pneumatic.jpg",
        width=180
    )

    st.markdown(
        "<p style='font-size:14px;font-weight:600;color:#111827;margin-bottom:14px;margin-top:16px;'>Upload Excel File</p>",
        unsafe_allow_html=True
    )
    file = st.file_uploader(
        "",
        type=["xlsx"],
        label_visibility="collapsed"
    )
    if file is None:
        st.stop()
    df = load_data(file)

    data_min_date = df["Actual_Start"].min().date()
    data_max_date = df["Actual_Start"].max().date()


    st.markdown(
        "<p style='font-size:14px;font-weight:600;color:#111827;margin-bottom:15px;margin-top:16px;'>🔻 Filters</p>",
        unsafe_allow_html=True
    )

    company = st.multiselect(
        "Company Location",
        sorted(df["Company"].unique()),
        placeholder="All Locations"
    )

    state_source = df.copy()

    if company:
        state_source = state_source[
            state_source["Company"].isin(company)
        ]

    state = st.multiselect(
        "State",
        sorted(
            state_source["State"]
            .dropna()
            .unique()
        ),
        placeholder="All States"
    )

    dealer_source = df.copy()

    if company:
        dealer_source = dealer_source[
            dealer_source["Company"].isin(company)
        ]

    if state:
        dealer_source = dealer_source[
            dealer_source["State"].isin(state)
        ]

    dealer = st.multiselect(
        "Dealer",
        sorted(
            dealer_source["Dealer"]
            .dropna()
            .unique()
        ),
        placeholder="All Dealers"
    )
    engineer_source = df.copy()

    if company:
        engineer_source = engineer_source[
            engineer_source["Company"].isin(company)
        ]

    if state:
        engineer_source = engineer_source[
            engineer_source["State"].isin(state)
        ]

    if dealer:
        engineer_source = engineer_source[
            engineer_source["Dealer"].isin(dealer)
        ]

    engineer = st.multiselect(
        "Engineer",
        sorted(
            engineer_source["Engineer"]
            .dropna()
            .unique()
        ),
        placeholder="All Engineers"
    )

    start_date = st.date_input(
        "Start Date",
        value=data_min_date,
        min_value=data_min_date,
        max_value=data_max_date
    )

    end_date = st.date_input(
        "End Date",
        value=data_max_date,
        min_value=data_min_date,
        max_value=data_max_date
    )
    duration_filter = st.selectbox(
        "Duration Range",
        [
            "All",
            "0-1 Hour",
            "1-4 Hours",
            "4-8 Hours",
            "8-24 Hours",
            "24-48 Hours",
            "48+ Hours"
        ]
    )

# ================= FILTER =================
engineer_pool = df.copy()
filtered = df.copy()
if company:

    engineer_pool = engineer_pool[
        engineer_pool["Company"].isin(company)
    ]

    filtered = filtered[
        filtered["Company"].isin(company)
    ]

if state:

    engineer_pool = engineer_pool[
        engineer_pool["State"].isin(state)
    ]

    filtered = filtered[
        filtered["State"].isin(state)
    ]

if dealer:

    engineer_pool = engineer_pool[
        engineer_pool["Dealer"].isin(dealer)
    ]

    filtered = filtered[
        filtered["Dealer"].isin(dealer)
    ]
if engineer:

    engineer_pool = engineer_pool[
        engineer_pool["Engineer"].isin(engineer)
    ]

    filtered = filtered[
        filtered["Engineer"].isin(engineer)
    ]
    # Duration Filter

if duration_filter == "0-1 Hour":

    filtered = filtered[
        filtered["Hours"] < 1
    ]

elif duration_filter == "1-4 Hours":

    filtered = filtered[
        (filtered["Hours"] >= 1) &
        (filtered["Hours"] < 4)
    ]

elif duration_filter == "4-8 Hours":

    filtered = filtered[
        (filtered["Hours"] >= 4) &
        (filtered["Hours"] < 8)
    ]

elif duration_filter == "8-24 Hours":

    filtered = filtered[
        (filtered["Hours"] >= 8) &
        (filtered["Hours"] < 24)
    ]

elif duration_filter == "24-48 Hours":

    filtered = filtered[
        (filtered["Hours"] >= 24) &
        (filtered["Hours"] <= 48)
    ]

elif duration_filter == "48+ Hours":

    filtered = filtered[
        filtered["Hours"] > 48
    ]
filtered = filtered[
    (filtered["Actual_Start"].notna()) &
    (
        (filtered["Actual_Start"] >= pd.to_datetime(start_date)) &
        (filtered["Actual_Start"] <= pd.to_datetime(end_date))
    )
]

def calculate_active_days(start_date, end_date):
    total_days = 0
    
    current = pd.to_datetime(start_date).replace(day=1)
    end = pd.to_datetime(end_date)

    while current <= end:
        month_start = current
        month_end = (current + pd.offsets.MonthEnd(0))

        # overlap with selected range
        actual_start = max(month_start, pd.to_datetime(start_date))
        actual_end = min(month_end, end)

        days_in_range = (actual_end - actual_start).days + 1

        # cap at 24 per month
        total_days += min(days_in_range, 24)

        current = current + pd.DateOffset(months=1)

    return total_days
# ================= AVAILABILITY =================
active_days = calculate_active_days(start_date, end_date)
if active_days == 0:
    active_days = 1
available_hours = active_days * 8

# ================= AGG =================
data = filtered.groupby(
    ["Dealer", "Engineer"], dropna=False
)["Hours_Capped"].sum().reset_index()

data = data.rename(columns={"Hours_Capped": "Utilized Hours"})

# Visits
visits = filtered.groupby(
    ["Dealer", "Engineer"]
)["Call_Ref"].nunique().reset_index(name="Visits")

data = data.merge(visits, on=["Dealer", "Engineer"], how="left")

# Clean visits
data["Visits"] = data["Visits"].fillna(0)

# ---------------- Efficiency ----------------
data["Hours per Visit"] = data["Utilized Hours"] / data["Visits"]
data["Hours per Visit"] = data["Hours per Visit"].replace([np.inf, -np.inf], 0).fillna(0).round(2)

# ---------------- Capacity ----------------
data["Active Days"] = active_days
data["Available Hours"] = available_hours
data["Idle Hours"] = (data["Available Hours"] - data["Utilized Hours"]).clip(lower=0)
data["Time Utilization%"] = (
    data["Utilized Hours"] / data["Available Hours"] * 100
).replace([np.inf, -np.inf], 0).fillna(0).round(1)

data["Visits per Day"] = data["Visits"] / data["Active Days"]
data["Visits per Day"] = data["Visits per Day"].replace([np.inf, -np.inf], 0).fillna(0).round(2)

VISITS_PER_DAY_TARGET = 1
data["Expected Visits"] = data["Active Days"] * VISITS_PER_DAY_TARGET
data["Visit %"] = (
    data["Visits"] / data["Expected Visits"] * 100
)
data["Visit %"] = data["Visit %"].replace([np.inf, -np.inf], 0).fillna(0).round(1)

with main:
    if "show_util" not in st.session_state:
        st.session_state.show_util = False

    if "show_visits" not in st.session_state:
        st.session_state.show_visits = False

    if "show_dealer" not in st.session_state:
        st.session_state.show_dealer = False
    # ================= KPI =================
    st.markdown("""
    <div class="section-header">
    Performance Summary
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11 = st.columns(
        [1,1,1,1,1,1,1,1,1,1,1],
        gap=None
    )

    total_engineers = (
        engineer_pool["Engineer"]
        .dropna()
        .nunique()
    )
    active_engineers = data["Engineer"].nunique()
    all_engineers = set(
        engineer_pool["Engineer"]
        .dropna()
        .unique()
    )

    active_engineers_period = set(
        filtered["Engineer"]
        .dropna()
        .unique()
    )

    inactive_engineers = (
        all_engineers -
        active_engineers_period
    )

    inactive_df = (
        engineer_pool[
            engineer_pool["Engineer"].isin(
                inactive_engineers
            )
        ][
            ["Company", "Dealer", "Engineer"]
        ]
        .drop_duplicates(subset=["Engineer"])
        .sort_values("Engineer")
    )
    total_expected_visits = (
        total_engineers *
        active_days *
        VISITS_PER_DAY_TARGET
    )
    total_actual_visits = data["Visits"].sum()
    visit_pct = (
        total_actual_visits /
        total_expected_visits * 100
        if total_expected_visits > 0
        else 0
    )
    total_util = data["Utilized Hours"].sum()
    total_avail = active_days * 8 * total_engineers
    delayed_cases = filtered["Delayed Closure"].sum()
    low_duration_calls = filtered["Below 1hr Calls"].sum()
    normal_calls = (
        (filtered["Hours"] >= 1) &
        (filtered["Hours"] <= 48)
    ).sum()

    def card(icon, title, value, card_class=""):

        html = f"""
        <div class="kpi-box {card_class}">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{title}</div>
            <div class="kpi-number">{value}</div>
        </div>
        """

        st.markdown(
            html,
            unsafe_allow_html=True
        )
    with k1:
        card("👥", "Total Engineers", total_engineers)

    with k2:
        card("🧑‍🔧","Active Engineers", active_engineers)

    with k3:
        card("🕒","Available Hours", f"{int(total_avail):,}")

    with k4:
        card("⏱️","Utilized Hours", f"{round(total_util,1):,}")

    with k5:
        card(
            "📈",
            "Time Utilization",
            f"{(total_util/total_avail)*100:.1f}%",
            "kpi-orange"
        )

    with k6:
        card(
            "🎯",
            "Expected Visits",
            f"{int(total_expected_visits):,}"
        )
    with k7:
        card("👁️","Actual Visits", f"{int(total_actual_visits):,}")

    with k8:
        card(
            "📊",
            "Visit %",
            f"{visit_pct:.1f}%",
            "kpi-green"
        )
    with k9:
        card("📅","Active Days", active_days)

    with k10:
        card("⏳","Delayed Closures", int(delayed_cases))

    with k11:
        card("📞"," <1hr Calls", int(low_duration_calls))
    st.markdown("""
    <div class="section-header">
    Performance Insights
    </div>
    """, unsafe_allow_html=True)

    def style_chart(fig):

        fig.update_layout(
            title=None,

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                family="Inter",
                color="#111827",
                size=10
            ),

            margin=dict(
                l=5,
                r=40,
                t=0,
                b=0
            ),

            showlegend=False,
            bargap=0.01
            
        )

        return fig


    # ================= CHART DATA =================

    top_eng = data.sort_values("Time Utilization%", ascending=False).head(5)

    fig_rank = px.bar(
        top_eng,
        x="Time Utilization%",
        y="Engineer",
        orientation="h",
        text="Time Utilization%"
    )
    top_visit = data.sort_values(
        "Visits",
        ascending=False
    ).head(5)

    fig_visits = px.bar(
        top_visit,
        x="Visits",
        y="Engineer",
        orientation="h",
        text="Visits"
    )
    fig_visits.update_layout(
        yaxis={'categoryorder':'total ascending'}, height=180, xaxis_title=None, yaxis_title=None)
    fig_visits.update_traces(
        marker=dict(
            color="#F4A3A3",
            line=dict(
                color="#E58E8E",
                width=1
            )
        ),
        width=0.42,
        texttemplate="%{x}",
        textposition="outside",
        cliponaxis=False
    )

    fig_visits.update_xaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        title=None
    )
    fig_visits.update_yaxes(
        tickfont=dict(
            size=9,
            family="Arial Black"
        )
    )
    fig_rank.update_layout(yaxis={'categoryorder':'total ascending'}, height=180, xaxis_title=None, yaxis_title=None)
    fig_rank.update_traces(
        marker=dict(
            color="#F6B37A",
            line=dict(
                color="#E89A5D",
                width=1
            )
        ),
        width=0.42,
        texttemplate="%{x:.1f}%",
        textposition="outside",
        cliponaxis=False
    )
    fig_rank.update_xaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        title=None
    )
    fig_rank.update_yaxes(
        tickfont=dict(
            size=9,
            family="Arial Black"
        )
    )
    dealer_perf = data.groupby("Dealer").agg({
        "Utilized Hours":"sum",
        "Available Hours":"sum"
    }).reset_index()

    dealer_perf["Util %"] = (
        dealer_perf["Utilized Hours"] / dealer_perf["Available Hours"] * 100
    ).round(1)

    fig_dealer = px.bar(
        dealer_perf.sort_values(
            "Util %",
            ascending=False
        ).head(5),
        x="Dealer",
        y="Util %",
        text="Util %"
    )
    fig_dealer.update_layout(
        xaxis_tickangle=-25,
        height=180,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )
    fig_dealer.update_traces(
        width=0.55,
        marker=dict(
            color="#A9C2F5",
            line=dict(
                color="#8EAEEB",
                width=1
            )
        ),
        texttemplate="%{y:.1f}%",
        textposition="outside"
    )
    fig_dealer.update_xaxes(
        tickfont=dict(
            size=10,
            family="Arial Black"
        )
    )
    # APPLY COMMON CHART STYLE

    fig_rank = style_chart(fig_rank)
    fig_visits = style_chart(fig_visits)
    fig_dealer = style_chart(fig_dealer)

    fig_rank.update_layout(title="")
    fig_visits.update_layout(title="")
    fig_dealer.update_layout(title="")

    # ================= CHART LAYOUT =================

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            title_col, btn_col = st.columns([6,1])

            with title_col:
                st.markdown(
                    "<h6 style='margin:0;font-weight:600;'>🏅 Top Utilized Engineers</h6>",
                    unsafe_allow_html=True
                )

            with btn_col:
                util_btn_text = (
                    "View All ▴"
                    if st.session_state.show_util
                    else "View All ▾"
                )

                if st.button(
                    util_btn_text,
                    key="view_util",
                ):
                    st.session_state.show_util = not st.session_state.show_util
                    st.rerun()
            st.plotly_chart(
                fig_rank,
                use_container_width=True,
                config={"displayModeBar": False}
            )
            if st.session_state.show_util:

                st.dataframe(
                    data.sort_values(
                        "Time Utilization%",
                        ascending=False
                    )[
                        ["Engineer","Dealer","Time Utilization%"]
                    ],
                    use_container_width=True
                )

    with col2:

        with st.container(border=True):

            title_col, btn_col = st.columns([6,1])

            with title_col:
                st.markdown(
                    "<h6 style='margin:0;font-weight:600;'>📋 Most Visits</h6>",
                    unsafe_allow_html=True
                )
            with btn_col:
                visits_btn_text = (
                    "View All ▴"
                    if st.session_state.show_visits
                    else "View All ▾"
                )

                if st.button(
                    visits_btn_text,
                    key="view_visits",
                ):
                    st.session_state.show_visits = not st.session_state.show_visits
                    st.rerun()

            st.plotly_chart(
                fig_visits,
                use_container_width=True,
                config={"displayModeBar": False}
            )
            if st.session_state.show_visits:

                st.dataframe(
                    data.sort_values(
                        "Visits",
                        ascending=False
                    )[
                        ["Engineer","Dealer","Visits"]
                    ],
                    use_container_width=True
                )

    with col3:

        with st.container(border=True):

            title_col, btn_col = st.columns([6,1])

            with title_col:
                st.markdown(
                    "<h6 style='margin:0;font-weight:600;'>🏬 Dealer Utilization</h6>",
                    unsafe_allow_html=True
                )
            with btn_col:
                dealer_btn_text = (
                    "View All ▴"
                    if st.session_state.show_dealer
                    else "View All ▾"
                )

                if st.button(
                    dealer_btn_text,
                    key="view_dealer",
                ):
                    st.session_state.show_dealer = not st.session_state.show_dealer
                    st.rerun()

            st.plotly_chart(
                fig_dealer,
                use_container_width=True,
                config={"displayModeBar": False}
            )
            if st.session_state.show_dealer:

                st.dataframe(
                    dealer_perf.sort_values(
                        "Util %",
                        ascending=False
                    ),
                    use_container_width=True
                )
    # ================= TABLE =================
    st.markdown("""
    <div class="section-header">
    Engineer Utilization
    </div>
    """, unsafe_allow_html=True)

    display_data = data.sort_values(
        ["Time Utilization%","Utilized Hours"],
        ascending=[False, False]
    ).reset_index(drop=True)
    display_data.insert(0, "No.", display_data.index + 1)
    display_data = display_data[[
        "No.",
        "Dealer","Engineer",
        "Active Days","Available Hours","Utilized Hours","Idle Hours",
        "Visits","Hours per Visit","Visits per Day",
        "Time Utilization%"
    ]]

    display_data["Hours per Visit"] = display_data["Hours per Visit"].round(2)
    styled_df = (
        display_data.style
        .format({
            "Available Hours":"{:,.0f}",
            "Utilized Hours":"{:,.1f}",
            "Idle Hours":"{:,.1f}",
            "Hours per Visit":"{:,.2f}",
            "Visits per Day":"{:,.2f}",
            "Time Utilization%":"{:.1f}%"
        })
    )

    with st.container(border=True):

        st.data_editor(
            display_data,
            use_container_width=True,
            hide_index=True,
            disabled=True,
            height=250,
            row_height=34,

            column_config={

                "Available Hours":
                st.column_config.NumberColumn(
                    "Available Hours",
                    format="%d"
                ),

                "Utilized Hours":
                st.column_config.NumberColumn(
                    "Utilized Hours",
                    format="%.1f"
                ),

                "Idle Hours":
                st.column_config.NumberColumn(
                    "Idle Hours",
                    format="%.1f"
                ),

                "Visits":
                st.column_config.NumberColumn(
                    "Visits",
                    format="%d"
                ),

                "Time Utilization%":
                st.column_config.ProgressColumn(
                    "Time Utilization %",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%"
                )
            }
        )

    
    display_cols = [
        "Company",
        "State",
        "Dealer",
        "Engineer",
        "Start_Date",
        "Start Time",
        "End_Date",
        "End Time",
        "Recorded Duration",
        "Actual Duration (Adjusted)",
        "Call Status"
    ]

    details_df = filtered[display_cols].sort_values("Start_Date").reset_index(drop=True)
    details_df.insert(0, "No.", details_df.index + 1)
    styled_details = (
        details_df.style
        .set_properties(**{
            "font-size":"12px"
        })
    )
    title_col, filter_col = st.columns([4, 3])

    with title_col:
        st.markdown(
            "<div class='section-header'>Detailed Work Log</div>",
            unsafe_allow_html=True
        )

    with st.container(border=True):


        details_df = filtered[display_cols].sort_values(
            "Start_Date"
        ).reset_index(drop=True)

        details_df.insert(0, "No.", details_df.index + 1)


        def highlight_status(row):

            status = row["Call Status"]

            if status == "1-48 Hours":
                return ["background-color: #ECFDF3"] * len(row)

            elif status == "Below 1 Hour":
                return ["background-color: #FFFBEB"] * len(row)

            elif status == "Delayed Closure":
                return ["background-color: #FEF2F2"] * len(row)

            return [""] * len(row)


        styled_details = details_df.style.apply(
            highlight_status,
            axis=1
        )

        st.dataframe(
            styled_details,
            use_container_width=True,
            height=350,
            hide_index=True
        )
    st.markdown("""
    <div class="section-header">
        Inactive Engineers
        </div>
        """, unsafe_allow_html=True)
    inactive_df = inactive_df.reset_index(drop=True)

    inactive_df.insert(
        0,
        "No.",
        inactive_df.index + 1
    )
    with st.container(border=True):

        st.data_editor(
            inactive_df,
            use_container_width=True,
            hide_index=True,
            disabled=True,
            height=200,

            column_config={

                "No.": st.column_config.NumberColumn(
                    "No.",
                    width="small"
                ),

                "Company": st.column_config.TextColumn(
                    "Company",
                    width="large"
                ),

                "Dealer": st.column_config.TextColumn(
                    "Dealer",
                    width="large"
                ),

                "Engineer": st.column_config.TextColumn(
                    "Engineer",
                    width="large"
                )
            }
        )
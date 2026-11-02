
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from datetime import datetime, date
import json

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Road Intelligence | Andhra Pradesh",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path("road_accidents.csv")
NOTES_FILE = Path("road_notes.json")

# =====================================================
# ANDHRA PRADESH DISTRICTS
# =====================================================
AP_DISTRICTS = [
    "Alluri Sitharama Raju",
    "Anakapalli",
    "Ananthapuramu",
    "Annamayya",
    "Bapatla",
    "Chittoor",
    "Dr. B.R. Ambedkar Konaseema",
    "East Godavari",
    "Eluru",
    "Guntur",
    "Kakinada",
    "Krishna",
    "Kurnool",
    "Nandyal",
    "NTR",
    "Palnadu",
    "Parvathipuram Manyam",
    "Prakasam",
    "Sri Potti Sriramulu Nellore",
    "Sri Sathya Sai",
    "Srikakulam",
    "Tirupati",
    "Visakhapatnam",
    "Vizianagaram",
    "West Godavari",
    "YSR Kadapa",
]

# Illustrative city-to-district mapping.
# Verify administrative boundaries before production use.
AP_CITIES = {
    "Tirupati": "Tirupati",
    "Chittoor": "Chittoor",
    "Madanapalle": "Annamayya",
    "Vijayawada": "NTR",
    "Machilipatnam": "Krishna",
    "Guntur": "Guntur",
    "Tenali": "Guntur",
    "Amaravati": "Guntur",
    "Visakhapatnam": "Visakhapatnam",
    "Anakapalli": "Anakapalli",
    "Kakinada": "Kakinada",
    "Rajamahendravaram": "East Godavari",
    "Amalapuram": "Dr. B.R. Ambedkar Konaseema",
    "Eluru": "Eluru",
    "Bhimavaram": "West Godavari",
    "Nellore": "Sri Potti Sriramulu Nellore",
    "Ongole": "Prakasam",
    "Bapatla": "Bapatla",
    "Kurnool": "Kurnool",
    "Nandyal": "Nandyal",
    "Kadapa": "YSR Kadapa",
    "Proddatur": "YSR Kadapa",
    "Anantapur": "Ananthapuramu",
    "Hindupur": "Sri Sathya Sai",
    "Srikakulam": "Srikakulam",
    "Vizianagaram": "Vizianagaram",
    "Parvathipuram": "Parvathipuram Manyam",
    "Paderu": "Alluri Sitharama Raju",
    "Pithapuram": "Kakinada",
    "Narasaraopet": "Palnadu",
    "Mangalagiri": "Guntur",
}

# =====================================================
# THEMES
# =====================================================
THEMES = {
    "Light": {
        "bg": "#FFF9F0",
        "surface": "#FFFFFF",
        "surface2": "#FFF0E8",
        "text": "#40334A",
        "muted": "#817587",
        "border": "#EADFEA",
        "pink": "#F5B6C8",
        "yellow": "#FFE79A",
        "green": "#B9E6CF",
        "red": "#FFC1B9",
        "blue": "#BBDDF8",
        "purple": "#DCCCF8",
        "accent": "#8275DB",
        "navy": "#D7E3F8",
    },
    "Dark": {
        "bg": "#101827",
        "surface": "#19243A",
        "surface2": "#24314B",
        "text": "#F3F0FF",
        "muted": "#B5BCD0",
        "border": "#35425E",
        "pink": "#873E64",
        "yellow": "#796027",
        "green": "#185C4B",
        "red": "#843D46",
        "blue": "#254F7B",
        "purple": "#523D83",
        "accent": "#B6A1FF",
        "navy": "#263D64",
    }
}

# =====================================================
# SESSION STATE
# =====================================================
DEFAULTS = {
    "theme": "Light",
    "page": "Home",
    "history": [],
    "search": "",
    "notes": None,
    "selected_record": None,
    "flash": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

if st.session_state.notes is None:
    try:
        if NOTES_FILE.exists():
            st.session_state.notes = json.loads(
                NOTES_FILE.read_text(encoding="utf-8")
            )
        else:
            st.session_state.notes = []
    except (OSError, json.JSONDecodeError):
        st.session_state.notes = []

T = THEMES[st.session_state.theme]

# =====================================================
# CSS
# =====================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {{
    --bg:{T["bg"]};
    --surface:{T["surface"]};
    --surface2:{T["surface2"]};
    --text:{T["text"]};
    --muted:{T["muted"]};
    --border:{T["border"]};
    --accent:{T["accent"]};
}}

html, body, [class*="css"] {{
    font-family:'DM Sans',sans-serif;
}}

.stApp {{
    background:var(--bg);
    color:var(--text);
}}

[data-testid="stHeader"] {{
    background:transparent;
}}

[data-testid="stSidebar"] {{
    background:var(--surface);
    border-right:1px solid var(--border);
}}

[data-testid="stSidebar"] * {{
    color:var(--text);
}}

.block-container {{
    max-width:1500px;
    padding-top:1.6rem;
    padding-bottom:3rem;
}}

h1,h2,h3,h4 {{
    font-family:'Manrope',sans-serif;
    color:var(--text);
    font-weight:800;
}}

div[data-testid="stMetric"] {{
    background:var(--surface);
    border:1px solid var(--border);
    padding:20px;
    border-radius:20px;
    box-shadow:0 8px 28px rgba(30,30,60,.07);
    animation:fadeUp .5s ease both;
}}

.stButton>button {{
    border-radius:12px;
    border:1px solid var(--border);
    background:var(--surface);
    color:var(--text);
    font-weight:700;
    min-height:42px;
    transition:all .2s ease;
}}

.stButton>button:hover {{
    border-color:var(--accent);
    transform:translateY(-2px) scale(1.01);
}}

.stTextInput input,
.stTextArea textarea,
.stDateInput input {{
    border-radius:12px;
}}

.hero {{
    padding:30px;
    border-radius:25px;
    margin-bottom:22px;
    background:linear-gradient(
        120deg,
        {T["pink"]},
        {T["yellow"]},
        {T["green"]},
        {T["blue"]}
    );
    color:#34283E;
    animation:fadeUp .6s ease both;
}}

.hero h1 {{
    color:#34283E;
    font-size:clamp(28px,3vw,44px);
}}

.hero p {{
    color:#493B52;
}}

.card {{
    padding:22px;
    border:1px solid var(--border);
    border-radius:20px;
    background:var(--surface);
    margin-bottom:14px;
    box-shadow:0 8px 28px rgba(30,30,60,.05);
    animation:fadeUp .45s ease both;
    transition:transform .2s ease;
}}

.card:hover {{
    transform:translateY(-3px);
}}

.muted {{
    color:var(--muted);
    font-size:13px;
}}

.pill {{
    display:inline-block;
    border-radius:30px;
    padding:6px 12px;
    margin:3px;
    background:var(--surface2);
    font-size:12px;
    font-weight:700;
}}

[data-testid="stDataFrame"] {{
    border-radius:14px;
    overflow:hidden;
}}

@keyframes fadeUp {{
    from {{opacity:0;transform:translateY(12px)}}
    to {{opacity:1;transform:translateY(0)}}
}}

@media(prefers-reduced-motion:reduce) {{
    *,*::before,*::after {{
        animation:none!important;
        transition:none!important;
    }}
}}

.footer {{
    text-align:center;
    border-top:1px solid var(--border);
    padding-top:20px;
    margin-top:35px;
    color:var(--muted);
    font-size:12px;
}}
</style>
""", unsafe_allow_html=True)

# =====================================================
# PERSISTENT DATA
# =====================================================
COLUMNS = [
    "Accident_ID",
    "Accident_Date",
    "Accident_Time",
    "State",
    "District",
    "City",
    "Location",
    "Road_Type",
    "Vehicle_Type",
    "Severity",
    "Weather",
    "Casualties",
    "Fatalities",
    "Notes",
]

def make_demo_data():
    rng = np.random.default_rng(42)
    n = 350

    cities = list(AP_CITIES.keys())
    chosen = rng.choice(cities, n)

    rows = pd.DataFrame({
        "Accident_ID": [f"DEMO-{i+1:04d}" for i in range(n)],
        "Accident_Date": rng.choice(
            pd.date_range("2023-01-01", "2025-12-31"),
            n
        ),
        "Accident_Time": [
            f"{h:02d}:{m:02d}"
            for h, m in zip(
                rng.integers(0, 24, n),
                rng.integers(0, 60, n)
            )
        ],
        "State": "Andhra Pradesh",
        "District": [AP_CITIES[c] for c in chosen],
        "City": chosen,
        "Location": [
            f"{city} - Demo location {i % 8 + 1}"
            for i, city in enumerate(chosen)
        ],
        "Road_Type": rng.choice(
            ["Highway", "City Road", "Junction", "Rural Road"],
            n
        ),
        "Vehicle_Type": rng.choice(
            ["Motorcycle", "Car", "Bus", "Truck", "Auto"],
            n
        ),
        "Severity": rng.choice(
            ["Minor", "Serious", "Fatal"],
            n,
            p=[.57, .32, .11]
        ),
        "Weather": rng.choice(
            ["Clear", "Rainy", "Cloudy", "Foggy"],
            n
        ),
        "Casualties": rng.poisson(1.5, n),
        "Fatalities": rng.binomial(1, .08, n),
        "Notes": "Synthetic demo record",
    })

    return rows[COLUMNS]

def load_data():
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = np.nan
            return df[COLUMNS], "Saved project dataset"
        except Exception as exc:
            st.error(f"Dataset read error: {exc}")

    return make_demo_data(), "Synthetic demo dataset"

if "records_df" not in st.session_state:
    st.session_state.records_df, st.session_state.data_source = load_data()

def save_records(df):
    df = df[COLUMNS].copy()
    df.to_csv(DATA_FILE, index=False)
    st.session_state.records_df = df
    st.session_state.data_source = "Saved project dataset"

def save_notes():
    NOTES_FILE.write_text(
        json.dumps(st.session_state.notes, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

# =====================================================
# HELPERS
# =====================================================
def log_activity(message):
    st.session_state.history.insert(
        0,
        {
            "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            "message": str(message),
        }
    )
    st.session_state.history = st.session_state.history[:200]

def show_hero():
    st.markdown("""
    <div class="hero">
        <div class="pill">🚦 ANDHRA PRADESH · ROAD SAFETY</div>
        <h1>Road Intelligence</h1>
        <p>Understand accident patterns, explore districts and make
        data-informed road-safety decisions.</p>
        <span class="pill">📊 Analytics</span>
        <span class="pill">📍 District insights</span>
        <span class="pill">✨ Interactive dashboard</span>
    </div>
    """, unsafe_allow_html=True)

def style_chart(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T["text"], family="DM Sans"),
        margin=dict(l=15, r=20, t=55, b=25),
        clickmode="event+select",
    )
    return fig

def display_chart_details(df, chart_name):
    st.markdown(f"#### 🔍 {chart_name} — detailed records")
    st.caption("Select a category above or filter the records below.")
    st.dataframe(df, use_container_width=True, hide_index=True)

def calculate_zones(df, threshold):
    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby(["District", "City"], dropna=False)
        .size()
        .reset_index(name="Accident Records")
    )

    result["Zone"] = np.where(
        result["Accident Records"] >= threshold,
        "Red Zone",
        "Green Zone"
    )

    return result.sort_values("Accident Records", ascending=False)

# =====================================================
# SIDEBAR
# =====================================================
PAGES = [
    "Home",
    "Search",
    "Analytics",
    "Locations",
    "Red Zones",
    "Green Zones",
    "Traffic Signals",
    "History",
    "Dataset",
    "Add New",
    "Notes",
    "Settings",
    "Deploy",
]

ICONS = {
    "Home": "🏠",
    "Search": "🔎",
    "Analytics": "📊",
    "Locations": "📍",
    "Red Zones": "🔴",
    "Green Zones": "🟢",
    "Traffic Signals": "🚦",
    "History": "🕘",
    "Dataset": "📂",
    "Add New": "➕",
    "Notes": "📝",
    "Settings": "⚙️",
    "Deploy": "🚀",
}

with st.sidebar:
    st.markdown("# 🚦 Road Intelligence")
    st.caption("Andhra Pradesh Road Safety")
    st.markdown("---")

    for page in PAGES:
        if st.button(
            f"{ICONS[page]}  {page}",
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if st.session_state.page == page else "secondary",
        ):
            st.session_state.page = page
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎨 Appearance")

    theme = st.radio(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1,
        horizontal=True,
        key="sidebar_theme",
    )

    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()

    st.markdown("---")
    st.markdown("### 📥 Import data")

    uploaded = st.file_uploader(
        "CSV or Excel",
        type=["csv", "xlsx"],
        key="global_upload"
    )

    if uploaded is not None:
        try:
            new_data = (
                pd.read_excel(uploaded)
                if uploaded.name.lower().endswith(".xlsx")
                else pd.read_csv(uploaded)
            )

            st.session_state.import_preview = new_data

            if st.button("Import uploaded records", key="import_records"):
                new_data.columns = [
                    str(c).strip().replace(" ", "_")
                    for c in new_data.columns
                ]

                # Normalize common column names.
                aliases = {
                    "Date": "Accident_Date",
                    "Time": "Accident_Time",
                    "Region": "District",
                    "Area": "Location",
                    "Vehicle": "Vehicle_Type",
                    "Accident_Severity": "Severity",
                }

                new_data = new_data.rename(
                    columns={
                        c: aliases[c]
                        for c in new_data.columns
                        if c in aliases
                    }
                )

                for col in COLUMNS:
                    if col not in new_data.columns:
                        new_data[col] = np.nan

                new_data = new_data[COLUMNS]
                combined = pd.concat(
                    [st.session_state.records_df, new_data],
                    ignore_index=True
                )

                save_records(combined)
                log_activity(f"Imported file: {uploaded.name}")
                st.session_state.pop("import_preview", None)
                st.success("Records imported and saved.")
                st.rerun()

        except Exception as exc:
            st.error(f"Could not import file: {exc}")

# =====================================================
# GLOBAL FILTERS
# =====================================================
df = st.session_state.records_df.copy()

for col in COLUMNS:
    if col not in df.columns:
        df[col] = np.nan

df["District"] = df["District"].fillna("Unknown").astype(str)
df["City"] = df["City"].fillna("Unknown").astype(str)
df["Severity"] = df["Severity"].fillna("Unknown").astype(str)

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔎 Quick filters")

    district_options = sorted(df["District"].unique().tolist())
    chosen_districts = st.multiselect(
        "District",
        district_options,
        default=district_options,
        key="district_filter"
    )

    severity_options = sorted(df["Severity"].unique().tolist())
    chosen_severity = st.multiselect(
        "Severity",
        severity_options,
        default=severity_options,
        key="severity_filter"
    )

filtered = df.copy()

if chosen_districts:
    filtered = filtered[filtered["District"].isin(chosen_districts)]
else:
    filtered = filtered.iloc[0:0]

if chosen_severity:
    filtered = filtered[filtered["Severity"].isin(chosen_severity)]
else:
    filtered = filtered.iloc[0:0]

# =====================================================
# PAGE: HOME
# =====================================================
page = st.session_state.page

if page == "Home":
    show_hero()

    st.markdown("## 📍 Andhra Pradesh overview")
    st.caption(f"Data source: {st.session_state.data_source}")

    if "Synthetic" in st.session_state.data_source:
        st.warning(
            "Demo mode: displayed accident records are synthetic, "
            "not official Andhra Pradesh statistics."
        )

    a, b, c, d = st.columns(4)
    a.metric("🚘 Accident records", f"{len(filtered):,}")
    b.metric("🚨 Fatal-severity records", int(
        filtered["Severity"].str.lower().str.contains(
            "fatal|death|killed", regex=True
        ).sum()
    ))
    c.metric("🩹 Casualties", int(
        pd.to_numeric(filtered["Casualties"], errors="coerce").fillna(0).sum()
    ))
    d.metric("📍 Districts", filtered["District"].nunique())

    st.markdown("## 🗺️ District coverage")

    district_summary = (
        filtered.groupby("District")
        .size()
        .reset_index(name="Accident Records")
        .sort_values("Accident Records", ascending=False)
    )

    if not district_summary.empty:
        fig = px.bar(
            district_summary,
            x="District",
            y="Accident Records",
            color="Accident Records",
            color_continuous_scale=[
                T["green"], T["yellow"], T["red"]
            ],
            title="Accident records by district",
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

        chosen = st.selectbox(
            "View district details",
            district_summary["District"].tolist(),
            key="home_district_detail"
        )

        display_chart_details(
            filtered[filtered["District"] == chosen],
            chosen
        )

    st.markdown("## ✨ Quick actions")
    x, y, z = st.columns(3)

    with x:
        if st.button("➕ Add accident record", use_container_width=True):
            st.session_state.page = "Add New"
            st.rerun()

    with y:
        if st.button("🔴 View red zones", use_container_width=True):
            st.session_state.page = "Red Zones"
            st.rerun()

    with z:
        if st.button("📝 Write today's notes", use_container_width=True):
            st.session_state.page = "Notes"
            st.rerun()

# =====================================================
# PAGE: SEARCH
# =====================================================
elif page == "Search":
    show_hero()
    st.markdown("## 🔎 Search accident records")

    query = st.text_input(
        "Search city, district, severity, vehicle, date or road type",
        key="main_search",
        placeholder="Example: Tirupati, Motorcycle, Fatal"
    )

    if st.button("Search records", use_container_width=True):
        if query.strip():
            log_activity(f"Search: {query.strip()}")

        st.session_state.search_results_query = query.strip()

    query_to_use = st.session_state.get("search_results_query", "")

    if query_to_use:
        mask = filtered.astype(str).apply(
            lambda col: col.str.contains(
                query_to_use, case=False, na=False, regex=False
            )
        ).any(axis=1)

        results = filtered[mask]
        st.success(f"{len(results):,} matching records")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download search results",
            results.to_csv(index=False).encode("utf-8"),
            file_name="search_results.csv",
            mime="text/csv"
        )

        if not results.empty:
            selected_id = st.selectbox(
                "Select record for full details",
                results["Accident_ID"].astype(str).tolist()
            )

            st.json(
                results[
                    results["Accident_ID"].astype(str) == selected_id
                ].iloc[0].to_dict()
            )
    else:
        st.info("Enter a search term and click Search records.")

# =====================================================
# PAGE: ANALYTICS
# =====================================================
elif page == "Analytics":
    show_hero()
    st.markdown("## 📊 Analytics Studio")

    a, b = st.columns(2)

    with a:
        st.markdown("### Accident severity")

        severity_data = (
            filtered["Severity"].value_counts()
            .rename_axis("Severity")
            .reset_index(name="Records")
        )

        fig = px.pie(
            severity_data,
            names="Severity",
            values="Records",
            hole=.55,
            color_discrete_sequence=[
                T["green"], T["yellow"], T["red"], T["purple"]
            ],
        )
        st.plotly_chart(fig, use_container_width=True)

    with b:
        st.markdown("### Vehicle type")

        vehicle_data = (
            filtered["Vehicle_Type"].fillna("Unknown")
            .astype(str).value_counts()
            .rename_axis("Vehicle")
            .reset_index(name="Records")
        )

        fig = px.bar(
            vehicle_data,
            x="Vehicle",
            y="Records",
            color="Vehicle",
            color_discrete_sequence=[
                T["blue"], T["pink"], T["green"], T["yellow"], T["purple"]
            ],
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🕒 Accident trends")

    dated = filtered.copy()
    dated["_date"] = pd.to_datetime(
        dated["Accident_Date"], errors="coerce", dayfirst=True
    )
    dated = dated.dropna(subset=["_date"])

    if not dated.empty:
        dated["_month"] = dated["_date"].dt.to_period("M").astype(str)

        monthly = (
            dated.groupby("_month")
            .size()
            .reset_index(name="Records")
        )

        fig = px.area(
            monthly,
            x="_month",
            y="Records",
            markers=True,
            color_discrete_sequence=[T["accent"]],
        )
        st.plotly_chart(fig, use_container_width=True)

        month_choice = st.selectbox(
            "Inspect month",
            monthly["_month"].tolist()
        )

        display_chart_details(
            dated[dated["_month"] == month_choice],
            month_choice
        )
    else:
        st.info("No valid dates available for trend analysis.")

    st.markdown("### 🌦️ Risk-factor comparison")

    factor = st.selectbox(
        "Choose factor",
        ["Weather", "Road_Type", "Vehicle_Type", "District"]
    )

    risk_data = (
        filtered[factor].fillna("Unknown")
        .astype(str).value_counts()
        .rename_axis("Category")
        .reset_index(name="Records")
    )

    fig = px.bar(
        risk_data,
        x="Category",
        y="Records",
        color="Category",
        title=f"Accident records by {factor}",
    )
    st.plotly_chart(fig, use_container_width=True)

    selected_category = st.selectbox(
        "Click-equivalent: inspect a category",
        risk_data["Category"].tolist(),
        key="risk_category"
    )

    display_chart_details(
        filtered[
            filtered[factor].fillna("Unknown").astype(str)
            == selected_category
        ],
        selected_category
    )

    st.caption(
        "Interactive detail tables accompany the charts. "
        "Counts alone do not establish accident causation or individual risk."
    )

# =====================================================
# PAGE: LOCATIONS
# =====================================================
elif page == "Locations":
    show_hero()
    st.markdown("## 📍 District & city explorer")

    summary = (
        filtered.groupby(["District", "City"], dropna=False)
        .size()
        .reset_index(name="Accident Records")
        .sort_values("Accident Records", ascending=False)
    )

    st.dataframe(summary, use_container_width=True, hide_index=True)

    if not summary.empty:
        district = st.selectbox(
            "Select district",
            sorted(summary["District"].unique())
        )

        city_data = summary[summary["District"] == district]

        fig = px.bar(
            city_data,
            x="City",
            y="Accident Records",
            color="Accident Records",
            color_continuous_scale=[T["green"], T["yellow"], T["red"]]
        )

        st.plotly_chart(fig, use_container_width=True)

        city = st.selectbox("Select city", city_data["City"].tolist())

        display_chart_details(
            filtered[
                (filtered["District"] == district)
                & (filtered["City"] == city)
            ],
            f"{city}, {district}"
        )

# =====================================================
# PAGES: RED ZONES / GREEN ZONES
# =====================================================
elif page in ["Red Zones", "Green Zones"]:
    show_hero()

    is_red = page == "Red Zones"
    st.markdown(
        "## 🔴 Red Zone Analysis" if is_red
        else "## 🟢 Green Zone Analysis"
    )

    st.caption(
        "These are dataset-based classifications, not official government "
        "designations or verified per-kilometre safety-risk ratings."
    )

    threshold = st.number_input(
        "Accident-record threshold",
        min_value=1,
        max_value=100000,
        value=10,
        step=1,
    )

    zones = calculate_zones(filtered, threshold)

    if not zones.empty:
        desired = "Red Zone" if is_red else "Green Zone"

        shown = zones[zones["Zone"] == desired]

        if shown.empty:
            st.info(
                "No locations match this threshold in the currently filtered dataset."
            )
        else:
            st.metric("Locations in this category", len(shown))

            fig = px.bar(
                shown.head(30).sort_values("Accident Records"),
                x="Accident Records",
                y="City",
                color="Accident Records",
                orientation="h",
                color_continuous_scale=(
                    ["#651E2E", "#E54D61"] if is_red
                    else ["#176447", "#77D6A5"]
                ),
                title=f"{desired} — recorded accident counts"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                shown,
                use_container_width=True,
                hide_index=True
            )

            selected_city = st.selectbox(
                "Inspect location records",
                shown["City"].tolist()
            )

            display_chart_details(
                filtered[filtered["City"] == selected_city],
                selected_city
            )

            st.download_button(
                f"Download {desired} locations",
                shown.to_csv(index=False).encode("utf-8"),
                file_name=f"{desired.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No records available.")

# =====================================================
# PAGE: TRAFFIC SIGNALS
# =====================================================
elif page == "Traffic Signals":
    show_hero()
    st.markdown("## 🚦 Traffic signal studio")

    signal = st.selectbox(
        "Choose a signal",
        ["🔴 Red — Stop", "🟡 Yellow — Prepare", "🟢 Green — Proceed safely"]
    )

    messages = {
        "🔴 Red — Stop": (
            "#F39B91",
            "STOP",
            "Stop before the line and wait for a permitted signal."
        ),
        "🟡 Yellow — Prepare": (
            "#F7D774",
            "PREPARE",
            "Slow down safely and prepare to stop where appropriate."
        ),
        "🟢 Green — Proceed safely": (
            "#A9DCC4",
            "PROCEED SAFELY",
            "Check the junction and pedestrians before proceeding."
        ),
    }

    colour, title, message = messages[signal]

    st.markdown(
        f"""
        <div class="card" style="background:{colour};color:#30273A;">
            <h1 style="color:#30273A;">🚦 {title}</h1>
            <p style="color:#30273A;font-size:17px;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("This is an educational illustration, not a live traffic-signal feed.")

# =====================================================
# PAGE: HISTORY
# =====================================================
elif page == "History":
    show_hero()
    st.markdown("## 🕘 Search & activity history")

    if not st.session_state.history:
        st.info("No recent activity yet.")
    else:
        for item in st.session_state.history:
            st.markdown(
                f"""
                <div class="card">
                    <b>🔎 {item["message"]}</b>
                    <div class="muted">{item["time"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("🧹 Clear history"):
            st.session_state.history = []
            st.rerun()

    st.caption("History lasts for the current app session.")

# =====================================================
# PAGE: DATASET
# =====================================================
elif page == "Dataset":
    show_hero()
    st.markdown("## 📂 Dataset management")

    d1, d2, d3, d4 = st.columns(4)

    d1.metric("Rows", len(df))
    d2.metric("Columns", len(df.columns))
    d3.metric("Missing cells", int(df.isna().sum().sum()))
    d4.metric("Duplicate rows", int(df.duplicated().sum()))

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.markdown("### 🧪 Data quality")

    quality = pd.DataFrame({
        "Column": df.columns,
        "Data type": [str(df[c].dtype) for c in df.columns],
        "Missing": [int(df[c].isna().sum()) for c in df.columns],
        "Unique": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })

    st.dataframe(quality, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download dataset",
        df.to_csv(index=False).encode("utf-8"),
        file_name="road_intelligence_dataset.csv",
        mime="text/csv"
    )

    st.warning(
        "The CSV stored locally is suitable for a single-user demo. "
        "For a public multi-user deployment, use a database."
    )

# =====================================================
# PAGE: ADD NEW
# =====================================================
elif page == "Add New":
    show_hero()
    st.markdown("## ➕ Add a new accident record")

    with st.form("add_record_form", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            accident_date = st.date_input(
                "Accident date",
                value=date.today()
            )

            accident_time = st.time_input(
                "Accident time"
            )

            district = st.selectbox(
                "District",
                AP_DISTRICTS
            )

            cities_for_district = [
                city for city, dist in AP_CITIES.items()
                if dist == district
            ]

            city = st.selectbox(
                "City",
                cities_for_district if cities_for_district else ["Other"]
            )

            location = st.text_input("Road / location name")

            road_type = st.selectbox(
                "Road type",
                ["Highway", "City Road", "Junction", "Rural Road", "Residential"]
            )

        with c2:
            vehicle = st.selectbox(
                "Vehicle type",
                ["Motorcycle", "Car", "Bus", "Truck", "Auto", "Other"]
            )

            severity = st.selectbox(
                "Severity",
                ["Minor", "Serious", "Fatal", "Unknown"]
            )

            weather = st.selectbox(
                "Weather",
                ["Clear", "Rainy", "Cloudy", "Foggy", "Unknown"]
            )

            casualties = st.number_input(
                "Casualties",
                min_value=0,
                max_value=10000,
                value=0
            )

            fatalities = st.number_input(
                "Fatalities",
                min_value=0,
                max_value=10000,
                value=0
            )

            notes = st.text_area("Additional notes")

        submitted = st.form_submit_button(
            "💾 Save accident record",
            use_container_width=True
        )

    if submitted:
        if fatalities > casualties:
            st.error("Fatalities cannot exceed the entered casualty count.")
        elif not location.strip():
            st.error("Please enter the road or location name.")
        else:
            new_record = {
                "Accident_ID": f"AP-{datetime.now():%Y%m%d%H%M%S%f}",
                "Accident_Date": accident_date.isoformat(),
                "Accident_Time": accident_time.strftime("%H:%M"),
                "State": "Andhra Pradesh",
                "District": district,
                "City": city,
                "Location": location.strip(),
                "Road_Type": road_type,
                "Vehicle_Type": vehicle,
                "Severity": severity,
                "Weather": weather,
                "Casualties": casualties,
                "Fatalities": fatalities,
                "Notes": notes.strip(),
            }

            updated = pd.concat(
                [
                    st.session_state.records_df,
                    pd.DataFrame([new_record])
                ],
                ignore_index=True
            )

            save_records(updated)
            log_activity(f"Added record: {new_record['Accident_ID']}")

            st.success("Accident record saved successfully!")
            st.rerun()

# =====================================================
# PAGE: NOTES
# =====================================================
elif page == "Notes":
    show_hero()
    st.markdown("## 📝 Personal notes")

    st.caption("Save today's observations, reminders and project ideas.")

    with st.form("notes_form", clear_on_submit=True):
        note_title = st.text_input(
            "Note title",
            placeholder="Example: Today's accident analysis"
        )

        note_date = st.date_input(
            "Note date",
            value=date.today()
        )

        note_text = st.text_area(
            "Write your note",
            height=180,
            placeholder="What did you observe today?"
        )

        save_note = st.form_submit_button(
            "💾 Save note",
            use_container_width=True
        )

    if save_note:
        if not note_title.strip() or not note_text.strip():
            st.error("Please enter both a title and note content.")
        else:
            st.session_state.notes.insert(
                0,
                {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                    "title": note_title.strip(),
                    "date": note_date.isoformat(),
                    "text": note_text.strip(),
                }
            )

            save_notes()
            st.success("Note saved!")
            st.rerun()

    st.markdown("### 📚 Saved notes")

    if not st.session_state.notes:
        st.info("Your notes will appear here.")
    else:
        for note in st.session_state.notes:
            with st.expander(
                f"📝 {note['title']} — {note['date']}"
            ):
                st.write(note["text"])

                if st.button(
                    "🗑️ Delete note",
                    key=f"delete_{note['id']}"
                ):
                    st.session_state.notes = [
                        n for n in st.session_state.notes
                        if n["id"] != note["id"]
                    ]

                    save_notes()
                    st.rerun()

# =====================================================
# PAGE: SETTINGS
# =====================================================
elif page == "Settings":
    show_hero()
    st.markdown("## ⚙️ Workspace settings")

    theme = st.radio(
        "Appearance",
        ["Light", "Dark"],
        horizontal=True,
        index=0 if st.session_state.theme == "Light" else 1,
        key="settings_theme_choice",
    )

    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()

    st.markdown("### 📊 Data settings")
    st.write(f"**Source:** {st.session_state.data_source}")
    st.write(f"**Records:** {len(df):,}")

    st.markdown("### 🔄 Maintenance")

    if st.button("Reset district and severity filters"):
        for key in ["district_filter", "severity_filter"]:
            st.session_state.pop(key, None)

        st.rerun()

    if st.button("Export complete dataset"):
        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="road_intelligence_backup.csv",
            mime="text/csv"
        )

    st.markdown("### ℹ️ About")

    st.markdown("""
    <div class="card">
        <h3>Road Intelligence</h3>
        <p class="muted">
        Andhra Pradesh road accident data exploration system.
        Built with Python, Streamlit, Pandas, NumPy and Plotly.
        </p>
        <p class="muted">
        Use verified and anonymised records for real analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PAGE: DEPLOY
# =====================================================
elif page == "Deploy":
    show_hero()
    st.markdown("## 🚀 Deploy your application")

    st.markdown("""
    ### Step 1 — Prepare requirements.txt

    ```text
    streamlit
    pandas
    numpy
    plotly
    openpyxl
    ```

    ### Step 2 — Test locally

    ```bash
    python -m pip install -r requirements.txt
    python -m streamlit run proj.py
    ```

    ### Step 3 — Publish online

    1. Create a GitHub repository.
    2. Upload `proj.py` and `requirements.txt`.
    3. Open Streamlit Community Cloud.
    4. Connect your repository.
    5. Select `proj.py` as the app entry point.
    6. Deploy.

    ### Important

    The current CSV and JSON files are local storage. A cloud deployment
    may not preserve changes reliably across restarts or multiple users.
    Use a persistent database for production.
    """)

    st.info(
        "Before deployment, use anonymised records and verify that "
        "your dataset can legally be published."
    )

# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div class="footer">
    <h3>🚦 Road Intelligence</h3>
    <p>Read the patterns. Understand the risks. Make roads safer.</p>
    <p>Python · Streamlit · Pandas · NumPy · Plotly</p>
    <p>Zone labels are dataset-based, not official government designations.</p>
</div>
""", unsafe_allow_html=True)

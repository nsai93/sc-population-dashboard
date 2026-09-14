import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Scheduled Caste Population Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COLOR PALETTE
# ============================================================

NAVY = "#141C33"
NAVY_LIGHT = "#1E2A4A"
INK = "#17233F"
MUTED = "#6B7688"
BORDER = "#E5E8F0"
BG = "#F4F6FB"

TEAL = "#2F8F83"
AMBER = "#E39A45"
INDIGO = "#4C6FFF"
CORAL = "#DA5A6A"

CHART_PALETTE = ["#4C6FFF", "#2F8F83", "#E39A45", "#DA5A6A", "#8C6FE0", "#3FA7D6"]


# ============================================================
# CUSTOM CSS
# ============================================================
# NOTE: every HTML fragment rendered below via st.markdown is built as a
# SINGLE-LINE string (no embedded newlines, no leading indentation).
# Multi-line indented HTML inside st.markdown gets misparsed by the
# Markdown engine (a blank line ends the HTML block, and the following
# indented lines are then treated as a code block) -- that was the root
# cause of the raw "<div class=...>" text showing up on the old dashboard.

st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');"
    "html, body, [class*='css']{font-family:'Inter',sans-serif;}"
    ".stApp{background-color:" + BG + ";}"
    ".main .block-container{max-width:1500px;padding:2rem 3rem 3rem;}"
    "#MainMenu, footer{visibility:hidden;}"

    # ---------- SIDEBAR ----------
    "section[data-testid='stSidebar']{background:linear-gradient(180deg," + NAVY + " 0%," + NAVY_LIGHT + " 100%);}"
    "section[data-testid='stSidebar'] .block-container{padding-top:1.6rem;}"
    "section[data-testid='stSidebar'] label{color:#C7CFE2 !important;font-weight:600;font-size:13px;letter-spacing:.02em;text-transform:uppercase;}"
    "section[data-testid='stSidebar'] .stMarkdown p{color:#C7CFE2;}"
    "section[data-testid='stSidebar'] hr{border-color:#2B3860;}"

    # Selectbox control itself: force a legible WHITE box with DARK text
    # (fixes the white-on-white invisible text bug)
    "section[data-testid='stSidebar'] div[data-baseweb='select'] > div{"
    "background-color:#FFFFFF;border-radius:10px;border:1px solid #2B3860;min-height:44px;}"
    "section[data-testid='stSidebar'] div[data-baseweb='select'] *{color:" + INK + " !important;fill:" + INK + " !important;}"
    "section[data-testid='stSidebar'] div[data-baseweb='select'] input{color:" + INK + " !important;}"

    # The dropdown menu is rendered in a portal at the body level, so it
    # must be styled globally, not scoped to the sidebar.
    "div[data-baseweb='popover'] ul{background-color:#FFFFFF !important;border-radius:10px;overflow:hidden;}"
    "div[data-baseweb='popover'] li{color:" + INK + " !important;font-size:14px;}"
    "div[data-baseweb='popover'] li:hover{background-color:#EEF1FA !important;}"

    # ---------- SIDEBAR BRAND ----------
    ".brand-title{font-size:24px;font-weight:800;color:#FFFFFF;margin-bottom:2px;letter-spacing:-.01em;}"
    ".brand-sub{font-size:13px;color:#9AA6C4;margin-bottom:26px;}"

    # ---------- HEADERS ----------
    ".dashboard-title{font-size:38px;font-weight:800;color:" + INK + ";line-height:1.2;margin-bottom:4px;letter-spacing:-.02em;}"
    ".dashboard-subtitle{font-size:16px;color:" + MUTED + ";margin-bottom:26px;}"
    ".section-title{font-size:21px;font-weight:700;color:" + INK + ";margin-top:6px;margin-bottom:2px;}"
    ".section-subtitle{font-size:14px;color:" + MUTED + ";margin-bottom:16px;}"

    # ---------- KPI CARDS ----------
    ".kpi-card{background:#FFFFFF;border:1px solid " + BORDER + ";border-radius:16px;padding:20px 22px;min-height:132px;"
    "box-shadow:0 2px 10px rgba(20,28,51,0.04);transition:box-shadow .15s ease,transform .15s ease;}"
    ".kpi-card:hover{box-shadow:0 8px 22px rgba(20,28,51,0.09);transform:translateY(-1px);}"
    ".kpi-top{display:flex;align-items:center;gap:8px;margin-bottom:10px;}"
    ".kpi-dot{width:9px;height:9px;border-radius:50%;display:inline-block;}"
    ".kpi-label{font-size:12.5px;color:" + MUTED + ";font-weight:700;letter-spacing:.04em;text-transform:uppercase;}"
    ".kpi-value{font-size:27px;font-weight:800;color:" + INK + ";line-height:1.2;}"
    ".kpi-small{font-size:13px;color:" + MUTED + ";margin-top:6px;}"

    # ---------- STATE HERO ----------
    ".state-hero{background:linear-gradient(135deg," + NAVY + " 0%," + NAVY_LIGHT + " 100%);border-radius:18px;"
    "padding:26px 30px;margin-bottom:22px;box-shadow:0 10px 28px rgba(20,28,51,0.14);"
    "display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;}"
    ".state-name{color:#FFFFFF;font-size:32px;font-weight:800;margin-bottom:3px;letter-spacing:-.01em;}"
    ".state-description{color:#B9C2DE;font-size:14.5px;}"
    ".state-badge{background:rgba(255,255,255,0.12);color:#FFFFFF;padding:7px 14px;border-radius:20px;font-size:13px;font-weight:600;}"

    # ---------- CHART CARDS ----------
    ".chart-card{background:#FFFFFF;border:1px solid " + BORDER + ";border-radius:16px;padding:18px 20px 6px;"
    "box-shadow:0 2px 10px rgba(20,28,51,0.04);margin-bottom:20px;}"
    ".chart-header{font-size:17px;font-weight:700;color:" + INK + ";margin-bottom:1px;}"
    ".chart-description{font-size:13px;color:" + MUTED + ";margin-bottom:6px;}"

    # ---------- TABLES ----------
    "div[data-testid='stDataFrame']{border:1px solid " + BORDER + ";border-radius:14px;overflow:hidden;}"

    # ---------- FOOTER ----------
    ".footer{text-align:center;color:" + MUTED + ";font-size:12.5px;padding-top:22px;border-top:1px solid " + BORDER + ";margin-top:10px;}"

    # ---------- MOBILE ----------
    "@media (max-width:900px){.main .block-container{padding-left:1rem;padding-right:1rem;}"
    ".dashboard-title{font-size:28px;}.state-name{font-size:26px;}}"

    "</style>",
    unsafe_allow_html=True
)


# ============================================================
# HTML HELPERS (all single-line -> always render correctly)
# ============================================================

def render(html_string):
    st.markdown(html_string, unsafe_allow_html=True)


def kpi_card(label, value, small, accent=INDIGO, value_size=None):
    size_style = f"font-size:{value_size}px;" if value_size else ""
    return (
        '<div class="kpi-card">'
        f'<div class="kpi-top"><span class="kpi-dot" style="background:{accent}"></span>'
        f'<span class="kpi-label">{label}</span></div>'
        f'<div class="kpi-value" style="{size_style}">{value}</div>'
        f'<div class="kpi-small">{small}</div>'
        '</div>'
    )


def section_header(title, subtitle):
    return (
        f'<div class="section-title">{title}</div>'
        f'<div class="section-subtitle">{subtitle}</div>'
    )


def chart_header(title, subtitle):
    return (
        f'<div class="chart-header">{title}</div>'
        f'<div class="chart-description">{subtitle}</div>'
    )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = "data/sc_population.csv"

    data = pd.read_csv(file_path)

    data.columns = data.columns.astype(str).str.strip()

    for column in data.columns:
        if data[column].dtype == "object":
            data[column] = data[column].astype(str).str.strip()

    data["State"] = data["State"].astype(str).str.strip()
    data["SC Name"] = data["SC Name"].astype(str).str.strip()

    if "SC Code" in data.columns:
        data["SC Code"] = (
            data["SC Code"]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.zfill(3)
        )

    return data


df = load_data()


# ============================================================
# FIND POPULATION COLUMN
# ============================================================

possible_population_columns = [
    "Total Population",
    "Population",
    "SC Population",
    "SC_Population",
    "Scheduled Caste Population",
    "Scheduled_Caste_Population",
    "Total_Population"
]

population_column = None

for column in possible_population_columns:
    if column in df.columns:
        population_column = column
        break

if population_column is None:
    st.error("Population column was not found in data/sc_population.csv.")
    st.stop()

df[population_column] = pd.to_numeric(df[population_column], errors="coerce").fillna(0)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = ["State", "SC Name"]
missing_columns = [c for c in required_columns if c not in df.columns]

if missing_columns:
    st.error("Missing required column(s): " + ", ".join(missing_columns))
    st.stop()


# ============================================================
# INDIAN NUMBER FORMAT
# ============================================================

def indian_number(value):

    try:
        number = int(round(float(value)))
    except Exception:
        return "0"

    sign = "-" if number < 0 else ""
    number_string = str(abs(number))

    if len(number_string) <= 3:
        return sign + number_string

    last_three = number_string[-3:]
    remaining = number_string[:-3]
    parts = []

    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        parts.insert(0, remaining)

    return sign + ",".join(parts) + "," + last_three


# ============================================================
# BASIC DATA SUMMARY
# ============================================================

states = sorted(df["State"].dropna().unique().tolist())
loaded_states = len(states)
total_categories = df["SC Name"].nunique()
total_population = int(df[population_column].sum())


# ============================================================
# SIDEBAR
# ============================================================

render(
    '<div class="brand-title">📊 SC Dashboard</div>'
    '<div class="brand-sub">Census 2011 Population Explorer</div>'
)

st.sidebar.markdown("**Select State**")

state_options = ["All India"] + states

selected_state = st.sidebar.selectbox(
    "State / UT",
    state_options,
    index=0
)

if selected_state == "All India":
    state_filtered_df = df.copy()
else:
    state_filtered_df = df[df["State"] == selected_state].copy()

available_sc_categories = sorted(
    state_filtered_df["SC Name"].dropna().unique().tolist()
)

sc_options = ["All Scheduled Castes"] + available_sc_categories

selected_sc = st.sidebar.selectbox(
    "Scheduled Caste Category",
    sc_options
)

if selected_sc == "All Scheduled Castes":
    selected_df = state_filtered_df.copy()
else:
    selected_df = state_filtered_df[state_filtered_df["SC Name"] == selected_sc].copy()

st.sidebar.markdown("---")
st.sidebar.caption("Source: Census of India 2011")


# ============================================================
# INDIA OVERVIEW
# ============================================================

if selected_state == "All India":

    render(
        '<div class="dashboard-title">Scheduled Caste Population Dashboard — India</div>'
        '<div class="dashboard-subtitle">Census 2011 · Scheduled Caste Population Statistics</div>'
    )

    largest_row = df.loc[df[population_column].idxmax()]
    largest_category = largest_row["SC Name"]
    largest_state = largest_row["State"]
    largest_population = int(largest_row[population_column])

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        render(kpi_card(
            "States / UTs Loaded", loaded_states,
            "States and Union Territories", accent=INDIGO
        ))

    with k2:
        render(kpi_card(
            "Total SC Population", indian_number(total_population),
            "Across all loaded states / UTs", accent=TEAL
        ))

    with k3:
        render(kpi_card(
            "SC Categories", indian_number(total_categories),
            "Unique Scheduled Caste groups", accent=AMBER
        ))

    with k4:
        render(kpi_card(
            "Largest SC Category", largest_category,
            f"{largest_state} · {indian_number(largest_population)}",
            accent=CORAL, value_size=19
        ))

    st.markdown("<br>", unsafe_allow_html=True)

    state_summary = (
        df.groupby("State", as_index=False)[population_column]
        .sum()
        .rename(columns={population_column: "SC Population"})
        .sort_values("SC Population", ascending=False)
        .reset_index(drop=True)
    )
    state_summary.insert(0, "Rank", range(1, len(state_summary) + 1))

    left_chart, right_chart = st.columns([1.55, 1])

    with left_chart:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        render(chart_header("SC Population by State / UT", "Ranked from highest to lowest population"))

        chart_df = state_summary.copy()
        chart_df["Display Population"] = chart_df["SC Population"].apply(indian_number)

        fig = px.bar(
            chart_df, x="SC Population", y="State",
            orientation="h", text="Display Population"
        )
        fig.update_traces(
            marker_color=INDIGO,
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>SC Population: %{x:,}<extra></extra>"
        )
        fig.update_layout(
            height=480,
            margin=dict(l=10, r=70, t=10, b=30),
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter, Arial", color=INK),
            xaxis=dict(title="SC Population", tickformat=",", gridcolor="#EEF1F7"),
            yaxis=dict(title="", autorange="reversed"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right_chart:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        render(chart_header("Top 5 States vs Remaining", "Share of loaded SC population"))

        top5 = state_summary.head(5).copy()
        remaining_population = int(state_summary.iloc[5:]["SC Population"].sum())

        donut_labels = top5["State"].tolist()
        donut_values = top5["SC Population"].tolist()

        if remaining_population > 0:
            donut_labels.append("Remaining States / UTs")
            donut_values.append(remaining_population)

        donut = go.Figure(data=[go.Pie(
            labels=donut_labels, values=donut_values, hole=0.62,
            textinfo="percent",
            marker=dict(colors=CHART_PALETTE + ["#C9CFDE"]),
            hovertemplate="<b>%{label}</b><br>Population: %{value:,}<br>Share: %{percent}<extra></extra>"
        )])
        donut.update_layout(
            height=480,
            margin=dict(l=10, r=10, t=10, b=70),
            paper_bgcolor="white",
            font=dict(family="Inter, Arial", color=INK),
            legend=dict(orientation="h", yanchor="bottom", y=-0.20, xanchor="center", x=0.5)
        )
        st.plotly_chart(donut, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    render(section_header(
        "State / UT Population Summary",
        "Total Scheduled Caste population by loaded State / UT"
    ))

    display_state_summary = state_summary.copy()
    display_state_summary["SC Population"] = display_state_summary["SC Population"].apply(indian_number)

    st.dataframe(display_state_summary, use_container_width=True, hide_index=True, height=500)


# ============================================================
# STATE PAGE
# ============================================================

else:

    state_data = (
        df[df["State"] == selected_state]
        .copy()
        .sort_values(population_column, ascending=False)
    )

    state_total_population = int(state_data[population_column].sum())
    state_category_count = state_data["SC Name"].nunique()

    largest_state_row = state_data.loc[state_data[population_column].idxmax()]
    largest_state_category = largest_state_row["SC Name"]
    largest_state_category_population = int(largest_state_row[population_column])

    selected_population = int(selected_df[population_column].sum())

    render(
        '<div class="state-hero">'
        '<div><div class="state-name">' + str(selected_state) + '</div>'
        '<div class="state-description">Census 2011 · Scheduled Caste Population Statistics</div></div>'
        '<div class="state-badge">' + str(state_category_count) + ' SC categories</div>'
        '</div>'
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        render(kpi_card(
            "Total SC Population", indian_number(state_total_population),
            selected_state, accent=INDIGO
        ))

    with k2:
        render(kpi_card(
            "SC Categories", state_category_count,
            "Scheduled Caste groups", accent=TEAL
        ))

    with k3:
        render(kpi_card(
            "Largest SC Category", largest_state_category,
            indian_number(largest_state_category_population),
            accent=AMBER, value_size=19
        ))

    with k4:
        if selected_sc == "All Scheduled Castes":
            metric_label = "Selected Population"
            metric_value = state_total_population
            metric_description = "All Scheduled Castes"
        else:
            metric_label = "Selected Population"
            metric_value = selected_population
            metric_description = selected_sc

        render(kpi_card(
            metric_label, indian_number(metric_value),
            metric_description, accent=CORAL
        ))

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # IF CATEGORY SELECTED
    # --------------------------------------------------------

    if selected_sc != "All Scheduled Castes":

        render(section_header(
            selected_sc,
            f"Detailed population records for {selected_state}"
        ))

        caste_data = selected_df.copy()

        preferred_columns = ["SC Code", "SC Name", population_column]
        existing_preferred_columns = [c for c in preferred_columns if c in caste_data.columns]
        remaining_columns = [c for c in caste_data.columns if c not in existing_preferred_columns]

        caste_data = caste_data[existing_preferred_columns + remaining_columns]

        rename_map = {
            "SC Code": "SC Code",
            "SC Name": "Scheduled Caste",
            population_column: "Population"
        }
        caste_data = caste_data.rename(columns=rename_map)

        if "Population" in caste_data.columns:
            caste_data["Population"] = caste_data["Population"].apply(indian_number)

        st.dataframe(caste_data, use_container_width=True, hide_index=True, height=500)

    # --------------------------------------------------------
    # ALL SC CATEGORIES STATE VIEW
    # --------------------------------------------------------

    else:

        category_summary = (
            state_data.groupby("SC Name", as_index=False)[population_column]
            .sum()
            .rename(columns={population_column: "Population"})
            .sort_values("Population", ascending=False)
            .reset_index(drop=True)
        )
        category_summary.insert(0, "Rank", range(1, len(category_summary) + 1))

        left_chart, right_chart = st.columns([1.25, 1])

        with left_chart:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            render(chart_header("Top 10 SC Groups by Population", "Largest Scheduled Caste groups in this state"))

            top10 = category_summary.head(10).sort_values("Population", ascending=True).copy()
            top10["Display Population"] = top10["Population"].apply(indian_number)

            fig = px.bar(top10, x="Population", y="SC Name", orientation="h", text="Display Population")
            fig.update_traces(
                marker_color=TEAL,
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Population: %{x:,}<extra></extra>"
            )
            fig.update_layout(
                height=430,
                margin=dict(l=10, r=70, t=10, b=35),
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Inter, Arial", color=INK),
                xaxis=dict(title="Population", tickformat=",", gridcolor="#EEF1F7"),
                yaxis=dict(title=""),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with right_chart:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            render(chart_header("Top 5 vs Remaining Groups", "Share of state-level SC population"))

            top5_groups = category_summary.head(5).copy()
            remaining_groups_population = int(category_summary.iloc[5:]["Population"].sum())

            group_labels = top5_groups["SC Name"].tolist()
            group_values = top5_groups["Population"].tolist()

            if remaining_groups_population > 0:
                group_labels.append("Remaining Groups")
                group_values.append(remaining_groups_population)

            group_donut = go.Figure(data=[go.Pie(
                labels=group_labels, values=group_values, hole=0.62,
                textinfo="percent",
                marker=dict(colors=CHART_PALETTE + ["#C9CFDE"]),
                hovertemplate="<b>%{label}</b><br>Population: %{value:,}<br>Share: %{percent}<extra></extra>"
            )])
            group_donut.update_layout(
                height=430,
                margin=dict(l=10, r=10, t=10, b=85),
                paper_bgcolor="white",
                font=dict(family="Inter, Arial", color=INK),
                legend=dict(orientation="h", yanchor="bottom", y=-0.30, xanchor="center", x=0.5)
            )
            st.plotly_chart(group_donut, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        render(section_header(
            "SC Population Distribution",
            "Complete Scheduled Caste category data for this state"
        ))

        display_categories = category_summary.copy()
        display_categories["Population"] = display_categories["Population"].apply(indian_number)
        display_categories = display_categories.rename(columns={"SC Name": "Scheduled Caste"})

        st.dataframe(display_categories, use_container_width=True, hide_index=True, height=550)


# ============================================================
# FOOTER
# ============================================================

render('<div class="footer">Source: Census of India 2011 · Scheduled Caste Population Data</div>')

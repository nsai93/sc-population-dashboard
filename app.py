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
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM / CSS
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --navy: #17233F;
        --navy-2: #24375F;
        --ink: #17233F;
        --muted: #6B778C;
        --border: #E2E7EF;
        --surface: #FFFFFF;
        --page: #F5F7FB;
        --gold: #D89A3D;
        --teal: #2D8A7E;
        --blue: #6E91B5;
        --red: #C26052;
        --purple: #7563A5;
        --green: #62A56E;
    }

    .stApp {
        background: var(--page);
    }

    .main .block-container {
        max-width: 1480px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* ---------------- SIDEBAR ---------------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #17233F 0%, #1D2C4D 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem;
    }

    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }

    /* IMPORTANT: selectbox values/dropdowns must be DARK on WHITE */
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #17233F !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="input"] input {
        color: #17233F !important;
        background: #FFFFFF !important;
    }

    [data-baseweb="popover"] [role="option"],
    [data-baseweb="popover"] [role="option"] * {
        color: #17233F !important;
        background: #FFFFFF !important;
    }

    [data-baseweb="menu"] [role="option"],
    [data-baseweb="menu"] [role="option"] * {
        color: #17233F !important;
    }

    .sidebar-brand {
        font-size: 27px;
        font-weight: 800;
        color: white;
        letter-spacing: -0.4px;
        margin-bottom: 2px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #C9D3E5 !important;
        margin-bottom: 30px;
    }

    .sidebar-section {
        font-size: 17px;
        font-weight: 750;
        color: white !important;
        margin: 10px 0 12px 0;
    }

    /* ---------------- HEADERS ---------------- */
    .dashboard-title {
        font-size: 43px;
        font-weight: 800;
        color: var(--ink);
        line-height: 1.08;
        letter-spacing: -1.2px;
        margin-bottom: 9px;
    }

    .dashboard-subtitle {
        font-size: 17px;
        color: var(--muted);
        margin-bottom: 26px;
    }

    .state-hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #17233F 0%, #29446F 62%, #2D8A7E 140%);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 20px;
        box-shadow: 0 12px 32px rgba(23,35,63,0.13);
    }

    .state-hero:after {
        content: "";
        position: absolute;
        width: 210px;
        height: 210px;
        right: -55px;
        top: -85px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }

    .state-name {
        position: relative;
        z-index: 1;
        color: white;
        font-size: 39px;
        font-weight: 850;
        letter-spacing: -0.8px;
        margin-bottom: 5px;
    }

    .state-description {
        position: relative;
        z-index: 1;
        color: #DCE5F3;
        font-size: 15px;
    }

    /* ---------------- KPI CARDS ---------------- */
    .kpi-card {
        position: relative;
        background: white;
        border: 1px solid var(--border);
        border-radius: 17px;
        padding: 20px 21px;
        min-height: 142px;
        box-shadow: 0 5px 18px rgba(23,35,63,0.055);
        overflow: hidden;
    }

    .kpi-card:before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #D89A3D, #2D8A7E);
    }

    .kpi-label {
        font-size: 12px;
        letter-spacing: 0.8px;
        color: #748095;
        font-weight: 750;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: var(--ink);
        line-height: 1.15;
        word-break: break-word;
    }

    .kpi-value-long {
        font-size: 19px;
        line-height: 1.28;
    }

    .kpi-small {
        font-size: 12px;
        color: #7A8495;
        margin-top: 8px;
        line-height: 1.35;
    }

    /* ---------------- SECTION / CHART ---------------- */
    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: var(--ink);
        margin-top: 18px;
        margin-bottom: 3px;
        letter-spacing: -0.3px;
    }

    .section-subtitle {
        font-size: 14px;
        color: #7A8495;
        margin-bottom: 14px;
    }

    .chart-header {
        font-size: 20px;
        font-weight: 780;
        color: var(--ink);
        margin-bottom: 2px;
    }

    .chart-description {
        font-size: 13px;
        color: #7A8495;
        margin-bottom: 7px;
    }

    .chart-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 17px;
        padding: 16px 16px 5px 16px;
        box-shadow: 0 5px 18px rgba(23,35,63,0.045);
    }

    .insight-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F7F9FC 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 16px 18px;
        margin: 7px 0 16px 0;
    }

    .insight-title {
        color: var(--ink);
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 5px;
    }

    .insight-text {
        color: #5F6B7E;
        font-size: 14px;
        line-height: 1.45;
    }

    .footer {
        text-align: center;
        color: #7A8495;
        font-size: 12px;
        padding-top: 26px;
        border-top: 1px solid #E1E5EC;
        margin-top: 30px;
    }

    /* Streamlit dataframe/table polish */
    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #E2E7EF;
    }

    @media (max-width: 900px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .dashboard-title {
            font-size: 31px;
        }

        .dashboard-subtitle {
            font-size: 15px;
        }

        .state-name {
            font-size: 30px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA
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

possible_population_columns = [
    "Total Population",
    "Population",
    "SC Population",
    "SC_Population",
    "Scheduled Caste Population",
    "Scheduled_Caste_Population",
    "Total_Population",
]

population_column = next(
    (column for column in possible_population_columns if column in df.columns),
    None,
)

if population_column is None:
    st.error("Population column was not found in data/sc_population.csv.")
    st.stop()

df[population_column] = pd.to_numeric(
    df[population_column], errors="coerce"
).fillna(0)

required_columns = ["State", "SC Name"]
missing_columns = [c for c in required_columns if c not in df.columns]

if missing_columns:
    st.error("Missing required column(s): " + ", ".join(missing_columns))
    st.stop()


# ============================================================
# HELPERS
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


def add_share(dataframe, value_col, total):
    out = dataframe.copy()
    if total and total > 0:
        out["Share"] = (out[value_col] / total * 100).round(2)
    else:
        out["Share"] = 0.0
    return out


# ============================================================
# GLOBAL SUMMARY
# ============================================================
states = sorted(df["State"].dropna().unique().tolist())
loaded_states = len(states)
total_categories = df["SC Name"].nunique()
total_population = int(df[population_column].sum())

state_options = ["All India"] + states


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown(
    """
    <div class="sidebar-brand">SC Dashboard</div>
    <div class="sidebar-subtitle">Census 2011 Population Explorer</div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    '<div class="sidebar-section">Select State / UT</div>',
    unsafe_allow_html=True,
)

selected_state = st.sidebar.selectbox(
    "State / UT",
    state_options,
    index=0,
    label_visibility="collapsed",
)

if selected_state == "All India":
    state_filtered_df = df.copy()
else:
    state_filtered_df = df[df["State"] == selected_state].copy()

available_sc_categories = sorted(
    state_filtered_df["SC Name"].dropna().unique().tolist()
)

sc_options = ["All Scheduled Castes"] + available_sc_categories

st.sidebar.markdown(
    '<div class="sidebar-section" style="margin-top:20px;">Scheduled Caste Category</div>',
    unsafe_allow_html=True,
)

selected_sc = st.sidebar.selectbox(
    "Scheduled Caste Category",
    sc_options,
    label_visibility="collapsed",
)

if selected_sc == "All Scheduled Castes":
    selected_df = state_filtered_df.copy()
else:
    selected_df = state_filtered_df[
        state_filtered_df["SC Name"] == selected_sc
    ].copy()


# ============================================================
# INDIA OVERVIEW
# ============================================================
if selected_state == "All India":

    st.markdown(
        """
        <div class="dashboard-title">
            Scheduled Caste Population Dashboard — India
        </div>
        <div class="dashboard-subtitle">
            Census 2011 · Scheduled Caste Population Statistics
        </div>
        """,
        unsafe_allow_html=True,
    )

    largest_row = df.loc[df[population_column].idxmax()]
    largest_category = largest_row["SC Name"]
    largest_state = largest_row["State"]
    largest_population = int(largest_row[population_column])

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">States / UTs Loaded</div>
                <div class="kpi-value">{loaded_states}</div>
                <div class="kpi-small">States and Union Territories in the dataset</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total SC Population</div>
                <div class="kpi-value">{indian_number(total_population)}</div>
                <div class="kpi-small">Across all loaded States / UTs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">SC Categories</div>
                <div class="kpi-value">{indian_number(total_categories)}</div>
                <div class="kpi-small">Unique Scheduled Caste groups</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Largest SC Category</div>
                <div class="kpi-value kpi-value-long">{largest_category}</div>
                <div class="kpi-small">{largest_state} · {indian_number(largest_population)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ---------------- STATE SUMMARY ----------------
    state_summary = (
        df.groupby("State", as_index=False)[population_column]
        .sum()
        .rename(columns={population_column: "SC Population"})
        .sort_values("SC Population", ascending=False)
        .reset_index(drop=True)
    )

    state_summary.insert(0, "Rank", range(1, len(state_summary) + 1))
    state_summary = add_share(
        state_summary,
        "SC Population",
        int(state_summary["SC Population"].sum()),
    )

    left_chart, right_chart = st.columns([1.45, 1], gap="large")

    # ---------------- INDIA BAR ----------------
    with left_chart:
        st.markdown(
            """
            <div class="chart-card">
                <div class="chart-header">SC Population by State / UT</div>
                <div class="chart-description">Ranked from highest to lowest population</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        chart_df = state_summary.copy()
        chart_df["Display Population"] = chart_df["SC Population"].apply(indian_number)

        fig = px.bar(
            chart_df,
            x="SC Population",
            y="State",
            orientation="h",
            text="Display Population",
            color="State",
            color_discrete_sequence=[
                "#D89A3D", "#2D8A7E", "#6E91B5", "#C26052",
                "#7563A5", "#62A56E", "#C39A55", "#4F7F9F",
                "#A66A58", "#6F7FA8", "#4A9388", "#8E7A54",
            ],
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b>"
                "<br>SC Population: %{x:,}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            height=400,
            margin=dict(l=5, r=70, t=10, b=25),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Arial", color="#17233F"),
            xaxis=dict(
                title="SC Population",
                tickformat=",",
                gridcolor="#E7EAF0",
                zeroline=False,
            ),
            yaxis=dict(title="", autorange="reversed"),
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # ---------------- INDIA DONUT ----------------
    with right_chart:
        st.markdown(
            """
            <div class="chart-card">
                <div class="chart-header">Top 5 States vs Remaining</div>
                <div class="chart-description">Share of loaded SC population</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        top5 = state_summary.head(5).copy()
        remaining_population = int(state_summary.iloc[5:]["SC Population"].sum())

        donut_labels = top5["State"].tolist()
        donut_values = top5["SC Population"].tolist()

        if remaining_population > 0:
            donut_labels.append("Remaining States / UTs")
            donut_values.append(remaining_population)

        donut = go.Figure(
            data=[
                go.Pie(
                    labels=donut_labels,
                    values=donut_values,
                    hole=0.66,
                    textinfo="percent",
                    textfont=dict(size=12),
                    marker=dict(
                        colors=[
                            "#D89A3D", "#2D8A7E", "#6E91B5",
                            "#C26052", "#7563A5", "#D7D3C9"
                        ],
                        line=dict(color="white", width=2),
                    ),
                    hovertemplate=(
                        "<b>%{label}</b>"
                        "<br>Population: %{value:,}"
                        "<br>Share: %{percent}"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        donut.update_layout(
            height=400,
            margin=dict(l=5, r=5, t=5, b=70),
            paper_bgcolor="white",
            font=dict(family="Arial", color="#17233F"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.28,
                xanchor="center",
                x=0.5,
                font=dict(size=11),
            ),
            showlegend=True,
        )

        st.plotly_chart(
            donut,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # ---------------- QUICK INSIGHT ----------------
    top_state = state_summary.iloc[0]
    top_state_share = float(top_state["Share"])

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">Quick Insight</div>
            <div class="insight-text">
                <b>{top_state['State']}</b> has the largest loaded Scheduled Caste population
                at <b>{indian_number(top_state['SC Population'])}</b>, representing
                <b>{top_state_share:.2f}%</b> of the loaded total.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- INDIA TABLE ----------------
    st.markdown(
        """
        <div class="section-title">State / UT Population Summary</div>
        <div class="section-subtitle">
            Total Scheduled Caste population by loaded State / UT
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_state_summary = state_summary.copy()
    display_state_summary["SC Population"] = (
        display_state_summary["SC Population"].apply(indian_number)
    )
    display_state_summary["Share"] = (
        display_state_summary["Share"].map(lambda x: f"{x:.2f}%")
    )

    st.dataframe(
        display_state_summary,
        use_container_width=True,
        hide_index=True,
        height=470,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "State": st.column_config.TextColumn("State / UT"),
            "SC Population": st.column_config.TextColumn("SC Population"),
            "Share": st.column_config.TextColumn("Share of Loaded Total"),
        },
    )


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

    largest_state_row = state_data.loc[
        state_data[population_column].idxmax()
    ]

    largest_state_category = largest_state_row["SC Name"]
    largest_state_category_population = int(
        largest_state_row[population_column]
    )

    selected_population = int(selected_df[population_column].sum())

    # ---------------- HERO ----------------
    st.markdown(
        f"""
        <div class="state-hero">
            <div class="state-name">{selected_state}</div>
            <div class="state-description">
                Census 2011 · Scheduled Caste Population Statistics
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- STATE KPIs ----------------
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total SC Population</div>
                <div class="kpi-value">{indian_number(state_total_population)}</div>
                <div class="kpi-small">{selected_state}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">SC Categories</div>
                <div class="kpi-value">{state_category_count}</div>
                <div class="kpi-small">Scheduled Caste groups in this State / UT</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Largest SC Category</div>
                <div class="kpi-value kpi-value-long">{largest_state_category}</div>
                <div class="kpi-small">{indian_number(largest_state_category_population)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        if selected_sc == "All Scheduled Castes":
            metric_value = state_total_population
            metric_description = "All Scheduled Castes"
        else:
            metric_value = selected_population
            metric_description = selected_sc

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Selected Population</div>
                <div class="kpi-value">{indian_number(metric_value)}</div>
                <div class="kpi-small">{metric_description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # CATEGORY SELECTED
    # ========================================================
    if selected_sc != "All Scheduled Castes":

        st.markdown(
            f"""
            <div class="section-title">{selected_sc}</div>
            <div class="section-subtitle">
                Detailed population records for {selected_state}
            </div>
            """,
            unsafe_allow_html=True,
        )

        caste_data = selected_df.copy()

        preferred_columns = [
            "SC Code",
            "SC Name",
            population_column,
        ]

        existing_preferred_columns = [
            c for c in preferred_columns if c in caste_data.columns
        ]

        remaining_columns = [
            c for c in caste_data.columns
            if c not in existing_preferred_columns
        ]

        caste_data = caste_data[
            existing_preferred_columns + remaining_columns
        ]

        rename_map = {
            "SC Name": "Scheduled Caste",
            population_column: "Population",
        }

        caste_data = caste_data.rename(columns=rename_map)

        if "Population" in caste_data.columns:
            caste_data["Population"] = (
                caste_data["Population"].apply(indian_number)
            )

        st.dataframe(
            caste_data,
            use_container_width=True,
            hide_index=True,
            height=500,
        )

    # ========================================================
    # ALL SC CATEGORIES STATE VIEW
    # ========================================================
    else:

        # IMPORTANT: retain SC Code in the state-level distribution table.
        # Group by SC Code + SC Name so the official code is never lost.
        if "SC Code" in state_data.columns:
            category_summary = (
                state_data.groupby(
                    ["SC Code", "SC Name"],
                    as_index=False,
                )[population_column]
                .sum()
                .rename(columns={population_column: "Population"})
                .sort_values("Population", ascending=False)
                .reset_index(drop=True)
            )
        else:
            category_summary = (
                state_data.groupby(
                    ["SC Name"],
                    as_index=False,
                )[population_column]
                .sum()
                .rename(columns={population_column: "Population"})
                .sort_values("Population", ascending=False)
                .reset_index(drop=True)
            )

        category_summary.insert(
            0,
            "Rank",
            range(1, len(category_summary) + 1),
        )

        category_summary = add_share(
            category_summary,
            "Population",
            state_total_population,
        )

        # ---------------- TOP 10 + DONUT ----------------
        left_chart, right_chart = st.columns([1.22, 1], gap="large")

        with left_chart:
            st.markdown(
                """
                <div class="chart-card">
                    <div class="chart-header">Top 10 SC Groups by Population</div>
                    <div class="chart-description">
                        Largest Scheduled Caste groups in this State / UT
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            top10 = (
                category_summary.head(10)
                .sort_values("Population", ascending=True)
                .copy()
            )

            top10["Display Population"] = (
                top10["Population"].apply(indian_number)
            )

            fig = px.bar(
                top10,
                x="Population",
                y="SC Name",
                orientation="h",
                text="Display Population",
                color="SC Name",
                color_discrete_sequence=[
                    "#D89A3D", "#2D8A7E", "#6E91B5", "#C26052",
                    "#7563A5", "#62A56E", "#C39A55", "#4F7F9F",
                    "#A66A58", "#6F7FA8",
                ],
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b>"
                    "<br>Population: %{x:,}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=390,
                margin=dict(l=5, r=72, t=10, b=28),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(family="Arial", color="#17233F"),
                xaxis=dict(
                    title="Population",
                    tickformat=",",
                    gridcolor="#E7EAF0",
                    zeroline=False,
                ),
                yaxis=dict(title=""),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with right_chart:
            st.markdown(
                """
                <div class="chart-card">
                    <div class="chart-header">Top 5 vs Remaining Groups</div>
                    <div class="chart-description">
                        Share of state-level SC population
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            top5_groups = category_summary.head(5).copy()
            remaining_groups_population = int(
                category_summary.iloc[5:]["Population"].sum()
            )

            group_labels = top5_groups["SC Name"].tolist()
            group_values = top5_groups["Population"].tolist()

            if remaining_groups_population > 0:
                group_labels.append("Remaining Groups")
                group_values.append(remaining_groups_population)

            group_colors = [
                "#D89A3D",
                "#2D8A7E",
                "#6E91B5",
                "#C26052",
                "#7563A5",
                "#D7D3C9",
            ]

            group_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=group_labels,
                        values=group_values,
                        hole=0.66,
                        textinfo="percent",
                        textfont=dict(size=11),
                        marker=dict(
                            colors=group_colors[:len(group_labels)],
                            line=dict(color="white", width=2),
                        ),
                        hovertemplate=(
                            "<b>%{label}</b>"
                            "<br>Population: %{value:,}"
                            "<br>Share: %{percent}"
                            "<extra></extra>"
                        ),
                    )
                ]
            )

            group_donut.update_layout(
                height=390,
                margin=dict(l=5, r=5, t=5, b=78),
                paper_bgcolor="white",
                font=dict(family="Arial", color="#17233F"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.34,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10),
                ),
            )

            st.plotly_chart(
                group_donut,
                use_container_width=True,
                config={"displayModeBar": False},
            )

        # ---------------- INSIGHT ----------------
        top_group = category_summary.iloc[0]
        top_group_share = float(top_group["Share"])

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">State-Level Insight</div>
                <div class="insight-text">
                    <b>{top_group['SC Name']}</b> is the largest recorded SC group in
                    <b>{selected_state}</b>, with a population of
                    <b>{indian_number(top_group['Population'])}</b>
                    ({top_group_share:.2f}% of the state's SC population).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------------- FULL STATE DATA ----------------
        st.markdown(
            """
            <div class="section-title">SC Population Distribution</div>
            <div class="section-subtitle">
                Complete Scheduled Caste category data for this State / UT
            </div>
            """,
            unsafe_allow_html=True,
        )

        display_categories = category_summary.copy()

        display_categories["Population"] = (
            display_categories["Population"].apply(indian_number)
        )

        display_categories["Share"] = (
            display_categories["Share"].map(lambda x: f"{x:.2f}%")
        )

        display_categories = display_categories.rename(
            columns={
                "SC Name": "Scheduled Caste",
            }
        )

        # Explicit column order keeps SC Code visible.
        output_columns = ["Rank"]
        if "SC Code" in display_categories.columns:
            output_columns.append("SC Code")
        output_columns += ["Scheduled Caste", "Population", "Share"]

        display_categories = display_categories[output_columns]

        st.dataframe(
            display_categories,
            use_container_width=True,
            hide_index=True,
            height=560,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank", width="small"),
                "SC Code": st.column_config.TextColumn("SC Code", width="small"),
                "Scheduled Caste": st.column_config.TextColumn("Scheduled Caste"),
                "Population": st.column_config.TextColumn("Population"),
                "Share": st.column_config.TextColumn("Share of State Total"),
            },
        )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        Source: Census of India 2011 · Scheduled Caste Population Data
    </div>
    """,
    unsafe_allow_html=True,
)

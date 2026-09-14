

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Scheduled Caste Population Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #F7F8FA;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F1F3F6;
        border-right: 1px solid #E1E4E8;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Main title */
    .dashboard-title {
        font-size: 42px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 4px;
        letter-spacing: -1px;
    }

    .dashboard-subtitle {
        font-size: 17px;
        color: #6B7280;
        margin-bottom: 25px;
    }

    /* State header */
    .state-title {
        font-size: 40px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 2px;
    }

    .state-subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 20px;
    }

    /* KPI cards */
    .metric-card {
        background: white;
        border: 1px solid #E2E5E9;
        border-radius: 14px;
        padding: 20px 22px;
        min-height: 125px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.035);
    }

    .metric-label {
        color: #6B7280;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #111827;
        font-size: 28px;
        font-weight: 700;
        line-height: 1.2;
    }

    .metric-description {
        color: #9CA3AF;
        font-size: 12px;
        margin-top: 7px;
    }

    /* Chart cards */
    .section-title {
        font-size: 21px;
        font-weight: 650;
        color: #1F2937;
        margin-bottom: 3px;
    }

    .section-subtitle {
        font-size: 13px;
        color: #8A93A1;
        margin-bottom: 10px;
    }

    /* Divider */
    .soft-divider {
        height: 1px;
        background: #E5E7EB;
        margin: 25px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9CA3AF;
        font-size: 12px;
        padding-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/sc_population.csv")

    df.columns = df.columns.str.strip()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

    return df


df = load_data()


# ============================================================
# FIND POPULATION COLUMN
# ============================================================

possible_population_columns = [
    "Population",
    "SC Population",
    "SC_Population",
    "Scheduled Caste Population",
    "Scheduled_Caste_Population",
    "Total Population",
    "Total_Population"
]

population_column = None

for col in possible_population_columns:

    if col in df.columns:
        population_column = col
        break


if population_column is None:

    st.error(
        "Population column was not found in data/sc_population.csv."
    )

    st.stop()


df[population_column] = pd.to_numeric(
    df[population_column],
    errors="coerce"
).fillna(0)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "State",
    "SC Name"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"Missing required columns: {', '.join(missing_columns)}"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:24px;
        font-weight:700;
        color:#1F2937;
        margin-bottom:20px;
    ">
        Dashboard Filters
    </div>
    """,
    unsafe_allow_html=True
)


states = [
    "All India"
] + sorted(
    df["State"]
    .dropna()
    .unique()
    .tolist()
)


selected_state = st.sidebar.selectbox(
    "Select State / UT",
    states
)


# ============================================================
# STATE FILTER
# ============================================================

if selected_state == "All India":

    filtered_df = df.copy()
    india_view = True

else:

    filtered_df = df[
        df["State"] == selected_state
    ].copy()

    india_view = False


# ============================================================
# SC CATEGORY DROPDOWN
# ============================================================

available_categories = sorted(
    filtered_df["SC Name"]
    .dropna()
    .unique()
    .tolist()
)


sc_options = [
    "All Scheduled Castes"
] + available_categories


selected_sc = st.sidebar.selectbox(
    "Select Scheduled Caste",
    sc_options
)


# ============================================================
# APPLY SC FILTER
# ============================================================

if selected_sc != "All Scheduled Castes":

    selected_df = filtered_df[
        filtered_df["SC Name"] == selected_sc
    ].copy()

else:

    selected_df = filtered_df.copy()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def indian_number(value):

    value = int(round(value))

    s = str(abs(value))

    if len(s) <= 3:
        result = s

    else:

        last_three = s[-3:]

        remaining = s[:-3]

        parts = []

        while len(remaining) > 2:

            parts.insert(
                0,
                remaining[-2:]
            )

            remaining = remaining[:-2]

        if remaining:
            parts.insert(
                0,
                remaining
            )

        result = ",".join(parts) + "," + last_three

    if value < 0:
        result = "-" + result

    return result


def metric_card(
    label,
    value,
    description=""
):

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def chart_layout(fig):

    fig.update_layout(

        margin=dict(
            l=10,
            r=10,
            t=15,
            b=10
        ),

        font=dict(
            family="Arial",
            color="#374151"
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="white",

        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        )
    )

    return fig


# ============================================================
# ALL INDIA PAGE
# ============================================================

if india_view:

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="dashboard-title">
            Scheduled Caste Population Dashboard — India
        </div>

        <div class="dashboard-subtitle">
            Census 2011 · Scheduled Caste Population Statistics
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # INDIA METRICS
    # --------------------------------------------------------

    total_states = df["State"].nunique()

    total_categories = df["SC Name"].nunique()

    total_population = df[population_column].sum()


    category_totals = (
        df.groupby("SC Name")[population_column]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    largest_category = (
        category_totals.index[0]
        if len(category_totals) > 0
        else "N/A"
    )


    largest_category_population = (
        category_totals.iloc[0]
        if len(category_totals) > 0
        else 0
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        metric_card(
            "States / UTs Loaded",
            f"{total_states} / 36",
            "States and UTs currently available"
        )


    with c2:

        metric_card(
            "Total SC Population",
            indian_number(total_population),
            "Across all loaded states / UTs"
        )


    with c3:

        metric_card(
            "SC Categories",
            indian_number(total_categories),
            "Unique SC groups in loaded data"
        )


    with c4:

        metric_card(
            "Largest SC Category",
            largest_category,
            indian_number(largest_category_population)
        )


    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # STATE SUMMARY
    # ========================================================

    state_summary = (
        df.groupby("State", as_index=False)[
            population_column
        ]
        .sum()
        .sort_values(
            population_column,
            ascending=False
        )
    )


    # --------------------------------------------------------
    # STATE RANKING + DONUT
    # --------------------------------------------------------

    col_left, col_right = st.columns(
        [1.55, 1]
    )


    with col_left:

        st.markdown(
            """
            <div class="section-title">
                SC Population by State / UT
            </div>

            <div class="section-subtitle">
                Ranked from highest to lowest
            </div>
            """,
            unsafe_allow_html=True
        )


        chart_df = state_summary.copy()

        chart_df["Display"] = chart_df[
            population_column
        ].apply(indian_number)


        fig_state = px.bar(

            chart_df,

            x=population_column,

            y="State",

            orientation="h",

            text=population_column,

            color=population_column,

            color_continuous_scale=[
                "#D97706",
                "#E59B42",
                "#1F7A6E"
            ],

            labels={
                population_column:
                "SC Population",

                "State":
                ""
            }

        )


        fig_state.update_traces(
            texttemplate="%{x:,.0f}",
            textposition="outside",
            cliponaxis=False
        )


        fig_state.update_layout(
            height=570,
            coloraxis_showscale=False,
            yaxis=dict(
                categoryorder="total ascending"
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor="#E5E7EB"
            )
        )


        fig_state = chart_layout(
            fig_state
        )


        st.plotly_chart(
            fig_state,
            use_container_width=True
        )


    with col_right:

        st.markdown(
            """
            <div class="section-title">
                Top 5 States vs Remaining
            </div>

            <div class="section-subtitle">
                Share of total loaded SC population
            </div>
            """,
            unsafe_allow_html=True
        )


        top5 = state_summary.head(5)

        top5_total = top5[
            population_column
        ].sum()

        remaining_total = (
            state_summary[
                population_column
            ].sum()
            - top5_total
        )


        donut_df = pd.DataFrame(
            {
                "Group":
                list(
                    top5["State"]
                ) + ["Remaining States"],

                "Population":
                list(
                    top5[
                        population_column
                    ]
                ) + [
                    remaining_total
                ]
            }
        )


        fig_donut = px.pie(

            donut_df,

            names="Group",

            values="Population",

            hole=0.60,

            color_discrete_sequence=[
                "#E59B42",
                "#287C70",
                "#89A4BF",
                "#B95C50",
                "#7462A3",
                "#D8D4C8"
            ]
        )


        fig_donut.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Population: %{value:,.0f}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )


        fig_donut.update_layout(
            height=570
        )


        fig_donut = chart_layout(
            fig_donut
        )


        st.plotly_chart(
            fig_donut,
            use_container_width=True
        )


    # ========================================================
    # TOP SC GROUPS
    # ========================================================

    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="section-title">
            Top 10 Scheduled Caste Groups Nationwide
        </div>

        <div class="section-subtitle">
            Largest individual SC entries across all loaded states / UTs
        </div>
        """,
        unsafe_allow_html=True
    )


    top_categories = (
        df.groupby(
            ["State", "SC Name"],
            as_index=False
        )[population_column]
        .sum()
        .sort_values(
            population_column,
            ascending=False
        )
        .head(10)
    )


    top_categories["Label"] = (
        top_categories["SC Name"]
        .str.slice(0, 45)
    )


    fig_categories = px.bar(

        top_categories,

        x=population_column,

        y="Label",

        orientation="h",

        color="State",

        text=population_column,

        labels={
            population_column:
            "Population",

            "Label":
            ""
        },

        color_discrete_sequence=[
            "#287C70",
            "#D97706",
            "#7462A3",
            "#B95C50",
            "#89A4BF",
            "#A67C52"
        ]
    )


    fig_categories.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        cliponaxis=False
    )


    fig_categories.update_layout(
        height=500,
        yaxis=dict(
            categoryorder="total ascending"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB"
        )
    )


    fig_categories = chart_layout(
        fig_categories
    )


    st.plotly_chart(
        fig_categories,
        use_container_width=True
    )


    # ========================================================
    # STATE TABLE
    # ========================================================

    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="section-title">
            State / UT Population Details
        </div>

        <div class="section-subtitle">
            Complete state-wise summary
        </div>
        """,
        unsafe_allow_html=True
    )


    display_state = state_summary.rename(
        columns={
            "State": "State / UT",
            population_column: "SC Population"
        }
    )


    display_state[
        "SC Population"
    ] = display_state[
        "SC Population"
    ].apply(indian_number)


    st.dataframe(
        display_state,
        use_container_width=True,
        hide_index=True,
        height=450
    )


# ============================================================
# STATE PAGE
# ============================================================

else:

    # --------------------------------------------------------
    # STATE HEADER
    # --------------------------------------------------------

    state_code = ""

    if "State Code" in filtered_df.columns:

        codes = (
            filtered_df["State Code"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        if codes:
            state_code = codes[0]


    st.markdown(
        f"""
        <div class="state-title">
            {selected_state}
        </div>

        <div class="state-subtitle">
            Census 2011 · Scheduled Caste Population Statistics
            {" · Code " + state_code if state_code else ""}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # STATE METRICS
    # --------------------------------------------------------

    state_population = filtered_df[
        population_column
    ].sum()


    state_categories = filtered_df[
        "SC Name"
    ].nunique()


    state_category_totals = (
        filtered_df.groupby(
            "SC Name"
        )[population_column]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    largest_state_category = (
        state_category_totals.index[0]
        if len(state_category_totals)
        else "N/A"
    )


    largest_state_category_population = (
        state_category_totals.iloc[0]
        if len(state_category_totals)
        else 0
    )


    selected_population = selected_df[
        population_column
    ].sum()


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        metric_card(
            "Total SC Population",
            indian_number(state_population),
            selected_state
        )


    with c2:

        metric_card(
            "SC Groups",
            indian_number(state_categories),
            "Scheduled Caste groups"
        )


    with c3:

        metric_card(
            "Largest SC Group",
            largest_state_category,
            indian_number(
                largest_state_category_population
            )
        )


    with c4:

        if selected_sc == "All Scheduled Castes":

            metric_card(
                "Selected Population",
                indian_number(
                    state_population
                ),
                "All Scheduled Castes"
            )

        else:

            metric_card(
                "Selected Population",
                indian_number(
                    selected_population
                ),
                selected_sc
            )


    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # STATE CHARTS
    # ========================================================

    col_left, col_right = st.columns(
        [1.55, 1]
    )


    # --------------------------------------------------------
    # TOP 10 BAR
    # --------------------------------------------------------

    with col_left:

        st.markdown(
            """
            <div class="section-title">
                Top 10 SC Groups by Population
            </div>

            <div class="section-subtitle">
                Largest Scheduled Caste groups in this state
            </div>
            """,
            unsafe_allow_html=True
        )


        top10 = (
            state_category_totals
            .head(10)
            .reset_index()
        )


        top10.columns = [
            "SC Name",
            "Population"
        ]


        top10["Short Name"] = (
            top10["SC Name"]
            .str.slice(0, 42)
        )


        fig_top10 = px.bar(

            top10,

            x="Population",

            y="Short Name",

            orientation="h",

            text="Population",

            color="Population",

            color_continuous_scale=[
                "#1F7A6E",
                "#5C9D93",
                "#D6A04A"
            ],

            labels={
                "Population":
                "Population",

                "Short Name":
                ""
            }
        )


        fig_top10.update_traces(
            texttemplate="%{x:,.0f}",
            textposition="outside",
            cliponaxis=False
        )


        fig_top10.update_layout(
            height=520,
            coloraxis_showscale=False,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )


        fig_top10 = chart_layout(
            fig_top10
        )


        st.plotly_chart(
            fig_top10,
            use_container_width=True
        )


    # --------------------------------------------------------
    # DONUT
    # --------------------------------------------------------

    with col_right:

        st.markdown(
            """
            <div class="section-title">
                Top 5 vs Remaining Groups
            </div>

            <div class="section-subtitle">
                Share of state-level SC population
            </div>
            """,
            unsafe_allow_html=True
        )


        top5_state = (
            state_category_totals
            .head(5)
        )


        top5_state_total = (
            top5_state.sum()
        )


        remaining_state_total = (
            state_population
            - top5_state_total
        )


        state_donut = pd.DataFrame(
            {
                "Group":
                list(
                    top5_state.index
                ) + ["Remaining Groups"],

                "Population":
                list(
                    top5_state.values
                ) + [
                    remaining_state_total
                ]
            }
        )


        fig_state_donut = px.pie(

            state_donut,

            names="Group",

            values="Population",

            hole=0.60,

            color_discrete_sequence=[
                "#D99A45",
                "#287C70",
                "#89A4BF",
                "#B95C50",
                "#7462A3",
                "#D8D4C8"
            ]
        )


        fig_state_donut.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Population: %{value:,.0f}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )


        fig_state_donut.update_layout(
            height=520
        )


        fig_state_donut = chart_layout(
            fig_state_donut
        )


        st.plotly_chart(
            fig_state_donut,
            use_container_width=True
        )


    # ========================================================
    # POPULATION DISTRIBUTION
    # ========================================================

    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="section-title">
            SC Population Distribution
        </div>

        <div class="section-subtitle">
            Population of individual Scheduled Caste groups
        </div>
        """,
        unsafe_allow_html=True
    )


    distribution_df = state_category_totals.reset_index()

    distribution_df.columns = [
        "SC Name",
        "Population"
    ]


    fig_distribution = px.scatter(

        distribution_df,

        x="SC Name",

        y="Population",

        size="Population",

        color="Population",

        hover_name="SC Name",

        color_continuous_scale=[
            "#7462A3",
            "#287C70",
            "#D99A45"
        ],

        labels={
            "SC Name":
            "",

            "Population":
            "Population"
        }
    )


    fig_distribution.update_layout(
        height=420,
        coloraxis_showscale=False,
        xaxis=dict(
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB"
        )
    )


    fig_distribution = chart_layout(
        fig_distribution
    )


    st.plotly_chart(
        fig_distribution,
        use_container_width=True
    )


    # ========================================================
    # FULL DATA
    # ========================================================

    st.markdown(
        '<div class="soft-divider"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="section-title">
            Complete SC Data
        </div>

        <div class="section-subtitle">
            All Scheduled Caste groups available for this state
        </div>
        """,
        unsafe_allow_html=True
    )


    state_table = filtered_df.copy()


    preferred_columns = []

    if "SC Code" in state_table.columns:
        preferred_columns.append("SC Code")

    preferred_columns.extend(
        [
            "SC Name",
            population_column
        ]
    )


    other_columns = [
        col
        for col in state_table.columns
        if col not in preferred_columns
    ]


    state_table = state_table[
        preferred_columns + other_columns
    ]


    rename_map = {
        "SC Code": "SC Code",
        "SC Name": "Scheduled Caste",
        population_column: "Population"
    }


    state_table = state_table.rename(
        columns=rename_map
    )


    if "Population" in state_table.columns:

        state_table["Population"] = (
            state_table["Population"]
            .apply(indian_number)
        )


    st.dataframe(
        state_table,
        use_container_width=True,
        hide_index=True,
        height=600
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Source: Census of India 2011 · Scheduled Caste Population Data
        <br>
        Dashboard updates automatically when the underlying CSV is updated.
    </div>
    """,
    unsafe_allow_html=True
)


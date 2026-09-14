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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    .stApp {
        background-color: #f6f8fb;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #17233F;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        font-weight: 600;
    }

    /* --------------------------------------------------------
       HEADERS
    -------------------------------------------------------- */

    .dashboard-title {
        font-size: 42px;
        font-weight: 750;
        color: #17233F;
        line-height: 1.15;
        margin-bottom: 8px;
    }

    .dashboard-subtitle {
        font-size: 18px;
        color: #687386;
        margin-bottom: 28px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #17233F;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        font-size: 15px;
        color: #7a8495;
        margin-bottom: 18px;
    }

    /* --------------------------------------------------------
       KPI CARDS
    -------------------------------------------------------- */

    .kpi-card {
        background: white;
        border: 1px solid #e2e6ed;
        border-radius: 16px;
        padding: 22px 24px;
        min-height: 135px;
        box-shadow: 0 4px 16px rgba(23, 35, 63, 0.05);
    }

    .kpi-label {
        font-size: 14px;
        color: #748095;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 29px;
        font-weight: 750;
        color: #17233F;
        line-height: 1.15;
    }

    .kpi-small {
        font-size: 13px;
        color: #7a8495;
        margin-top: 7px;
    }

    /* --------------------------------------------------------
       STATE HERO
    -------------------------------------------------------- */

    .state-hero {
        background: linear-gradient(
            135deg,
            #17233F 0%,
            #24375f 100%
        );
        border-radius: 18px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 25px rgba(23, 35, 63, 0.12);
    }

    .state-name {
        color: white;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .state-description {
        color: #d9dfeb;
        font-size: 16px;
    }

    /* --------------------------------------------------------
       CHART CONTAINERS
    -------------------------------------------------------- */

    .chart-header {
        font-size: 21px;
        font-weight: 700;
        color: #17233F;
        margin-bottom: 2px;
    }

    .chart-description {
        font-size: 14px;
        color: #7a8495;
        margin-bottom: 10px;
    }

    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        text-align: center;
        color: #7a8495;
        font-size: 13px;
        padding-top: 20px;
    }

    /* --------------------------------------------------------
       MOBILE
    -------------------------------------------------------- */

    @media (max-width: 900px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .dashboard-title {
            font-size: 30px;
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
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = "data/sc_population.csv"

    data = pd.read_csv(file_path)

    # Clean column names
    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
    )

    # Clean text columns
    for column in data.columns:

        if data[column].dtype == "object":

            data[column] = (
                data[column]
                .astype(str)
                .str.strip()
            )

    # Standardize State
    data["State"] = (
        data["State"]
        .astype(str)
        .str.strip()
    )

    # Standardize SC Name
    data["SC Name"] = (
        data["SC Name"]
        .astype(str)
        .str.strip()
    )

    # Standardize SC Code if available
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

    st.error(
        "Population column was not found in "
        "data/sc_population.csv."
    )

    st.stop()


# Convert population to numeric

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
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "Missing required column(s): "
        + ", ".join(missing_columns)
    )

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

    return (
        sign
        + ",".join(parts)
        + ","
        + last_three
    )


# ============================================================
# BASIC DATA SUMMARY
# ============================================================

states = sorted(
    df["State"]
    .dropna()
    .unique()
    .tolist()
)

loaded_states = len(states)

total_categories = df["SC Name"].nunique()

total_population = int(
    df[population_column].sum()
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:26px;
        font-weight:800;
        margin-bottom:5px;
    ">
        SC Dashboard
    </div>

    <div style="
        font-size:13px;
        color:#CBD3E2 !important;
        margin-bottom:25px;
    ">
        Census 2011 Population Explorer
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown(
    "### Select State"
)


state_options = [
    "All India"
] + states


selected_state = st.sidebar.selectbox(
    "State / UT",
    state_options,
    index=0
)


# ============================================================
# DYNAMIC SC CATEGORY FILTER
# ============================================================

if selected_state == "All India":

    state_filtered_df = df.copy()

else:

    state_filtered_df = df[
        df["State"] == selected_state
    ].copy()


available_sc_categories = sorted(
    state_filtered_df["SC Name"]
    .dropna()
    .unique()
    .tolist()
)


sc_options = [
    "All Scheduled Castes"
] + available_sc_categories


selected_sc = st.sidebar.selectbox(
    "Scheduled Caste Category",
    sc_options
)


# ============================================================
# APPLY SC FILTER
# ============================================================

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
    # INDIA KPI VALUES
    # --------------------------------------------------------

    largest_row = df.loc[
        df[population_column].idxmax()
    ]

    largest_category = largest_row["SC Name"]
    largest_state = largest_row["State"]
    largest_population = int(
        largest_row[population_column]
    )


    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)


    with k1:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    STATES / UTs LOADED
                </div>

                <div class="kpi-value">
                    {loaded_states}
                </div>

                <div class="kpi-small">
                    States and Union Territories
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with k2:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    TOTAL SC POPULATION
                </div>

                <div class="kpi-value">
                    {indian_number(total_population)}
                </div>

                <div class="kpi-small">
                    Across all loaded states / UTs
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with k3:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    SC CATEGORIES
                </div>

                <div class="kpi-value">
                    {indian_number(total_categories)}
                </div>

                <div class="kpi-small">
                    Unique Scheduled Caste groups
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with k4:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    LARGEST SC CATEGORY
                </div>

                <div class="kpi-value"
                     style="font-size:20px;">

                    {largest_category}

                </div>

                <div class="kpi-small">
                    {largest_state}
                    ·
                    {indian_number(largest_population)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # STATE SUMMARY
    # ========================================================

    state_summary = (
        df
        .groupby(
            "State",
            as_index=False
        )[population_column]
        .sum()
        .rename(
            columns={
                population_column:
                    "SC Population"
            }
        )
        .sort_values(
            "SC Population",
            ascending=False
        )
        .reset_index(drop=True)
    )


    state_summary.insert(
        0,
        "Rank",
        range(
            1,
            len(state_summary) + 1
        )
    )


    # ========================================================
    # INDIA CHARTS
    # ========================================================

    left_chart, right_chart = st.columns(
        [1.55, 1]
    )


    # --------------------------------------------------------
    # STATE BAR CHART
    # --------------------------------------------------------

    with left_chart:

        st.markdown(
            '<div class="chart-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="chart-header">
                SC Population by State / UT
            </div>
            <div class="chart-description">
                Ranked from highest to lowest population
            </div>
            """,
            unsafe_allow_html=True
        )

        chart_df = state_summary.copy()
        chart_df["Display Population"] = chart_df["SC Population"].apply(indian_number)

        fig = px.bar(
            chart_df,
            x="SC Population",
            y="State",
            orientation="h",
            text="Display Population"
        )

        fig.update_traces(
            marker_color="#4F6FF5",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b>"
                "<br>SC Population: %{x:,}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=480,
            margin=dict(l=10, r=70, t=10, b=30),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                family="Inter, Arial",
                color="#17233F"
            ),
            xaxis=dict(
                title="SC Population",
                tickformat=",",
                gridcolor="#EEF1F7"
            ),
            yaxis=dict(
                title="",
                autorange="reversed"
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # TOP 5 DONUT
    # --------------------------------------------------------

    with right_chart:

        st.markdown(
            """
            <div class="chart-header">
                Top 5 States vs Remaining
            </div>

            <div class="chart-description">
                Share of loaded SC population
            </div>
            """,
            unsafe_allow_html=True
        )


        top5 = state_summary.head(5).copy()

        remaining_population = int(
            state_summary.iloc[5:][
                "SC Population"
            ].sum()
        )


        donut_labels = top5[
            "State"
        ].tolist()

        donut_values = top5[
            "SC Population"
        ].tolist()


        if remaining_population > 0:

            donut_labels.append(
                "Remaining States / UTs"
            )

            donut_values.append(
                remaining_population
            )


        donut = go.Figure(
            data=[
                go.Pie(
                    labels=donut_labels,
                    values=donut_values,
                    hole=0.62,
                    textinfo="percent",
                    hovertemplate=(
                        "<b>%{label}</b>"
                        "<br>Population: %{value:,}"
                        "<br>Share: %{percent}"
                        "<extra></extra>"
                    )
                )
            ]
        )


        donut.update_layout(

            height=480,

            margin=dict(
                l=10,
                r=10,
                t=10,
                b=70
            ),

            paper_bgcolor="white",

            font=dict(
                family="Arial",
                color="#17233F"
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.20,
                xanchor="center",
                x=0.5
            )
        )


        st.plotly_chart(
            donut,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


    # ========================================================
    # STATE TABLE
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            State / UT Population Summary
        </div>

        <div class="section-subtitle">
            Total Scheduled Caste population by loaded State / UT
        </div>
        """,
        unsafe_allow_html=True
    )


    display_state_summary = state_summary.copy()

    display_state_summary[
        "SC Population"
    ] = (
        display_state_summary[
            "SC Population"
        ]
        .apply(indian_number)
    )


    st.dataframe(
        display_state_summary,
        use_container_width=True,
        hide_index=True,
        height=500
    )


# ============================================================
# STATE PAGE
# ============================================================

else:

    # --------------------------------------------------------
    # STATE DATA
    # --------------------------------------------------------

    state_data = (
        df[
            df["State"] == selected_state
        ]
        .copy()
        .sort_values(
            population_column,
            ascending=False
        )
    )


    state_total_population = int(
        state_data[population_column].sum()
    )


    state_category_count = (
        state_data["SC Name"]
        .nunique()
    )


    largest_state_row = state_data.loc[
        state_data[population_column].idxmax()
    ]


    largest_state_category = (
        largest_state_row["SC Name"]
    )


    largest_state_category_population = int(
        largest_state_row[population_column]
    )


    selected_population = int(
        selected_df[population_column].sum()
    )


    # --------------------------------------------------------
    # STATE HEADER
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="state-hero">

            <div class="state-name">
                {selected_state}
            </div>

            <div class="state-description">
                Census 2011 · Scheduled Caste Population Statistics
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # STATE KPI CARDS
    # --------------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)


    with k1:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    TOTAL SC POPULATION
                </div>

                <div class="kpi-value">
                    {indian_number(state_total_population)}
                </div>

                <div class="kpi-small">
                    {selected_state}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with k2:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    SC CATEGORIES
                </div>

                <div class="kpi-value">
                    {state_category_count}
                </div>

                <div class="kpi-small">
                    Scheduled Caste groups
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with k3:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    LARGEST SC CATEGORY
                </div>

                <div class="kpi-value"
                     style="font-size:20px;">

                    {largest_state_category}

                </div>

                <div class="kpi-small">
                    {indian_number(
                        largest_state_category_population
                    )}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with k4:

        if selected_sc == "All Scheduled Castes":

            metric_label = "SELECTED POPULATION"
            metric_value = state_total_population
            metric_description = "All Scheduled Castes"

        else:

            metric_label = "SELECTED POPULATION"
            metric_value = selected_population
            metric_description = selected_sc


        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    {metric_label}
                </div>

                <div class="kpi-value">
                    {indian_number(metric_value)}
                </div>

                <div class="kpi-small">
                    {metric_description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # IF CATEGORY SELECTED
    # ========================================================

    if selected_sc != "All Scheduled Castes":

        st.markdown(
            f"""
            <div class="section-title">
                {selected_sc}
            </div>

            <div class="section-subtitle">
                Detailed population records for
                {selected_state}
            </div>
            """,
            unsafe_allow_html=True
        )


        caste_data = selected_df.copy()


        preferred_columns = [
            "SC Code",
            "SC Name",
            population_column
        ]


        existing_preferred_columns = [
            column
            for column in preferred_columns
            if column in caste_data.columns
        ]


        remaining_columns = [
            column
            for column in caste_data.columns
            if column not in existing_preferred_columns
        ]


        caste_data = caste_data[
            existing_preferred_columns
            + remaining_columns
        ]


        rename_map = {

            "SC Code":
                "SC Code",

            "SC Name":
                "Scheduled Caste",

            population_column:
                "Population"
        }


        caste_data = caste_data.rename(
            columns=rename_map
        )


        if "Population" in caste_data.columns:

            caste_data["Population"] = (
                caste_data["Population"]
                .apply(indian_number)
            )


        st.dataframe(
            caste_data,
            use_container_width=True,
            hide_index=True,
            height=500
        )


    # ========================================================
    # ALL SC CATEGORIES STATE VIEW
    # ========================================================

    else:

        # ----------------------------------------------------
        # CATEGORY SUMMARY
        # ----------------------------------------------------

        category_summary = (
            state_data
            .groupby(
                "SC Name",
                as_index=False
            )[population_column]
            .sum()
            .rename(
                columns={
                    population_column:
                        "Population"
                }
            )
            .sort_values(
                "Population",
                ascending=False
            )
            .reset_index(drop=True)
        )


        category_summary.insert(
            0,
            "Rank",
            range(
                1,
                len(category_summary) + 1
            )
        )


        # ----------------------------------------------------
        # TOP 10 + DONUT
        # ----------------------------------------------------

        left_chart, right_chart = st.columns(
            [1.25, 1]
        )


        # ----------------------------------------------------
        # TOP 10 BAR
        # ----------------------------------------------------

        with left_chart:

            st.markdown(
                """
                <div class="chart-header">
                    Top 10 SC Groups by Population
                </div>

                <div class="chart-description">
                    Largest Scheduled Caste groups in this state
                </div>
                """,
                unsafe_allow_html=True
            )


            top10 = (
                category_summary
                .head(10)
                .sort_values(
                    "Population",
                    ascending=True
                )
                .copy()
            )


            top10["Display Population"] = (
                top10["Population"]
                .apply(indian_number)
            )


            fig = px.bar(
                top10,
                x="Population",
                y="SC Name",
                orientation="h",
                text="Display Population"
            )


            fig.update_traces(

                marker_color="#2F8F83",

                textposition="outside",

                hovertemplate=(
                    "<b>%{y}</b>"
                    "<br>Population: %{x:,}"
                    "<extra></extra>"
                )
            )


            fig.update_layout(

                height=430,

                margin=dict(
                    l=10,
                    r=70,
                    t=10,
                    b=35
                ),

                plot_bgcolor="white",
                paper_bgcolor="white",

                font=dict(
                    family="Arial",
                    color="#17233F"
                ),

                xaxis=dict(
                    title="Population",
                    tickformat=",",
                    gridcolor="#E7EAF0"
                ),

                yaxis=dict(
                    title=""
                ),

                showlegend=False
            )


            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )


        # ----------------------------------------------------
        # TOP 5 VS REMAINING DONUT
        # ----------------------------------------------------

        with right_chart:

            st.markdown(
                """
                <div class="chart-header">
                    Top 5 vs Remaining Groups
                </div>

                <div class="chart-description">
                    Share of state-level SC population
                </div>
                """,
                unsafe_allow_html=True
            )


            top5_groups = (
                category_summary
                .head(5)
                .copy()
            )


            remaining_groups_population = int(
                category_summary.iloc[5:][
                    "Population"
                ].sum()
            )


            group_labels = (
                top5_groups["SC Name"]
                .tolist()
            )


            group_values = (
                top5_groups["Population"]
                .tolist()
            )


            if remaining_groups_population > 0:

                group_labels.append(
                    "Remaining Groups"
                )

                group_values.append(
                    remaining_groups_population
                )


            group_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=group_labels,
                        values=group_values,
                        hole=0.62,
                        textinfo="percent",
                        hovertemplate=(
                            "<b>%{label}</b>"
                            "<br>Population: %{value:,}"
                            "<br>Share: %{percent}"
                            "<extra></extra>"
                        )
                    )
                ]
            )


            group_donut.update_layout(

                height=430,

                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=85
                ),

                paper_bgcolor="white",

                font=dict(
                    family="Arial",
                    color="#17233F"
                ),

                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.30,
                    xanchor="center",
                    x=0.5
                )
            )


            st.plotly_chart(
                group_donut,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )


        # ====================================================
        # FULL CATEGORY TABLE
        # ====================================================

        st.markdown(
            """
            <div class="section-title">
                SC Population Distribution
            </div>

            <div class="section-subtitle">
                Complete Scheduled Caste category data for this state
            </div>
            """,
            unsafe_allow_html=True
        )


        display_categories = category_summary.copy()


        display_categories[
            "Population"
        ] = (
            display_categories[
                "Population"
            ]
            .apply(indian_number)
        )


        display_categories = (
            display_categories
            .rename(
                columns={
                    "SC Name":
                        "Scheduled Caste"
                }
            )
        )


        st.dataframe(
            display_categories,
            use_container_width=True,
            hide_index=True,
            height=550
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
    unsafe_allow_html=True
)
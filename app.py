
import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Scheduled Caste Population Dashboard",
    page_icon="📊",
    layout="wide"
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
            df[col] = df[col].astype(str).str.strip()

    return df


df = load_data()


# ============================================================
# IDENTIFY POPULATION COLUMN
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
        "Population column was not found in the CSV file."
    )
    st.stop()


df[population_column] = pd.to_numeric(
    df[population_column],
    errors="coerce"
).fillna(0)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = ["State", "SC Name"]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"Missing required column(s): {', '.join(missing_columns)}"
    )
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Filters")

states = ["All States"] + sorted(
    df["State"].dropna().unique().tolist()
)

selected_state = st.sidebar.selectbox(
    "Select State",
    states
)


# ============================================================
# FILTER BY STATE
# ============================================================

if selected_state == "All States":
    filtered_df = df.copy()
    india_view = True
else:
    filtered_df = df[
        df["State"] == selected_state
    ].copy()
    india_view = False


# ============================================================
# SECOND DROPDOWN — SC CATEGORY
# ============================================================

available_sc_categories = sorted(
    filtered_df["SC Name"]
    .dropna()
    .unique()
    .tolist()
)

sc_options = [
    "All Scheduled Castes"
] + available_sc_categories

selected_sc = st.sidebar.selectbox(
    "Select Scheduled Caste",
    sc_options
)


# ============================================================
# APPLY SC CATEGORY FILTER
# ============================================================

if selected_sc != "All Scheduled Castes":
    selected_df = filtered_df[
        filtered_df["SC Name"] == selected_sc
    ].copy()
else:
    selected_df = filtered_df.copy()


# ============================================================
# PAGE TITLE
# ============================================================

if india_view:

    st.title(
        "Scheduled Caste Population Dashboard — India"
    )

    st.caption(
        "Census 2011 Scheduled Caste Population Data"
    )

else:

    st.title(
        f"Scheduled Caste Population — {selected_state}"
    )

    st.caption(
        f"Census 2011 Scheduled Caste Population Data | {selected_state}"
    )


# ============================================================
# METRICS
# ============================================================

if india_view:

    total_states = df["State"].nunique()

    total_categories = df["SC Name"].nunique()

    total_population = df[population_column].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "States / UTs",
            f"{total_states:,}"
        )

    with col2:
        st.metric(
            "Scheduled Caste Categories",
            f"{total_categories:,}"
        )

    with col3:
        st.metric(
            "Total SC Population",
            f"{total_population:,.0f}"
        )

else:

    state_population = filtered_df[population_column].sum()

    state_categories = filtered_df["SC Name"].nunique()

    selected_population = selected_df[population_column].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "State / UT",
            selected_state
        )

    with col2:
        st.metric(
            "SC Categories",
            f"{state_categories:,}"
        )

    with col3:

        if selected_sc == "All Scheduled Castes":
            label = "Total SC Population"
        else:
            label = "Selected SC Population"

        st.metric(
            label,
            f"{selected_population:,.0f}"
        )


# ============================================================
# ALL INDIA PAGE
# ============================================================

if india_view:

    st.divider()

    st.subheader(
        "State / UT Population Details"
    )

    state_summary = (
        df.groupby("State", as_index=False)[population_column]
        .sum()
        .sort_values(
            population_column,
            ascending=False
        )
    )

    display_state_summary = state_summary.rename(
        columns={
            "State": "State / UT",
            population_column: "SC Population"
        }
    )

    display_state_summary["SC Population"] = (
        display_state_summary["SC Population"]
        .round(0)
        .astype(int)
    )

    st.dataframe(
        display_state_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# STATE PAGE
# ============================================================

else:

    st.divider()

    if selected_sc == "All Scheduled Castes":

        st.subheader(
            f"Scheduled Caste Categories — {selected_state}"
        )

        category_summary = (
            filtered_df
            .groupby("SC Name", as_index=False)[population_column]
            .sum()
            .sort_values(
                population_column,
                ascending=False
            )
        )

        category_summary = category_summary.rename(
            columns={
                "SC Name": "Scheduled Caste",
                population_column: "Population"
            }
        )

        category_summary["Population"] = (
            category_summary["Population"]
            .round(0)
            .astype(int)
        )

        st.dataframe(
            category_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.subheader(
            f"{selected_sc} — {selected_state}"
        )

        caste_data = selected_df.copy()

        preferred_columns = [
            "State",
            "SC Name",
            population_column
        ]

        available_columns = [
            col for col in preferred_columns
            if col in caste_data.columns
        ]

        remaining_columns = [
            col for col in caste_data.columns
            if col not in available_columns
        ]

        caste_data = caste_data[
            available_columns + remaining_columns
        ]

        rename_map = {
            "State": "State / UT",
            "SC Name": "Scheduled Caste",
            population_column: "Population"
        }

        caste_data = caste_data.rename(
            columns=rename_map
        )

        st.dataframe(
            caste_data,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Source: Census of India 2011 | Scheduled Caste Population Data"
)

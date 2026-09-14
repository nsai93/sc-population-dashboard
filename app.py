
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Scheduled Caste Population Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
df = pd.read_csv("data/sc_population.csv")

# Title
st.title("Scheduled Caste Population Dashboard — India")
st.caption("Census 2011 Scheduled Caste Population Data")

# Sidebar
st.sidebar.header("Filters")

states = ["All States"] + sorted(df["State"].unique().tolist())
selected_state = st.sidebar.selectbox("Select State", states)

if selected_state == "All States":
    filtered_df = df.copy()
else:
    filtered_df = df[df["State"] == selected_state].copy()

# Search SC Name
search = st.sidebar.text_input("Search Scheduled Caste")

if search:
    filtered_df = filtered_df[
        filtered_df["SC Name"].str.contains(search, case=False, na=False)
    ]

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "States / UTs",
        filtered_df["State"].nunique()
    )

with col2:
    st.metric(
        "Scheduled Caste Categories",
        len(filtered_df)
    )

with col3:
    st.metric(
        "Total SC Population",
        f"{filtered_df['Total Population'].sum():,}"
    )

st.divider()

# Population chart
st.subheader("Scheduled Caste Population")

chart_df = (
    filtered_df
    .groupby("State")["Total Population"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(chart_df)

st.divider()

# Data table
st.subheader("Scheduled Caste Population Details")

display_df = filtered_df.sort_values(
    "Total Population",
    ascending=False
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

import streamlit as st
import plotly.express as px
from dashboard.styles import load_css
from mining.data_loader import DataLoader
from dashboard.components import (
    section_header,
    kpi_card
)

st.set_page_config(
    page_title="MedIntel360 - Operations",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# =====================================================
# Load Dataset
# =====================================================

operations = DataLoader.operations()

# =====================================================
# Ward Level Dataset (One row per ward)
# =====================================================

ward_data = (
    operations
    .drop_duplicates(subset="ward_name")
    .copy()
)

# =====================================================
# KPI Calculations
# =====================================================

total_wards = ward_data["ward_name"].nunique()

total_beds = ward_data["total_beds"].sum()

average_occupancy = ward_data["ward_occupancy_rate"].mean()

total_staff = ward_data["staff_count"].sum()

total_nurses = ward_data["nurse_count"].sum()

high_workload = ward_data["high_workload_ward_flag"].sum()

night_shift = ward_data["night_shift_percentage"].mean()

# =====================================================
# KPI Section
# =====================================================

section_header(

    "Operational KPIs",

    "Ward, staffing and occupancy overview"

)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:

    kpi_card(

        title="Wards",

        value=f"{total_wards}",

        trend="▲ Active",

        badge="Operational"

    )

with col2:

    kpi_card(

        title="Beds",

        value=f"{total_beds:,}",

        trend="▲ Capacity",

        badge="Infrastructure"

    )

with col3:

    kpi_card(

        title="Occupancy",

        value=f"{average_occupancy:.1f}%",

        trend="▲ Stable",

        badge="Healthy"

    )

with col4:

    kpi_card(

        title="High Workload Wards",

        value=f"{high_workload}",

        trend="▲ Available",

        badge="Medical"

    )

with col5:

    kpi_card(

        title="Nurses",

        value=f"{total_nurses:,}",

        trend="▲ Ready",

        badge="Care"

    )

with col6:

    kpi_card(

        title="Staff",

        value=f"{total_staff:,}",

        trend="▲ Workforce",

        badge="Operations"

    )

with col7:

    kpi_card(

        title="Night Shift",

        value=f"{night_shift:.1f}%",

        trend="▲ Coverage",

        badge="Shift Management"
    )

# =====================================================
# Ward Performance
# =====================================================

section_header(

    "Ward Performance",

    "Occupancy and admission analysis across hospital wards"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

occupancy_data = (

    ward_data

    .sort_values(

        "ward_occupancy_rate",

        ascending=False

    )

)

admission_data = (

    operations

    .groupby(

        "ward_name",

        as_index=False

    )["admission_id"]

    .count()

    .rename(

        columns={

            "admission_id": "admissions"

        }

    )

    .sort_values(

        "admissions",

        ascending=False

    )

)

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

col1, col2 = st.columns(2)

# =====================================================
# Ward Occupancy
# =====================================================

with col1:

    fig_occupancy = px.bar(

        occupancy_data,

        x="ward_occupancy_rate",

        y="ward_name",

        orientation="h",

        text_auto=".1f",

        title="Ward Occupancy (%)"

    )

    fig_occupancy.update_layout(

        template="plotly_dark",

        height=450,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Occupancy (%)",

        yaxis_title="Ward"

    )

    st.plotly_chart(

        fig_occupancy,

        width="stretch"

    )

# =====================================================
# Admissions by Ward
# =====================================================

with col2:

    fig_admissions = px.bar(

        admission_data,

        x="admissions",

        y="ward_name",

        orientation="h",

        text_auto=True,

        title="Admissions by Ward"

    )

    fig_admissions.update_layout(

        template="plotly_dark",

        height=450,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Admissions",

        yaxis_title="Ward"

    )

    st.plotly_chart(

        fig_admissions,

        width="stretch"

    )   

# =====================================================
# Workforce Analytics
# =====================================================

section_header(

    "Workforce Analytics",

    "Hospital staffing and workforce allocation"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

staff_data = ward_data[

    [

        "ward_name",

        "staff_count",

        "nurse_count",

        "technician_count"

    ]

].sort_values(

    "staff_count",

    ascending=False

)

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

col1, col2 = st.columns(2)

# =====================================================
# Staff Count by Ward
# =====================================================

with col1:

    fig_staff = px.bar(

        staff_data,

        x="ward_name",

        y="staff_count",

        text_auto=True,

        title="Staff Count by Ward"

    )

    fig_staff.update_layout(

        template="plotly_dark",

        height=420,

        margin=dict(l=20, r=20, t=60, b=20),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Ward",

        yaxis_title="Staff"

    )

    st.plotly_chart(

        fig_staff,

        width="stretch"

    )

# =====================================================
# Nurse vs Technician Distribution
# =====================================================

with col2:

    fig_workforce = px.bar(

        staff_data,

        x="ward_name",

        y=["nurse_count", "technician_count"],

        barmode="group",

        title="Nurse vs Technician Distribution"

    )

    fig_workforce.update_layout(

        template="plotly_dark",

        height=420,

        margin=dict(l=20, r=20, t=60, b=20),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Ward",

        yaxis_title="Employees"

    )

    st.plotly_chart(

        fig_workforce,

        width="stretch"

    )

# =====================================================
# Operational Insights
# =====================================================

section_header(

    "Operational Insights",

    "Key operational indicators across hospital wards"

)

# -----------------------------------------------------
# Calculations
# -----------------------------------------------------

highest_occupancy = ward_data.loc[
    ward_data["ward_occupancy_rate"].idxmax()
]

highest_workload = ward_data.loc[
    ward_data["high_workload_ward_flag"].idxmax()
]

average_staff_ratio = ward_data["staff_to_bed_ratio"].mean()

average_night_shift = ward_data["night_shift_percentage"].mean()

occupied_beds = ward_data["occupied_bed_flag"].sum()

# -----------------------------------------------------
# Display
# -----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"🏆 Highest Occupancy Ward: **{highest_occupancy['ward_name']}** "
        f"({highest_occupancy['ward_occupancy_rate']:.1f}%)"
    )

    st.warning(
        f"⚠ High Workload Ward: **{highest_workload['ward_name']}**"
    )

    st.info(
        f"🛏 Average Staff / Bed Ratio: **{average_staff_ratio:.2f}**"
    )

with col2:

    st.info(
        f"🌙 Average Night Shift: **{average_night_shift:.1f}%**"
    )

    st.success(
        f"🛌 Occupied Beds: **{occupied_beds}**"
    )

    st.metric(

        "Average Ward Occupancy",

        f"{ward_data['ward_occupancy_rate'].mean():.1f}%"

    )
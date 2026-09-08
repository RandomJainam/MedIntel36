"""
=========================================================
MedIntel360
Medical Dashboard
=========================================================

Enterprise Medical Dashboard

Author : Jainam Gada
"""

# =====================================================
# Imports
# =====================================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from dashboard.styles import load_css

from dashboard.components import (
    page_title,
    section_header,
    kpi_card
)

from mining.data_loader import DataLoader


# =====================================================
# Page Config
# =====================================================

st.set_page_config(

    page_title="Medical Dashboard",

    page_icon="🩺",

    layout="wide"

)

load_css()


# =====================================================
# Load Dataset
# =====================================================

medical = DataLoader.medical()


# =====================================================
# Disease Level Dataset
# =====================================================

disease_data = (

    medical

    .drop_duplicates(

        subset="disease_name"

    )

    .copy()

)


# =====================================================
# Page Title
# =====================================================

page_title(

    "🩺 Medical Dashboard",

    "Clinical intelligence and disease analytics"

)


# =====================================================
# KPI Calculations
# =====================================================

total_diseases = disease_data["disease_name"].nunique()

total_tests = medical["test_name"].nunique()

total_drugs = medical["drug_name"].nunique()

total_doctors = medical["employee_name"].nunique()

average_los = disease_data["average_los_by_disease"].mean()

high_volume_cases = disease_data["high_volume_disease_flag"].sum()


# =====================================================
# KPI Section
# =====================================================

section_header(

    "Medical KPIs",

    "Clinical performance and healthcare insights"

)


col1, col2, col3, col4, col5, col6 = st.columns(6)


# =====================================================
# Diseases
# =====================================================

with col1:

    kpi_card(

        title="Diseases",

        value=f"{total_diseases}",

        trend="▲ Active",

        badge="Clinical"

    )


# =====================================================
# Tests
# =====================================================

with col2:

    kpi_card(

        title="Tests",

        value=f"{total_tests}",

        trend="▲ Running",

        badge="Diagnostics"

    )


# =====================================================
# Drugs
# =====================================================

with col3:

    kpi_card(

        title="Drugs",

        value=f"{total_drugs}",

        trend="▲ Available",

        badge="Pharmacy"

    )


# =====================================================
# Doctors
# =====================================================

with col4:

    kpi_card(

        title="Doctors",

        value=f"{total_doctors}",

        trend="▲ Serving",

        badge="Medical"

    )


# =====================================================
# Average LOS
# =====================================================

with col5:

    kpi_card(

        title="Avg LOS",

        value=f"{average_los:.2f} Days",

        trend="▼ Efficient",

        badge="Performance"

    )


# =====================================================
# High Volume Diseases
# =====================================================

with col6:

    kpi_card(

        title="High Volume",

        value=f"{int(high_volume_cases)}",

        trend="▲ Priority",

        badge="Cases"

    )

# =====================================================
# Disease Analytics
# =====================================================

section_header(

    "Disease Analytics",

    "Disease prevalence and average hospital stay"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

disease_cases = (
    disease_data
    .sort_values(
        "disease_case_count",
        ascending=False
    )
    .head(10)
)

average_los_data = (
    disease_data
    .sort_values(
        "average_los_by_disease",
        ascending=False
    )
    .head(10)
)

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

col1, col2 = st.columns(2)

# =====================================================
# Disease Case Count
# =====================================================

with col1:

    fig_cases = px.bar(

        disease_cases,

        x="disease_case_count",

        y="disease_name",

        orientation="h",

        text_auto=True,

        title="Disease Case Count"

    )

    fig_cases.update_layout(

        template="plotly_dark",

        height=430,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Cases",

        yaxis_title="Disease"

    )

    st.plotly_chart(

        fig_cases,

        width="stretch"

    )

# =====================================================
# Average LOS by Disease
# =====================================================

with col2:

    fig_los = px.bar(

        average_los_data,

        x="average_los_by_disease",

        y="disease_name",

        orientation="h",

        text_auto=".2f",

        title="Average LOS by Disease"

    )

    fig_los.update_layout(

        template="plotly_dark",

        height=430,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Days",

        yaxis_title="Disease"

    )

    st.plotly_chart(

        fig_los,

        width="stretch"

    )

# =====================================================
# Diagnostic & Drug Analytics
# =====================================================

section_header(

    "Diagnostic & Drug Analytics",

    "Diagnostic test utilization and medication trends"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

test_usage = (

    medical

    .groupby(

        "test_name",

        as_index=False

    )["test_usage_count"]

    .max()

    .sort_values(

        "test_usage_count",

        ascending=False

    )

    .head(10)

)

drug_usage = (

    medical

    .groupby(

        "drug_name",

        as_index=False

    )["drug_usage_count"]

    .max()

    .sort_values(

        "drug_usage_count",

        ascending=False

    )

    .head(10)

)

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

col1, col2 = st.columns(2)

# =====================================================
# Test Usage
# =====================================================

with col1:

    fig_test = px.bar(

        test_usage,

        x="test_usage_count",

        y="test_name",

        orientation="h",

        text_auto=True,

        title="Top Diagnostic Tests"

    )

    fig_test.update_layout(

        template="plotly_dark",

        height=430,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Usage",

        yaxis_title="Test"

    )

    st.plotly_chart(

        fig_test,

        width="stretch"

    )

# =====================================================
# Drug Usage
# =====================================================

with col2:

    fig_drug = px.bar(

        drug_usage,

        x="drug_usage_count",

        y="drug_name",

        orientation="h",

        text_auto=True,

        title="Top Prescribed Drugs"

    )

    fig_drug.update_layout(

        template="plotly_dark",

        height=430,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Usage",

        yaxis_title="Drug"

    )

    st.plotly_chart(

        fig_drug,

        width="stretch"

    )

# =====================================================
# Clinical Insights
# =====================================================

section_header(

    "Clinical Insights",

    "Key medical observations and disease intelligence"

)

# -----------------------------------------------------
# Calculations
# -----------------------------------------------------

most_common_disease = disease_data.loc[
    disease_data["disease_case_count"].idxmax()
]

highest_los = disease_data.loc[
    disease_data["average_los_by_disease"].idxmax()
]

most_used_test = medical.loc[
    medical["test_usage_count"].idxmax()
]

most_used_drug = medical.loc[
    medical["drug_usage_count"].idxmax()
]

top_doctor = medical.loc[
    medical["doctor_patient_count"].idxmax()
]

average_revenue = disease_data[
    "average_revenue_by_disease"
].mean()

# -----------------------------------------------------
# Display
# -----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.success(

        f"🦠 Most Common Disease: **{most_common_disease['disease_name']}**"

    )

    st.info(

        f"👨‍⚕️ Doctor Handling Most Patients: **{top_doctor['employee_name']}**"

    )

    st.success(

        f"🧪 Most Used Diagnostic Test: **{most_used_test['test_name']}**"

    )

with col2:

    st.warning(

        f"💊 Most Prescribed Drug: **{most_used_drug['drug_name']}**"

    )

    st.info(

        f"⏳ Highest Average LOS: **{highest_los['disease_name']}** "
        f"({highest_los['average_los_by_disease']:.2f} Days)"

    )

    st.metric(

        "Average Revenue per Disease",

        f"₹{average_revenue:,.0f}"

    )
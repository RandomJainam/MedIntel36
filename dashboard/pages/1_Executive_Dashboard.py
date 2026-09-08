"""
=========================================================
MedIntel360
Executive Dashboard
=========================================================

Enterprise Executive Dashboard

Author : Jainam Gada
"""

import streamlit as st
import plotly.express as px

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
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

load_css()


# =====================================================
# Load Dataset
# =====================================================

patient = DataLoader.patient()


# =====================================================
# Page Title
# =====================================================

page_title(

    "📊 Executive Dashboard",

    "Enterprise-wide Healthcare Performance Overview"

)


# =====================================================
# KPI Calculations
# =====================================================

total_patients = patient["patient_id"].nunique()

total_admissions = patient["admission_id"].nunique()

total_revenue = patient["total_amount"].sum()

average_revenue = patient["total_amount"].mean()

average_los = patient["los"].mean()

total_departments = patient["department_name"].nunique()


# =====================================================
# KPI Section
# =====================================================

section_header(

    "Executive KPIs",

    "Key Performance Indicators across the hospital"

)


col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:

    kpi_card(

        title="Patients",

        value=f"{total_patients:,}",

        trend="▲ Healthy",

        badge="Healthy"

    )


with col2:

    kpi_card(

        title="Admissions",

        value=f"{total_admissions:,}",

        trend="▲ Stable",

        badge="Stable"

    )


with col3:

    kpi_card(

        title="Revenue",

        value=f"₹{total_revenue/10000000:.2f} Cr",

        trend="▲ Positive",

        badge="Positive"

    )


with col4:

    kpi_card(

        title="Avg Revenue",

        value=f"₹{average_revenue:,.0f}",

        trend="▲ Healthy Growth",

        badge="Growth"

    )


with col5:

    kpi_card(

        title="Average LOS",

        value=f"{average_los:.2f} Days",

        trend="▼ Improved",

        badge="Improved"

    )


with col6:

    kpi_card(

        title="Departments",

        value=f"{total_departments}",

        trend="▲ Active",

        badge="Operational"

    )


# =====================================================
# Revenue & Admissions Trends
# =====================================================

section_header(

    "Revenue & Admission Trends",

    "Monthly hospital performance overview"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

revenue_trend = (

    patient.groupby("admission_month", as_index=False)["total_amount"]

    .sum()

)

admission_trend = (

    patient.groupby("admission_month", as_index=False)["admission_id"]

    .count()

)

revenue_trend = revenue_trend.sort_values("admission_month")

admission_trend = admission_trend.sort_values("admission_month")

# -----------------------------------------------------
# Charts
# -----------------------------------------------------

col1, col2 = st.columns(2)

# =====================================================
# Revenue Trend
# =====================================================

with col1:

    fig_revenue = px.line(

        revenue_trend,

        x="admission_month",

        y="total_amount",

        markers=True,

        title="Monthly Revenue"

    )

    fig_revenue.update_layout(

        template="plotly_dark",

        height=420,

        margin=dict(l=20, r=20, t=60, b=20),

        xaxis_title="Month",

        yaxis_title="Revenue",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(

        fig_revenue,

        width="stretch"

    )

# =====================================================
# Admission Trend
# =====================================================

with col2:

    fig_admission = px.line(

        admission_trend,

        x="admission_month",

        y="admission_id",

        markers=True,

        title="Monthly Admissions"

    )

    fig_admission.update_layout(

        template="plotly_dark",

        height=420,

        margin=dict(l=20, r=20, t=60, b=20),

        xaxis_title="Month",

        yaxis_title="Admissions",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(

        fig_admission,

        width="stretch"

    )

# =====================================================
# Department Analytics
# =====================================================

section_header(

    "Department Analytics",

    "Department performance and disease distribution"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

department_revenue = (

    patient.groupby("department_name", as_index=False)["total_amount"]

    .sum()

    .sort_values("total_amount", ascending=False)

)

disease_summary = (

    patient.groupby(

        "disease_name",

        as_index=False

    )["patient_id"]

    .count()

    .rename(

        columns={

            "patient_id":"case_count"

        }

    )

    .sort_values(

        "case_count",

        ascending=False

    )

    .head(10)

)

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

col1, col2 = st.columns(2)

# =====================================================
# Revenue by Department
# =====================================================

with col1:

    fig_department = px.bar(

        department_revenue,

        x="total_amount",

        y="department_name",

        orientation="h",

        text_auto=".2s",

        title="Revenue by Department"

    )

    fig_department.update_layout(

        template="plotly_dark",

        height=450,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        xaxis_title="Revenue",

        yaxis_title="Department",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(

        fig_department,

        width="stretch"

    )

# =====================================================
# Top Diseases
# =====================================================

with col2:

    fig_disease = px.bar(

        disease_summary,

        x="case_count",

        y="disease_name",

        orientation="h",

        text_auto=True,

        title="Top Diseases"

    )

    fig_disease.update_layout(

        template="plotly_dark",

        height=450,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        xaxis_title="Cases",

        yaxis_title="Disease",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(

        fig_disease,

        width="stretch"

    )

# =====================================================
# Gender Distribution & Executive Insights
# =====================================================

section_header(

    "Executive Insights",

    "Patient demographics and hospital intelligence"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

gender_distribution = (

    patient["gender"]

    .value_counts()

    .reset_index()

)

gender_distribution.columns = [

    "Gender",

    "Count"

]

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

col1, col2 = st.columns([1, 1.3])

# =====================================================
# Gender Distribution
# =====================================================

with col1:

    fig_gender = px.pie(

        gender_distribution,

        names="Gender",

        values="Count",

        hole=0.55,

        title="Gender Distribution"

    )

    fig_gender.update_layout(

        template="plotly_dark",

        height=420,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(

        fig_gender,

        width="stretch"

    )

# =====================================================
# Executive Insights
# =====================================================

with col2:

    highest_department = (

        patient.groupby("department_name")["total_amount"]

        .sum()

        .idxmax()

    )

    highest_disease = (

        patient["disease_name"]

        .value_counts()

        .idxmax()

    )

    senior_percentage = (

        patient["senior_citizen_flag"]

        .mean()

        * 100

    )

    weekend_percentage = (

        patient["weekend_admission"]

        .mean()

        * 100

    )

    frequent_percentage = (

        patient["frequent_patient_flag"]

        .mean()

        * 100

    )

    average_daily_revenue = (

        patient["revenue_per_day"]

        .mean()

    )

    st.markdown("### 📌 Executive Insights")

    st.success(f"🏆 Highest Revenue Department : **{highest_department}**")

    st.info(f"🦠 Most Common Disease : **{highest_disease}**")

    st.warning(f"👴 Senior Citizens : **{senior_percentage:.1f}%**")

    st.info(f"🏥 Weekend Admissions : **{weekend_percentage:.1f}%**")

    st.success(f"⭐ Frequent Patients : **{frequent_percentage:.1f}%**")

    st.metric(

        "Average Revenue Per Day",

        f"₹{average_daily_revenue:,.0f}"

    )
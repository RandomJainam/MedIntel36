"""
=========================================================
MedIntel360
Finance Dashboard
=========================================================

Enterprise Finance Dashboard

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

load_css()

st.set_page_config(layout="wide")

# =====================================================
# Load Dataset
# =====================================================

finance = DataLoader.finance()

# =====================================================
# Finance Level Dataset
# One row per bill (Grain Safe)
# =====================================================

finance_data = (

    finance

    .drop_duplicates(subset="bill_id")

    .copy()

)

# =====================================================
# KPI Calculations
# =====================================================

total_revenue = finance_data["total_amount"].sum()

average_bill = finance_data["total_amount"].mean()

insurance_revenue = finance_data["insurance_covered_amount"].sum()

patient_revenue = finance_data["patient_payable_amount"].sum()

payment_completion = finance_data["payment_completion_ratio"].mean()

top_departments = finance_data["top_department_flag"].sum()

# =====================================================
# KPI Section
# =====================================================

section_header(

    "Financial KPIs",

    "Revenue, billing and payment overview"

)

col1, col2, col3, col4, col5, col6 = st.columns(6)

# =====================================================
# Total Revenue
# =====================================================

with col1:

    kpi_card(

        title="Revenue",

        value=f"₹{total_revenue/10000000:.2f} Cr",

        trend="▲ Positive",

        badge="Revenue"

    )

# =====================================================
# Average Bill
# =====================================================

with col2:

    kpi_card(

        title="Avg Bill",

        value=f"₹{average_bill:,.0f}",

        trend="▲ Healthy",

        badge="Billing"

    )

# =====================================================
# Insurance Revenue
# =====================================================

with col3:

    kpi_card(

        title="Insurance",

        value=f"₹{insurance_revenue/10000000:.2f} Cr",

        trend="▲ Covered",

        badge="Insurance"

    )

# =====================================================
# Patient Payments
# =====================================================

with col4:

    kpi_card(

        title="Patient Pay",

        value=f"₹{patient_revenue/10000000:.2f} Cr",

        trend="▲ Received",

        badge="Payments"

    )

# =====================================================
# Payment Completion
# =====================================================

with col5:

    kpi_card(

        title="Completion",

        value=f"{payment_completion:.1f}%",

        trend="▲ Excellent",

        badge="Completed"

    )

# =====================================================
# Top Departments
# =====================================================

with col6:

    kpi_card(

        title="Top Dept.",

        value=f"{int(top_departments)}",

        trend="▲ Performing",

        badge="Ranking"

    )

# =====================================================
# Revenue Analytics
# =====================================================

section_header(

    "Revenue Analytics",

    "Department-wise revenue performance"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

department_revenue = (

    finance_data

    .groupby(

        "department_name",

        as_index=False

    )["department_total_revenue"]

    .max()

    .sort_values(

        "department_total_revenue",

        ascending=False

    )

)

department_share = (

    finance_data

    .groupby(

        "department_name",

        as_index=False

    )["department_revenue_share"]

    .max()

)

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

col1, col2 = st.columns(2)

# =====================================================
# Revenue by Department
# =====================================================

with col1:

    fig_revenue = px.bar(

        department_revenue,

        x="department_total_revenue",

        y="department_name",

        orientation="h",

        text_auto=".2s",

        title="Revenue by Department"

    )

    fig_revenue.update_layout(

        template="plotly_white",

        height=430,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Revenue",

        yaxis_title="Department"

    )

    st.plotly_chart(

        fig_revenue,

        width="stretch"

    )

# =====================================================
# Revenue Share
# =====================================================

with col2:

    fig_share = px.pie(

        department_share,

        names="department_name",

        values="department_revenue_share",

        hole=0.55,

        title="Department Revenue Share"

    )

    fig_share.update_layout(

        template="plotly_dark",

        height=430,

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

        fig_share,

        width="stretch"

    )

# =====================================================
# Payment Analytics
# =====================================================

section_header(

    "Payment Analytics",

    "Insurance coverage and payment behaviour"

)

# -----------------------------------------------------
# Prepare Data
# -----------------------------------------------------

payment_mode = (

    finance_data["payment_mode"]

    .value_counts()

    .reset_index()

)

payment_mode.columns = [

    "Payment Mode",

    "Count"

]

insurance_summary = {

    "Category": [

        "Insurance Covered",

        "Patient Payable"

    ],

    "Amount": [

        finance_data["insurance_covered_amount"].sum(),

        finance_data["patient_payable_amount"].sum()

    ]

}

import plotly.graph_objects as go

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

col1, col2 = st.columns(2)

# =====================================================
# Payment Mode
# =====================================================

with col1:

    fig_payment = px.pie(

        payment_mode,

        names="Payment Mode",

        values="Count",

        hole=0.55,

        title="Payment Modes"

    )

    fig_payment.update_layout(

        template="plotly_dark",

        height=430,

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

        fig_payment,

        width="stretch"

    )

# =====================================================
# Insurance vs Patient
# =====================================================

with col2:

    fig_compare = go.Figure()

    fig_compare.add_bar(

        x=["Insurance"],

        y=[finance_data["insurance_covered_amount"].sum()],

        name="Insurance"

    )

    fig_compare.add_bar(

        x=["Patient"],

        y=[finance_data["patient_payable_amount"].sum()],

        name="Patient"

    )

    fig_compare.update_layout(

        title="Insurance vs Patient Payments",

        template="plotly_dark",

        barmode="group",

        height=430,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="",

        yaxis_title="Amount"

    )

    st.plotly_chart(

        fig_compare,

        width="stretch"

    )

# =====================================================
# Financial Insights
# =====================================================

section_header(

    "Financial Insights",

    "Key financial observations and business indicators"

)

# -----------------------------------------------------
# Calculations
# -----------------------------------------------------

highest_revenue = finance_data.loc[
    finance_data["department_total_revenue"].idxmax()
]

payment_completion = finance_data[
    "payment_completion_ratio"
].mean()

insurance_percentage = finance_data[
    "insurance_coverage_percentage"
].mean()

average_bill = finance_data[
    "total_amount"
].mean()

high_coverage = finance_data[
    "high_coverage_flag"
].sum()

top_departments = finance_data[
    "top_department_flag"
].sum()

# -----------------------------------------------------
# Display
# -----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.success(

        f"🏆 Highest Revenue Department: "
        f"**{highest_revenue['department_name']}**"

    )

    st.info(

        f"💳 Payment Completion Rate: "
        f"**{payment_completion:.1f}%**"

    )

    st.success(

        f"🛡 Insurance Coverage: "
        f"**{insurance_percentage:.1f}%**"

    )

with col2:

    st.metric(

        "Average Bill Amount",

        f"₹{average_bill:,.0f}"

    )

    st.warning(

        f"⭐ High Coverage Bills: "
        f"**{int(high_coverage)}**"

    )

    st.info(

        f"🥇 Top Revenue Departments: "
        f"**{int(top_departments)}**"

    )
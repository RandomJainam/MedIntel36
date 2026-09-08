"""
=========================================================
MedIntel360
Dashboard Utilities
=========================================================

Shared data loaders for all dashboard pages.

Author : Jainam Gada
"""

import pandas as pd
import streamlit as st


# =====================================================
# Patient Gold
# =====================================================

@st.cache_data(show_spinner=False)
def load_patient():

    return pd.read_csv(

        "data/gold/gold_patient_analytics.csv"

    )


# =====================================================
# Finance Gold
# =====================================================

@st.cache_data(show_spinner=False)
def load_finance():

    return pd.read_csv(

        "data/gold/gold_finance_analytics.csv"

    )


# =====================================================
# Operations Gold
# =====================================================

@st.cache_data(show_spinner=False)
def load_operations():

    return pd.read_csv(

        "data/gold/gold_operations_analytics.csv"

    )


# =====================================================
# Medical Gold
# =====================================================

@st.cache_data(show_spinner=False)
def load_medical():

    return pd.read_csv(

        "data/gold/gold_medical_analytics.csv"

    )


# =====================================================
# Dashboard Data
# =====================================================

@st.cache_data(show_spinner=False)
def load_dashboard():

    return {

        "patient": load_patient(),

        "finance": load_finance(),

        "operations": load_operations(),

        "medical": load_medical()

    }
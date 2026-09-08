import streamlit as st

from dashboard.styles import load_css
from dashboard.components import (
    hero,
    kpi_card,
    workspace_card,
    health_card,
    intelligence_feed,
    section_header,
    sidebar_toggle_backup
)

from dashboard.utils import load_dashboard


st.set_page_config(

    page_title="MedIntel360",

    page_icon="🏥",

    layout="wide",

    initial_sidebar_state="expanded"

)

load_css()
sidebar_toggle_backup()

data = load_dashboard()

patient = data["patient"]
finance = data["finance"]
operations = data["operations"]
medical = data["medical"]


# =====================================================
# Hero
# =====================================================

hero()


# =====================================================
# Executive KPIs
# =====================================================

section_header(

    "Executive Snapshot",

    "Real-time overview of hospital performance."

)

c1, c2, c3, c4 = st.columns(4)

with c1:

    kpi_card(

        "Patients",

        f"{patient['patient_id'].nunique():,}",

        "▲ Healthy Growth"

    )

with c2:

    kpi_card(

        "Admissions",

        f"{patient['admission_id'].nunique():,}",

        "▲ Stable"

    )

with c3:

    revenue = patient["total_amount"].sum()

    kpi_card(

        "Revenue",

        f"₹{revenue/1e7:.2f} Cr",

        "▲ Positive"

    )

with c4:

    los = patient["los"].mean()

    kpi_card(

        "Average LOS",

        f"{los:.2f} Days",

        "▼ Improved"

    )


st.write("")

# =====================================================
# Workspace Modules
# =====================================================

section_header(

    "Workspace",

    "Choose an analytics workspace."

)

w1, w2, w3 = st.columns(3)

with w1:

    workspace_card(

        "📊",

        "Executive Intelligence",

        "Hospital level KPIs and strategic insights.",

        "6 KPIs",

        "Administrator"

    )

with w2:

    workspace_card(

        "🏥",

        "Operations Command Center",

        "Beds, wards, staffing and operations.",

        "Operations",

        "Manager"

    )

with w3:

    workspace_card(

        "💰",

        "Financial Performance",

        "Revenue, billing and insurance.",

        "Finance",

        "CFO"

    )

st.write("")

w4, w5, w6 = st.columns(3)

with w4:

    workspace_card(

        "🧠",

        "Advanced Analytics",

        "Association rules, clustering and anomaly detection.",

        "Mining",

        "Analyst"

    )

with w5:

    workspace_card(

        "🤖",

        "AI Copilot",

        "Natural language healthcare analytics.",

        "AI",

        "Assistant"

    )

with w6:

    workspace_card(

        "📄",

        "Smart Reports",

        "Executive summaries and exports.",

        "Reports",

        "Management"

    )


st.write("")

# =====================================================
# Health
# =====================================================

section_header(

    "System Health"

)

h1, h2, h3, h4 = st.columns(4)

with h1:

    health_card("Data Warehouse")

with h2:

    health_card("ETL Pipeline")

with h3:

    health_card("AI Engine")

with h4:

    health_card("Mining Engine")


st.write("")

# =====================================================
# Feed
# =====================================================

section_header(

    "Recent Intelligence"

)

intelligence_feed("Patient analytics refreshed.")

intelligence_feed("Finance warehouse synchronized.")

intelligence_feed("Operations dashboard updated.")

intelligence_feed("Association Rules generated.")

intelligence_feed("AI Copilot ready.")
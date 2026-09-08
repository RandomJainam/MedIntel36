"""
=========================================================
MedIntel360
Global Styles
=========================================================

Reusable CSS for the complete dashboard.

Author : Jainam Gada
"""

import streamlit as st

from dashboard.theme import *


def load_css():

    st.markdown(

        f"""
<style>

/* ---------------------------------------------------- */
/* Hide Streamlit Default Elements */
/* ---------------------------------------------------- */

#MainMenu {{
    visibility:hidden;
}}

footer {{
    visibility:hidden;
}}

/* Do NOT hide the whole <header> — in Streamlit 1.58 the
   sidebar expand/collapse control (>>) lives inside <header>
   alongside the hamburger menu and Deploy button. Hiding the
   entire header hides the sidebar toggle with it. Instead,
   hide only the specific toolbar widgets we don't want, and
   keep the header itself transparent but interactive so its
   children (including the sidebar toggle) remain clickable. */
header {{
    background:transparent;
}}

header [data-testid="stToolbar"] {{
    visibility:hidden;
}}

/* Explicitly force the sidebar toggle (collapsed and expanded
   states) to always render, regardless of any rule above. */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"] {{
    visibility:visible !important;
    display:flex !important;
    opacity:1 !important;
    z-index:999999 !important;
}}

/* Hides the hover "copy" / fullscreen toolbar Streamlit
   auto-injects on markdown/HTML blocks — this was the
   floating copy icon appearing on the feed cards. */
[data-testid="stElementToolbar"] {{
    display:none;
}}

div.block-container {{
    padding-top:1.2rem;
    max-width:{MAX_WIDTH};
}}

/* ---------------------------------------------------- */
/* App */
/* ---------------------------------------------------- */

.stApp {{
    background:{BACKGROUND};
    color:{TEXT};
}}

/* ---------------------------------------------------- */
/* Sidebar */
/* ---------------------------------------------------- */

section[data-testid="stSidebar"] {{
    background:{SIDEBAR};
    border-right:1px solid {BORDER};
}}

section[data-testid="stSidebar"] * {{
    color:{TEXT};
}}

section[data-testid="stSidebarNav"] {{
    padding-top:1rem;
}}

section[data-testid="stSidebar"] button:hover {{
    background:{PRIMARY};
    color:white;
    transition:.25s;
}}

/* ---------------------------------------------------- */
/* Equal-height columns                                  */
/* Forces every card in a st.columns() row to match the  */
/* tallest sibling instead of drifting to its own content*/
/* height — this is what was causing row misalignment.   */
/* ---------------------------------------------------- */

div[data-testid="stHorizontalBlock"] {{
    align-items:stretch;
}}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
    display:flex;
}}

div[data-testid="column"] > div {{
    width:100%;
}}

/* Scoped to ONLY the vertical block sitting directly inside a
   st.columns() column — NOT a global selector. stVerticalBlock
   wraps almost every container in Streamlit (including the
   sidebar and header internals), so an unscoped height:100%
   here cascades through those ancestors too and can collapse
   the header/sidebar-toggle box to zero height after layout
   settles. This was the actual cause of the vanishing toggle. */
div[data-testid="column"] > div[data-testid="stVerticalBlock"] {{
    height:100%;
}}

/* ---------------------------------------------------- */
/* Typography */
/* ---------------------------------------------------- */

h1 {{
    color:{TEXT};
    font-size:2.4rem;
    font-weight:800;
    letter-spacing:-.02em;
}}

h2 {{
    color:{TEXT};
    font-size:1.5rem;
    font-weight:700;
    letter-spacing:-.01em;
    margin-bottom:.25rem;
}}

h3 {{
    color:{TEXT};
    font-size:1.1rem;
    font-weight:600;
}}

p {{
    color:{SECONDARY};
    font-size:.95rem;
    line-height:1.5;
}}

/* ---------------------------------------------------- */
/* Hero */
/* ---------------------------------------------------- */

.hero {{
    background:linear-gradient(135deg, {PRIMARY}, {CYAN});
    padding:2.75rem 2.5rem;
    border-radius:{CARD_RADIUS};
    box-shadow:{CARD_SHADOW};
    margin-bottom:2rem;
    display:flex;
    flex-direction:column;
    justify-content:center;
    min-height:170px;
    box-sizing:border-box;
}}

.hero-title {{
    color:#FFFFFF;
    font-size:42px;
    font-weight:800;
    letter-spacing:-.02em;
    line-height:1.15;
}}

.hero-subtitle {{
    color:rgba(255,255,255,.92);
    font-size:17px;
    font-weight:400;
    margin-top:10px;
    line-height:1.5;
    max-width:640px;
}}

/* ---------------------------------------------------- */
/* KPI Cards */
/* ---------------------------------------------------- */

.kpi-card {{
    background:{CARD};
    border:1px solid {BORDER};
    padding:20px;
    height:100%;
    min-height:180px;
    box-sizing:border-box;
    border-radius:{CARD_RADIUS};
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    gap:8px;
    overflow:visible;
    transition:.25s ease;
    min-width:0;
}}

.kpi-card:hover {{
    transform:translateY(-5px);
    border-color:{PRIMARY};
    box-shadow:{HOVER_SHADOW};
}}

.kpi-card:focus,
.kpi-card:focus-visible {{
    outline:none;
}}

.kpi-title {{
    font-size:13px;
    font-weight:600;
    letter-spacing:.04em;
    text-transform:uppercase;
    color:#94A3B8;
    min-width:0;
    white-space:normal;
    overflow-wrap:break-word;
    word-break:break-word;
}}

.kpi-value {{
    font-size:28px;
    font-weight:700;
    line-height:1.2;
    color:{TEXT};
    margin:0;
    min-width:0;
    white-space:normal;
    overflow-wrap:break-word;
    word-break:break-word;
}}

.kpi-trend {{
    color:{SUCCESS};
    font-weight:600;
    font-size:13px;
    min-width:0;
    white-space:normal;
    overflow-wrap:break-word;
}}

/* ---------------------------------------------------- */
/* Health Cards (separate from KPI cards — different     */
/* content shape: single-line title + single badge)      */
/* ---------------------------------------------------- */

.health-card {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:{CARD_RADIUS};
    padding:18px;
    height:100%;
    min-height:110px;
    box-sizing:border-box;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    gap:10px;
    transition:.25s ease;
    min-width:0;
}}

.health-card:hover {{
    border-color:{PRIMARY};
    box-shadow:{HOVER_SHADOW};
}}

.health-card:focus,
.health-card:focus-visible {{
    outline:none;
}}

.health-title {{
    font-size:15px;
    font-weight:600;
    color:{TEXT};
    min-width:0;
    overflow-wrap:break-word;
}}

/* ---------------------------------------------------- */
/* Workspace Cards */
/* ---------------------------------------------------- */

.workspace-card {{
    background:{CARD};
    border-radius:{CARD_RADIUS};
    border:1px solid {BORDER};
    padding:24px;
    height:100%;
    min-height:230px;
    box-sizing:border-box;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    gap:12px;
    transition:.25s ease;
    cursor:pointer;
    overflow:hidden;
    min-width:0;
}}

.workspace-card:hover {{
    transform:translateY(-6px);
    border-color:{PRIMARY};
    box-shadow:{HOVER_SHADOW};
}}

.workspace-card:focus,
.workspace-card:focus-visible {{
    outline:none;
}}

.workspace-title {{
    color:{TEXT};
    font-size:19px;
    font-weight:600;
    display:flex;
    align-items:center;
    gap:10px;
    min-width:0;
    overflow-wrap:break-word;
}}

.workspace-description {{
    color:{SECONDARY};
    font-size:14px;
    line-height:1.5;
    min-width:0;
    overflow-wrap:break-word;
}}

.workspace-metric {{
    color:{PRIMARY};
    font-size:1.6rem;
    font-weight:700;
}}

/* ---------------------------------------------------- */
/* Status Badge */
/* ---------------------------------------------------- */

.status-success,
.status-warning,
.status-danger {{
    display:inline-flex;
    align-items:center;
    width:fit-content;
    max-width:100%;
    padding:6px 14px;
    border-radius:30px;
    font-size:.75rem;
    font-weight:600;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
    margin-top:4px;
}}

.status-success {{
    background:rgba(16,185,129,.12);
    color:{SUCCESS};
}}

.status-warning {{
    background:rgba(245,158,11,.12);
    color:{WARNING};
}}

.status-danger {{
    background:rgba(239,68,68,.12);
    color:{DANGER};
}}

/* ---------------------------------------------------- */
/* Feed */
/* ---------------------------------------------------- */

.feed-card {{
    background:{CARD};
    border-radius:0 {CARD_RADIUS} {CARD_RADIUS} 0;
    padding:16px 20px;
    min-height:24px;
    box-sizing:border-box;
    display:flex;
    align-items:center;
    border-left:4px solid {PRIMARY};
    margin-bottom:.8rem;
}}

/* ---------------------------------------------------- */
/* Tables */
/* ---------------------------------------------------- */

[data-testid="stDataFrame"] {{
    border-radius:{CARD_RADIUS};
    overflow:hidden;
    border:1px solid {BORDER};
}}

/* ---------------------------------------------------- */
/* Plotly */
/* ---------------------------------------------------- */

.js-plotly-plot {{
    border-radius:{CARD_RADIUS};
    overflow:hidden;
}}

/* ---------------------------------------------------- */
/* Buttons */
/* ---------------------------------------------------- */

.stButton>button {{
    border-radius:{BUTTON_RADIUS};
    border:none;
    background:{PRIMARY};
    color:white;
    transition:.25s;
}}

.stButton>button:hover {{
    background:{CYAN};
}}

/* ---------------------------------------------------- */
/* Metrics */
/* ---------------------------------------------------- */

[data-testid="metric-container"] {{
    background:{CARD};
    border-radius:{CARD_RADIUS};
    border:1px solid {BORDER};
    padding:15px;
}}

</style>

""",

        unsafe_allow_html=True

    )
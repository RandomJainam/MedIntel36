"""
=========================================================
MedIntel360
Reusable UI Components
=========================================================

Reusable dashboard widgets.

IMPORTANT: every HTML string passed to st.markdown() below
is written with ZERO leading whitespace on content lines.
CommonMark (Streamlit's markdown parser) treats any line
indented 4+ spaces as an indented code block, which silently
renders content in a monospace font, disables wrapping, and
adds a "Copy to clipboard" button. This was the actual root
cause of the clipped/cut-off text and stray copy icons seen
in earlier versions of these components -- not a CSS/flexbox
issue. Keep every line below flush-left.

Author : Jainam Gada
"""

import streamlit as st
import streamlit.components.v1 as components


# =====================================================
# Sidebar Backup Toggle
# =====================================================
# Works around a confirmed upstream Streamlit bug where the
# native sidebar expand/collapse control can vanish shortly
# after a collapsed page finishes rendering, permanently
# blocking navigation (see streamlit/streamlit issues #11848,
# #11861, #12065, #7547 for the same failure pattern).
#
# This renders a small, fixed-position "☰" button that is NOT
# part of Streamlit's own sidebar DOM, so it can't be affected
# by whatever causes the native control to disappear. Clicking
# it looks for Streamlit's real toggle button under several
# possible data-testids (these have changed across Streamlit
# versions) and clicks it programmatically. If the sidebar is
# already open, clicking again collapses it the same way.
#
# Call this once near the top of every page, right after
# load_css().

def sidebar_toggle_backup():

    components.html(
"""<script>
(function() {
    const doc = window.parent.document;
    if (doc.getElementById("mi360-sidebar-toggle")) return;
    const btn = doc.createElement("div");
    btn.id = "mi360-sidebar-toggle";
    btn.title = "Toggle sidebar";
    btn.innerText = "☰";
    btn.style.cssText = "position:fixed;top:14px;left:14px;z-index:1000000;width:34px;height:34px;border-radius:8px;background:#161B22;border:1px solid #2D3748;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px;color:#F8FAFC;user-select:none;";
    btn.addEventListener("click", function() {
        const selectors = [
            '[data-testid="stSidebarCollapsedControl"] button',
            '[data-testid="stSidebarCollapsedControl"]',
            '[data-testid="collapsedControl"] button',
            '[data-testid="collapsedControl"]',
            '[data-testid="stSidebarCollapseButton"] button',
            '[data-testid="stSidebarCollapseButton"]',
            'button[kind="header"]'
        ];
        for (const sel of selectors) {
            const el = doc.querySelector(sel);
            if (el) { el.click(); return; }
        }
    });
    doc.body.appendChild(btn);
})();
</script>""",
        height=0,
        width=0
    )


# =====================================================
# Hero Banner
# =====================================================

def hero():

    st.markdown(
f"""<div class="hero">
<div class="hero-title">🏥 MedIntel360</div>
<div class="hero-subtitle">Healthcare Intelligence Platform<br>Crafting Clear Decisions from Clinical Data</div>
</div>""",
        unsafe_allow_html=True
    )


# =====================================================
# KPI Card
# =====================================================

def kpi_card(

    title,

    value,

    trend,

    badge="Healthy"

):

    st.markdown(
f"""<div class="kpi-card">
<div class="kpi-title">{title}</div>
<div class="kpi-value">{value}</div>
<div class="kpi-trend">{trend}</div>
<span class="status-success">{badge}</span>
</div>""",
        unsafe_allow_html=True
    )


# =====================================================
# Workspace Card
# =====================================================

def workspace_card(

    icon,

    title,

    description,

    metric,

    badge

):

    st.markdown(
f"""<div class="workspace-card">
<div class="workspace-title">
<span style="font-size:24px">{icon}</span>
<span>{title}</span>
</div>
<div class="workspace-description">{description}</div>
<div class="workspace-metric">{metric}</div>
<span class="status-success">{badge}</span>
</div>""",
        unsafe_allow_html=True
    )


# =====================================================
# System Health
# =====================================================

def health_card(

    title,

    status=True

):

    badge = "Online"

    css = "status-success"

    if not status:

        badge = "Offline"

        css = "status-danger"

    st.markdown(
f"""<div class="health-card">
<div class="health-title">{title}</div>
<span class="{css}">● {badge}</span>
</div>""",
        unsafe_allow_html=True
    )


# =====================================================
# Intelligence Feed
# =====================================================

def intelligence_feed(

    message

):

    st.markdown(
f"""<div class="feed-card">✅ {message}</div>""",
        unsafe_allow_html=True
    )


# =====================================================
# Section Header
# =====================================================

def section_header(title, subtitle=""):

    st.markdown(
f"""<h2>{title}</h2>
<p>{subtitle}</p>""",
        unsafe_allow_html=True
    )


def page_title(title: str, subtitle: str):

    st.markdown(
f"""<div style="margin-bottom:25px">
<h1 style="margin-bottom:0">{title}</h1>
<p style="color:#94A3B8;font-size:18px">{subtitle}</p>
</div>""",
        unsafe_allow_html=True
    )


def horizontal_divider():

    st.markdown(
f"""<hr style="border:1px solid #2D3748;margin:25px 0">""",
        unsafe_allow_html=True
    )
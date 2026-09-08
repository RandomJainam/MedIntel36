"""
=========================================================
MedIntel360
AI Copilot
=========================================================
"""

import streamlit as st

from dashboard.styles import load_css

from dashboard.components import (
    page_title,
    section_header
)

from ai_engine.query_engine import QueryEngine
from ai_engine.openrouter_client import OpenRouterClient


# =====================================================
# Page Config
# =====================================================

st.set_page_config(
    page_title="AI Copilot",
    page_icon="🤖",
    layout="wide"
)

load_css()


# =====================================================
# Initialize LLM
# =====================================================

@st.cache_resource
def get_llm():

    return OpenRouterClient()


# =====================================================
# Initialize Query Engine
# =====================================================

@st.cache_resource
def get_query_engine():

    return QueryEngine(
        llm_client=get_llm()
    )


query_engine = get_query_engine()


# =====================================================
# Page Title
# =====================================================

page_title(
    "🤖 MedIntel360 AI Copilot",
    "Enterprise Healthcare Intelligence Assistant"
)


# =====================================================
# Example Questions
# =====================================================

section_header(
    "Example Questions",
    "Click any question to instantly query the AI"
)

col1, col2, col3 = st.columns(3)

if "question" not in st.session_state:
    st.session_state.question = ""


with col1:

    if st.button(
        "💰 Total Revenue",
        width="stretch"
    ):

        st.session_state.question = (
            "What is the total revenue?"
        )

    if st.button(
        "📈 Highest Revenue Department",
        width="stretch"
    ):

        st.session_state.question = (
            "Which department generated the highest revenue?"
        )


with col2:

    if st.button(
        "🏥 Bed Occupancy",
        width="stretch"
    ):

        st.session_state.question = (
            "What is the current bed occupancy?"
        )

    if st.button(
        "🩺 Average LOS",
        width="stretch"
    ):

        st.session_state.question = (
            "What is the average length of stay?"
        )


with col3:

    if st.button(
        "💳 Insurance Coverage",
        width="stretch"
    ):

        st.session_state.question = (
            "What is the insurance coverage percentage?"
        )

    if st.button(
        "🦠 Most Common Disease",
        width="stretch"
    ):

        st.session_state.question = (
            "Which disease has the highest number of cases?"
        )


# =====================================================
# User Query
# =====================================================

question = st.text_area(

    "Ask MedIntel360",

    value=st.session_state.question,

    placeholder=(
        "Example: Which department generated "
        "the highest revenue?"
    )
)


# =====================================================
# Ask AI
# =====================================================

if st.button(
    "🤖 Analyze",
    width="stretch"
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Analyzing Healthcare Data..."
        ):

            try:

                result = query_engine.ask(
                    question
                )

                if result.success:

                    st.success(
                        "Analysis Complete"
                    )

                    st.markdown(
                        "### 🤖 AI Response"
                    )

                    st.markdown(
                        result.answer
                    )

                    # ------------------------------------
                    # Optional debug information
                    # ------------------------------------

                    with st.expander(
                        "View Generated SQL"
                    ):

                        st.code(
                            result.sql,
                            language="sql"
                        )

                else:

                    st.error(
                        result.error
                        or "Unable to analyze the query."
                    )

            except Exception as error:

                st.error(
                    f"Error: {error}"
                )
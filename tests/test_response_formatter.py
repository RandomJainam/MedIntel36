"""
Tests for MedIntel360 AI Response Formatter.
"""

from ai_engine.response_formatter import (
    ResponseFormatter,
    format_response
)


# =====================================================
# Basic Formatting
# =====================================================

def test_empty_response():

    assert ResponseFormatter.format("") == ""


def test_none_response():

    assert ResponseFormatter.format(None) == ""


def test_basic_response():

    response = "Total revenue is ₹25 Cr."

    result = ResponseFormatter.format(response)

    assert result == "Total revenue is ₹25 Cr."


# =====================================================
# Whitespace
# =====================================================

def test_excessive_whitespace():

    response = """
    
    ### Revenue
    
    
    Total revenue is ₹25 Cr.
    
    
    
    """

    result = ResponseFormatter.format(response)

    assert result == (
        "### Revenue\n\n"
        "Total revenue is ₹25 Cr."
    )


def test_trailing_whitespace():

    response = (
        "### Revenue   \n"
        "Total revenue is ₹25 Cr.   "
    )

    result = ResponseFormatter.format(response)

    assert result == (
        "### Revenue\n"
        "Total revenue is ₹25 Cr."
    )


# =====================================================
# Markdown
# =====================================================

def test_bullet_normalization():

    response = """
    • Total Revenue: ₹25 Cr
    • Average Bill: ₹18,500
    • Insurance: 72%
    """

    result = ResponseFormatter.format(response)

    assert "- Total Revenue: ₹25 Cr" in result
    assert "- Average Bill: ₹18,500" in result
    assert "- Insurance: 72%" in result


def test_heading_cleanup():

    response = "#### Revenue Overview"

    result = ResponseFormatter.format(response)

    assert result == "### Revenue Overview"


# =====================================================
# Code Fence Cleanup
# =====================================================

def test_markdown_code_fence_removed():

    response = """
    ```markdown
    ### Revenue

    Total revenue is ₹25 Cr.
    ```
    """

    result = ResponseFormatter.format(response)

    assert result == (
        "### Revenue\n\n"
        "Total revenue is ₹25 Cr."
    )


# =====================================================
# Number Formatting
# =====================================================

def test_large_integer_formatting():

    response = "Total patients: 125000"

    result = ResponseFormatter.format(response)

    assert result == "Total patients: 125,000"


def test_large_decimal_formatting():

    response = "Revenue: 245678934.25"

    result = ResponseFormatter.format(response)

    assert result == "Revenue: 245,678,934.25"


def test_year_is_not_formatted():

    response = "Data available from 2025."

    result = ResponseFormatter.format(response)

    assert result == "Data available from 2025."


# =====================================================
# Convenience Function
# =====================================================

def test_convenience_function():

    response = "Total patients: 125000"

    result = format_response(response)

    assert result == "Total patients: 125,000"


# =====================================================
# Preserve Meaning
# =====================================================

def test_content_is_preserved():

    response = """
    ### Financial Summary

    Total revenue is ₹25 Cr.

    The Cardiology department generated the highest revenue.

    Insurance contributed 72% of the total.
    """

    result = ResponseFormatter.format(response)

    assert "Financial Summary" in result
    assert "₹25 Cr" in result
    assert "Cardiology" in result
    assert "72%" in result
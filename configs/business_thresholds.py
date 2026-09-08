"""
=========================================================
MedIntel360
Business Threshold Configuration
=========================================================

Centralized configurable thresholds for
business rules.

Author : Jainam Gada
"""

# =====================================================
# Patient Thresholds
# =====================================================

FREQUENT_VISITS = 3

LONG_STAY_DAYS = 7

CRITICAL_STAY_DAYS = 14

HIGH_REVENUE = 75000

VERY_HIGH_REVENUE = 150000


# =====================================================
# Finance Thresholds
# =====================================================

PREMIUM_COVERAGE = 80

STANDARD_COVERAGE = 50

HIGH_DEPARTMENT_REVENUE_SHARE = 20


# =====================================================
# Operations Thresholds
# =====================================================

HIGH_OCCUPANCY = 80

CRITICAL_OCCUPANCY = 95

UNDERSTAFFED_RATIO = 0.25

HIGH_WORKLOAD_ADMISSIONS = 200

HIGH_NIGHT_SHIFT_PERCENTAGE = 40


# =====================================================
# Medical Thresholds
# =====================================================

HIGH_DISEASE_VOLUME = 100

HIGH_TEST_USAGE = 50

HIGH_DRUG_USAGE = 50

HIGH_DOCTOR_WORKLOAD = 100


# =====================================================
# Executive Thresholds
# =====================================================

EXCELLENT_PERFORMANCE = 90

GOOD_PERFORMANCE = 75
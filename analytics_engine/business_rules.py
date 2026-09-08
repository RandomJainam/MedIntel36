"""
=========================================================
MedIntel360
Business Rules Engine
=========================================================

Centralized business decision logic for MedIntel360.

This layer interprets KPIs and applies
business-specific rules that are reused by
AI agents, dashboards and analytics.

Author : Jainam Gada
"""

import numpy as np
import pandas as pd
from configs.business_thresholds import *

class BusinessRules:

    """
    Enterprise Business Rules Engine

    Converts KPIs into business decisions.
    """

    # =====================================================
    # Patient Business Rules
    # =====================================================
    @staticmethod
    def visit_category(df):

        df["visit_category"] = np.select(

            [

                df["patient_visit_count"] == 1,

                df["patient_visit_count"].between(2, FREQUENT_VISITS - 1),

                df["patient_visit_count"] >= FREQUENT_VISITS

            ],

            [

                "New",

                "Returning",

                "Frequent"

            ],

            default="Unknown"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def patient_priority(df):

        df["patient_priority"] = np.select(

            [

                (df["los"] >= CRITICAL_STAY_DAYS),

                (df["los"] >= LONG_STAY_DAYS),

                (df["high_revenue_flag"] == 1),

                (df["senior_citizen_flag"] == 1)

            ],

            [

                "Critical",

                "High",

                "Priority",

                "Monitor"

            ],

            default="Routine"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def patient_risk_level(df):

        df["patient_risk_level"] = np.select(

            [

                (df["long_stay_flag"] == 1) &
                (df["senior_citizen_flag"] == 1),

                (df["long_stay_flag"] == 1),

                (df["senior_citizen_flag"] == 1)

            ],

            [

                "High",

                "Medium",

                "Medium"

            ],

            default="Low"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def admission_priority(df):

        df["admission_priority"] = np.select(

            [

                df["admission_type"] == "Emergency",

                df["admission_type"] == "Urgent",

                df["admission_type"] == "Elective"

            ],

            [

                "Critical",

                "Priority",

                "Routine"

            ],

            default="Routine"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def patient_segment(df):

        df["patient_segment"] = np.select(

            [

                (df["patient_visit_count"] >= FREQUENT_VISITS)
                &
                (df["high_revenue_flag"] == 1),

                df["patient_visit_count"] >= FREQUENT_VISITS,

                df["high_revenue_flag"] == 1

            ],

            [

                "VIP",

                "Loyal",

                "Premium"

            ],

            default="Standard"

        )

        return df




    # =====================================================
    # Finance Business Rules
    # ====================================================

    @staticmethod
    def payment_status_category(df):

        df["payment_status_category"] = np.where(

            df["payment_status"] == "Paid",

            "Complete",

            "Pending"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def insurance_tier(df):

        df["insurance_tier"] = np.select(

            [

                df["maximum_coverage_percentage"] >= PREMIUM_COVERAGE,

                df["maximum_coverage_percentage"] >= STANDARD_COVERAGE

            ],

            [

                "Premium",

                "Standard"

            ],

            default="Basic"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def financial_risk(df):

        df["financial_risk"] = np.select(

            [

                (df["payment_status"] != "Paid") &
                (df["patient_payable_amount"] > df["average_revenue"]),

                (df["payment_status"] != "Paid"),

                (df["patient_payable_amount"] > df["average_revenue"])

            ],

            [

                "High",

                "Medium",

                "Medium"

            ],

            default="Low"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def department_performance(df):

        df["department_performance"] = np.select(

            [

                df["department_revenue_rank"] <= 3,

                df["department_revenue_rank"] <= 6

            ],

            [

                "Excellent",

                "Good"

            ],

            default="Average"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def payment_priority(df):

        df["payment_priority"] = np.select(

            [

                (df["payment_status"] != "Paid") &
                (df["patient_payable_amount"] >= VERY_HIGH_REVENUE),

                (df["payment_status"] != "Paid")

            ],

            [

                "Immediate",

                "Follow-up"

            ],

            default="Closed"

        )

        return df


    # =====================================================
    # Operations Business Rules
    # =====================================================
    # -----------------------------------------------------

    @staticmethod
    def staffing_level(df):

        ratio = df["staff_count"] / df["total_beds"].replace(0, 1)

        df["staffing_level"] = np.select(

            [

                ratio < UNDERSTAFFED_RATIO,

                ratio < 0.50,

                ratio < 0.80

            ],

            [

                "Understaffed",

                "Balanced",

                "Well Staffed"

            ],

            default="Overstaffed"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def ward_workload(df):

        df["ward_workload"] = np.select(

            [

                df["ward_admission_count"] >= HIGH_WORKLOAD_ADMISSIONS * 2,

                df["ward_admission_count"] >= HIGH_WORKLOAD_ADMISSIONS,

                df["ward_admission_count"] >= HIGH_WORKLOAD_ADMISSIONS / 2

            ],

            [

                "Critical",

                "High",

                "Medium"

            ],

            default="Low"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def shift_load(df):

        df["shift_load"] = np.select(

            [

                df["shift_count"] >= 6,

                df["shift_count"] >= 4,

                df["shift_count"] >= 2

            ],

            [
                "Heavy",

                "Moderate",

                "Light"

            ],

            default="Minimal"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def night_shift_category(df):

        percentage = (

            df["night_shift_count"]

            /

            df["shift_count"].replace(0, 1)

            * 100

        )

        df["night_shift_category"] = np.select(

            [

                percentage >= HIGH_NIGHT_SHIFT_PERCENTAGE,

                percentage >= 20

            ],

            [

                "Night Intensive",

                "Balanced"

            ],

            default="Day Focused"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def ward_efficiency(df):

        df["ward_efficiency"] = np.select(

            [

                (df["staffing_level"] == "Well Staffed") &
                (df["ward_workload"] == "Low"),

                (df["staffing_level"] == "Balanced")

            ],

            [

                "Excellent",

                "Good"

            ],

            default="Needs Attention"

        )

        return df


    # =====================================================
    # Medical Business Rules
    # =====================================================
    @staticmethod
    def disease_volume(df):

        df["disease_volume"] = np.select(

            [

                df["disease_case_count"] >= HIGH_DISEASE_VOLUME * 2,

                df["disease_case_count"] >= HIGH_DISEASE_VOLUME,

                df["disease_case_count"] >= HIGH_DISEASE_VOLUME / 2

            ],

            [

                "Very High",

                "High",

                "Medium"

            ],

            default="Low"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def disease_severity(df):

        df["disease_severity"] = np.select(

            [

                df["average_los_by_disease"] >= CRITICAL_STAY_DAYS,

            df["average_los_by_disease"] >= LONG_STAY_DAYS

            ],

            [
                "Critical",

                "Moderate"

            ],

            default="Low"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def test_utilization(df):

        df["test_utilization"] = np.select(

            [

                df["test_usage_count"] >= HIGH_TEST_USAGE * 2,

                df["test_usage_count"] >= HIGH_TEST_USAGE,

                df["test_usage_count"] >= HIGH_TEST_USAGE / 2

            ],

            [

                "Very High",

                "High",

                "Medium"

            ],

            default="Low"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def drug_utilization(df):

        df["drug_utilization"] = np.select(

            [

                df["drug_usage_count"] >= HIGH_DRUG_USAGE * 2,

                df["drug_usage_count"] >= HIGH_DRUG_USAGE,

                df["drug_usage_count"] >= HIGH_DRUG_USAGE / 2

            ],

            [
                "Very High",

                "High",

                "Medium"

            ],

            default="Low"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def doctor_workload(df):

        df["doctor_workload"] = np.select(

            [

                df["doctor_patient_count"] >= HIGH_DOCTOR_WORKLOAD * 2,

                df["doctor_patient_count"] >= HIGH_DOCTOR_WORKLOAD,

                df["doctor_patient_count"] >= HIGH_DOCTOR_WORKLOAD / 2

            ],

            [
                "Very High",

                "High",

                "Medium"

            ],

            default="Low"

        )

        return df


    # =====================================================
    # Executive Business Rules
    # =====================================================
    # -----------------------------------------------------

    @staticmethod
    def hospital_performance(df):

        df["hospital_performance"] = np.select(

            [

                (df["revenue_performance"] == "High") &
                (df["los_performance"] == "Good"),

                (df["revenue_performance"] == "High"),

                (df["los_performance"] == "Good")

            ],

            [

                "Excellent",

                "Good",

                "Average"

            ],

            default="Needs Improvement"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def department_health(df):

        df["department_health"] = np.select(

            [

                (df["department_average_los"] <= df["department_average_los"].median()) &
                (df["department_average_revenue"] >= df["department_average_revenue"].median()),

                (df["department_average_revenue"] >= df["department_average_revenue"].median())

            ],

            [

                "Excellent",

                "Good"

            ],

            default="Needs Attention"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def revenue_health(df):

        df["revenue_health"] = np.select(

            [

                df["department_revenue_share"] >= 20,

            df["department_revenue_share"] >= 10

            ],

            [
                "High",

                "Medium"

            ],

            default="Low"

        )

        return df


    # -----------------------------------------------------

    @staticmethod
    def operational_health(df):

        if "ward_efficiency" in df.columns:

            df["operational_health"] = np.where(

                df["ward_efficiency"] == "Excellent",

                "Healthy",

                "Needs Attention"

            )

        return df


    # -----------------------------------------------------

    @staticmethod
    def executive_priority(df):

        df["executive_priority"] = np.select(

            [

                (df["hospital_performance"] == "Needs Improvement"),

                (df["department_health"] == "Needs Attention"),

                (df["financial_risk"] == "High")

            ],

            [

                "Immediate Action",

                "High Priority",

                "Monitor"

            ],

            default="Normal"

        )

        return df


    # =====================================================
    # Master Pipelines
    # =====================================================

    @staticmethod
    def build_patient_rules(df):
        df = BusinessRules.visit_category(df)

        df = BusinessRules.patient_priority(df)

        df = BusinessRules.patient_risk_level(df)

        df = BusinessRules.admission_priority(df)

        df = BusinessRules.patient_segment(df)

        return df



    @staticmethod
    def build_finance_rules(df):
        df = BusinessRules.payment_status_category(df)

        df = BusinessRules.insurance_tier(df)

        df = BusinessRules.financial_risk(df)

        df = BusinessRules.department_performance(df)

        df = BusinessRules.payment_priority(df)
        return df


    @staticmethod
    def build_operations_rules(df):
        df = BusinessRules.staffing_level(df)

        df = BusinessRules.ward_workload(df)

        df = BusinessRules.shift_load(df)

        df = BusinessRules.night_shift_category(df)

        df = BusinessRules.ward_efficiency(df)
        return df


    @staticmethod
    def build_medical_rules(df):
        df = BusinessRules.disease_volume(df)

        df = BusinessRules.disease_severity(df)

        df = BusinessRules.test_utilization(df)

        df = BusinessRules.drug_utilization(df)

        df = BusinessRules.doctor_workload(df)

        return df


    @staticmethod
    def build_executive_rules(df):
        df = BusinessRules.hospital_performance(df)

        df = BusinessRules.department_health(df)

        df = BusinessRules.revenue_health(df)

        df = BusinessRules.operational_health(df)

        df = BusinessRules.executive_priority(df)
        return df